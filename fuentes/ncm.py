# -*- coding: utf-8 -*-
"""Nomenclador NCM y diccionario de sufijos (archivo oficial 'NCM Completo').

Sirve para dejar de adivinar del texto libre: la posición y sus sufijos codifican
oficialmente la presentación, el calibre en piezas por kilo y el congelado a bordo.

Equivalencias que resuelve (0306.17, langostino):

  presentación   por apertura SIM        0306.17.10 entero · 0306.17.90 cola
                                         (pelado, devenado y easy peel son
                                          presentaciones de la cola, no otra cosa)
  calibre        sufijo NA/NB            entero: NA01 11-20 pzas/kg … NA06 >80
                                         cola:   NB01 30-55 · NB02 56-100 · NB03 101-150
  defecto        sufijo NC / NA          NC01 rotos · NA03 rotos en bloque ·
                                         NA04 melanósicos en bloque
  proceso        SA01                    CONGELADO A BORDO

Con esto el calibre declarado por el exportador en el campo AI(...) —L1, C1, «COLA
45/55 PPK»— queda anclado a un rango de piezas por kilo verificable.
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
ARCHIVO = fuente("softrade_langostino", "EXPO ARGENTINA LANGO", "NCM Completo ver 07.2026.xlsx")

# Rango de piezas por kilo de cada grado comercial, leído de los sufijos oficiales.
# El grado que escribe el exportador (L1, C1…) se corresponde con estos tramos.
CALIBRE_ENTERO = {"NA01": (11, 20), "NA02": (21, 30), "NA03": (31, 40),
                  "NA04": (41, 60), "NA05": (61, 80), "NA06": (81, 999)}
CALIBRE_COLA = {"NB01": (30, 55), "NB02": (56, 100), "NB03": (101, 150)}
CALIBRE_BLOQUE = {"NA01": (30, 55), "NA02": (56, 100)}
DEFECTO = {"NC01": "rotos", "NA03": "rotos", "NA04": "melanósicos"}

# Grado comercial ↔ tramo oficial. El exportador escribe L1/C1; la aduana, el tramo.
GRADO_ENTERO = {"NA01": "L1", "NA02": "L2", "NA03": "L3",
                "NA04": "L4", "NA05": "L5", "NA06": "L6"}
GRADO_COLA = {"NB01": "C1", "NB02": "C2", "NB03": "C3"}


def sufijos(ncm_prefijo: str = "0306.17") -> pd.DataFrame:
    """Sufijos oficiales de una posición: código, descripción y NCM al que aplican."""
    s = pd.read_excel(ARCHIVO, "sufijos")
    s["NCM"] = s["NCM"].astype(str).str.strip()
    s = s[s["NCM"].str.match(re.escape(ncm_prefijo).replace(r"0306", r"0?306"))]
    return s.rename(columns={"Código Sufijo": "sufijo",
                             "Descripción": "descripcion"})[["NCM", "sufijo",
                                                             "descripcion"]]


def nomenclador(ncm_prefijo: str = "0306.17") -> pd.DataFrame:
    """Descripciones oficiales de la posición y sus aperturas."""
    n = pd.read_excel(ARCHIVO, "nomenclador")
    n["NCM"] = n["NCM"].astype(str).str.strip()
    return n[n["NCM"].str.startswith(ncm_prefijo)][["NCM", "Descripción"]]


def clasificar(descripcion: str, sim: str) -> dict:
    """Lee los sufijos que vienen en la descripción aduanera de un despacho.

    La descripción trae los sufijos declarados, del estilo
    'AA(marca)-AI(L1)-AJ(6X2)-CA01-CB00-SA01-NA01-NB01-'. Qué significa NA depende
    de la posición: en el entero es el calibre; en la cola es un atributo
    (sin cabeza / pelado) salvo en la apertura de bloque, donde vuelve a ser calibre.
    """
    t = str(descripcion).upper()
    cods = set(re.findall(r"\b([A-Z]{2}\d{2})\b", t))
    s = str(sim).replace(".", "")
    entero = s.startswith("03061710")
    bloque = s[-4:] in ("919N",)

    out = {"a_bordo": "SA01" in cods, "grado": None, "piezas_kg": None,
           "defecto": None}
    if entero:
        tabla, grados = CALIBRE_ENTERO, GRADO_ENTERO
        cand = [c for c in cods if c in tabla]
    elif bloque:
        tabla, grados = CALIBRE_BLOQUE, {"NA01": "C1", "NA02": "C2"}
        cand = [c for c in cods if c in tabla]
    else:
        tabla, grados = CALIBRE_COLA, GRADO_COLA
        cand = [c for c in cods if c in tabla]
    if cand:
        c = sorted(cand)[0]
        out["grado"] = grados.get(c)
        out["piezas_kg"] = tabla[c]
    for c in cods:
        if c in DEFECTO and (bloque or c == "NC01"):
            out["defecto"] = DEFECTO[c]
    return out


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("=== nomenclador 0306.17 ===")
    print(nomenclador().to_string(index=False)[:1200])
    print("\n=== sufijos ===")
    print(sufijos().to_string(index=False))
