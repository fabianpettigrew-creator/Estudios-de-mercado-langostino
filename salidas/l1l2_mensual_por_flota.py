# -*- coding: utf-8 -*-
"""Langostino ENTERO calibre L1 y L2, mes a mes, por flota y hacia los cuatro destinos
que concentran el 86% del volumen: España, China, Italia y Japón.

Regla de flota (industria): el entero congelado A BORDO es de la flota TANGONERA; lo
que se despacha sin esa marca es de la FRESQUERA, procesada en tierra.

Por qué la ventana arranca en 2020. Son dos límites distintos que se acumulan:
  · el corte por flota es limpio recién desde 2018, cuando entra el sufijo SIM; antes
    hay despachos sin marca que no se pueden asignar;
  · el VOLUMEN del despacho es confiable recién desde 2020 —antes hay doble conteo que
    infla los kilos hasta 1,45x—, mientras que el precio no se ve afectado porque es
    un cociente.
Las hojas mensuales van de 2020 en adelante. La hoja «Datos» arranca en 2018 y marca
fila por fila si el volumen de ese año es confiable, para que quede a la vista y no se
use por descuido.

Las toneladas son de PRODUCTO tal cual se despacha, no peso de langostino entero
equivalente. El precio es el FOB declarado sobre los kilos, ponderado.

Uso:  python l1l2_mensual_por_flota.py
Salida: salidas/L1_L2_mensual_por_flota_destino.xlsx
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
# El script vive en salidas/ pero importa `fuentes`, que cuelga de la raíz.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
SALIDA = os.path.join(RAIZ, "salidas", "L1_L2_mensual_por_flota_destino.xlsx")

MAPA = {"ESPAÑA": "España", "ESPANA": "España", "ITALIA": "Italia", "CHINA": "China",
        "JAPON": "Japón", "JAPÓN": "Japón"}
DEST = ["España", "China", "Italia", "Japón"]
FLOTAS = ["tangonera", "fresquera"]
CAL = ["L1", "L2"]
DESDE_HOJA, DESDE_DATOS = 2020, 2018
MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
       "septiembre", "octubre", "noviembre", "diciembre"]


def datos() -> pd.DataFrame:
    from fuentes import expo
    e = expo.cargar_todos()
    d = e[(e.pres == "entero") & (e.cal.isin(CAL)) & (e.kg > 0) & (e.fob_tot > 0)
          & (e.anio >= DESDE_DATOS)].copy()
    d["dest"] = d.destino.str.upper().str.strip().map(MAPA).fillna(d.destino.str.title())
    d = d[d.dest.isin(DEST)].copy()
    d["flota"] = np.where(d.ruta == "a bordo", "tangonera", "fresquera")
    d["per"] = pd.PeriodIndex(d.anio.astype(str) + "-"
                              + d.mes.astype(str).str.zfill(2), freq="M")
    d["tn"] = d.kg / 1000.0
    return d


def cubos(d: pd.DataFrame, cal: str):
    """Toneladas y FOB por mes × (destino, flota), con el índice mensual completo."""
    s = d[(d.cal == cal) & (d.anio >= DESDE_HOJA)]
    idx = pd.period_range(f"{DESDE_HOJA}-01", d.per.max(), freq="M")
    cols = pd.MultiIndex.from_product([DEST, FLOTAS])
    tn = s.pivot_table(index="per", columns=["dest", "flota"], values="tn",
                       aggfunc="sum").reindex(index=idx, columns=cols)
    kg = s.pivot_table(index="per", columns=["dest", "flota"], values="kg",
                       aggfunc="sum").reindex(index=idx, columns=cols)
    fo = s.pivot_table(index="per", columns=["dest", "flota"], values="fob_tot",
                       aggfunc="sum").reindex(index=idx, columns=cols)
    return tn, kg, fo


# ------------------------------------------------------------------ estilos
AZUL, AZUL2, GRIS, GRISTXT = "1F4E79", "2E6DA4", "F2F5F8", "5A5A5A"
AR = Font(name="Arial", size=10)
ARB = Font(name="Arial", size=10, bold=True)
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
TIT = Font(name="Arial", size=13, bold=True, color=AZUL)
SUB = Font(name="Arial", size=9, color=GRISTXT)
AZB = Font(name="Arial", size=10, bold=True, color=AZUL)
FA, FA2 = PatternFill("solid", fgColor=AZUL), PatternFill("solid", fgColor=AZUL2)
FG = PatternFill("solid", fgColor=GRIS)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DER = Alignment(horizontal="right")
TOPB = Border(top=Side(style="thin", color=AZUL))
SEP = Border(left=Side(style="thin", color="BFBFBF"))


def encabezado(ws, titulo, bajada):
    ws["A1"] = titulo
    ws["A1"].font = TIT
    ws["A2"] = bajada
    ws["A2"].font = SUB
    ws["A2"].alignment = Alignment(vertical="top")


def hoja(wb, nombre, titulo, bajada, idx, valores, totales, fmt, banda):
    """`valores` es un DataFrame mes × (destino, flota); `totales` las tres columnas
    de la derecha, ya calculadas."""
    ws = wb.create_sheet(nombre)
    encabezado(ws, titulo, bajada)
    r0 = 4
    ws.cell(r0, 1, banda).font = AZB

    # banda de destinos, dos columnas cada uno
    r1 = r0 + 1
    for i, dst in enumerate(DEST):
        c0 = 2 + 2 * i
        ws.merge_cells(start_row=r1, start_column=c0, end_row=r1, end_column=c0 + 1)
        c = ws.cell(r1, c0, dst.upper())
        c.font, c.fill, c.alignment = HDR, FA, CEN
    ws.merge_cells(start_row=r1, start_column=10, end_row=r1, end_column=12)
    c = ws.cell(r1, 10, "TOTAL DE LOS CUATRO DESTINOS")
    c.font, c.fill, c.alignment = HDR, FA, CEN

    # cabecera
    r2 = r1 + 1
    enc = ["Mes"] + ["Tangonera", "Fresquera"] * 4 + ["Tangonera", "Fresquera", "Total"]
    for j, t in enumerate(enc, start=1):
        c = ws.cell(r2, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    ws.row_dimensions[r2].height = 26

    r = r2 + 1
    for i, per in enumerate(idx):
        gris = FG if per.year % 2 else None
        c = ws.cell(r, 1, f"{per.year}-{per.month:02d}")
        c.font = AR
        for j, (dst, fl) in enumerate([(d_, f_) for d_ in DEST for f_ in FLOTAS]):
            v = valores.loc[per, (dst, fl)]
            c = ws.cell(r, 2 + j, None if pd.isna(v) else float(v))
            c.font, c.number_format, c.alignment = AR, fmt, DER
            if j % 2 == 0:
                c.border = SEP
        for j, col in enumerate(totales.columns):
            v = totales.loc[per, col]
            c = ws.cell(r, 10 + j, None if pd.isna(v) else float(v))
            c.font = ARB if col == "total" else AR
            c.number_format, c.alignment = fmt, DER
            if j == 0:
                c.border = SEP
        if gris:
            for j in range(1, 13):
                ws.cell(r, j).fill = gris
        r += 1

    ws.column_dimensions["A"].width = 10
    for j in range(2, 13):
        ws.column_dimensions[L(j)].width = 11
    ws.freeze_panes = "B7"
    return ws, r


def main() -> None:
    d = datos()
    ultimo = d.per.max()
    print(f"Despachos de entero L1/L2 a los cuatro destinos: {len(d):,} filas, "
          f"{d.anio.min()} a {ultimo}")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    BAJ = ("Despachos de exportación (base de comercio), partida 0306.17 · langostino "
           "ENTERO · toneladas de PRODUCTO tal cual se despacha y FOB declarado.\n"
           "Flota tangonera = congelado a bordo; fresquera = procesado en tierra.")

    resumen = []
    for cal in CAL:
        tn, kg, fo = cubos(d, cal)
        tot_tn = pd.DataFrame({
            "tangonera": tn.xs("tangonera", axis=1, level=1).sum(axis=1, min_count=1),
            "fresquera": tn.xs("fresquera", axis=1, level=1).sum(axis=1, min_count=1)})
        tot_tn["total"] = tot_tn.sum(axis=1, min_count=1)
        hoja(wb, f"{cal} toneladas",
             f"Langostino entero {cal} — toneladas por mes, flota y destino, "
             f"{DESDE_HOJA}-{ultimo.year}", BAJ, tn.index, tn, tot_tn, "#,##0.0",
             f"VOLUMEN · toneladas de producto · calibre {cal}")

        pr = (fo / kg).where(kg.notna())
        tot_pr = pd.DataFrame({
            "tangonera": (fo.xs("tangonera", axis=1, level=1).sum(axis=1, min_count=1)
                          / kg.xs("tangonera", axis=1, level=1).sum(axis=1, min_count=1)),
            "fresquera": (fo.xs("fresquera", axis=1, level=1).sum(axis=1, min_count=1)
                          / kg.xs("fresquera", axis=1, level=1).sum(axis=1, min_count=1))})
        tot_pr["total"] = fo.sum(axis=1, min_count=1) / kg.sum(axis=1, min_count=1)
        hoja(wb, f"{cal} US$ por kg",
             f"Langostino entero {cal} — precio FOB US$/kg por mes, flota y destino, "
             f"{DESDE_HOJA}-{ultimo.year}", BAJ, pr.index, pr, tot_pr, "#,##0.00",
             f"PRECIO · FOB en dólares por kilo, ponderado por volumen · calibre {cal}")

        s = d[(d.cal == cal) & (d.anio >= DESDE_HOJA)]
        g = s.groupby(["anio", "dest", "flota"]).agg(tn=("tn", "sum"),
                                                     kg=("kg", "sum"),
                                                     fob=("fob_tot", "sum"))
        g["usd_kg"] = g.fob / g.kg
        g["cal"] = cal
        resumen.append(g.reset_index())

    # ------------------------------------------------------------- anual
    R = pd.concat(resumen, ignore_index=True)
    ws = wb.create_sheet("Resumen anual")
    encabezado(ws, f"Resumen anual por calibre, destino y flota, {DESDE_HOJA}-{ultimo.year}",
               BAJ)
    enc = ["Calibre", "Destino", "Flota", "Año", "Toneladas", "FOB (millones US$)",
           "US$/kg"]
    for j, t in enumerate(enc, start=1):
        c = ws.cell(4, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    r = 5
    for i, f in enumerate(R.sort_values(["cal", "dest", "flota", "anio"]).itertuples()):
        vals = [f.cal, f.dest, f.flota.capitalize(), int(f.anio), f.tn, f.fob / 1e6,
                f.usd_kg]
        fmts = [None, None, None, "0", "#,##0.0", "#,##0.00", "#,##0.00"]
        for j, (v, fm) in enumerate(zip(vals, fmts), start=1):
            c = ws.cell(r, j, v)
            c.font = AR
            if fm:
                c.number_format, c.alignment = fm, DER
            if i % 2:
                c.fill = FG
        r += 1
    for j, w in enumerate([9, 12, 12, 8, 12, 17, 10], start=1):
        ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = "A5"

    # -------------------------------------------------------------- datos
    ws = wb.create_sheet("Datos")
    encabezado(ws, f"Base larga, {DESDE_DATOS}-{ultimo.year}",
               "Una fila por mes, destino, calibre y flota. Los años 2018 y 2019 traen "
               "el corte por flota pero NO volumen confiable: van marcados.")
    G = (d.groupby(["per", "dest", "cal", "flota", "anio"])
         .agg(tn=("tn", "sum"), kg=("kg", "sum"), fob=("fob_tot", "sum"),
              n=("kg", "size"))
         .reset_index())
    G["usd_kg"] = G.fob / G.kg
    G["vol"] = np.where(G.anio >= 2020, "sí", "NO — doble conteo")
    enc = ["Mes", "Año", "Mes nº", "Destino", "Calibre", "Flota", "Despachos",
           "Toneladas", "FOB (US$)", "US$/kg", "¿Volumen confiable?"]
    for j, t in enumerate(enc, start=1):
        c = ws.cell(4, j, t)
        c.font, c.fill, c.alignment = HDR, FA2, CEN
    r = 5
    for f in G.sort_values(["per", "dest", "cal", "flota"]).itertuples():
        vals = [str(f.per), int(f.anio), int(f.per.month), f.dest, f.cal,
                f.flota.capitalize(), int(f.n), f.tn, f.fob, f.usd_kg, f.vol]
        fmts = [None, "0", "0", None, None, None, "#,##0", "#,##0.0", "#,##0",
                "#,##0.00", None]
        for j, (v, fm) in enumerate(zip(vals, fmts), start=1):
            c = ws.cell(r, j, v)
            c.font = AR
            if fm:
                c.number_format, c.alignment = fm, DER
            if f.anio < 2020:
                c.fill = PatternFill("solid", fgColor="FDF0E6")
        r += 1
    for j, w in enumerate([10, 8, 8, 12, 9, 12, 11, 12, 14, 10, 18], start=1):
        ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:K{r - 1}"

    # -------------------------------------------------------------- notas
    NOTAS = [
        ("Qué contiene esta planilla", True),
        ("Langostino ENTERO de calibres L1 y L2 despachado a España, China, Italia y "
         "Japón, mes a mes, separado por flota. Fuente: base de comercio, despachos de "
         "exportación de la partida 0306.17.", False),
        ("Los cuatro destinos concentran el 86% del volumen de entero L1+L2 exportado "
         "desde 2020.", False),
        ("", False),
        ("Cómo se separa la flota", True),
        ("Por indicación de la industria: el entero congelado A BORDO es de la flota "
         "TANGONERA; lo que se despacha sin esa marca es de la FRESQUERA, procesada en "
         "tierra. La marca sale del sufijo SIM «01» desde 2018 y de la descripción "
         "comercial «congelado a bordo» en los años previos.", False),
        ("", False),
        ("Por qué las hojas mensuales arrancan en 2020", True),
        ("Son dos límites distintos que se acumulan. El corte por flota es limpio "
         "recién desde 2018: antes hay despachos sin marca que no se pueden asignar y "
         "que llegan a dos tercios del total. Y el VOLUMEN del despacho es confiable "
         "recién desde 2020, porque antes hay doble conteo que infla los kilos hasta "
         "1,45 veces. El PRECIO no se ve afectado por ese doble conteo, porque es un "
         "cociente entre valor y kilos y el error se cancela.", False),
        ("La hoja «Datos» arranca en 2018 y marca fila por fila si el volumen de ese "
         "año es confiable. Los años 2018 y 2019 sirven para precio, no para nivel de "
         "volumen.", False),
        ("", False),
        ("Qué miden las cifras", True),
        ("Las toneladas son de PRODUCTO tal cual se despacha, no peso de langostino "
         "entero equivalente. El precio es el FOB declarado dividido por los kilos, "
         "ponderado por volumen dentro de cada mes; no es una cotización de mercado y "
         "se mueve también con la mezcla de producto de cada embarque.", False),
        ("Es FOB de despacho argentino: no es comparable con los precios CIF de "
         "importación de la UE que publica EUMOFA.", False),
        ("", False),
        ("Cuidado con los meses de pocos despachos", True),
        ("Cuando un mes tiene tres o cuatro despachos, el promedio deja de describir "
         "el mercado y pasa a describir esos embarques. El caso más visible es Japón "
         "en enero de 2020, que da 10,46 US$/kg: son cinco despachos de producto "
         "envasado para venta minorista —cajas de 6 × 2 kg netos, estuches—, que "
         "cotiza al doble que el mismo calibre a granel. No es un error de la base, "
         "es mezcla de producto. La columna «Despachos» de la hoja «Datos» permite "
         "detectar estos meses antes de leerlos como precio de mercado.", False),
        ("", False),
        ("Celdas vacías", True),
        ("Un mes en blanco significa que no hubo despachos de ese calibre, a ese "
         "destino y por esa flota. No es un dato faltante.", False),
        ("", False),
        ("Reproducibilidad", True),
        ("«salidas/l1l2_mensual_por_flota.py». Elaboración: Lic. Fabián Pettigrew · "
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
        wb[h].sheet_properties.tabColor = "7F7F7F" if h == "Notas" else AZUL
    wb.save(SALIDA)
    print("escrito:", SALIDA)

    # control en consola
    for cal in CAL:
        s = d[(d.cal == cal) & (d.anio >= DESDE_HOJA)]
        g = s.groupby(["anio", "flota"]).agg(t=("tn", "sum"), kg=("kg", "sum"),
                                             f=("fob_tot", "sum"))
        g["usd_kg"] = g.f / g.kg
        print(f"\n{cal} · los cuatro destinos")
        print(g[["t", "usd_kg"]].unstack().round(2).to_string())


if __name__ == "__main__":
    main()
