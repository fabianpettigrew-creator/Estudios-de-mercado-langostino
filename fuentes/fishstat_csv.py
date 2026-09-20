# -*- coding: utf-8 -*-
"""FishStat (FAO) — exportaciones CSV en español, formato ancho.

Supera a la base local `datos/fishstat.db` en dos cosas: llega hasta 2024 (la db
corta en 2023) y trae el VALOR de la acuicultura en miles de USD, que permite
sacar el precio de granja del vannamei por país.

Formato del archivo: una fila por (país, especie, área, origen) y una columna por
año entre corchetes, cada una seguida de una columna de estado (S) sin nombre útil.
Vienen en latin-1 y con los nombres en español.
"""
from __future__ import annotations

import os
import re
import warnings

import pandas as pd

warnings.simplefilter("ignore")

import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR = fuente("fao_fishstat")
ARCHIVOS = {
    "capturas": "CAPTURAS MUNDIAL FISHSTAT FAO-1.csv",
    "produccion": "PRODUCCIÓN MUNDIAL FISHSTAT FAO.csv",
    "acuicultura": "PRODUCCIÓN MUNDIAL ACUICULTURA FISHSTAT FAO.csv",
    "acuicultura_valor": "PRODUCCIÓN MUNDIAL ACUICULTURA VALOR FISHSTAT FAO.csv",
}
# Los nombres de columna llegan mal codificados; se reconocen por su forma, no por su texto.
_REN = [(r"^Pa.?s", "pais"), (r"^Especie", "especie"), (r"rea principal", "area"),
        (r"^Origen", "origen"), (r"^Ambiente", "ambiente"), (r"^Unidad", "unidad")]


def cargar(cual: str = "capturas", desde: int = 1990) -> pd.DataFrame:
    """Devuelve el archivo en formato largo: pais, especie, area, anio, valor."""
    d = pd.read_csv(os.path.join(DIR, ARCHIVOS[cual]), encoding="latin-1",
                    low_memory=False)
    ren = {}
    for c in d.columns:
        for pat, nom in _REN:
            if re.search(pat, c) and nom not in ren.values():
                ren[c] = nom
                break
    d = d.rename(columns=ren)
    idc = [c for c in ["pais", "especie", "area", "origen", "ambiente"] if c in d.columns]
    anios = [c for c in d.columns if re.fullmatch(r"\[\d{4}\]", str(c))]
    anios = [a for a in anios if int(a[1:5]) >= desde]

    m = d.melt(id_vars=idc, value_vars=anios, var_name="anio", value_name="valor")
    m["anio"] = m["anio"].str[1:5].astype(int)
    m["valor"] = pd.to_numeric(m["valor"], errors="coerce").fillna(0)
    for c in idc:
        m[c] = m[c].astype(str).str.strip()
    return m[m["valor"] > 0].reset_index(drop=True)


# Nombres tal como los escribe FishStat en español (verificados contra el archivo).
# Ojo: el langostino NO figura como "langostino" sino como "camarón langostín", y
# cualquier filtro por "amar" se lleva puesto al calamar.
LANGOSTINO = "Camarón langostín argentino"      # Pleoticus muelleri
VANNAMEI = "Camarón patiblanco"                 # Penaeus vannamei
ILLEX = "Pota argentina"                        # Illex argentinus
MERLUZA = "Merluza argentina"                   # Merluccius hubbsi
AREA41 = "Atlántico, sudoccidental"


def especies(cual: str = "capturas", patron: str = "") -> pd.Series:
    """Lista de especies disponibles (para encontrar el nombre exacto en español)."""
    d = cargar(cual, desde=2020)
    s = d.groupby("especie")["valor"].sum().sort_values(ascending=False)
    return s[s.index.str.contains(patron, case=False, na=False)] if patron else s


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for k in ARCHIVOS:
        d = cargar(k, desde=2015)
        print(f"{k:20} {len(d):>8,} filas · {d.anio.min()}-{d.anio.max()} · "
              f"{d.especie.nunique()} especies · {d.pais.nunique()} países")
