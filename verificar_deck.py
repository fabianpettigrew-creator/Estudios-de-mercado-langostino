# -*- coding: utf-8 -*-
"""Verifica que el PPT entregable siga siendo lo que produce `deck_ceo.js`.

Desde el rediseño, `deck_ceo.js` lo EMITE `extraer_deck.py` leyendo el propio PPT,
así que esta verificación deja de ser «el código produce el entregable» y pasa a
ser «la extracción sigue estando al día». El deck nuevo no tiene gráficos de
Office —las series están dibujadas como formas—, de modo que la comparación de
datos de gráfico queda vacía y lo que manda es el texto.

Genera el deck a un archivo temporal y lo compara contra el que está en `salidas/`,
placa por placa: texto, datos de los gráficos y notas del orador.

Ignora a propósito lo que NO es contenido, porque reaparece cada vez que alguien abre
el archivo en PowerPoint y lo guarda:

  * **Compresión.** pptxgenjs escribe con compresión mínima y PowerPoint recomprime.
    El entregable pesa ~170 KB y el generado ~560 KB, pero descomprimidos son 520 y
    539 KB: no falta nada. Comparar tamaños de archivo no sirve para nada acá.
  * **Partes de housekeeping** que agrega PowerPoint: `changesInfos/`, `revisionInfo`,
    un segundo `theme`, `webextensions/` (paneles de complementos).
  * **Entradas de directorio** del zip (`ppt/`, `ppt/media/`, …) que escribe pptxgenjs.
    Ojo: `ppt/media/` aparece vacío en el generado — el deck no tiene imágenes, y esa
    entrada es un directorio, no un medio perdido.
  * **Numeración de los libros embebidos** de los gráficos (`Microsoft_Excel_Worksheet`
    con y sin número), que PowerPoint reasigna.
  * **Runs vacíos** en las notas, que PowerPoint elimina al guardar.

Uso:  python verificar_deck.py
Devuelve 0 si no hay diferencias de contenido, 1 si las hay.
"""
from __future__ import annotations

import os
import difflib
import re
import subprocess
import sys
import tempfile
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
ENTREGABLE = os.path.join(
    RAIZ, "salidas",
    "Estudio econométrico - testeo reducción  de captura.pptx")
GENERADOR = os.path.join(RAIZ, "deck_ceo.js")

RE_SLIDE = re.compile(r"ppt/slides/slide(\d+)\.xml$")
RE_CHART = re.compile(r"ppt/charts/chart\d+\.xml$")
RE_RUN = re.compile(r"<a:t>(.*?)</a:t>", re.S)
RE_PT = re.compile(r'<c:pt idx="\d+"><c:v>([^<]*)</c:v>')


def _norm(s: str) -> str:
    """Espacios colapsados y entidades XML resueltas: PowerPoint las reescribe."""
    s = (s.replace("&apos;", "'").replace("&quot;", '"')
          .replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))
    return re.sub(r"\s+", " ", s).strip()


def _num(v: str):
    """'6' y '6.0' son el mismo número; el resto queda como texto."""
    try:
        return round(float(v), 6)
    except ValueError:
        return v


def _orden(z: zipfile.ZipFile) -> list[str]:
    """Las placas en el ORDEN DE LA PRESENTACIÓN, no por número de archivo.

    No es lo mismo desde que el deck se actualiza por parche: una placa insertada en el
    medio se guarda como `slide28.xml` pero se muestra en la posición 26, así que
    ordenar por nombre de archivo compara placas distintas entre sí e inventa brechas.
    El orden real lo da el `sldIdLst` de presentation.xml.
    """
    pres = z.read("ppt/presentation.xml").decode("utf-8")
    rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
    mapa = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="(slides/slide\d+\.xml)"', rels))
    return ["ppt/" + mapa[r]
            for r in re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', pres)]


def leer(ruta: str) -> dict:
    z = zipfile.ZipFile(ruta)
    slides = _orden(z)
    texto, notas = {}, {}
    for i, n in enumerate(slides, 1):
        texto[i] = _norm(" ".join(RE_RUN.findall(z.read(n).decode("utf-8"))))
        rels = z.read(n.replace("slides/", "slides/_rels/") + ".rels").decode("utf-8")
        m = re.search(r'Target="\.\./(notesSlides/notesSlide\d+\.xml)"', rels)
        crudo = RE_RUN.findall(z.read("ppt/" + m.group(1)).decode("utf-8")) if m else []
        # El número de placa que PowerPoint guarda en la placa de notas NO es contenido:
        # es un campo que se renumera solo y difiere entre el entregable y lo generado.
        crudo = [x for x in crudo if not x.strip().isdigit()]
        notas[i] = _norm(" ".join(x for x in crudo if x.strip()))
    graficos = {}
    for n in sorted(x for x in z.namelist() if RE_CHART.match(x)):
        t = z.read(n).decode("utf-8")
        cat = re.search(r"<c:cat>.*?</c:cat>", t, re.S)
        val = re.search(r"<c:val>.*?</c:val>", t, re.S)
        # Las categorías y valores vacíos se descartan: en los ejes con etiqueta
        # salteada pptxgenjs escribe un punto por período con el texto en blanco y
        # PowerPoint guarda solo los que tienen etiqueta. Es la misma serie.
        graficos[n] = ([_norm(x) for x in RE_PT.findall(cat.group(0)) if x.strip()]
                       if cat else [],
                       [_num(x) for x in RE_PT.findall(val.group(0)) if x.strip()]
                       if val else [])
    # Los medios se comparan por CONTENIDO y no por nombre: pptxgenjs los rebautiza
    # («image-1-1.jpeg» donde PowerPoint puso «image1.jpeg») y eso no es una
    # diferencia — la foto es la misma. El hash lo dice sin ambigüedad.
    import hashlib
    medios = sorted(hashlib.sha1(z.read(n)).hexdigest()[:12]
                    for n in z.namelist()
                    if n.startswith("ppt/media/") and not n.endswith("/"))
    return {"texto": texto, "notas": notas, "graficos": graficos, "medios": medios}


def main() -> int:
    if not os.path.exists(ENTREGABLE):
        print(f"No está el entregable: {ENTREGABLE}")
        return 1
    tmp = os.path.join(tempfile.mkdtemp(), "deck_verificacion.pptx")
    r = subprocess.run(["node", GENERADOR, tmp], capture_output=True, text=True,
                       cwd=RAIZ, shell=(os.name == "nt"))
    if r.returncode or not os.path.exists(tmp):
        print("No se pudo generar el deck:", (r.stderr or r.stdout)[-500:])
        return 1

    A, B = leer(ENTREGABLE), leer(tmp)
    print(f"entregable: {len(A['texto'])} placas · generado: {len(B['texto'])} placas")
    fallas = []

    if len(A["texto"]) != len(B["texto"]):
        fallas.append(f"distinta cantidad de placas: {len(A['texto'])} vs {len(B['texto'])}")

    for clave, etiqueta in [("texto", "TEXTO"), ("notas", "NOTAS")]:
        d = [i for i in A[clave] if i in B[clave] and A[clave][i] != B[clave][i]]
        print(f"  {etiqueta:6s}: " + (f"difieren las placas {d}" if d else "sin diferencias"))
        for i in d:
            fallas.append(f"{etiqueta.lower()} de la placa {i}")
            sm = difflib.SequenceMatcher(None, A[clave][i].split(), B[clave][i].split())
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                print(f"     placa {i} · entregable: "
                      f"{' '.join(A[clave][i].split()[i1:i2])[:110] or '(nada)'}")
                print(f"     placa {i} · generado  : "
                      f"{' '.join(B[clave][i].split()[j1:j2])[:110] or '(nada)'}")

    d = [k for k in A["graficos"] if A["graficos"][k] != B["graficos"].get(k)]
    print("  GRÁFICOS: " + (f"difieren {d}" if d else "sin diferencias"))
    for k in d:
        fallas.append(f"gráfico {k}")
        print(f"     entregable: {A['graficos'][k]}")
        print(f"     generado  : {B['graficos'].get(k)}")

    if A["medios"] != B["medios"]:
        fallas.append("medios embebidos")
        print(f"  MEDIOS  : entregable {A['medios']} vs generado {B['medios']}")
    else:
        print(f"  MEDIOS  : sin diferencias ({len(A['medios'])} archivos)")

    os.remove(tmp)
    print()
    if fallas:
        print(f"HAY BRECHA — {len(fallas)}: " + "; ".join(fallas))
        print("Si cambió un TEXTO, se edita el PPT y se vuelve a correr "
              "`python extraer_deck.py`,")
        print("que es lo que emite deck_ceo.js. Si cambió el DISEÑO, el camino es el "
              "mismo: el PPT")
        print("es la fuente y el generador lo reproduce.")
        return 1
    print("SIN BRECHA: el entregable es lo que produce el generador.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
