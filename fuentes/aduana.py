# -*- coding: utf-8 -*-
"""Base agregada de la aduana argentina: exportación mensual por NCM, país y aduana.

Es la mejor fuente de VOLUMEN del proyecto: mensual, oficial y —a diferencia de las
consultas por país del INDEC— **sin secreto estadístico**. Además trae precio máximo,
mínimo y promedio de cada celda, que permite ver dispersión y no solo el promedio.

Los zips traen tres archivos; solo se lee el de exportación agregada (~1 MB). El de
importaciones pesa 6 GB por mes y no se toca: este proyecto es de exportación.

Formato: campos delimitados por comilla simple, con relleno de espacios.
  E'202507'001'0306.17.10'225'8'01'  891.49'  15724.57'  5'  891.49'  31.31'  .09'  18.2
  tipo fecha aduana  NCM   país medio unidad  kilos      FOB   decl.   unid.est.  max min prom
"""
from __future__ import annotations

import glob
import os
import re
import zipfile

import pandas as pd

# La carpeta 2017-2026 supersede a la vieja "BASES ADUANA 2020 A 2026":
# cubre 2017-02 en adelante (falta solo 2017-01) con los mismos formatos.
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR = fuente("aduana_ar")
CACHE = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                      "datos", "aduana_langostino.pkl")
COLS = ["tipo", "periodo", "aduana", "ncm", "pais_cod", "medio", "unidad",
        "kg", "fob", "declaraciones", "unidad_est", "precio_max", "precio_min",
        "precio_prom"]


def _num(v):
    v = str(v).strip()
    if not v or v in ("-", "."):
        return None
    try:
        return float(v)
    except ValueError:
        return None


COLS_TOT = ["periodo", "ncm", "unidad", "kg", "fob", "declaraciones",
            "unidad_est", "precio_max", "precio_min", "precio_prom"]


def _leer_zip(path: str, ncm_prefijo: str) -> tuple[list[dict], list[dict]]:
    """Devuelve (filas por país, filas de total por NCM).

    El zip trae DOS archivos de exportación y no dicen lo mismo:
    'expo_agregado' abre por país y aduana pero le faltan las celdas alcanzadas por
    el secreto estadístico (entre 17% y 42% del volumen según el mes);
    'total_expo_agregado' no abre por país pero está COMPLETO. Para volumen se usa
    el total; para composición por destino, el desglose, sabiendo que es un piso.
    """
    pais, total = [], []
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not n.endswith(".lst"):
                continue
            # Algunos zips traen los .lst bajo rutas internas (oper/salidas/...):
            # el filtro va sobre el nombre de archivo, no sobre la ruta completa.
            base = n.rsplit("/", 1)[-1]
            es_total = base.startswith("total_expo_agregado")
            if not (es_total or base.startswith("expo_agregado")):
                continue
            with z.open(n) as f:
                for linea in io_lineas(f):
                    if ncm_prefijo not in linea:
                        continue
                    p = [x.strip() for x in linea.split("'")]
                    if es_total:
                        if len(p) < 10 or not p[1].startswith(ncm_prefijo):
                            continue
                        total.append(dict(zip(COLS_TOT, p[:10])))
                    else:
                        if len(p) < 14 or not p[3].startswith(ncm_prefijo):
                            continue
                        pais.append(dict(zip(COLS, p[:14])))
    return pais, total


def io_lineas(f):
    """Itera líneas decodificando latin-1 (la base trae acentos de esa página)."""
    for raw in f:
        yield raw.decode("latin-1", errors="replace").rstrip("\n\r")


CACHE_TOT = CACHE.replace(".pkl", "_total.pkl")


def construir(ncm_prefijo: str = "0306.17", force: bool = False):
    """Devuelve (por_pais, total). Para volumen se usa el total: no tiene secreto."""
    if os.path.exists(CACHE) and os.path.exists(CACHE_TOT) and not force:
        return pd.read_pickle(CACHE), pd.read_pickle(CACHE_TOT)
    filas, totales = [], []
    zips = sorted(glob.glob(os.path.join(DIR, "*.zip")))
    vistos = set()
    for zp in zips:
        m = re.search(r"(\d{6})", os.path.basename(zp))
        if not m or m.group(1) in vistos:      # '202512 (1).zip' duplica a '202512.zip'
            continue
        vistos.add(m.group(1))
        a, b = _leer_zip(zp, ncm_prefijo)
        filas += a
        totales += b
        print(f"  · {m.group(1)}: {len(filas):5,} por país · {len(totales):4,} total",
              flush=True)

    def limpiar(df):
        for c in ("kg", "fob", "declaraciones", "unidad_est", "precio_max",
                  "precio_min", "precio_prom"):
            df[c] = df[c].map(_num)
        df["anio"] = df.periodo.str[:4].astype(int)
        df["mes"] = df.periodo.str[4:6].astype(int)
        return df[df.kg > 0]

    d = limpiar(pd.DataFrame(filas))
    d = d[d.tipo == "E"]
    t = limpiar(pd.DataFrame(totales))
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    d.to_pickle(CACHE)
    t.to_pickle(CACHE_TOT)
    return d, t


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    d, t = construir(force=True)
    print(f"\npor país {len(d):,} filas · total {len(t):,} filas · "
          f"{t.periodo.min()}-{t.periodo.max()}")
    g = t.groupby("anio").agg(kt=("kg", lambda s: s.sum() / 1e6),
                              MUSD=("fob", lambda s: s.sum() / 1e6),
                              meses=("mes", "nunique"))
    g["usd_kg"] = g.MUSD / g.kt
    g["kt_por_pais"] = d.groupby("anio")["kg"].sum() / 1e6
    g["cobertura%"] = g.kt_por_pais / g.kt * 100
    print("\n=== TOTAL sin secreto vs desglose por país ===")
    print(g.round(2).to_string())
