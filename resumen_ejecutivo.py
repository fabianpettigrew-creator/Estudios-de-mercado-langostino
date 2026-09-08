# -*- coding: utf-8 -*-
"""Resumen ejecutivo del estudio del langostino tangonero, para empresarios del sector.

Dos páginas, sin econometría. El contenido sale del PPT vigente («Estudio econométrico
- testeo reducción  de captura.pptx»), que es el entregable que manda.

Las cifras que cargan el argumento NO están escritas acá. El recorte de política lo da
`recorte_conxemar.py`; los efectos de la simulación salen de la hoja `simulacion` de
`salidas/demanda_inversa_tangonera.xlsx`, y las del episodio de 2025 —captura, precio
relativo y el umbral aritmético— de la hoja `anual` del mismo archivo. Si cambia el
dato, cambia el texto solo.

Siguen transcriptas del PPT las de las tres palancas comerciales, que viven en otros
scripts o sólo en el deck.

Formato de la casa: Calibri en todo el documento y pie de 12 pt con el autor a la
izquierda y el número de página a la derecha. `pie()`, `_campo()`, `_fijar_fuente()` y
`tipografia()` son los del estudio de calamar Illex, copiados para que este estudio
quede autocontenido.

Uso:  python resumen_ejecutivo.py
Salida: salidas/Resumen_ejecutivo_langostino_tangonero.docx
"""
from __future__ import annotations

import os
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, "salidas", "Resumen_ejecutivo_langostino_tangonero.docx")

TINTA = RGBColor(0x12, 0x33, 0x3F)
CORAL = RGBColor(0xE2, 0x70, 0x3A)
GRIS = RGBColor(0x47, 0x56, 0x6B)
GRIS_CLARO = RGBColor(0x6B, 0x7A, 0x8F)


# ------------------------------------------------------------------ formato
def _campo(run, instruccion, marcador):
    """Inserta un campo de Word (PAGE) dentro de un run ya creado."""
    ini = OxmlElement("w:fldChar"); ini.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve")
    instr.text = instruccion
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate")
    txt = OxmlElement("w:t"); txt.text = marcador
    fin = OxmlElement("w:fldChar"); fin.set(qn("w:fldCharType"), "end")
    for e in (ini, instr, sep, txt, fin):
        run._r.append(e)


def pie(doc, autor="Lic. Fabián Pettigrew"):
    """Autor a la izquierda y número de página a la derecha, en 12 pt.

    El número va como campo PAGE para que Word lo recalcule al repaginar, y la
    alineación derecha se resuelve con una tabulación al ancho útil de la caja.
    """
    for s in doc.sections:
        pp = s.footer.paragraphs
        par = pp[0] if pp else s.footer.add_paragraph()
        for r in list(par.runs):
            r._r.getparent().remove(r._r)
        pf = par.paragraph_format
        pf.tab_stops.clear_all()
        pf.tab_stops.add_tab_stop(s.page_width - s.left_margin - s.right_margin,
                                  WD_TAB_ALIGNMENT.RIGHT)
        izq = par.add_run(autor + "\t")
        der = par.add_run()
        for r in (izq, der):
            r.font.name = "Calibri"
            r.font.size = Pt(12)
            r.font.color.rgb = GRIS_CLARO
        _campo(der, " PAGE ", "1")


def _fijar_fuente(rPr, fuente):
    """w:rFonts con la misma familia en los cuatro juegos de caracteres."""
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), fuente)


def _runs(zona):
    for par in zona.paragraphs:
        yield from par.runs
    for t in getattr(zona, "tables", []):
        for fila in t.rows:
            for celda in fila.cells:
                for par in celda.paragraphs:
                    yield from par.runs


def tipografia(doc, fuente="Calibri"):
    """Una sola tipografía en todo el documento: estilos y runs ya escritos.

    Los encabezados heredan la fuente mayor del tema y se saltean el estilo
    Normal, así que hay que fijarla en los dos niveles. Va al final del armado.
    """
    for st in doc.styles:
        try:
            st.font.name = fuente
            _fijar_fuente(st.element.get_or_add_rPr(), fuente)
        except (AttributeError, NotImplementedError):
            continue
    zonas = [doc]
    for s in doc.sections:
        for nombre in ("header", "footer", "first_page_header", "first_page_footer",
                       "even_page_header", "even_page_footer"):
            z = getattr(s, nombre, None)
            if z is not None:
                zonas.append(z)
    for z in zonas:
        for r in _runs(z):
            r.font.name = fuente
            _fijar_fuente(r._r.get_or_add_rPr(), fuente)


def p(doc, texto="", size=10.5, color=TINTA, bold=False, italic=False,
      space_after=6, align=None):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.space_before = Pt(0)
    if align is not None:
        par.alignment = align
    if texto:
        r = par.add_run(texto)
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.bold = bold
        r.italic = italic
    return par


def rico(doc, trozos, size=10.5, space_after=6):
    """Un párrafo con tramos en negrita: [(texto, bold), ...]."""
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.space_before = Pt(0)
    for texto, bold in trozos:
        r = par.add_run(texto)
        r.font.size = Pt(size)
        r.font.color.rgb = TINTA
        r.bold = bold
    return par


def h1(doc, texto):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(14)
    par.paragraph_format.space_after = Pt(6)
    r = par.add_run(texto)
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = TINTA


def vineta(doc, trozos, size=10.5):
    par = doc.add_paragraph(style="List Bullet")
    par.paragraph_format.space_after = Pt(4)
    for texto, bold in trozos:
        r = par.add_run(texto)
        r.font.size = Pt(size)
        r.font.color.rgb = TINTA
        r.bold = bold
    return par


# ------------------------------------------------------------------ datos
def _mil(x) -> str:
    """15520 -> '15.520'."""
    return f"{x:,.0f}".replace(",", ".")


def _dec(x, n=1) -> str:
    """7.3614 -> '7,4'."""
    return f"{abs(x):,.{n}f}".replace(",", "@").replace(".", ",").replace("@", ".")


_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho",
      "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis",
      "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós",
      "veintitrés", "veinticuatro", "veinticinco", "veintiséis", "veintisiete",
      "veintiocho", "veintinueve"]
_D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta",
      8: "ochenta", 9: "noventa"}


def _letras(n: int, femenino: bool = False) -> str:
    """En prosa los números van en letras. Cubre 0-99; afuera cae al dígito."""
    n = int(n)
    if n < 30:
        pal = _U[n] if 0 <= n < len(_U) else str(n)
    elif n < 100:
        d, u = divmod(n, 10)
        pal = _D[d] + (f" y {_U[u]}" if u else "")
    else:
        return str(n)
    return "una" if femenino and pal in ("uno", "veintiuno") else pal


def simulacion() -> dict:
    """El escenario de política, leído de donde se calcula y no escrito acá."""
    import pandas as pd
    import recorte_conxemar

    r = recorte_conxemar.recorte()
    xls = os.path.join(RAIZ, "salidas", "demanda_inversa_tangonera.xlsx")
    if not os.path.exists(xls):
        raise SystemExit("Falta " + xls + ": corré antes demanda_inversa_tangonera.py")
    S = pd.read_excel(xls, sheet_name="simulacion", index_col=0)
    usd = "Δ facturación US$ M"
    pref = S.iloc[0]                                   # la fila preferida va primera
    esc = S[S["Δ facturación %"] < 0]                  # sin la fila del umbral
    return {"corte_t": r["corte_t"], "corte_pct": -r["dq"] * 100,
            "precio_pct": pref["Δ precio %"], "fact_pct": pref["Δ facturación %"],
            "usd": pref[usd], "usd_peor": esc[usd].min(), "usd_mejor": esc[usd].max(),
            "n_esc": len(esc)}


def episodio(a=2024, b=2025) -> dict:
    """El parate de 2025: captura tangonera y precio relativo al camarón de cultivo.

    Sale de la hoja `anual` de `demanda_inversa_tangonera.xlsx`, donde `captura` es el
    desembarque tangonero del año completo y `rel` el precio del entero L1 congelado a
    bordo dividido por el del cultivo, ambos en euros. El umbral es aritmética: cuánto
    debería subir el precio para que la facturación quede igual con menos toneladas.
    """
    import pandas as pd

    xls = os.path.join(RAIZ, "salidas", "demanda_inversa_tangonera.xlsx")
    if not os.path.exists(xls):
        raise SystemExit("Falta " + xls + ": corré antes demanda_inversa_tangonera.py")
    A = pd.read_excel(xls, sheet_name="anual", index_col=0)
    cap_a, cap_b = A.loc[a, "captura"], A.loc[b, "captura"]
    d_cap = (cap_b / cap_a - 1) * 100
    d_pre = (A.loc[b, "rel"] / A.loc[a, "rel"] - 1) * 100
    umbral = (cap_a / cap_b - 1) * 100
    return {"anio_a": a, "anio_b": b, "cap_a": cap_a, "cap_b": cap_b,
            "cap_pct": d_cap, "precio_pct": d_pre, "umbral_pct": umbral,
            "veces": umbral / d_pre}


# ------------------------------------------------------------------ contenido
def main() -> None:
    sim = simulacion()
    ep = episodio()
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(0.8)
        s.left_margin = s.right_margin = Inches(0.9)

    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(2)
    r = par.add_run("LANGOSTINO ARGENTINO · FLOTA TANGONERA")
    r.font.size = Pt(9.5); r.bold = True; r.font.color.rgb = CORAL

    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(2)
    r = par.add_run("¿Conviene pescar menos para vender mejor?")
    r.font.size = Pt(19); r.bold = True; r.font.color.rgb = TINTA

    p(doc, "Resumen ejecutivo · septiembre de 2026", size=10, color=GRIS,
      italic=True, space_after=12)

    p(doc, "La pregunta y la respuesta", size=11, bold=True, space_after=4)
    rico(doc, [
        ("En el sector conviven dos ideas razonables y opuestas. Una dice que si sale "
         "menos mercadería el precio sube y se gana más; es lo que hay detrás de "
         "acortar zafras o cerrar temporadas antes. La otra dice que el precio no lo "
         "ponemos nosotros, lo pone el mercado mundial del camarón, y que recortar "
         "oferta resigna toneladas sin recuperar precio. Este trabajo midió cuál de "
         "las dos describe al langostino argentino. ", False),
        ("Gana la segunda, y por amplio margen.", True)])

    h1(doc, "La prueba: lo que pasó en 2025")
    rico(doc, [
        ("El conflicto gremial de 2025 dejó a la flota tangonera parada cuatro meses. "
         "Entre abril y julio se desembarcaron 106, 150, 103 y 157 toneladas por mes, "
         "contra miles en cualquier año normal: la flota no pescó menos, no salió. Eso "
         "es exactamente la prueba que el dato no suele regalar, una caída de oferta "
         "que no la causó el mercado. El resultado se lee sin ninguna técnica:", False)])
    vineta(doc, [(f"La captura tangonera cayó {_dec(ep['cap_pct'], 0)}%", True),
                 (f", de {_mil(ep['cap_a'])} a {_mil(ep['cap_b'])} toneladas entre "
                  f"{ep['anio_a']} y {ep['anio_b']}.", False)])
    vineta(doc, [(f"El precio subió {_dec(ep['precio_pct'])}%", True),
                 (", medido contra el camarón de cultivo para descontar lo que hizo el "
                  "mercado mundial.", False)])
    rico(doc, [
        ("Para que recortar oferta dejara más plata, el precio tendría que haber "
         "compensado todo el volumen resignado. La cuenta es de almacenero: con la "
         "captura partida al medio, ", False),
        (f"el precio tendría que haber subido {_dec(ep['umbral_pct'])}% sólo para "
         "facturar lo mismo", True),
        (f". Subió {_dec(ep['precio_pct'])}%: {_letras(round(ep['veces']))} veces menos "
         "de lo necesario. No es que el precio no "
         "reaccione —reacciona, y en la dirección esperada—, es que reacciona muchísimo "
         "menos de lo que haría falta para que pescar menos sea negocio.", False)])

    h1(doc, "Qué pasaría con un recorte concreto")
    rico(doc, [
        ("Se simuló un paquete realista: zafra de Rawson acortada a cuatro meses y "
         f"cierre de la zafra nacional a mediados de septiembre. Son {_mil(sim['corte_t'])} "
         f"toneladas menos, el {_dec(sim['corte_pct'])}% del total. El precio sube, sí, "
         f"pero {_dec(sim['precio_pct'])}%. La facturación cae {_dec(sim['fact_pct'])}%: ",
         False),
        (f"unos {_dec(sim['usd'], 0)} millones de dólares por año que el sector deja de "
         "percibir", True),
        (f". La cuenta se repitió con {_letras(sim['n_esc'])} formas distintas de estimar cuánto "
         f"reacciona el precio, y todas dan pérdida: entre {_dec(sim['usd_mejor'], 0)} y "
         f"{_dec(sim['usd_peor'], 0)} millones. El signo y el orden de magnitud son "
         "firmes; la cifra exacta, indicativa.", False)])

    h1(doc, "Entonces, ¿dónde está el valor?")
    p(doc, "Si la palanca del volumen no rinde, el mismo trabajo muestra tres que sí. "
           "Ninguna cuesta toneladas.", space_after=6)
    vineta(doc, [("El canal. ", True),
                 ("El langostino entero se come afuera de casa: restaurante, hotel, "
                  "catering. Si esa actividad cae 10% en los cuatro destinos que "
                  "importan, el precio cae 2,5%; si la captura cae 10%, se mueve 1,8%. "
                  "Seguir la actividad gastronómica de España, Italia, China y Japón "
                  "anticipa mejor el precio que mirar el propio desembarque. Hoy Japón "
                  "sigue 12% por debajo de 2019 y no se recupera: es uno de cada nueve "
                  "kilos de L1.", False)])
    vineta(doc, [("El destino. ", True),
                 ("El mismo producto físico, en el mismo mes, vale distinto según a "
                  "dónde va: China paga 8,6% más que España, Italia 6,0% y Japón 3,5%. "
                  "España se lleva casi la mitad del volumen y paga el precio más bajo "
                  "de la tabla. Ahí hay una decisión comercial, no un dato de la "
                  "naturaleza.", False)])
    vineta(doc, [("La flota y la talla. ", True),
                 ("El entero L1 congelado a bordo vale 25% más que el mismo talle "
                  "procesado en tierra —7,23 contra 5,80 dólares por kilo en 2025—, y "
                  "es 3,4 veces más grande que el camarón ecuatoriano que llega a "
                  "España. Es un producto que el cultivo no replica, y ese tamaño hoy "
                  "no se está cobrando entero.", False)])

    h1(doc, "Qué tan firme es esto")
    rico(doc, [
        ("Conviene decirlo antes de que lo diga otro. ", False),
        ("Sólido:", True),
        (" que el parate fue un shock de oferta genuino y no un efecto del precio; que "
         f"las dos magnitudes del episodio —{_dec(ep['cap_pct'], 0)}% menos "
         f"de captura, {_dec(ep['precio_pct'])}% más de precio— "
         "son observación directa y no dependen de ningún modelo; y que tres "
         "estimaciones con bases y métodos distintos dan lo mismo, todas lejísimos del "
         "umbral en que recortar convendría. ", False),
        ("No conviene afirmar:", True),
        (" el valor exacto del parámetro. La medición se apoya en un solo episodio, y "
         "con un solo episodio no se puede defender el número con decimales. Lo que se "
         "sostiene es el orden de magnitud y la conclusión de política, no la "
         "precisión.", False)])

    h1(doc, "Qué haría falta para afinarlo")
    rico(doc, [
        ("Dos datos que hoy no existen y dependen del sector: las ", False),
        ("existencias mensuales de congelado", True),
        (" —cuánto producto hay en cámara, por presentación y talla, porque hoy se mide "
         "la respuesta del precio al desembarque y no a lo que efectivamente llega al "
         "mercado— y el ", False),
        ("precio del competidor abierto por calibre", True),
        (", que cierra la comparación con el camarón de cultivo. El calendario oficial "
         "de aperturas y cierres ya se probó y no alcanza: el Consejo cierra cuando cae "
         "el rendimiento, así que sus decisiones siguen al recurso en vez de moverlo.",
         False)])

    h1(doc, "En una línea")
    rico(doc, [
        ("Recortar oferta no mejora el ingreso, porque el precio lo pone el mercado "
         "mundial y no la flota. ", True),
        ("El valor está en el canal, el destino y la talla, y ninguna de esas tres "
         "palancas cuesta un solo kilo.", False)])

    p(doc)
    p(doc, "Base del trabajo: trece años y medio de datos mensuales sin huecos "
           "(2013-2026), 68.000 despachos de exportación uno por uno con precio, talla, "
           "destino y flota, y las 547 actas del Consejo Federal Pesquero. Fuentes "
           "primarias: registro aduanero de exportación, base de comercio, INDEC, "
           "Subsecretaría de Pesca y Acuicultura, Eurostat, EUMOFA, NOAA y FAO. El "
           "detalle metodológico está en la presentación completa y su anexo.",
      size=8.5, color=GRIS, space_after=0)

    pie(doc)
    tipografia(doc)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    doc.save(SALIDA)
    print("Guardado:", SALIDA)


if __name__ == "__main__":
    main()
