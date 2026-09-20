# -*- coding: utf-8 -*-
"""Los tres precios de España, mes a mes, 2023-2026.

Qué va en la planilla, y de dónde sale cada uno:

  · FOB del langostino entero L1 despachado a España, en dólares y en euros. Sale de
    los despachos de exportación (base de comercio), que son los únicos que abren por
    CALIBRE y por FLOTA. Es precio en origen: no incluye flete ni seguro.
  · CIF del langostino argentino que ingresa a España, de EUMOFA / Eurostat-Comext. Es
    el precio oficial de ingreso al mercado, con flete y seguro adentro, pero NO abre
    por calibre ni por flota: es todo el congelado argentino junto.
  · CIF del vannamei ecuatoriano que ingresa a España, de la misma fuente y con el
    mismo tratamiento, que es el competidor directo en ese mercado.

DOS ADVERTENCIAS DE LECTURA, las dos importantes.

Primera: el FOB y el CIF no son comparables como niveles. Entre uno y otro hay una cuña
de flete y seguro que en España promedia 0,62 EUR/kg. Restarlos da esa cuña, no un
margen comercial.

Segunda: no están fechados igual. El despacho se cuenta cuando la mercadería SALE y la
importación cuando ENTRA, y a España el tránsito son unos dos meses. Por eso la hoja
«Alineada» corre el FOB dos meses hacia adelante, que es la comparación que empareja el
mismo embarque.

Uso:  python precios_espana_2023_2026.py
Salida: salidas/Precios_Espana_2023_2026.xlsx
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
EUMOFA = fuente("eumofa_ue")
SALIDA = os.path.join(RAIZ, "salidas", "Precios_Espana_2023_2026.xlsx")
DESDE, HASTA = "2023-01", "2026-12"
CONGELADO = ["PS2 Frozen", "PS5 Unspecified"]
TRANSITO = 2          # meses de tránsito a España, medidos en cif_por_destino.py
COLS = ["year", "month", "country", "flow_type", "intra_extra_EU", "partner_contry",
        "main_commercial_species", "preservation", "value(EUR)", "volume(kg)"]


def eumofa_espana() -> pd.DataFrame:
    """CIF de importación declarado por España: langostino argentino y vannamei de
    Ecuador, congelados."""
    files = sorted(glob.glob(os.path.join(
        EUMOFA, "EUMOFA BASES", "DESCARGA MASIVA", "EXPO IMPO", "EU",
        "*_Trade_data_reported_by_EU_countries.csv")))
    parcial = os.path.join(EUMOFA, "2026_Trade_data_reported_by_EU_countries.csv")
    if os.path.exists(parcial):
        files.append(parcial)
    tr = []
    for f in files:
        if not any(str(y) in os.path.basename(f) for y in range(2023, 2027)):
            continue
        d = pd.read_csv(f, sep=";", dtype=str, low_memory=False,
                        usecols=lambda c: c in COLS)
        tr.append(d[(d.flow_type == "Import") & (d.intra_extra_EU == "Extra EU")
                    & (d.country == "Spain")
                    & d.partner_contry.isin(["Argentina", "Ecuador"])
                    & d.main_commercial_species.str.startswith("Shrimp", na=False)
                    & d.preservation.isin(CONGELADO)])
    d = pd.concat(tr, ignore_index=True)
    d["eur"] = pd.to_numeric(d["value(EUR)"], errors="coerce")
    d["kg"] = pd.to_numeric(d["volume(kg)"], errors="coerce")
    d = d[(d.kg > 0) & (d.eur > 0)]
    d["per"] = pd.PeriodIndex(
        pd.to_numeric(d.year).astype(int).astype(str) + "-"
        + pd.to_numeric(d.month).astype(int).astype(str).str.zfill(2), freq="M")
    ar = d[d.partner_contry == "Argentina"].groupby("per")[["eur", "kg"]].sum()
    # el vannamei es «warmwater»; el «miscellaneous» ecuatoriano es otra cosa
    ec = (d[(d.partner_contry == "Ecuador")
            & (d.main_commercial_species == "Shrimp, warmwater")]
          .groupby("per")[["eur", "kg"]].sum())
    return pd.DataFrame({
        "cif_ar_eur_kg": ar.eur / ar.kg, "cif_ar_t": ar.kg / 1000,
        "cif_ec_eur_kg": ec.eur / ec.kg, "cif_ec_t": ec.kg / 1000})


def fob_l1_espana() -> pd.DataFrame:
    """FOB del entero L1 despachado a España, total y por flota."""
    from fuentes import expo
    import demanda_inversa_modelo as M0
    fx = pd.Series({k: float(v) for k, v in (x.split("=") for x in M0.FX.split(";"))})
    fx.index = pd.PeriodIndex(fx.index, freq="M")

    e = expo.cargar_todos()
    d = e[(e.pres == "entero") & (e.cal == "L1") & (e.kg > 0) & (e.fob_tot > 0)
          & e.destino.astype(str).str.upper().str.strip()
          .isin(["ESPAÑA", "ESPANA"])].copy()
    d["per"] = pd.PeriodIndex(d.anio.astype(str) + "-"
                              + d.mes.astype(str).str.zfill(2), freq="M")
    d["flota"] = np.where(d.ruta == "a bordo", "tangonera", "fresquera")
    d["eurusd"] = d.per.map(fx)

    def bloque(s, pre):
        g = s.groupby("per").agg(kg=("kg", "sum"), fob=("fob_tot", "sum"))
        eu = s.groupby("per").apply(lambda x: (x.fob_tot / x.eurusd).sum())
        return pd.DataFrame({f"{pre}_usd_kg": g.fob / g.kg,
                             f"{pre}_eur_kg": eu / g.kg,
                             f"{pre}_t": g.kg / 1000})

    return pd.concat([bloque(d, "fob"),
                      bloque(d[d.flota == "tangonera"], "tan"),
                      bloque(d[d.flota == "fresquera"], "fre")], axis=1)


# ------------------------------------------------------------------- estilos
AZUL, AZUL2, GRIS = "1F4E79", "2E6DA4", "F2F5F8"
AR = Font(name="Arial", size=10)
ARB = Font(name="Arial", size=10, bold=True)
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
TIT = Font(name="Arial", size=13, bold=True, color=AZUL)
SUB = Font(name="Arial", size=9, color="5A5A5A")
FA, FA2 = PatternFill("solid", fgColor=AZUL), PatternFill("solid", fgColor=AZUL2)
FG = PatternFill("solid", fgColor=GRIS)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DER = Alignment(horizontal="right")
SEP = Border(left=Side(style="thin", color="BFBFBF"))

COLUMNAS = [
    ("fob_usd_kg", "FOB L1 total (US$/kg)", "#,##0.00", 1),
    ("fob_eur_kg", "FOB L1 total (EUR/kg)", "#,##0.00", 0),
    ("fob_t", "FOB L1 total · toneladas", "#,##0.0", 0),
    ("tan_eur_kg", "FOB tangonera (EUR/kg)", "#,##0.00", 1),
    ("tan_t", "Tangonera · toneladas", "#,##0.0", 0),
    ("fre_eur_kg", "FOB fresquera (EUR/kg)", "#,##0.00", 1),
    ("fre_t", "Fresquera · toneladas", "#,##0.0", 0),
    ("sh_tan", "Tangonera · % del volumen", '#,##0.0"%"', 0),
    ("cif_ar_eur_kg", "CIF langostino AR (EUR/kg)", "#,##0.00", 1),
    ("cif_ar_t", "CIF AR · toneladas", "#,##0.0", 0),
    ("cif_ec_eur_kg", "CIF vannamei EC (EUR/kg)", "#,##0.00", 1),
    ("cif_ec_t", "CIF EC · toneladas", "#,##0.0", 0),
    ("coc_ar_ec", "Cociente AR / EC (CIF)", "#,##0.000", 1),
    ("prima", "Prima AR sobre EC", '+#,##0.0"%";-#,##0.0"%"', 0),
    ("cuna", "Cuña CIF − FOB (EUR/kg)", "#,##0.00", 1),
]


def hoja(wb, nombre, titulo, bajada, d):
    ws = wb.create_sheet(nombre)
    ws["A1"] = titulo
    ws["A1"].font = TIT
    ws["A2"] = bajada
    ws["A2"].font = SUB
    ws["A2"].alignment = Alignment(vertical="top", wrap_text=True)
    r0 = 4
    ws.cell(r0, 1, "Mes").font = HDR
    ws.cell(r0, 1).fill = FA2
    ws.cell(r0, 1).alignment = CEN
    for j, (c, etq, _, sep) in enumerate(COLUMNAS, start=2):
        cel = ws.cell(r0, j, etq)
        cel.font, cel.fill, cel.alignment = HDR, FA2, CEN
        if sep:
            cel.border = SEP
    ws.row_dimensions[r0].height = 32
    r = r0 + 1
    for per, fila in d.iterrows():
        gris = FG if per.year % 2 else None
        ws.cell(r, 1, f"{per.year}-{per.month:02d}").font = AR
        for j, (c, _, fmt, sep) in enumerate(COLUMNAS, start=2):
            v = fila.get(c, np.nan)
            cel = ws.cell(r, j, None if pd.isna(v) else float(v))
            cel.font, cel.number_format, cel.alignment = AR, fmt, DER
            if sep:
                cel.border = SEP
        if gris:
            for j in range(1, len(COLUMNAS) + 2):
                ws.cell(r, j).fill = gris
        r += 1
    ws.column_dimensions["A"].width = 10
    for j in range(2, len(COLUMNAS) + 2):
        ws.column_dimensions[L(j)].width = 14
    ws.freeze_panes = "B5"
    return ws


NOTAS = [
    ("Qué contiene esta planilla", True),
    ("Tres precios mensuales del mercado español, de enero de 2023 en adelante: el FOB "
     "del langostino entero L1 despachado a España, el CIF del langostino argentino que "
     "ingresa a España y el CIF del vannamei ecuatoriano que ingresa a España.", False),
    ("", False),
    ("De dónde sale cada uno", True),
    ("FOB L1: despachos de exportación (base de comercio), partida 0306.17, entero "
     "calibre L1, destino España. Es la única fuente que abre por CALIBRE y por FLOTA. "
     "Precio en origen, sin flete ni seguro. Se informa en dólares —como se declara— y "
     "convertido a euros al tipo de cambio del mes.", False),
    ("CIF langostino argentino: EUMOFA / Eurostat-Comext, importación extra-UE "
     "declarada por España, origen Argentina, camarón congelado. Es el precio oficial "
     "de ingreso al mercado. NO abre por calibre ni por flota: es todo el congelado "
     "argentino junto, entero y cola, las dos flotas.", False),
    ("CIF vannamei ecuatoriano: misma fuente y mismo tratamiento, origen Ecuador, "
     "especie comercial «Shrimp, warmwater», que es el vannamei de cultivo.", False),
    ("", False),
    ("Primera advertencia: FOB y CIF no se comparan como niveles", True),
    ("Entre el precio en origen y el precio en frontera hay una cuña de flete y seguro "
     "que en España promedia 0,62 euros por kilo. La columna «Cuña CIF − FOB» la "
     "muestra, pero ojo: esa resta mezcla el flete con el hecho de que las dos "
     "columnas no son el mismo producto —una es entero L1 y la otra es todo el "
     "congelado argentino—, así que no es una medición limpia del flete. La medición "
     "limpia está en «cif_vs_fob.py» y «cif_por_destino.py».", False),
    ("", False),
    ("Segunda advertencia: no están fechados igual", True),
    ("El despacho se cuenta cuando la mercadería SALE del país y la importación cuando "
     "ENTRA al mercado europeo. A España el tránsito son unos dos meses, medido por la "
     "correlación de volúmenes entre las dos fuentes. Por eso hay dos hojas: "
     "«Mensual» pone cada serie en su propia fecha, y «Alineada» corre el FOB dos meses "
     "hacia adelante, que es la comparación que empareja el mismo embarque.", False),
    ("", False),
    ("Qué miden los precios", True),
    ("Todos son valores unitarios: valor declarado sobre kilos declarados, ponderados "
     "dentro de cada mes. No son cotizaciones de mercado y se mueven también con la "
     "mezcla de producto y de calibre de cada embarque. Las toneladas son de PRODUCTO "
     "tal cual se despacha, no peso de langostino entero equivalente.", False),
    ("Un mes en blanco significa que no hubo operaciones, no que falte el dato. El lado "
     "EUMOFA llega hasta donde llega el archivo parcial de 2026.", False),
    ("", False),
    ("Por qué sólo el FOB se abre por flota", True),
    ("Las toneladas y el precio del FOB van separados en tangonera —congelado a "
     "bordo— y fresquera —procesada en tierra—, porque la descripción de cada despacho "
     "trae esa marca. El CIF no se puede abrir así: EUMOFA declara todo el congelado "
     "argentino como PR1 Whole/Gutted, sin flota y sin calibre. Las columnas de "
     "toneladas de las dos fuentes tampoco coinciden en nivel: el FOB es sólo entero "
     "L1 y el CIF es todo el congelado argentino, entero y cola.", False),
    ("En la hoja anual los precios van PONDERADOS por volumen y no promediados a "
     "secas: un mes con tres despachos no puede pesar lo mismo que uno de zafra.",
     False),
    ("", False),
    ("Reproducibilidad", True),
    ("«salidas/precios_espana_2023_2026.py». Elaboración: Lic. Fabián Pettigrew · AXIA.",
     False),
]


def main() -> None:
    E = eumofa_espana()
    F = fob_l1_espana()
    idx = pd.period_range(DESDE, max(E.index.max(), F.index.max()), freq="M")

    def armar(desfase: int) -> pd.DataFrame:
        f = F.copy()
        if desfase:
            f.index = f.index + desfase
        d = pd.concat([f, E], axis=1).reindex(idx)
        d["coc_ar_ec"] = d.cif_ar_eur_kg / d.cif_ec_eur_kg
        d["prima"] = (d.coc_ar_ec - 1) * 100
        d["cuna"] = d.cif_ar_eur_kg - d.fob_eur_kg
        d["sh_tan"] = d.tan_t / d.fob_t * 100
        return d.dropna(how="all")

    M, A = armar(0), armar(TRANSITO)
    print(f"FOB L1 a España: {F.fob_t.sum():,.0f} t · {F.index.min()} a {F.index.max()}")
    print(f"EUMOFA España:   AR {E.cif_ar_t.sum():,.0f} t · EC {E.cif_ec_t.sum():,.0f} t"
          f" · {E.index.min()} a {E.index.max()}")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    BAJ = ("FOB: despachos de exportación (base de comercio), entero L1, destino "
           "España. CIF: EUMOFA / Eurostat-Comext, importación declarada por España.\n"
           "El FOB es precio en origen y el CIF en frontera: entre los dos hay flete y "
           "seguro. Ver la hoja «Notas» antes de restarlos.")
    hoja(wb, "Mensual", "Precios del mercado español — cada serie en su propia fecha",
         BAJ, M)
    hoja(wb, "Alineada",
         f"Precios del mercado español — FOB corrido {TRANSITO} meses",
         "El despacho sale y la importación entra dos meses después: corriendo el FOB "
         "hacia adelante, las tres columnas describen el mismo embarque.\n" + BAJ, A)

    # Los precios anuales se ponderan por volumen, no se promedian a secas: un mes con
    # tres despachos no puede pesar lo mismo que uno de zafra.
    def _pond(g, p, t):
        return (g[p] * g[t]).sum() / g[t].sum() if g[t].sum() else np.nan

    an = M.groupby(M.index.year).apply(lambda g: pd.Series({
        "fob_eur_kg": _pond(g, "fob_eur_kg", "fob_t"),
        "tan_eur_kg": _pond(g, "tan_eur_kg", "tan_t"),
        "fre_eur_kg": _pond(g, "fre_eur_kg", "fre_t"),
        "cif_ar_eur_kg": _pond(g, "cif_ar_eur_kg", "cif_ar_t"),
        "cif_ec_eur_kg": _pond(g, "cif_ec_eur_kg", "cif_ec_t"),
        "fob_t": g.fob_t.sum(), "tan_t": g.tan_t.sum(), "fre_t": g.fre_t.sum(),
        "cif_ar_t": g.cif_ar_t.sum(), "cif_ec_t": g.cif_ec_t.sum()}))
    an["sh_tan"] = an.tan_t / an.fob_t * 100
    an["coc_ar_ec"] = an.cif_ar_eur_kg / an.cif_ec_eur_kg
    an["prima"] = (an.coc_ar_ec - 1) * 100
    ws = wb.create_sheet("Anual")
    ws["A1"] = "Anual — precios ponderados por volumen, toneladas sumadas"
    ws["A1"].font = TIT
    enc = ["Año", "FOB L1 total (EUR/kg)", "FOB L1 total · t", "FOB tangonera (EUR/kg)",
           "Tangonera · t", "FOB fresquera (EUR/kg)", "Fresquera · t",
           "Tangonera · % del volumen", "CIF AR (EUR/kg)", "CIF AR · t",
           "CIF EC (EUR/kg)", "CIF EC · t", "Cociente AR/EC", "Prima AR"]
    for j, t in enumerate(enc, start=1):
        c = ws.cell(3, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    ws.row_dimensions[3].height = 34
    r = 4
    for i, (y, f) in enumerate(an.iterrows()):
        vals = [int(y), f.fob_eur_kg, f.fob_t, f.tan_eur_kg, f.tan_t, f.fre_eur_kg,
                f.fre_t, f.sh_tan, f.cif_ar_eur_kg, f.cif_ar_t, f.cif_ec_eur_kg,
                f.cif_ec_t, f.coc_ar_ec, f.prima]
        fmts = ["0", "#,##0.00", "#,##0", "#,##0.00", "#,##0", "#,##0.00", "#,##0",
                '#,##0.0"%"', "#,##0.00", "#,##0", "#,##0.00", "#,##0", "#,##0.000",
                '+#,##0.0"%";-#,##0.0"%"']
        for j, (v, fm) in enumerate(zip(vals, fmts), start=1):
            c = ws.cell(r, j, None if pd.isna(v) else float(v))
            c.font, c.number_format, c.alignment = AR, fm, DER
            if i % 2:
                c.fill = FG
        r += 1
    for j, w in enumerate([8, 16, 14, 16, 13, 16, 13, 15, 14, 12, 14, 12, 13, 12],
                          start=1):
        ws.column_dimensions[L(j)].width = w

    ws = wb.create_sheet("Notas")
    ws.column_dimensions["A"].width = 118
    for i, (t, neg) in enumerate(NOTAS, start=1):
        c = ws.cell(i, 1, t)
        c.font = Font(name="Arial", size=10, bold=neg, color=AZUL if neg else "1A1A1A")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if not neg and t:
            ws.row_dimensions[i].height = 14 * (1 + len(t) // 108)
    for h in wb.sheetnames:
        wb[h].sheet_properties.tabColor = "7F7F7F" if h == "Notas" else AZUL

    try:
        wb.save(SALIDA)
        print("escrito:", SALIDA)
    except PermissionError:
        print("AVISO: no pude escribir el xlsx (¿abierto en Excel?)")

    print("\nanual:")
    print(an.round(2).to_string())


if __name__ == "__main__":
    main()
