# -*- coding: utf-8 -*-
"""Serie mensual de desembarques de langostino por flota, 2013-2026.

Fuente: Subsecretaría de Pesca y Acuicultura (SSPyA), planillas «Por puerto,
flota, especie y mes», un archivo por año en la carpeta de desembarques. Cada
archivo trae una hoja por provincia más «Otros puertos»; Puerto y Flota vienen
en celdas combinadas y se rellenan hacia abajo.

Tres auditorías, todas impresas al correr:

  1. suma de los doce meses contra la columna «Total» de la propia planilla,
     fila por fila. Es el control interno del archivo.
  2. contra `_lan.pkl`, que es la ingesta que ya usan los modelos del proyecto.
     Si difieren, algo se desincronizó y hay que mirarlo antes de usar nada.
  3. cobertura: meses con dato por año, para que un año parcial no se lea como
     una caída. 2026 está incompleto por definición.

Se filtra `Especie == 'Langostino'`. «Camarón» es otra especie y no entra.

Uso:  python desembarques_serie.py
Salida: salidas/desembarques_langostino_2013_2026.xlsx
"""
from __future__ import annotations

import glob
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")
sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.abspath(__file__))
DIR = r"C:\Users\fmpet\OneDrive\IA agentes\Desembarques historicos argentina"
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
ABREV = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct",
         "Nov", "Dic"]
TANGONERA = "CONG. TANGONEROS"


def _anio(path: str) -> int:
    """El año del archivo es el ÚLTIMO grupo 20xx del nombre: los prefijos de
    fecha de emisión (20240104_…, 2022_250328_…) también contienen 20xx."""
    m = re.findall(r"(20\d{2})", os.path.basename(path).rsplit(".", 1)[0])
    if not m:
        raise ValueError(f"sin año en el nombre: {path}")
    return int(m[-1])


def leer() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve el detalle largo (anio, mes, prov, puerto, flota, t) y el
    resultado del control interno contra la columna «Total» de cada planilla."""
    archivos = {}
    for p in glob.glob(os.path.join(DIR, "*.xlsx")):
        if os.path.basename(p).startswith("~$"):
            continue
        y = _anio(p)
        if y in archivos:
            raise ValueError(f"dos archivos para {y}: {archivos[y]} y {p}")
        archivos[y] = p

    filas, control = [], []
    for y, p in sorted(archivos.items()):
        xl = pd.ExcelFile(p)
        for hoja in xl.sheet_names:
            crudo = pd.read_excel(p, sheet_name=hoja, header=None)
            # la fila de encabezado es la que trae «Puerto» y «Especie»
            enc = None
            for i in range(min(10, len(crudo))):
                v = [str(x).strip() for x in crudo.iloc[i].tolist()]
                if "Puerto" in v and "Especie" in v:
                    enc = i
                    break
            if enc is None:
                continue
            d = pd.read_excel(p, sheet_name=hoja, header=enc)
            d.columns = [str(c).strip() for c in d.columns]
            if not {"Puerto", "Flota", "Especie"} <= set(d.columns):
                continue
            d[["Puerto", "Flota"]] = d[["Puerto", "Flota"]].ffill()
            d = d[d.Especie.astype(str).str.strip().str.lower() == "langostino"]
            if d.empty:
                continue
            # El archivo del año en curso trae sólo los meses publicados (2026
            # llega hasta agosto). Los que faltan se completan con cero para
            # poder sumar, pero abajo sólo se vuelcan al detalle las celdas con
            # valor, así que el mes no publicado queda ausente y no como cero.
            for c in MESES:
                s = d[c] if c in d.columns else pd.Series(0.0, index=d.index)
                if isinstance(s, pd.DataFrame):        # encabezado duplicado
                    s = s.iloc[:, 0]
                d[c] = pd.to_numeric(s, errors="coerce").fillna(0.0)
            if "Total" in d.columns:
                tot = pd.to_numeric(d["Total"], errors="coerce").fillna(0.0)
                control.append({"anio": y, "hoja": hoja,
                                "dif_max_t": float((d[MESES].sum(1) - tot).abs().max())})
            for _, r in d.iterrows():
                for i, c in enumerate(MESES, 1):
                    if r[c]:
                        filas.append({"anio": y, "mes": i, "prov": hoja,
                                      "puerto": str(r.Puerto).strip(),
                                      "flota": str(r.Flota).strip(),
                                      "t": float(r[c])})
    return pd.DataFrame(filas), pd.DataFrame(control)


def _matriz(d: pd.DataFrame) -> pd.DataFrame:
    """Mes × año, con fila de total anual. Los meses sin dato quedan vacíos,
    no en cero: un mes no publicado no es un mes sin pesca."""
    m = d.pivot_table(index="mes", columns="anio", values="t", aggfunc="sum")
    m = m.reindex(range(1, 13))
    m.index = ABREV
    m.loc["Total"] = m.sum(min_count=1)
    m.index.name = "Mes"
    return m.round(1)


def main() -> None:
    d, ctrl = leer()
    print(f"Detalle: {len(d):,} filas · {d.anio.min()}-{d.anio.max()} · "
          f"{d.flota.nunique()} flotas · {d.puerto.nunique()} puertos")

    print("\nAuditoría 1 — suma de meses contra la columna «Total» de la planilla:")
    print(f"  diferencia máxima sobre {len(ctrl)} hojas: "
          f"{ctrl.dif_max_t.max():.6f} t")

    print("\nAuditoría 2 — contra _lan.pkl (la ingesta que usan los modelos):")
    try:
        lan = pd.read_pickle(os.path.join(RAIZ, "_lan.pkl"))
        a = lan.pivot_table(index=["anio", "mes"], values="t", aggfunc="sum")
        b = d.pivot_table(index=["anio", "mes"], values="t", aggfunc="sum")
        j = a.join(b, how="outer", lsuffix="_pkl", rsuffix="_xlsx").fillna(0)
        dif = (j.t_pkl - j.t_xlsx).abs()
        print(f"  diferencia máxima sobre {len(j)} meses: {dif.max():.6f} t"
              + ("" if dif.max() < 1e-6 else "   ← REVISAR"))
    except FileNotFoundError:
        print("  _lan.pkl no está: se omite")

    cob = d.groupby("anio").mes.nunique()
    print("\nAuditoría 3 — meses con dato por año:")
    print("  " + " · ".join(f"{y}:{n}" for y, n in cob.items()))
    parciales = cob[cob < 12].index.tolist()
    if parciales:
        print(f"  AÑOS PARCIALES: {parciales} — no comparar su total contra "
              "un año completo")

    total = _matriz(d)
    tang = _matriz(d[d.flota == TANGONERA])
    fres = _matriz(d[d.flota != TANGONERA])
    anual = (d.pivot_table(index="flota", columns="anio", values="t", aggfunc="sum")
             .round(0))
    anual.loc["Total"] = anual.sum(min_count=1)
    mens = (d.pivot_table(index=["anio", "mes"], columns="flota", values="t",
                          aggfunc="sum").round(1).reset_index())
    part = (tang.loc[ABREV].sum() / total.loc[ABREV].sum() * 100).round(1)

    print("\n=== Total mensual (t) ===")
    print(total.to_string())
    print("\n=== Participación de la flota tangonera en el total anual (%) ===")
    print(part.to_string())

    out = os.path.join(RAIZ, "salidas", "desembarques_langostino_2013_2026.xlsx")
    notas = pd.DataFrame({"Campo": [
        "Serie", "Fuente", "Unidad", "Cobertura", "Especie", "Flotas",
        "Años parciales", "Auditoría 1", "Auditoría 2", "Auditoría 3",
        "Criterio de vacío", "Generado por"],
        "Detalle": [
        "Desembarques de langostino por flota, mensual",
        "Subsecretaría de Pesca y Acuicultura (SSPyA), «Por puerto, flota, "
        "especie y mes», un archivo por año",
        "Toneladas",
        f"{d.anio.min()}-{d.anio.max()}",
        "Sólo «Langostino». «Camarón» es otra especie y no se incluye.",
        "Las cinco de la planilla: congeladores tangoneros y arrastreros, "
        "fresqueros costeros, de altura y de rada o ría",
        (", ".join(map(str, parciales)) if parciales else "ninguno")
        + " — su total anual no es comparable contra un año completo",
        f"Suma de los doce meses contra la columna «Total» de cada hoja: "
        f"diferencia máxima {ctrl.dif_max_t.max():.6f} t",
        "Contra _lan.pkl, la ingesta que usan los modelos del proyecto",
        "Meses con dato por año",
        "Celda vacía = mes sin dato publicado. No se rellena con cero: un mes "
        "sin publicar no es un mes sin pesca.",
        "desembarques_serie.py"]})

    try:
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            total.to_excel(w, sheet_name="Total mensual")
            tang.to_excel(w, sheet_name="Tangonera")
            fres.to_excel(w, sheet_name="Fresquera")
            anual.to_excel(w, sheet_name="Anual por flota")
            mens.to_excel(w, sheet_name="Mensual por flota", index=False)
            d.to_excel(w, sheet_name="Detalle", index=False)
            notas.to_excel(w, sheet_name="Notas", index=False)
            for hoja in w.book.worksheets:
                hoja.freeze_panes = "B2"
                for col in hoja.columns:
                    largo = max((len(str(c.value)) for c in col if c.value), default=8)
                    hoja.column_dimensions[col[0].column_letter].width = min(
                        max(largo + 2, 9), 46)
                for fila in hoja.iter_rows(min_row=2):
                    for c in fila:
                        if isinstance(c.value, (int, float, np.floating)):
                            c.number_format = "#,##0.0"
            w.book["Notas"].freeze_panes = "A2"
        print(f"\nGuardado: {out}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {out} (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
