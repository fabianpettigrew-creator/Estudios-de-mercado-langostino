# -*- coding: utf-8 -*-
"""Exportación argentina oficial (INDEC): totales anuales por país y NCM, 2015-2026.

Es la fuente autorizada de VOLUMEN. Softrade sirve para precio, calibre, destino y
ruta —que son ratios— pero sus toneladas fallan el test de imposibilidad en los años
de boom (2020 y 2021 dan 115% y 123% de la captura). Ver expo.validar_volumen().

Secreto estadístico: las celdas con 's' están enmascaradas. En la apertura ANUAL por
país afecta ~30% de las filas pero casi todas son destinos chicos, así que el total
recuperado queda cerca del real; en la apertura mensual el enmascaramiento era mucho
mayor. Cada año trae, además, el total sin abrir, que permite medir cuánto falta.
"""
from __future__ import annotations

import glob
import os
import re
import warnings

import pandas as pd

warnings.simplefilter("ignore")

DIR = (r"C:\Users\fmpet\OneDrive\IA agentes\Softrade lango 2025 2026"
       r"\EXPO ARGENTINA LANGO\EXPO ADUANA CONTROL")
NCM = {"3061710": "entero", "3061790": "cola"}      # sin cero inicial: el CSV los trae
# como "03061710" y cargar() se lo saca con lstrip("0"). No cambiar las claves sin mirar
# esa línea: el CSV tiene el cero, el diccionario no.


def _num(s):
    """Formato español: '1.806.612,000' -> 1806612.0 · 's' (secreto) -> NaN."""
    s = str(s).strip()
    if s in ("s", "S", "", "nan", "-"):
        return None
    s = re.sub(r"[^\d.,\-]", "", s).replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _leer(path: str) -> pd.DataFrame:
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=enc)
        except Exception:
            continue
    raise OSError(path)


def cargar(carpeta: str = DIR) -> pd.DataFrame:
    """Todos los años en formato largo: anio, ncm, pres, pais, kg, fob."""
    filas = []
    for f in glob.glob(os.path.join(carpeta, "Resultado de la búsqueda_*.csv")):
        m = re.search(r"_(\d{4})_", os.path.basename(f))
        if not m:
            continue
        d = _leer(f)
        ren = {c: ("ncm" if c.strip() == "NCM" else
                   "pais" if "País" in c else
                   "kg" if "Peso" in c else
                   "fob" if "FOB" in c else
                   "mes" if c.strip() == "Mes" else c) for c in d.columns}
        d = d.rename(columns=ren)
        if "pais" not in d.columns:
            continue
        d["anio"] = int(m.group(1))
        d["ncm"] = d["ncm"].astype(str).str.replace(r"\D", "", regex=True).str.lstrip("0")
        d["kg"] = d["kg"].map(_num)
        d["fob"] = d["fob"].map(_num)
        d["pais"] = d["pais"].astype(str).str.strip()
        # el archivo mensual y el anual conviven en la carpeta: el anual no trae 'mes'
        d["granularidad"] = "mensual" if "mes" in d.columns else "anual"
        filas.append(d[["anio", "ncm", "pais", "kg", "fob", "granularidad"]])
    D = pd.concat(filas, ignore_index=True)
    # si un año está en las dos versiones, se queda la anual (menos secreto estadístico)
    anual = set(D.loc[D.granularidad == "anual", "anio"])
    D = D[(D.granularidad == "anual") | (~D.anio.isin(anual))]
    D = D[D.ncm.isin(NCM)]
    D["pres"] = D["ncm"].map(NCM)
    return D.drop(columns="granularidad").reset_index(drop=True)


def resumen(D: pd.DataFrame) -> pd.DataFrame:
    """Por año: kt recuperadas, cuántas filas vienen con secreto y qué peso tienen."""
    g = D.groupby("anio").apply(lambda s: pd.Series({
        "kt": s.kg.sum() / 1e6,
        "MUSD": s.fob.sum() / 1e6,
        "usd_kg": s.fob.sum() / s.kg.sum() if s.kg.sum() else None,
        "filas": len(s),
        "con_secreto": int(s.kg.isna().sum()),
        "pct_filas_secreto": 100 * s.kg.isna().mean(),
    }))
    return g.round(2)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    D = cargar()
    print(f"Cargado: {len(D):,} filas · {D.anio.min()}-{D.anio.max()}\n")
    print(resumen(D).to_string())
