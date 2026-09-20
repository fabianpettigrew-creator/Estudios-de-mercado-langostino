# -*- coding: utf-8 -*-
"""Extrae de EUMOFA la importación extra-UE de camarón, mensual, por especie y origen.

Genera los dos insumos europeos del modelo de demanda inversa:
  datos/eumofa_camaron_ue.pkl      serie mensual: precio y volumen del cultivo y de Argentina
  datos/eumofa_camaron_origen.pkl  valor y volumen por origen (AR, EC, IN, VN, resto)

Fuente: EUMOFA, «Trade data reported by EU countries», descarga masiva, un archivo por
año 2011-2025 más el parcial del año corriente. Separador «;», y el punto es separador
DECIMAL (tres decimales), no de miles: «542.000» son 542 euros, no 542.000.

Correr sólo cuando entren archivos nuevos: los CSV pesan 70-100 MB cada uno.
"""
from __future__ import annotations

import glob
import os

import pandas as pd

# Carpeta de EUMOFA (fuera del proyecto).
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from biblioteca import fuente
BASE = fuente("eumofa_ue")
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

COLS = ["year", "month", "country", "flow_type", "intra_extra_EU", "partner_contry",
        "commodity_group", "main_commercial_species", "presentation", "preservation",
        "value(EUR)", "volume(kg)"]
GRUPOS = {"Argentina": "AR", "Ecuador": "EC", "India": "IN", "Viet Nam": "VN"}
CULTIVO = ["Ecuador", "India", "Viet Nam", "Bangladesh", "Indonesia", "Thailand"]
CONGELADO = ["PS2 Frozen", "PS5 Unspecified"]


def cargar() -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(
        BASE, "EUMOFA BASES", "DESCARGA MASIVA", "EXPO IMPO", "EU",
        "*_Trade_data_reported_by_EU_countries.csv")))
    parcial = os.path.join(BASE, "2026_Trade_data_reported_by_EU_countries.csv")
    if os.path.exists(parcial):
        files.append(parcial)

    trozos = []
    for f in files:
        d = pd.read_csv(f, sep=";", dtype=str, low_memory=False,
                        usecols=lambda c: c in COLS)
        d = d[(d.flow_type == "Import")
              & (d.intra_extra_EU == "Extra EU")
              & (d.main_commercial_species.str.startswith("Shrimp", na=False))]
        d["eur"] = pd.to_numeric(d["value(EUR)"], errors="coerce")
        d["kg"] = pd.to_numeric(d["volume(kg)"], errors="coerce")
        d["anio"] = pd.to_numeric(d.year, errors="coerce")
        d["mes"] = pd.to_numeric(d.month, errors="coerce")
        trozos.append(d[["anio", "mes", "partner_contry", "main_commercial_species",
                         "preservation", "eur", "kg"]])
        print(f"  {os.path.basename(f)}: {len(d)} filas de camarón")

    d = pd.concat(trozos, ignore_index=True).dropna(subset=["anio", "mes"])
    d["per"] = pd.PeriodIndex(d.anio.astype(int).astype(str) + "-"
                              + d.mes.astype(int).astype(str).str.zfill(2), freq="M")
    return d


def main() -> None:
    d = cargar()
    fr = d[d.preservation.isin(CONGELADO)]

    def serie(sub, nom):
        g = sub.groupby("per")[["eur", "kg"]].sum()
        return pd.DataFrame({nom + "_eur_kg": g.eur / g.kg, nom + "_kt": g.kg / 1e6})

    war = fr[fr.main_commercial_species == "Shrimp, warmwater"]
    mis = fr[fr.main_commercial_species == "Shrimp, miscellaneous"]
    S = pd.concat([
        serie(war[war.partner_contry == "Ecuador"], "van_ec"),
        serie(war[war.partner_contry.isin(CULTIVO)], "van"),
        serie(mis[mis.partner_contry == "Argentina"], "ar"),
    ], axis=1).sort_index()
    S.index.name = "per"
    S.to_pickle(os.path.join(DESTINO, "eumofa_camaron_ue.pkl"))
    print("\nGuardado: datos/eumofa_camaron_ue.pkl", S.shape,
          f"({S.index.min()} a {S.index.max()})")

    # --- por origen, para el sistema de demanda inversa ---------------------
    seg = fr[fr.main_commercial_species.isin(
        ["Shrimp, warmwater", "Shrimp, miscellaneous"])].copy()
    seg["g"] = seg.partner_contry.map(GRUPOS).fillna("RE")
    O = seg.groupby(["per", "g"])[["eur", "kg"]].sum()
    O.to_pickle(os.path.join(DESTINO, "eumofa_camaron_origen.pkl"))
    print("Guardado: datos/eumofa_camaron_origen.pkl", O.shape)


if __name__ == "__main__":
    main()
