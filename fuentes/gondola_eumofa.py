# -*- coding: utf-8 -*-
"""Precios diarios de góndola online de EUMOFA, 2021-2026.

Complementa el relevamiento propio: el scraping da comparación por especie y origen
en un momento puntual; esto da SERIE, oficial y multi-país, pero sobre una canasta
estandarizada («camarón pelado y cocido, congelado») que NO distingue especie ni
origen. Sirve para el nivel y la tendencia del precio minorista, no para comparar
langostino contra vannamei.
"""
from __future__ import annotations

import glob
import os
import warnings

import pandas as pd

warnings.simplefilter("ignore")

import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR = fuente("eumofa_a", "EUMOFA BASES", "DESCARGA MASIVA")
CACHE = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                      "datos", "gondola_eumofa.pkl")
PATRON = "Daily-online retail prices"


def _num(s):
    """Los precios vienen con coma decimal y a veces con separador de miles."""
    return pd.to_numeric(
        s.astype(str).str.replace(r"[^\d,.\-]", "", regex=True)
         .str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce")


def construir(force: bool = False) -> pd.DataFrame:
    """Barre los CSV anuales y deja solo las filas de camarón."""
    if os.path.exists(CACHE) and not force:
        return pd.read_pickle(CACHE)
    acc = []
    for f in sorted(glob.glob(os.path.join(DIR, f"*{PATRON}*.csv"))):
        n = 0
        for ch in pd.read_csv(f, sep=";", chunksize=300_000, encoding="utf-8",
                              on_bad_lines="skip", low_memory=False):
            if "PRODUCT" not in ch.columns:
                break
            m = ch["PRODUCT"].astype(str).str.contains("Shrimp|Prawn", case=False,
                                                       na=False)
            if m.any():
                acc.append(ch[m])
                n += int(m.sum())
        print(f"  · {os.path.basename(f)[:4]}: {n:,} filas de camarón", flush=True)
    d = pd.concat(acc, ignore_index=True)
    d["eur_kg"] = _num(d["PRICE PER KG (EUR)"])
    d = d[(d.eur_kg > 1) & (d.eur_kg < 120)]          # descarta errores de carga
    d["fecha"] = pd.to_datetime(
        dict(year=d.YEAR, month=d.MONTH, day=d.DAY), errors="coerce")
    d = d.dropna(subset=["fecha"])
    d = d.rename(columns={"COUNTRY": "pais", "CATEGORY": "cat", "PRODUCT": "producto",
                          "YEAR": "anio", "MONTH": "mes"})
    d = d[["fecha", "anio", "mes", "pais", "cat", "producto", "eur_kg"]]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    d.to_pickle(CACHE)
    return d


def serie_anual(d: pd.DataFrame, paises=None) -> pd.DataFrame:
    """Precio medio anual por país (mediana: la media la mueven las promociones)."""
    s = d[d.pais.isin(paises)] if paises else d
    return (s.groupby(["pais", "anio"])["eur_kg"].median()
            .unstack().round(2))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    d = construir(force=True)
    print(f"\nTOTAL {len(d):,} observaciones · {d.anio.min()}-{d.anio.max()} · "
          f"{d.pais.nunique()} países")
    print("\n=== precio mediano de góndola, €/kg ===")
    print(serie_anual(d, ["Spain", "France", "Italy", "Germany", "Poland",
                          "Greece", "Sweden"]).to_string())
