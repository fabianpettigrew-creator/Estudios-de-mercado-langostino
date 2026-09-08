# -*- coding: utf-8 -*-
"""Destinos de exportación del langostino ENTERO calibre L1, por año y por flota, 2020-2025.

Regla de flota (industria): el entero congelado A BORDO es de la flota TANGONERA; lo que no
lleva esa marca es de la flota FRESQUERA, procesada en tierra.

La ventana arranca en 2020 porque es desde donde el volumen del despacho de Softrade es
confiable (antes hay doble conteo que infla los kilos hasta 1,45x; los precios no se afectan).
Las toneladas son de PRODUCTO tal cual se despacha, no peso entero equivalente.

Uso:  python destinos_l1_por_flota.py
Salida: salidas/Destinos_L1_entero_por_flota_2020_2025.xlsx
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

sys.stdout.reconfigure(encoding="utf-8")
# El script vive en salidas/ pero importa `fuentes`, que cuelga de la raíz del
# proyecto: hay que subir un nivel o `from fuentes import expo` no resuelve.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
SALIDA = os.path.join(RAIZ, "salidas", "Destinos_L1_entero_por_flota_2020_2025.xlsx")

MAPA = {"ESPAÑA": "España", "ESPANA": "España", "ITALIA": "Italia", "CHINA": "China",
        "JAPON": "Japón", "JAPÓN": "Japón", "ESTADOS UNIDOS": "Estados Unidos",
        "VIETNAM": "Vietnam", "VIET NAM": "Vietnam", "COREA DEL SUR": "Corea del Sur",
        "COREA REPUBLICANA": "Corea del Sur", "COREA, REPUBLICA DE": "Corea del Sur",
        "TAIWAN": "Taiwán", "TAIWÁN": "Taiwán", "GRECIA": "Grecia", "FRANCIA": "Francia",
        "RUSIA": "Rusia"}


def datos() -> pd.DataFrame:
    from fuentes import expo
    e = expo.cargar_todos()
    d = e[(e.pres == "entero") & (e.cal == "L1") & (e.kg > 0) & (e.fob_tot > 0)
          & e.anio.between(2020, 2025)].copy()
    d["dest"] = d.destino.str.upper().str.strip().map(MAPA).fillna(d.destino.str.title())
    d["flota"] = np.where(d.ruta == "a bordo", "tangonera", "fresquera")
    d["tn"] = d.kg / 1000.0
    return d


AZUL, AZUL2, GRIS, GRISTXT = "1F4E79", "2E6DA4", "F2F5F8", "5A5A5A"
AR = Font(name="Arial", size=10)
ARB = Font(name="Arial", size=10, bold=True)
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
TIT = Font(name="Arial", size=13, bold=True, color=AZUL)
SUB = Font(name="Arial", size=9, color=GRISTXT)
FA, FA2 = PatternFill("solid", fgColor=AZUL), PatternFill("solid", fgColor=AZUL2)
FG = PatternFill("solid", fgColor=GRIS)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DER = Alignment(horizontal="right")
TOPB = Border(top=Side(style="thin", color="1F4E79"))

d = datos()
TOP = ["España","Italia","Japón","China","Rusia","Grecia","Francia","Taiwán",
       "Sudáfrica","Hong Kong","Estados Unidos","Corea del Sur"]
d["destino_g"] = np.where(d.dest.isin(TOP), d.dest, "Resto del mundo")
ORD = TOP + ["Resto del mundo"]
YS = list(range(2020, 2026))

def cubo(sub):
    tn = sub.pivot_table(index="destino_g", columns="anio", values="tn", aggfunc="sum")
    fo = sub.pivot_table(index="destino_g", columns="anio", values="fob_tot", aggfunc="sum")
    tn = tn.reindex(index=ORD, columns=YS); fo = fo.reindex(index=ORD, columns=YS)
    return tn, fo/1e6

wb = openpyxl.Workbook(); wb.remove(wb.active)

def encabezado(ws, titulo, bajada):
    ws["A1"] = titulo; ws["A1"].font = TIT
    ws["A2"] = bajada; ws["A2"].font = SUB

def bloque(ws, r0, tn, fo, etiqueta):
    """Escribe el bloque toneladas + FOB a partir de la fila r0. Devuelve la última fila."""
    nY = len(YS)
    ws.cell(r0, 1, etiqueta).font = ARB; ws.cell(r0, 1).font = Font(name="Arial", size=10, bold=True, color=AZUL)
    # banda de títulos de bloque
    r1 = r0 + 1
    ws.merge_cells(start_row=r1, start_column=2, end_row=r1, end_column=1 + nY + 1)
    c = ws.cell(r1, 2, "VOLUMEN  ·  toneladas de producto"); c.font = HDR; c.fill = FA; c.alignment = CEN
    c0 = 2 + nY + 1
    ws.merge_cells(start_row=r1, start_column=c0 + 1, end_row=r1, end_column=c0 + nY + 1)
    c = ws.cell(r1, c0 + 1, "FOB  ·  millones de US$"); c.font = HDR; c.fill = FA; c.alignment = CEN
    cU = c0 + nY + 2
    # cabecera de columnas
    r2 = r1 + 1
    h = ["Destino"] + [str(y) for y in YS] + ["Total"] + [str(y) for y in YS] + ["Total"] + ["US$/kg\n2020-2025"]
    for j, t in enumerate(h, start=1):
        cc = ws.cell(r2, j, t); cc.font = HDR; cc.fill = FA2; cc.alignment = CEN
    ws.row_dimensions[r2].height = 30
    # filas
    r = r2 + 1
    for i, dest in enumerate(ORD):
        f = FG if i % 2 else None
        ws.cell(r, 1, dest).font = AR
        for j, y in enumerate(YS):
            v = tn.loc[dest, y]; cc = ws.cell(r, 2 + j, None if pd.isna(v) else float(v))
            cc.font = AR; cc.number_format = "#,##0"; cc.alignment = DER
            v = fo.loc[dest, y]; cc = ws.cell(r, c0 + 1 + j, None if pd.isna(v) else float(v))
            cc.font = AR; cc.number_format = "#,##0.0"; cc.alignment = DER
        cc = ws.cell(r, 2 + len(YS), f"=IF(COUNT(B{r}:{L(1+len(YS))}{r})=0,\"\",SUM(B{r}:{L(1+len(YS))}{r}))")
        cc.font = ARB; cc.number_format = "#,##0"; cc.alignment = DER
        a, b = L(c0 + 1), L(c0 + len(YS))
        cc = ws.cell(r, c0 + 1 + len(YS), f"=IF(COUNT({a}{r}:{b}{r})=0,\"\",SUM({a}{r}:{b}{r}))")
        cc.font = ARB; cc.number_format = "#,##0.0"; cc.alignment = DER
        tot_tn, tot_fo = L(2 + len(YS)), L(c0 + 1 + len(YS))
        cc = ws.cell(r, cU, f"=IF(N({tot_tn}{r})=0,\"\",{tot_fo}{r}*1000/{tot_tn}{r})")
        cc.font = AR; cc.number_format = "#,##0.00"; cc.alignment = DER
        if f:
            for j in range(1, cU + 1): ws.cell(r, j).fill = f
        r += 1
    # total
    ws.cell(r, 1, "Total").font = ARB
    for j in range(2, cU):
        if j == c0:            # columna separadora entre los dos bloques
            continue
        a = L(j); cc = ws.cell(r, j, f"=SUM({a}{r2+1}:{a}{r-1})")
        cc.font = ARB; cc.number_format = "#,##0" if j <= 1 + len(YS) + 1 else "#,##0.0"
        cc.alignment = DER
    for j in range(2, 2 + len(YS) + 1): ws.cell(r, j).number_format = "#,##0"
    tot_tn, tot_fo = L(2 + len(YS)), L(c0 + 1 + len(YS))
    cc = ws.cell(r, cU, f"={tot_fo}{r}*1000/{tot_tn}{r}"); cc.font = ARB
    cc.number_format = "#,##0.00"; cc.alignment = DER
    for j in range(1, cU + 1): ws.cell(r, j).border = TOPB
    return r

def anchos(ws, cU):
    ws.column_dimensions["A"].width = 17
    for j in range(2, cU + 1): ws.column_dimensions[L(j)].width = 9.5
    ws.column_dimensions[L(2 + len(YS) + 1)].width = 2.5
    ws.column_dimensions[L(cU)].width = 11

# ---------------- hoja por flota ----------------
NOM = {"tangonera": ("Tangonera", "FLOTA TANGONERA  ·  congelado a bordo, producto final"),
       "fresquera": ("Fresquera", "FLOTA FRESQUERA  ·  procesado en tierra")}
BAJ = ("Despachos de exportación (base de comercio), partida 0306.17 · langostino ENTERO calibre L1 · "
       "toneladas de producto tal cual se despacha y FOB declarado.")
for fl, (hoja, band) in NOM.items():
    ws = wb.create_sheet(hoja)
    encabezado(ws, f"Destinos del langostino entero L1 — flota {hoja.lower()}, 2020-2025", BAJ)
    tn, fo = cubo(d[d.flota == fl])
    last = bloque(ws, 4, tn, fo, band)
    cU = 2 + 2 * (len(YS) + 1)
    anchos(ws, cU); ws.freeze_panes = "B7"
    ws.cell(last + 2, 1, "Destinos ordenados por volumen total del período; «Resto del mundo» agrupa los "
                         "restantes 48 destinos, 2,9% del volumen L1 del período.").font = SUB

# ---------------- hoja total ----------------
ws = wb.create_sheet("Total L1", 0)
encabezado(ws, "Destinos del langostino entero L1 — total exportado, 2020-2025", BAJ)
tn, fo = cubo(d)
last = bloque(ws, 4, tn, fo, "TOTAL DE LAS DOS FLOTAS")
cU = 2 + 2 * (len(YS) + 1)
anchos(ws, cU); ws.freeze_panes = "B7"

# tabla de reparto por flota
r = last + 3
ws.cell(r, 1, "Reparto por flota").font = Font(name="Arial", size=10, bold=True, color=AZUL)
r += 1
enc = ["", "2020", "2021", "2022", "2023", "2024", "2025", "Total"]
for j, t in enumerate(enc, start=1):
    c = ws.cell(r, j, t); c.font = HDR; c.fill = FA2; c.alignment = CEN
S = d.groupby(["flota", "anio"]).agg(tn=("tn", "sum"), fob=("fob_tot", "sum"))
filas = [("Tangonera · toneladas", S.loc["tangonera"].tn, "#,##0"),
         ("Fresquera · toneladas", S.loc["fresquera"].tn, "#,##0"),
         ("Tangonera · FOB MUS$", S.loc["tangonera"].fob / 1e6, "#,##0.0"),
         ("Fresquera · FOB MUS$", S.loc["fresquera"].fob / 1e6, "#,##0.0"),
         ("Tangonera · % del volumen",
          S.loc["tangonera"].tn / (S.loc["tangonera"].tn + S.loc["fresquera"].tn) * 100, '0.0\\%')]
for i, (nom, serie, fmt) in enumerate(filas):
    r += 1
    f = FG if i % 2 else None
    ws.cell(r, 1, nom).font = AR
    for j, y in enumerate(YS):
        c = ws.cell(r, 2 + j, float(serie.get(y, np.nan))); c.font = AR
        c.number_format = fmt; c.alignment = DER
    c = ws.cell(r, 8, f"=SUM(B{r}:G{r})" if "%" not in nom else f"=B{r}")
    if "%" in nom:
        c.value = None
    c.font = ARB; c.number_format = fmt; c.alignment = DER
    if f:
        for j in range(1, 9): ws.cell(r, j).fill = f
ws.column_dimensions["A"].width = 24

wb.save(SALIDA)
print("escrito:", SALIDA)
