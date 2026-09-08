# -*- coding: utf-8 -*-
"""Importación española de camarón y langostino por NCM (CN8) y país de origen.

Fuente: EUMOFA / Eurostat-Comext, «Trade data reported by EU countries» con apertura
CN8. Se toma el flujo Import declarado por España, de todas las partidas de camarón y
langostino: 0306.16, 0306.17, 0306.35, 0306.36, 0306.95 y 1605.21 / 1605.29, es decir
la familia completa —congelado, fresco, seco y preparado—, identificada por la especie
comercial «Shrimp» que asigna EUMOFA.

DÓNDE ESTÁ EL LANGOSTINO ARGENTINO. Entra prácticamente todo por el CN8 03061799
(«Frozen shrimps and prawns, other»), entre 38 y 58 kt por año. El 03061792 es
«Penaeus» congelado, que es por donde entra el vannamei de cultivo. Los dos códigos
juntos son el 92% del volumen importado por España.

EL LÍMITE DE LA VENTANA. La apertura CN8 disponible arranca en 2019: el archivo anual
«2019_2025_Yearly_comext_cn8detail.xlsx» cubre 2019 a 2025 y el parcial
«2026_Trade_data_reported_by_EU_countries_CN8_details.csv» cubre enero a mayo de 2026.
La descarga masiva de 2018 NO trae el código CN8 —llega hasta especie comercial,
presentación y conservación—, así que 2018 va en su propia hoja, con esa resolución y
sin NCM. Se declara en vez de rellenarlo.

Los valores de importación de Comext son CIF en frontera: incluyen flete y seguro.

Uso:  python comext_espana_camaron.py
Salida: salidas/Comext_Espana_importacion_camaron_por_NCM.xlsx
"""
from __future__ import annotations

import os
import sys

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (r"C:\Users\fmpet\OneDrive\IA agentes\DATOS PESCA UE PROYECTO CLAUDE"
        r"\Bases para analizar")
ANUAL = os.path.join(BASE, "2019_2025_Yearly_comext_cn8detail.xlsx")
PARCIAL = os.path.join(BASE, "2026_Trade_data_reported_by_EU_countries_CN8_details.csv")
MASIVA = os.path.join(BASE, "EUMOFA BASES", "DESCARGA MASIVA", "EXPO IMPO", "EU",
                      "2018_Trade_data_reported_by_EU_countries.csv")
SALIDA = os.path.join(RAIZ, "salidas",
                      "Comext_Espana_importacion_camaron_por_NCM.xlsx")
TOP_ORIGEN = 18


def _num(s):
    return pd.to_numeric(s, errors="coerce")


def cn8() -> pd.DataFrame:
    """2019-2025 del anual y 2026 del parcial, ya filtrados a España / Import /
    camarón."""
    a = pd.read_excel(ANUAL, sheet_name="Datos")
    a.columns = [str(c).strip() for c in a.columns]
    a = a.rename(columns={"value(eur)": "eur", "volume(kg)": "kg"})

    p = pd.read_csv(PARCIAL, sep="~", dtype=str, low_memory=False)
    p.columns = [str(c).strip() for c in p.columns]
    p = p.rename(columns={"value(eur)": "eur", "volume(kg)": "kg"})
    p["year"] = _num(p.year)
    meses = sorted(_num(p.loc[(p.country == "Spain"), "month"]).dropna().unique())

    d = pd.concat([a, p], ignore_index=True)
    d["kg"], d["eur"] = _num(d.kg), _num(d.eur)
    d["year"] = _num(d.year).astype("Int64")
    d["cn8"] = (d.cn8code.astype(str).str.replace(r"\.0$", "", regex=True)
                .str.zfill(8))
    d = d[(d.country == "Spain") & (d.flow_type == "Import")
          & d.main_commercial_species.str.startswith("Shrimp", na=False)
          & (d.kg > 0) & (d.eur > 0)].copy()
    d["t"] = d.kg / 1000.0
    d["desc"] = d.desc_cn8.astype(str).str.strip()
    print(f"CN8: {len(d):,} filas · {d.t.sum():,.0f} t · "
          f"{int(d.year.min())}-{int(d.year.max())} "
          f"(2026: meses {int(min(meses))} a {int(max(meses))})")
    return d, [int(m) for m in meses]


def sin_cn8_2018() -> pd.DataFrame:
    """2018 con la resolución que hay: especie comercial, presentación y conservación."""
    COLS = ["year", "month", "country", "flow_type", "intra_extra_EU", "partner_contry",
            "main_commercial_species", "presentation", "preservation",
            "value(EUR)", "volume(kg)"]
    d = pd.read_csv(MASIVA, sep=";", dtype=str, low_memory=False,
                    usecols=lambda c: c in COLS)
    d = d[(d.country == "Spain") & (d.flow_type == "Import")
          & d.main_commercial_species.str.startswith("Shrimp", na=False)].copy()
    d["kg"], d["eur"] = _num(d["volume(kg)"]), _num(d["value(EUR)"])
    d = d[(d.kg > 0) & (d.eur > 0)]
    d["t"] = d.kg / 1000.0
    print(f"2018 sin CN8: {len(d):,} filas · {d.t.sum():,.0f} t")
    return d


# ------------------------------------------------------------------- estilos
AZUL, AZUL2, GRIS = "1F4E79", "2E6DA4", "F2F5F8"
AR = Font(name="Arial", size=10)
ARB = Font(name="Arial", size=10, bold=True)
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
TIT = Font(name="Arial", size=13, bold=True, color=AZUL)
SUB = Font(name="Arial", size=9, color="5A5A5A")
AZB = Font(name="Arial", size=10, bold=True, color=AZUL)
FA, FA2 = PatternFill("solid", fgColor=AZUL), PatternFill("solid", fgColor=AZUL2)
FG = PatternFill("solid", fgColor=GRIS)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DER = Alignment(horizontal="right")
SEP = Border(left=Side(style="thin", color="BFBFBF"))
TOPB = Border(top=Side(style="thin", color=AZUL))


def encabezado(ws, titulo, bajada):
    ws["A1"] = titulo
    ws["A1"].font = TIT
    ws["A2"] = bajada
    ws["A2"].font = SUB
    ws["A2"].alignment = Alignment(vertical="top", wrap_text=True)


def bloques(ws, r0, filas, anios, tn, eu, etiquetas, ancho1=46):
    """Tres bloques de columnas —toneladas, valor y precio— sobre las mismas filas."""
    nY = len(anios)
    grupos = [("VOLUMEN · toneladas", nY), ("VALOR · millones de euros", nY),
              ("PRECIO · euros por kilo (CIF)", nY)]
    j = 2
    cortes = []
    for tit, n in grupos:
        ws.merge_cells(start_row=r0, start_column=j, end_row=r0, end_column=j + n - 1)
        c = ws.cell(r0, j, tit)
        c.font, c.fill, c.alignment = HDR, FA, CEN
        cortes.append(j)
        j += n
    r1 = r0 + 1
    enc = [etiquetas[0]] + [str(y) for y in anios] * 3
    for j, t in enumerate(enc, start=1):
        c = ws.cell(r1, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    ws.row_dimensions[r1].height = 26

    r = r1 + 1
    for i, k in enumerate(filas):
        gris = FG if i % 2 else None
        ws.cell(r, 1, k if isinstance(k, str) else " · ".join(k)).font = AR
        for b, (M, fmt) in enumerate([(tn, "#,##0"), (eu, "#,##0.0"), (None, "#,##0.00")]):
            for jy, y in enumerate(anios):
                col = 2 + b * nY + jy
                if M is None:
                    t_, e_ = tn.loc[k, y], eu.loc[k, y]
                    v = (e_ * 1e6 / (t_ * 1000)) if (t_ and not pd.isna(t_)
                                                     and not pd.isna(e_)) else np.nan
                else:
                    v = M.loc[k, y]
                c = ws.cell(r, col, None if pd.isna(v) else float(v))
                c.font, c.number_format, c.alignment = AR, fmt, DER
                if col in cortes:
                    c.border = SEP
        if gris:
            for j in range(1, 2 + 3 * nY):
                ws.cell(r, j).fill = gris
        r += 1

    # total
    ws.cell(r, 1, "Total").font = ARB
    for b, fmt in enumerate(["#,##0", "#,##0.0", "#,##0.00"]):
        for jy, y in enumerate(anios):
            col = 2 + b * nY + jy
            if b == 2:
                v = (eu[y].sum() * 1e6) / (tn[y].sum() * 1000) if tn[y].sum() else np.nan
            else:
                v = (tn if b == 0 else eu)[y].sum()
            c = ws.cell(r, col, None if pd.isna(v) else float(v))
            c.font, c.number_format, c.alignment = ARB, fmt, DER
            c.border = TOPB
    ws.cell(r, 1).border = TOPB
    ws.column_dimensions["A"].width = ancho1
    for j in range(2, 2 + 3 * nY):
        ws.column_dimensions[L(j)].width = 10
    ws.freeze_panes = "B" + str(r1 + 1)
    return r


def main() -> None:
    D, meses26 = cn8()
    anios = sorted(int(y) for y in D.year.unique())
    ult = f"enero-{['','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][max(meses26)]} de 2026"

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    BAJ = ("Fuente: EUMOFA / Eurostat-Comext, comercio declarado por España, flujo de "
           "importación, familia completa de camarón y langostino (0306.16, 0306.17, "
           "0306.35, 0306.36,\n0306.95, 1605.21 y 1605.29). Valores CIF en frontera: "
           f"incluyen flete y seguro. 2026 es parcial, {ult}.")

    # ------------------------------------------------------------- por NCM
    D["etq"] = D.cn8 + " · " + D.desc.str.slice(0, 78)
    orden = (D.groupby("etq").t.sum().sort_values(ascending=False).index.tolist())
    tn = D.pivot_table(index="etq", columns="year", values="t",
                       aggfunc="sum").reindex(index=orden, columns=anios)
    eu = (D.pivot_table(index="etq", columns="year", values="eur", aggfunc="sum")
          .reindex(index=orden, columns=anios) / 1e6)
    ws = wb.create_sheet("Por NCM")
    encabezado(ws, "Importación española de camarón y langostino por NCM (CN8), "
                   f"{anios[0]}-{anios[-1]}", BAJ)
    r = bloques(ws, 4, orden, anios, tn, eu, ["NCM (CN8) y descripción"], ancho1=62)
    ws.cell(r + 2, 1, "El 03061799 es por donde entra el langostino argentino; el "
                      "03061792 «Penaeus» es por donde entra el vannamei de cultivo. "
                      "Juntos son el 92% del volumen.").font = SUB

    # ---------------------------------------------------------- por origen
    tot = D.groupby("partner_contry").t.sum().sort_values(ascending=False)
    top = tot.head(TOP_ORIGEN).index.tolist()
    D["org"] = np.where(D.partner_contry.isin(top), D.partner_contry,
                        "Resto de orígenes")
    orden_o = top + ["Resto de orígenes"]
    tn_o = D.pivot_table(index="org", columns="year", values="t",
                         aggfunc="sum").reindex(index=orden_o, columns=anios)
    eu_o = (D.pivot_table(index="org", columns="year", values="eur", aggfunc="sum")
            .reindex(index=orden_o, columns=anios) / 1e6)
    ws = wb.create_sheet("Por origen")
    encabezado(ws, "Importación española de camarón y langostino por país de origen, "
                   f"{anios[0]}-{anios[-1]}", BAJ)
    bloques(ws, 4, orden_o, anios, tn_o, eu_o, ["País de origen"], ancho1=26)

    # ------------------------------------------------------- NCM × origen
    D["par"] = D.cn8 + " · " + D.org
    tot_p = D.groupby("par").t.sum().sort_values(ascending=False)
    orden_p = tot_p[tot_p > 100].index.tolist()
    tn_p = D.pivot_table(index="par", columns="year", values="t",
                         aggfunc="sum").reindex(index=orden_p, columns=anios)
    eu_p = (D.pivot_table(index="par", columns="year", values="eur", aggfunc="sum")
            .reindex(index=orden_p, columns=anios) / 1e6)
    ws = wb.create_sheet("NCM x origen")
    encabezado(ws, f"Importación española por NCM y país de origen, {anios[0]}-{anios[-1]}",
               BAJ + "\nSe listan los pares NCM-origen que superan 100 toneladas en el "
                     "período; el resto está en la hoja «Datos».")
    bloques(ws, 5, orden_p, anios, tn_p, eu_p, ["NCM · país de origen"], ancho1=34)

    # -------------------------------------------------------------- datos
    G = (D.groupby(["year", "cn8", "desc", "partner_contry", "intra_extra_EU",
                    "presentation", "preservation"])
         .agg(t=("t", "sum"), eur=("eur", "sum")).reset_index())
    G["eur_kg"] = G.eur / (G.t * 1000)
    ws = wb.create_sheet("Datos")
    encabezado(ws, f"Base larga, {anios[0]}-{anios[-1]}",
               "Una fila por año, NCM, origen, presentación y conservación. Filtrable.")
    enc = ["Año", "NCM (CN8)", "Descripción del NCM", "País de origen", "Intra/Extra UE",
           "Presentación", "Conservación", "Toneladas", "Valor (EUR)", "EUR/kg"]
    for j, t in enumerate(enc, start=1):
        c = ws.cell(4, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    ws.row_dimensions[4].height = 28
    r = 5
    for f in G.sort_values(["year", "cn8", "t"], ascending=[True, True, False]).itertuples():
        vals = [int(f.year), f.cn8, f.desc, f.partner_contry, f.intra_extra_EU,
                f.presentation, f.preservation, f.t, f.eur, f.eur_kg]
        fmts = ["0", None, None, None, None, None, None, "#,##0.0", "#,##0", "#,##0.00"]
        for j, (v, fm) in enumerate(zip(vals, fmts), start=1):
            c = ws.cell(r, j, v)
            c.font = AR
            if fm:
                c.number_format, c.alignment = fm, DER
        r += 1
    for j, w in enumerate([7, 12, 62, 18, 14, 18, 20, 12, 15, 10], start=1):
        ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:J{r - 1}"

    # --------------------------------------------------------------- 2018
    E = sin_cn8_2018()
    ws = wb.create_sheet("2018 sin NCM")
    encabezado(ws, "2018 — la misma importación, sin apertura por NCM",
               "La descarga masiva de 2018 no trae el código CN8: llega hasta especie "
               "comercial, presentación y conservación. Va con esa resolución, sin "
               "rellenar nada.")
    enc = ["País de origen", "Intra/Extra UE", "Especie comercial", "Presentación",
           "Conservación", "Toneladas", "Valor (EUR)", "EUR/kg"]
    for j, t in enumerate(enc, start=1):
        c = ws.cell(4, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    ws.row_dimensions[4].height = 28
    g = (E.groupby(["partner_contry", "intra_extra_EU", "main_commercial_species",
                    "presentation", "preservation"])
         .agg(t=("t", "sum"), eur=("eur", "sum")).reset_index()
         .sort_values("t", ascending=False))
    g["eur_kg"] = g.eur / (g.t * 1000)
    r = 5
    for i, f in enumerate(g.itertuples()):
        vals = [f.partner_contry, f.intra_extra_EU, f.main_commercial_species,
                f.presentation, f.preservation, f.t, f.eur, f.eur_kg]
        fmts = [None, None, None, None, None, "#,##0.0", "#,##0", "#,##0.00"]
        for j, (v, fm) in enumerate(zip(vals, fmts), start=1):
            c = ws.cell(r, j, v)
            c.font = AR
            if fm:
                c.number_format, c.alignment = fm, DER
            if i % 2:
                c.fill = FG
        r += 1
    for j, w in enumerate([20, 14, 24, 18, 22, 12, 15, 10], start=1):
        ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:H{r - 1}"

    # -------------------------------------------------------------- notas
    NOTAS = [
        ("Qué contiene esta planilla", True),
        ("Importación declarada por España de la familia completa de camarón y "
         "langostino, abierta por NCM (código CN8 de ocho dígitos) y por país de "
         "origen, con toneladas, valor y precio. Fuente: EUMOFA / Eurostat-Comext, "
         "«Trade data reported by EU countries» con apertura CN8.", False),
        ("Las partidas incluidas son 0306.16, 0306.17, 0306.35, 0306.36, 0306.95, "
         "1605.21 y 1605.29: congelado, fresco, seco y preparado. El criterio de "
         "inclusión es la especie comercial «Shrimp» que asigna EUMOFA a cada CN8.", False),
        ("", False),
        ("Dónde está el langostino argentino", True),
        ("Entra prácticamente todo por el CN8 03061799, «Frozen shrimps and prawns, "
         "other»: entre 38 y 58 mil toneladas por año. El 03061792 es «Penaeus» "
         "congelado, que es por donde entra el vannamei de cultivo de Ecuador y de "
         "Asia. Los dos códigos juntos explican el 92% del volumen que importa España.", False),
        ("El NCM identifica la partida arancelaria, no la especie ni el calibre. El "
         "03061799 mezcla langostino argentino con otros camarones no-Penaeus, así que "
         "su precio no es el precio del langostino: es el valor unitario de la "
         "partida. Para separar por origen hay que cruzarlo con el país, que es lo que "
         "hace la hoja «NCM x origen».", False),
        ("", False),
        ("Por qué 2018 va aparte", True),
        ("La apertura CN8 disponible arranca en 2019. El archivo anual de Comext "
         "cubre 2019 a 2025 y el parcial de 2026 llega hasta mayo. La descarga masiva "
         "de 2018 NO trae el código CN8: llega hasta especie comercial, presentación y "
         "conservación. Por eso 2018 tiene su propia hoja, con esa resolución. No se "
         "rellenó ni se estimó nada.", False),
        ("", False),
        ("CIF, y no comparable con el FOB de despacho", True),
        ("Los valores de importación de Comext son CIF en frontera de la UE: incluyen "
         "flete y seguro hasta el puerto español. No son comparables con el FOB de "
         "despacho argentino ni ecuatoriano.", False),
        ("El precio es un valor unitario —valor declarado sobre volumen declarado—, no "
         "una cotización: se mueve con el precio y también con la mezcla de calibre y "
         "presentación de cada año.", False),
        ("", False),
        ("Intra y extra UE", True),
        ("La planilla incluye los dos flujos. El origen intra-UE —Portugal, Bélgica, "
         "Países Bajos— es en buena parte reexpedición de mercadería que entró a la "
         "Unión por otro puerto, así que el país que figura no es necesariamente el de "
         "captura o cultivo. La columna «Intra/Extra UE» permite separarlos.", False),
        ("", False),
        ("Reproducibilidad", True),
        ("«salidas/comext_espana_camaron.py». Elaboración: Lic. Fabián Pettigrew · "
         "AXIA.", False),
    ]
    ws = wb.create_sheet("Notas")
    ws.column_dimensions["A"].width = 118
    for i, (t, neg) in enumerate(NOTAS, start=1):
        c = ws.cell(i, 1, t)
        c.font = Font(name="Arial", size=10, bold=neg, color=AZUL if neg else "1A1A1A")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if not neg and t:
            ws.row_dimensions[i].height = 14 * (1 + len(t) // 108)

    for h in wb.sheetnames:
        wb[h].sheet_properties.tabColor = "7F7F7F" if h in ("Notas", "2018 sin NCM") else AZUL
    wb.save(SALIDA)
    print("escrito:", SALIDA)

    print("\nvolumen por año (kt):")
    print((D.groupby("year").t.sum() / 1000).round(1).to_string())
    print("\nlos dos NCM principales, precio EUR/kg:")
    for c in ("03061799", "03061792"):
        s = D[D.cn8 == c].groupby("year").agg(t=("t", "sum"), e=("eur", "sum"))
        print(f"   {c}: " + "  ".join(f"{int(y)} {r.e / (r.t * 1000):.2f}"
                                      for y, r in s.iterrows()))


if __name__ == "__main__":
    main()
