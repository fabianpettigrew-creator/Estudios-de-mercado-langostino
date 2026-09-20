# -*- coding: utf-8 -*-
"""Reescribe `deck_ceo.js` a partir del PPT vigente, que tiene el diseño nuevo.

POR QUÉ EXISTE ESTE GUION. El generador original escribía un diseño que ya no es el
del entregable: el PPT vigente se rediseñó en PowerPoint —Barlow Condensed, lienzo de
20 × 11,25 pulgadas, cabecera con rótulo y paginación, y los gráficos rehechos como
formas nativas en vez de gráficos de Office—. Reescribir ese diseño a mano en
pptxgenjs sería adivinar coordenada por coordenada sobre 636 formas. Se hace al revés:
se lee el PPT y se emite el generador que lo reproduce.

O sea que la autoría del diseño queda en PowerPoint y `deck_ceo.js` pasa a ser una
reproducción fiel y versionable, no la fuente de autor. Es la única forma honesta de
que el generador vuelva a coincidir con el entregable.

QUÉ SE EXTRAE de cada placa: el fondo, y por cada forma su geometría en pulgadas, el
relleno, y —si tiene texto— la tipografía, el cuerpo, el color, la negrita, el
espaciado entre letras, el interlineado y la alineación. Las tres imágenes se vuelcan
a `salidas/media_deck/`.

Uso:  python extraer_deck.py
Salida: deck_ceo.js reescrito + salidas/media_deck/*
"""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(RAIZ, "salidas",
                    "Estudio econométrico - testeo reducción  de captura.pptx")
MEDIA = os.path.join(RAIZ, "salidas", "media_deck")
JS = os.path.join(RAIZ, "deck_ceo.js")
EMU = 914400.0


def _num(x, d=3):
    return round(float(x) / EMU, d)


def _elem(tag: str, s: str):
    """El elemento completo, autocerrado o con hijos. Un `.*?(?:/>|</tag>)` no sirve:
    corta en el primer `/>`, que suele ser el de un hijo."""
    m = re.search(r"<%s\b[^>]*?/>" % tag, s)
    n = re.search(r"<%s\b[^>]*?>.*?</%s>" % (tag, tag), s, re.S)
    if m and (not n or m.start() < n.start()):
        return m.group(0)
    return n.group(0) if n else None


def _xfrm(s: str):
    m = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', s)
    if not m:
        return None
    return {"x": _num(m.group(1)), "y": _num(m.group(2)),
            "w": _num(m.group(3)), "h": _num(m.group(4))}


def _relleno(s: str):
    sp = _elem("p:spPr", s) or s
    if "<a:noFill/>" in sp:
        return None
    m = re.search(r'<a:solidFill><a:srgbClr val="([0-9A-Fa-f]{6})"/></a:solidFill>', sp)
    return m.group(1).upper() if m else None


def _parrafos(sp: str):
    """Cada párrafo con sus runs. Se conserva el formato del texto, que es lo que
    hace que la reproducción se parezca al original y no sólo diga lo mismo."""
    body = _elem("a:bodyPr", sp) or ""
    anchor = re.search(r'anchor="(\w+)"', body)
    # PowerPoint guarda el achique de interlineado del autoajuste aparte del pPr, y hay
    # que multiplicarlo: sin esto el texto queda más suelto de lo que se ve en el PPT.
    red = re.search(r'lnSpcReduction="(\d+)"', body)
    red = int(red.group(1)) / 100000.0 if red else 0.0
    ins = re.search(r'lIns="(\d+)" tIns="(\d+)" rIns="(\d+)" bIns="(\d+)"', body)
    # los insets vienen en EMU y pptxgenjs los quiere en puntos
    margen = round(int(ins.group(1)) / 12700.0, 2) if ins else 0.0
    out = []
    for p in re.findall(r"<a:p>.*?</a:p>", sp, re.S):
        ppr = _elem("a:pPr", p) or ""
        algn = re.search(r'algn="(\w+)"', ppr)
        lns = re.search(r'<a:lnSpc><a:spcPct val="(\d+)"/></a:lnSpc>', ppr)
        runs = []
        for r in re.findall(r"<a:r>.*?</a:r>", p, re.S):
            t = re.search(r"<a:t>(.*?)</a:t>", r, re.S)
            if t is None:
                continue
            rpr = _elem("a:rPr", r) or ""
            col = re.search(r'<a:srgbClr val="([0-9A-Fa-f]{6})"/>', rpr)
            fnt = re.search(r'<a:latin typeface="([^"]+)"', rpr)
            sz = re.search(r'sz="(\d+)"', rpr)
            spc = re.search(r'spc="(-?\d+)"', rpr)
            txt = (t.group(1).replace("&amp;", "&").replace("&lt;", "<")
                   .replace("&gt;", ">").replace("&quot;", '"')
                   .replace("&apos;", "'"))
            run = {"t": txt}
            if sz:
                run["sz"] = int(sz.group(1)) / 100.0
            if col:
                run["c"] = col.group(1).upper()
            if fnt:
                run["f"] = fnt.group(1)
            if re.search(r'\bb="1"', rpr):
                run["b"] = True
            if re.search(r'\bi="1"', rpr):
                run["i"] = True
            if spc:
                run["spc"] = int(spc.group(1)) / 100.0
            runs.append(run)
        if runs:
            par = {"runs": runs}
            if algn:
                par["algn"] = algn.group(1)
            if lns:
                par["lns"] = round(int(lns.group(1)) / 100000.0 * (1 - red), 4)
            out.append(par)
    return out, (anchor.group(1) if anchor else "t"), margen


RE_SP = re.compile(r"<p:sp>.*?</p:sp>", re.S)


def notas(xml: str) -> str:
    """El texto del cuerpo de la placa de notas. Hay que quedarse SÓLO con el
    marcador de posición «body»: las otras dos formas son la miniatura de la placa y
    el número de página, y meterlas ensuciaría las notas con un número suelto."""
    for m in RE_SP.finditer(xml):
        s = m.group(0)
        if '<p:ph type="body"' not in s:
            continue
        t = "".join(re.findall(r"<a:t>(.*?)</a:t>", s, re.S))
        return (t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&apos;", "'"))
    return ""


def placa(x: str, rels: dict):
    fondo = None
    bg = _elem("p:bg", x)
    if bg:
        m = re.search(r'<a:srgbClr val="([0-9A-Fa-f]{6})"/>', bg)
        fondo = m.group(1).upper() if m else None

    formas = []
    tree = x[x.find("<p:spTree>"):]
    for m in re.finditer(r"<p:sp>.*?</p:sp>|<p:pic>.*?</p:pic>", tree, re.S):
        s = m.group(0)
        geo = _xfrm(s)
        if not geo:
            continue
        if s.startswith("<p:pic>"):
            rid = re.search(r'r:embed="(rId\d+)"', s)
            formas.append({"tipo": "img", **geo,
                           "src": rels.get(rid.group(1), "") if rid else ""})
            continue
        pars, anchor, margen = _parrafos(s)
        if pars:
            formas.append({"tipo": "txt", **geo, "anchor": anchor, "m": margen,
                           "p": pars})
        else:
            formas.append({"tipo": "rect", **geo, "fill": _relleno(s)})
    return {"fondo": fondo, "formas": formas}


CABECERA = '''// Generador del deck del langostino tangonero.
//
// Uso:  node deck_ceo.js "salidas/Estudio econométrico - testeo reducción  de captura.pptx"
//
// ATENCIÓN, LEER ANTES DE EDITAR. Este archivo NO es la fuente de autor del diseño.
// El deck se diseña en PowerPoint y este generador lo REPRODUCE: lo emite
// `extraer_deck.py`, que lee el PPT vigente y vuelca placa por placa la geometría, los
// rellenos y el formato del texto. Se hizo así porque el diseño nuevo tiene %d formas
// sobre un lienzo de 20 x 11,25 pulgadas, con los gráficos rehechos como formas
// nativas: transcribirlo a mano sería adivinar coordenadas.
//
// En consecuencia:
//   · para cambiar el DISEÑO, se edita el PPT y se vuelve a correr `extraer_deck.py`;
//   · para cambiar un TEXTO puntual, se puede editar acá, en la constante PLACAS, y
//     regenerar — pero el cambio se pierde en la próxima extracción, así que conviene
//     hacerlo también en el PPT;
//   · `python verificar_deck.py` compara el entregable contra lo que sale de acá.
//
// Fuente del diseño: %s
// Generado por extraer_deck.py el %s
const pptxgen = require("pptxgenjs");
const path = require("path");

const MEDIA = path.join(__dirname, "salidas", "media_deck");
'''

CUERPO = r'''
const pptx = new pptxgen();
pptx.defineLayout({ name: "DECK", width: 20, height: 11.25 });
pptx.layout = "DECK";
pptx.author = "Lic. Fabián Pettigrew";
pptx.company = "AXIA";
pptx.title = "Estudio econométrico · testeo de reducción de captura";

const ALIN = { l: "left", ctr: "center", r: "right", just: "justify" };

PLACAS.forEach(function (pl, i) {
  const s = pptx.addSlide();
  if (pl.fondo) s.background = { color: pl.fondo };
  if (pl.notas) s.addNotes(pl.notas);
  pl.formas.forEach(function (f) {
    const caja = { x: f.x, y: f.y, w: f.w, h: f.h };
    if (f.tipo === "rect") {
      s.addShape(pptx.ShapeType.rect, Object.assign({}, caja, {
        fill: f.fill ? { color: f.fill } : { type: "none" }, line: { width: 0 },
      }));
      return;
    }
    if (f.tipo === "img") {
      s.addImage(Object.assign({}, caja, { path: path.join(MEDIA, f.src) }));
      return;
    }
    // texto: un run de pptxgenjs por cada run del original, para conservar los
    // cambios de cuerpo y color dentro de un mismo párrafo
    const runs = [];
    f.p.forEach(function (par, k) {
      par.runs.forEach(function (r, j) {
        runs.push({
          text: r.t,
          options: {
            fontFace: r.f || "Barlow", fontSize: r.sz || 12,
            color: r.c || "1D1F20", bold: !!r.b, italic: !!r.i,
            charSpacing: r.spc, align: ALIN[par.algn] || "left",
            lineSpacingMultiple: par.lns,
            breakLine: j === par.runs.length - 1 && k < f.p.length - 1,
          },
        });
      });
    });
    s.addText(runs, Object.assign({}, caja, {
      isTextBox: true, margin: f.m || 0, valign: f.anchor === "ctr" ? "middle"
        : f.anchor === "b" ? "bottom" : "top",
      wrap: true,
    }));
  });
});

const salida = process.argv[2]
  || path.join(__dirname, "salidas", "deck_regenerado.pptx");
pptx.writeFile({ fileName: salida })
  .then(function () { console.log("escrito:", salida, "·", PLACAS.length, "placas"); });
'''


def main() -> None:
    import time
    z = zipfile.ZipFile(DECK)
    pres = z.read("ppt/presentation.xml").decode("utf-8")
    prels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
    mapa = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="(slides/slide\d+\.xml)"', prels))
    orden = [mapa[r] for r in re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', pres)]

    os.makedirs(MEDIA, exist_ok=True)
    medios = 0
    for n in z.namelist():
        if n.startswith("ppt/media/"):
            with open(os.path.join(MEDIA, os.path.basename(n)), "wb") as f:
                f.write(z.read(n))
            medios += 1

    placas, formas = [], 0
    for s in orden:
        rels = {}
        rp = f"ppt/slides/_rels/{os.path.basename(s)}.rels"
        if rp in z.namelist():
            rels = {a: os.path.basename(b) for a, b in re.findall(
                r'Id="(rId\d+)"[^>]*Target="([^"]*media[^"]*)"',
                z.read(rp).decode("utf-8"))}
        p = placa(z.read("ppt/" + s).decode("utf-8"), rels)
        nn = ""
        if rp in z.namelist():
            m = re.search(r'Target="\.\./(notesSlides/notesSlide\d+\.xml)"',
                          z.read(rp).decode("utf-8"))
            if m and "ppt/" + m.group(1) in z.namelist():
                nn = notas(z.read("ppt/" + m.group(1)).decode("utf-8"))
        p["notas"] = nn
        formas += len(p["formas"])
        placas.append(p)

    js = (CABECERA % (formas, os.path.basename(DECK),
                      time.strftime("%d de %B de %Y").replace(" 0", " "))
          + "\nconst PLACAS = "
          + json.dumps(placas, ensure_ascii=False, indent=1) + ";\n"
          + CUERPO)
    with open(JS, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"placas: {len(placas)} · formas: {formas} · medios: {medios}")
    print(f"escrito: {JS} ({os.path.getsize(JS):,} bytes)")


if __name__ == "__main__":
    main()
