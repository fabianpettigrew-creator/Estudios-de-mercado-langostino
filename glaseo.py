# -*- coding: utf-8 -*-
"""¿Cuántos despachos declaran glaseo, y sobre qué universo?

El anexo dice «sobre unos 47.000 despachos, sólo dos mencionan si el producto está
glaseado». Ese denominador no coincide con ningún corte de la base actual —el total
son 67.844 despachos y el entero completo 34.331—, así que o quedó viejo o se contó
sobre otra cosa. Este guion vuelve a contar, y deja dicho el universo.

Qué se busca. El campo libre es «Marca o Descripcion», el mismo del que salen la talla,
la presentación y la marca de congelado a bordo. Se buscan las raíces del vocabulario
del glaseo, con y sin acento, y también su ausencia declarada, que informa igual:

    glase / glaze / glasead / glazed / sin glaseo / net weight / peso neto

Uso:  python glaseo.py
Salida: consola + salidas/glaseo.xlsx con las filas que mencionan algo
"""
from __future__ import annotations

import os
import re
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

from fuentes import expo   # noqa: E402

# El vocabulario del glaseo. Se separan las que afirman glaseo de las que declaran su
# ausencia o el peso neto, porque no dicen lo mismo.
RE_GLASEO = re.compile(r"GLASE|GLAZE|GLACE|GLAS\.", re.I)
RE_NETO = re.compile(r"SIN\s+GLASE|NET\s*WEIGHT|PESO\s+NETO|0\s*%\s*GLASE", re.I)


def main() -> None:
    d = expo.cargar_todos()
    if "desc" not in d.columns:
        sys.exit("ABORTA: expo.cargar_todos() no devuelve la columna «desc». "
                 "Hay que agregarla a la selección final de fuentes/expo.py.")
    txt = d.desc.astype(str)

    n = len(d)
    con_kg = d[(d.kg > 0) & (d.fob_tot > 0)]
    entero = con_kg[con_kg.pres == "entero"]
    l1 = entero[entero.cal == "L1"]
    l1_ab = l1[l1.ruta == "a bordo"]

    print("=" * 84)
    print("MENCIONES DE GLASEO EN LA DESCRIPCIÓN COMERCIAL")
    print("=" * 84)
    print(f"Universo: {n:,} despachos de langostino, "
          f"{d.anio.min()}-{d.anio.max()}".replace(",", "."))
    for etq, sub in [("con kg y FOB positivos", con_kg), ("entero, toda talla", entero),
                     ("entero L1", l1), ("entero L1 congelado a bordo", l1_ab)]:
        print(f"   {etq:<32s} {len(sub):>7,}".replace(",", "."))

    g = txt.str.contains(RE_GLASEO, na=False)
    neto = txt.str.contains(RE_NETO, na=False)
    print(f"\nDescripciones no vacías: {int(txt.str.strip().ne('').sum()):,}"
          .replace(",", "."))
    print(f"Mencionan glaseo:        {int(g.sum()):,}".replace(",", "."))
    print(f"Declaran peso neto o su ausencia: {int(neto.sum()):,}".replace(",", "."))

    if g.any():
        print("\nLas filas que lo mencionan:")
        for _, f in d[g].iterrows():
            print(f"   {f.anio}-{str(f.mes).zfill(2)}  {str(f.destino)[:22]:<22s} "
                  f"{f.pres}/{f.cal}  {f.kg:>9,.0f} kg   {str(f.desc)[:70]}"
                  .replace(",", "."))

    # El dato que hay que poder citar: menciones sobre el universo completo.
    print(f"\nPara citar: {int(g.sum())} de {n:,} despachos".replace(",", "."))

    sal = os.path.join(RAIZ, "salidas", "glaseo.xlsx")
    try:
        with pd.ExcelWriter(sal, engine="openpyxl") as w:
            d[g | neto].to_excel(w, sheet_name="menciones", index=False)
            pd.DataFrame([{"universo": "todos los despachos", "n": n},
                          {"universo": "con kg y FOB positivos", "n": len(con_kg)},
                          {"universo": "entero, toda talla", "n": len(entero)},
                          {"universo": "entero L1", "n": len(l1)},
                          {"universo": "entero L1 a bordo", "n": len(l1_ab)},
                          {"universo": "mencionan glaseo", "n": int(g.sum())},
                          {"universo": "declaran peso neto", "n": int(neto.sum())}
                          ]).to_excel(w, sheet_name="universos", index=False)
        print(f"\nGuardado: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal}")


if __name__ == "__main__":
    main()
