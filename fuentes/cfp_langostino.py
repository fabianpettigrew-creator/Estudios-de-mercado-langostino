# -*- coding: utf-8 -*-
"""Extrae de las actas del CFP lo que el modelo necesita: aperturas y cierres
de subáreas de langostino en aguas nacionales.

Método. Las actas son PDF de texto —no escaneos—, así que se leen con pypdf sin
OCR. De cada acta se guarda: fecha de la reunión, número, y cada PÁRRAFO que
menciona langostino junto con el texto que lo rodea. Sobre esos párrafos se
marcan los verbos de decisión (habilitar, abrir, cerrar, prorrogar, suspender,
vedar) y las coordenadas de subárea.

Por qué párrafos y no una tabla automática. Las actas no tienen formato fijo: la
misma decisión aparece redactada de maneras distintas según el año y el
secretario. Un parser que pretenda sacar la fecha de apertura de cada subárea
sin supervisión va a fallar en silencio, que es la peor forma de fallar. Lo que
este módulo produce es un LIBRO DE TRABAJO con los párrafos ya localizados y
clasificados, para revisar y codificar a mano lo que corresponda. La regla de la
casa vale acá: transcribir del articulado, no de un resumen automático.

Salida:
  salidas/cfp_langostino_parrafos.xlsx   un renglón por párrafo relevante
  salidas/cfp_langostino_resumen.xlsx    conteo por año y tipo de decisión

Uso:  python -m fuentes.cfp_langostino
"""
from __future__ import annotations

import os
import re
import sys
import warnings

import pandas as pd

warnings.simplefilter("ignore")
sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR = fuente("actas_cfp")

# Verbos con los que el CFP dispone sobre el esfuerzo. El orden importa: se
# reporta el primero que aparece, y los de cierre van antes que los de apertura
# porque «se cierra el área habilitada» es un cierre, no una habilitación.
DECISION = [
    ("cierre", r"\bcierr\w+|\bse cierra\b|clausur\w+|\bveda\w*\b|suspend\w+"),
    ("apertura", r"\bhabilit\w+|\bapertur\w+|\bse abre\b|autoriz\w+ la pesca"),
    ("prórroga", r"\bprórrog\w+|\bprorrog\w+|\bextend\w+ (el|la) (plazo|período)"),
    ("captura/cuota", r"\bcaptura máxima\b|\bcupo\b|\btonelad"),
]
RE_SUBAREA = re.compile(
    r"(?:subárea|sub-área|sub área|área)\s+([A-Z0-9º°\-/ ]{1,18})", re.I)
RE_COORD = re.compile(r"\d{1,2}[°º]\s?\d{0,2}['´]?\s?[SNEWOsnewo]")
RE_FECHA = re.compile(
    r"a los?\s+(\d{1,2})\s+d[ií]as?\s+del\s+mes\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})",
    re.I)
MES = {m: i + 1 for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
     "septiembre", "octubre", "noviembre", "diciembre"])}
MES["setiembre"] = 9


def _texto(path: str) -> str:
    import pypdf
    try:
        r = pypdf.PdfReader(path)
        return "\n".join((p.extract_text() or "") for p in r.pages)
    except Exception:
        return ""


def _fecha(t: str):
    m = RE_FECHA.search(t)
    if not m:
        return None
    d, mes, a = m.group(1), m.group(2).lower(), m.group(3)
    if mes not in MES:
        return None
    return f"{a}-{MES[mes]:02d}-{int(d):02d}"


def _tipo(p: str):
    for nombre, pat in DECISION:
        if re.search(pat, p, re.I):
            return nombre
    return "mención"


def procesar() -> pd.DataFrame:
    filas = []
    anios = sorted(x for x in os.listdir(DIR) if x.isdigit())
    for anio in anios:
        d = os.path.join(DIR, anio)
        pdfs = sorted(x for x in os.listdir(d) if x.lower().endswith(".pdf"))
        con = 0
        for n in pdfs:
            t = _texto(os.path.join(d, n))
            if not t:
                filas.append({"anio": int(anio), "archivo": n, "fecha_acta": None,
                              "tipo": "SIN TEXTO", "parrafo": "", "subareas": "",
                              "coords": 0})
                continue
            fecha = _fecha(t)
            # se corta en párrafos: doble salto, o salto seguido de mayúscula
            crudo = re.split(r"\n\s*\n|(?<=\.)\n(?=[A-ZÁÉÍÓÚ])", t)
            hubo = False
            for p in crudo:
                p = re.sub(r"\s+", " ", p).strip()
                if len(p) < 40 or "langostino" not in p.lower():
                    continue
                hubo = True
                sub = sorted(set(s.strip(" -/") for s in RE_SUBAREA.findall(p)
                                 if len(s.strip(" -/")) > 1))
                filas.append({
                    "anio": int(anio), "archivo": n, "fecha_acta": fecha,
                    "tipo": _tipo(p), "parrafo": p[:1500],
                    "subareas": " · ".join(sub[:6]),
                    "coords": len(RE_COORD.findall(p))})
            con += 1 if hubo else 0
        print(f"{anio}: {len(pdfs):3d} actas leídas · {con:3d} mencionan langostino")
    return pd.DataFrame(filas)


def main() -> None:
    if not os.path.isdir(DIR):
        sys.exit(f"No existe {DIR}: correr antes `python -m fuentes.cfp --bajar`")
    t = procesar()
    print(f"\nPárrafos con langostino: {len(t):,}")
    print("\nPor tipo de decisión:")
    print(t.tipo.value_counts().to_string())
    print("\nPor año y tipo:")
    print(pd.crosstab(t.anio, t.tipo).to_string())

    sal = os.path.join(RAIZ, "salidas")
    p1 = os.path.join(sal, "cfp_langostino_parrafos.xlsx")
    try:
        # engine explícito: si pandas elige xlsxwriter, `book.worksheets` es un
        # método y no una lista, y el formateo de abajo revienta
        with pd.ExcelWriter(p1, engine="openpyxl") as w:
            t.to_excel(w, sheet_name="parrafos", index=False)
            pd.crosstab(t.anio, t.tipo).to_excel(w, sheet_name="resumen")
            for h in w.book.worksheets:
                h.freeze_panes = "A2"
                for col in h.columns:
                    letra = col[0].column_letter
                    h.column_dimensions[letra].width = 60 if letra == "E" else 14
        print(f"\nGuardado: {p1}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {p1} (¿abierto en Excel?)")


if __name__ == "__main__":
    main()
