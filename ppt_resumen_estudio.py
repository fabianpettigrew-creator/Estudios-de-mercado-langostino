# -*- coding: utf-8 -*-
"""
Resumen ejecutivo en PPT del estudio de mercado de langostino argentino.

Las cifras NO se escriben a mano: las de tabla se leen del propio .docx y las
que viven en el cuerpo del texto se declaran como literales en PROSA, que
auditar() grepea contra el documento antes de armar nada.

Diseno: mismo sistema que "Estudio econometrico - testeo reduccion  de captura.pptx"
(20 x 11.25 in, Barlow / Barlow Condensed, paleta azul-pizarra).
"""
import math
import os
import re
import docx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

RAIZ = os.path.dirname(os.path.abspath(__file__))
SALIDAS = os.path.join(RAIZ, "salidas")
ESTUDIO = os.path.join(SALIDAS, "Estudio_mercado_langostino_ver08.09.26.docx")
DESTINO = os.path.join(SALIDAS, "Resumen_estudio_langostino_ver08.09.26.pptx")
FOTO_TAPA = os.path.join(SALIDAS, "media_deck", "image1.jpeg")   # (c) Ricardo Perez

AUTOR = "LIC. FABIÁN PETTIGREW"
FECHA = "SEPTIEMBRE DE 2026"

# --------------------------- paleta y tipografia ---------------------------
BG        = "F2F2F3"
BG_DARK   = "1D2D3D"
BG_ANEXO  = "E9E9EA"
INK       = "1D1F20"
INK_D     = "F2F2F3"
MUTED     = "5D5D60"
MUTED_D   = "D6EBFF"
EYEBROW   = "416180"
EYEBROW_D = "B5D9FD"
RULE      = "1F1F1F"
RULE_D    = "F1F1F4"
AZUL1     = "2C455D"
AZUL2     = "416180"
AZUL3     = "5980A6"
AZUL4     = "749DC4"
AZUL5     = "94BCE3"
AZUL6     = "B5D9FD"
PISTA     = "DEDEE3"
PISTA_D   = "33465A"
TARJETA   = "FFFFFF"
TARJETA_D = "24374B"

HEAD = "Barlow Condensed"
BODY = "Barlow"

M   = 1.17          # margen izquierdo
DER = 18.83         # borde derecho util
CW  = DER - M       # ancho util
T_REGLA_SUP = 1.28
T_TITULO    = 1.71
T_BAJADA    = 2.74
T_REGLA_INF = 9.60


def rgb(h):
    return RGBColor.from_string(h)


# Ancho medio de caracter en Barlow / Barlow Condensed, como fraccion del cuerpo.
# Calibrado midiendo el render de PowerPoint del propio deck.
CHAR_W = 0.55
CHAR_W_COND = 0.44


def alto_texto(txt, ancho, tam, interlinea=1.18, fuente=BODY, holgura=0.93):
    """Alto en pulgadas que ocupa txt en una caja de `ancho` pulgadas."""
    cw = CHAR_W_COND if fuente == HEAD else CHAR_W
    por_linea = max(ancho * 72.0 / (cw * tam) * holgura, 1.0)
    lineas = max(1, int(math.ceil(len(txt) / por_linea)))
    return lineas * tam * interlinea / 72.0


# --------------------------- primitivas de dibujo ---------------------------
class Lamina:
    def __init__(self, prs, fondo=BG, oscura=False):
        self.prs = prs
        self.s = prs.slides.add_slide(prs.slide_layouts[6])
        self.oscura = oscura
        fill = self.s.background.fill
        fill.solid()
        fill.fore_color.rgb = rgb(fondo)

    @property
    def ink(self):     return INK_D if self.oscura else INK

    @property
    def muted(self):   return MUTED_D if self.oscura else MUTED

    @property
    def eyebrow(self): return EYEBROW_D if self.oscura else EYEBROW

    @property
    def rule(self):    return RULE_D if self.oscura else RULE

    @property
    def pista(self):   return PISTA_D if self.oscura else PISTA

    @property
    def acento(self):  return AZUL6 if self.oscura else AZUL1

    def texto(self, txt, x, y, w, h, *, fuente=BODY, tam=20.25, color=None,
              bold=False, align=PP_ALIGN.LEFT, interlinea=None):
        color = color or self.ink
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = align
        if interlinea:
            p.line_spacing = interlinea
        r = p.add_run()
        r.text = txt
        r.font.name = fuente
        r.font.size = Pt(tam)
        r.font.bold = bold
        r.font.color.rgb = rgb(color)
        return tb

    def parrafos(self, lineas, x, y, w, h, *, fuente=BODY, tam=20.25, color=None,
                 bold=False, interlinea=1.15, espacio=9):
        color = color or self.ink
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for i, ln in enumerate(lineas):
            txt, b = (ln, bold) if isinstance(ln, str) else ln
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.line_spacing = interlinea
            p.space_after = Pt(espacio)
            r = p.add_run()
            r.text = txt
            r.font.name = fuente
            r.font.size = Pt(tam)
            r.font.bold = b
            r.font.color.rgb = rgb(color)
        return tb

    def rect(self, x, y, w, h, color):
        sh = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                     Inches(w), Inches(h))
        sh.fill.solid()
        sh.fill.fore_color.rgb = rgb(color)
        sh.line.fill.background()
        sh.shadow.inherit = False
        return sh

    def regla(self, x, y, w, color=None, grosor=0.014):
        return self.rect(x, y, w, grosor, color or self.rule)

    # -------- bloques compuestos --------
    def encabezado(self, seccion, num_lamina, total):
        self.texto(seccion.upper(), M, 0.71, 12.0, 0.43, fuente=HEAD, tam=18,
                   color=self.eyebrow)
        self.texto("%02d / %d" % (num_lamina, total), DER - 2.4, 0.71, 2.4, 0.43,
                   fuente=HEAD, tam=18, color=self.muted, align=PP_ALIGN.RIGHT)
        self.regla(M, T_REGLA_SUP, CW)

    def titulo(self, txt, tam=57, y=T_TITULO, w=None, numero=None):
        if numero is not None:
            self.texto(str(numero), M, y - 0.04, 0.72, 1.2, fuente=HEAD, tam=90,
                       color=AZUL5 if self.oscura else AZUL6)
            x = M + 0.87
        else:
            x = M
        self.texto(txt, x, y, (w or (DER - x)), 1.15, fuente=HEAD, tam=tam,
                   bold=True, color=self.ink, interlinea=0.95)
        return x

    def bajada(self, txt, x=M, y=T_BAJADA, w=None, tam=21.75):
        self.texto(txt, x, y, w or (DER - x), 1.0, fuente=BODY, tam=tam,
                   color=self.muted, interlinea=1.15)

    def pie(self, fuente_txt, y_regla=T_REGLA_INF):
        self.regla(M, y_regla, CW)
        self.texto(fuente_txt, M, y_regla + 0.22, CW, 0.95, fuente=BODY, tam=18,
                   color=self.muted, interlinea=1.15)

    def remate(self, txt, y=8.30, tam=22.5, w=None):
        self.texto(txt, M, y, w or CW, 1.05, fuente=BODY, tam=tam, color=self.ink,
                   interlinea=1.2)

    def barras(self, filas, x, y, *, ancho_etiqueta=2.6, ancho_pista=8.0,
               alto=0.58, paso=1.0, maximo=None, colores=None, sufijo="",
               tam_etiqueta=30, tam_valor=36, ancho_valor=2.3):
        """filas: lista de (etiqueta, valor_float, texto_valor)"""
        maximo = maximo or max(v for _, v, _ in filas)
        colores = colores or [AZUL1, AZUL2, AZUL3, AZUL4, AZUL5, AZUL6]
        xb = x + ancho_etiqueta
        for i, (et, val, txt) in enumerate(filas):
            yy = y + i * paso
            self.texto(et, x, yy - 0.06, ancho_etiqueta - 0.25, 0.7, fuente=HEAD,
                       tam=tam_etiqueta, color=self.ink)
            self.rect(xb, yy, ancho_pista, alto, self.pista)
            frac = 0.0 if maximo == 0 else max(val, 0.0) / maximo
            if frac > 0:
                self.rect(xb, yy, max(ancho_pista * frac, 0.035), alto,
                          colores[i % len(colores)])
            self.texto(txt + sufijo, xb + ancho_pista + 0.28, yy - 0.10,
                       ancho_valor, 0.84, fuente=HEAD, tam=tam_valor,
                       color=self.acento)
        return y + len(filas) * paso

    def cifra(self, valor, rotulo, detalle, x, y, w, *, tam=120):
        self.regla(x, y, min(w, 8.42), AZUL6 if self.oscura else AZUL3)
        self.texto(valor, x, y + 0.26, w, 2.1, fuente=HEAD, tam=tam,
                   color=self.ink, interlinea=0.9)
        yy = y + 0.26 + tam / 72.0 * 1.10
        self.texto(rotulo, x, yy, w, 0.62, fuente=HEAD, tam=33, color=self.ink)
        self.texto(detalle, x, yy + 0.66, w, 1.2, fuente=BODY, tam=20.25,
                   color=self.muted, interlinea=1.15)

    def tarjeta(self, x, y, w, h, titulo, cuerpo, *, kicker=None, acento=AZUL3,
                tam_titulo=31, tam_cuerpo=19.5):
        """Dibuja la tarjeta encogiendo el cuerpo hasta que entre en la caja."""
        aw = w - 0.92
        while True:
            ht = alto_texto(titulo, aw, tam_titulo, 0.98, HEAD)
            hc = alto_texto(cuerpo, aw, tam_cuerpo, 1.18, BODY)
            total = 0.44 + (0.56 if kicker else 0.0) + ht + 0.24 + hc + 0.40
            if total <= h or tam_cuerpo <= 14.0:
                break
            tam_cuerpo -= 0.5
            if tam_cuerpo < 17.0 and tam_titulo > 25:
                tam_titulo -= 1
        if total > h:
            raise SystemExit("Tarjeta '%s': no entra (%.2f in en %.2f in)"
                             % (titulo[:40], total, h))
        self.rect(x, y, w, h, TARJETA_D if self.oscura else TARJETA)
        self.rect(x, y, w, 0.09, acento)
        yy = y + 0.44
        if kicker:
            self.texto(kicker.upper(), x + 0.46, yy, aw, 0.42, fuente=HEAD,
                       tam=18, color=acento)
            yy += 0.56
        self.texto(titulo, x + 0.46, yy, aw, ht + 0.1, fuente=HEAD,
                   tam=tam_titulo, color=self.ink, interlinea=0.98)
        self.texto(cuerpo, x + 0.46, yy + ht + 0.24, aw, hc + 0.1,
                   fuente=BODY, tam=tam_cuerpo, color=self.muted, interlinea=1.18)

    def bloques(self, items, x, y, w, *, gap=0.32):
        """Apila textos calculando el alto de cada uno. items: dicts."""
        for it in items:
            tam = it.get("tam", 20.25)
            il = it.get("interlinea", 1.18)
            fu = it.get("fuente", BODY)
            h = alto_texto(it["txt"], w, tam, il, fu)
            self.texto(it["txt"], x, y, w, h + 0.12, fuente=fu, tam=tam,
                       color=it.get("color", self.muted), bold=it.get("bold", False),
                       interlinea=il)
            y += h + it.get("gap", gap)
        return y

    def columna(self, x, y, w, items, *, limite=9.42, acento_regla=True):
        """Regla de acento + bloques apilados, encogiendo el cuerpo hasta que entre."""
        if acento_regla:
            self.regla(x, y, w, AZUL6 if self.oscura else AZUL3, grosor=0.03)
            y += 0.27
        escala = 1.0
        while True:
            alto = 0.0
            for it in items:
                alto += alto_texto(it["txt"], w, it.get("tam", 20.25) * escala,
                                   it.get("interlinea", 1.18),
                                   it.get("fuente", BODY))
                alto += it.get("gap", 0.32) * (0.85 if escala < 1.0 else 1.0)
            if y + alto <= limite or escala <= 0.72:
                break
            escala -= 0.03
        if y + alto > limite:
            raise SystemExit("Columna en x=%.2f no entra ni al 72%%: %.2f > %.2f"
                             % (x, y + alto, limite))
        ajustados = []
        for it in items:
            c = dict(it)
            c["tam"] = it.get("tam", 20.25) * escala
            c["gap"] = it.get("gap", 0.32) * (0.85 if escala < 1.0 else 1.0)
            ajustados.append(c)
        return self.bloques(ajustados, x, y, w)

    def filas_dato(self, filas, x, y, w, *, paso=1.02, tam_izq=30, tam_der=21,
                   ancho_izq=8.6):
        """filas: lista de (izquierda, derecha). Fila con regla arriba."""
        for i, (izq, der) in enumerate(filas):
            yy = y + i * paso
            self.regla(x, yy, w, self.rule if not self.oscura else RULE_D,
                       grosor=0.010)
            self.texto(izq, x, yy + 0.16, ancho_izq, 0.66, fuente=HEAD,
                       tam=tam_izq, color=self.ink)
            self.texto(der, x + ancho_izq + 0.3, yy + 0.22, w - ancho_izq - 0.3,
                       0.66, fuente=BODY, tam=tam_der, color=self.muted)
        return y + len(filas) * paso

    def notas(self, txt):
        self.s.notes_slide.notes_text_frame.text = txt


# --------------------------- lectura del estudio ---------------------------
def leer_estudio(ruta):
    if not os.path.exists(ruta):
        raise SystemExit("No está el estudio: %s" % ruta)
    try:
        with open(ruta, "rb") as fh:
            fh.read(4)
    except PermissionError:
        raise SystemExit(
            "El estudio está abierto en Word y queda bloqueado para lectura.\n"
            "Cerralo y volvé a correr: %s" % os.path.basename(ruta))
    d = docx.Document(ruta)
    tablas = [[[c.text.strip().replace("\n", " ") for c in r.cells] for r in t.rows]
              for t in d.tables]
    texto = "\n".join(p.text for p in d.paragraphs)
    for t in d.tables:
        for r in t.rows:
            texto += "\n" + " | ".join(c.text.strip() for c in r.cells)
    return tablas, texto


def tabla(tablas, i, cabecera_esperada):
    """Devuelve la tabla i verificando su cabecera: si el .docx cambia, falla aca."""
    t = tablas[i]
    if cabecera_esperada.lower() not in t[0][0].lower():
        raise SystemExit("Tabla %d: se esperaba cabecera '%s' y dice '%s'"
                         % (i, cabecera_esperada, t[0][0]))
    return t


def num(s):
    """'>=141,1' -> 141.1 ; '~17%' -> 17.0 ; '-46%' -> -46.0"""
    s = (s.replace("−", "-").replace("≥", "").replace("~", "")
          .replace("%", "").replace("US$", "").replace("$", "").replace("€", ""))
    s = s.strip()
    s = s.split()[0] if s else "0"
    s = s.replace(".", "").replace(",", ".")
    m = re.match(r"^-?\d+(\.\d+)?", s)
    return float(m.group(0)) if m else 0.0


# ------- literales de prosa: se verifican contra el texto del estudio -------
PROSA = {
    "captura_pico": "255", "captura_2024": "222",
    "tang_2024": "90,1", "tang_2025": "48,3", "tang_caida": "−46%",
    "fresq_var": "+5%", "total_desem": "187,0",
    "l1_tang": "7,23", "l1_fresq": "5,80", "brecha_l1": "+25%",
    "brecha_2025": "2,15x", "tang_kg": "7,08",
    "fob_min": "5,68", "fob_max": "6,53", "amplitud": "15%", "mix_44": "44%",
    "cong_jun_oct": "80%", "fresq_dic_feb": "63%",
    "es_l1_planta": "19,8%", "abordo_it": "6,59", "abordo_es": "6,37",
    "eeuu_directo": "5,3 kt", "eeuu_origen": "17,0 kt", "via_terceros": "69%",
    "peru_kt": "8,6 kt", "peru_share": "34%", "peru_eeuu": "64%",
    "cola_a_peru": "29,5 kt", "peru_pelado": "20,0 kt",
    "margen_kg": "0,55", "margen_pct": "8%",
    "fao_share": "99,5%", "fason_fresquero": "99,6%",
    "vannamei_mt": "7,66 Mt", "vannamei_x": "×2,9", "vannamei_34": "34 veces",
    "ec_entero_2013": "5,9 kt", "ec_entero_2025": "202,4 kt",
    "ec_precio_2013": "6,90", "ec_precio_2025": "4,91",
    "granja_2015": "5,50", "granja_2024": "3,60", "granja_caida": "35%",
    "ec_cuota_ini": "14%", "ec_cuota_fin": "49%", "ar_cuota_fin": "21%",
    "es_ent_ar_2018": "72,6", "es_ent_ec_2018": "1,8",
    "es_ent_ar_2025": "28,3", "es_ent_ec_2025": "17,5", "ar_perdida": "61%",
    "premium": "1,6", "premium_rango": "1,3 y 1,8",
    "msc_share": "1-2%", "msc_upside": "US$15-30 millones",
    "gondola_es": "€12,00/kg", "gondola_us": "$25/kg",
    "sirena_ar": "€11,00", "sirena_ec": "€12,99", "prima_1520": "+33%",
    "expo_pico": "186 kt", "entero_2013": "86%",
    "tang_share_2013": "71%", "tang_share_2024": "41%", "correl": "+0,99",
    "tang_2026": "57,6 kt", "despachos": "13.003",
    "ventaja_india": "~7 puntos", "eeuu_prima": "60%",
    "ec_china": "50,1%", "cv_ec": "0,28", "cv_ar": "0,59",
    "total_caida": "−16%", "desem_2024_total": "222,2",
    "es_precio_ini": "€6,09", "es_precio_fin": "€6,51",
    "brecha_espana": "1,01", "tang_espana": "43,5%", "fresq_conc": "60%",
    "reproceso_ue": "menos del 4%",
}


def auditar(texto):
    faltan = [k for k, v in PROSA.items() if v not in texto]
    if faltan:
        raise SystemExit("Cifras de prosa ausentes del estudio: "
                         + ", ".join("%s=%r" % (k, PROSA[k]) for k in faltan))
    print("Auditoria: %d literales de prosa verificados contra el .docx."
          % len(PROSA))


# =========================== armado del deck ===========================
TOTAL = 22
P = PROSA


def construir():
    tablas, texto = leer_estudio(ESTUDIO)
    auditar(texto)

    t_clave   = tabla(tablas,  0, "Métrica")
    t_brecha  = tabla(tablas,  1, "Año")
    t_hubs    = tabla(tablas,  4, "País")
    t_talle   = tabla(tablas,  5, "Presentación / calibre")
    t_dest    = tabla(tablas,  8, "Destino (entero L1)")
    t_ue      = tabla(tablas,  9, "Cronograma UE")
    t_eeuu    = tabla(tablas, 10, "Origen (EE.UU.")
    t_vanna   = tabla(tablas, 11, "Productor de vannamei")
    t_serie   = tabla(tablas, 12, "Año")

    prs = Presentation()
    prs.slide_width = Inches(20)
    prs.slide_height = Inches(11.25)

    # ---------- 01 · portada ----------
    L = Lamina(prs)
    if os.path.exists(FOTO_TAPA):
        L.s.shapes.add_picture(FOTO_TAPA, Inches(10.81), Inches(1.54),
                               Inches(8.03), Inches(8.24))
    L.texto("ESTUDIO DE MERCADO · LANGOSTINO ARGENTINO", M, 1.00, 12.0, 0.43,
            fuente=HEAD, tam=18, color=EYEBROW)
    L.texto("Precio, comercio y\nposición competitiva", M, 2.70, 9.4, 3.6,
            fuente=HEAD, tam=78, bold=True, color=INK, interlinea=0.92)
    L.regla(M, 6.55, 2.08, AZUL3, grosor=0.03)
    L.texto("Un producto salvaje de nicho, sobre una base productiva que se achica, "
            "compitiendo contra una marea de langostino de cultivo. Su valor no está "
            "en el precio-commodity sino en lo que es —salvaje, entero, premium—, y "
            "los datos dicen dónde y cómo defenderlo.",
            M, 6.95, 8.9, 2.2, fuente=BODY, tam=23, color=MUTED, interlinea=1.2)
    L.texto("RESUMEN EJECUTIVO · %d LÁMINAS" % TOTAL, M, 9.35, 10.0, 0.43,
            fuente=HEAD, tam=18, color=AZUL3)
    L.texto("%s · %s" % (FECHA, AUTOR), M, 9.91, 12.0, 0.46, fuente=HEAD,
            tam=19.5, color=MUTED)
    L.notas("Resumen del estudio de mercado, versión 08.09.26. Doce secciones "
            "condensadas en veintidós láminas; todas las cifras salen del documento.")

    # ---------- 02 · el cuadro en cinco números ----------
    L = Lamina(prs, BG_DARK, oscura=True)
    L.encabezado("El cuadro", 2, TOTAL)
    L.titulo("El estudio en cinco números", tam=60)
    L.bajada("Dónde está parado hoy el langostino argentino, antes de entrar en el detalle.")
    L.filas_dato([(f[0], f[1]) for f in t_clave[1:]], M, 3.90, CW, paso=1.02)
    L.pie("Fuente: estudio de mercado de langostino argentino, versión 08.09.26 · "
          "aduana argentina oficial · base de comercio (transaccional, FOB, "
          "precio/calibre) · SSPyA · NOAA FOSS · FAO FishStat.")
    L.notas("Cinco números para abrir: el premium que sostiene el negocio, el mejor "
            "uso del calibre grande, la base productiva que se achica, la marea de "
            "cultivo que crece y la ausencia de competencia salvaje directa.")

    # ---------- 03 · la tesis ----------
    L = Lamina(prs)
    L.encabezado("La tesis", 3, TOTAL)
    L.titulo("No se compite por volumen ni por precio", tam=57)
    L.bajada("Una conclusión atraviesa las doce secciones del estudio, y ordena todo "
             "lo que viene después.")
    ancho = (CW - 2 * 0.55) / 3
    L.tarjeta(M, 3.90, ancho, 4.15, "La base productiva se achica",
              "La captura tocó máximo en 2018 (%s kt) y en 2024 está 13%% por debajo "
              "(%s kt). Una pesquería no puede expandirse a voluntad: cada tonelada "
              "es más escasa que la anterior."
              % (P["captura_pico"], P["captura_2024"]),
              kicker="1", acento=AZUL1)
    L.tarjeta(M + ancho + 0.55, 3.90, ancho, 4.15, "El sustituto crece y abarata",
              "El vannamei de cultivo se multiplicó %s desde 2010 y hoy son %s, "
              "%s la captura argentina. Y no baja el precio resignando margen: baja "
              "porque le baja el costo."
              % (P["vannamei_x"], P["vannamei_mt"], P["vannamei_34"]),
              kicker="2", acento=AZUL2)
    L.tarjeta(M + 2 * (ancho + 0.55), 3.90, ancho, 4.15, "El valor está en el atributo",
              "Salvaje, entero, calibre grande, origen identificable y —desde 2026— "
              "certificado MSC. Es lo único que el cultivo no puede replicar, y es "
              "donde se defiende el precio.",
              kicker="3", acento=AZUL3)
    L.remate("El corolario operativo: no hay que buscar más toneladas, hay que "
             "capturar más valor en cada tonelada — eligiendo flota, formato, "
             "calibre, destino y momento.", y=8.45)
    L.pie("Secciones 1, 9 y 10 del estudio.")
    L.notas("Si sólo se recuerda una lámina, es ésta. Las tres tarjetas son las tres "
            "restricciones estructurales; el resto del deck muestra dónde se ejecuta "
            "la respuesta.")

    # ---------- 04 · advertencia de lectura ----------
    L = Lamina(prs)
    L.encabezado("Advertencia de lectura", 4, TOTAL)
    L.titulo("2025 es un shock de oferta, no una pérdida de mercado", tam=54)
    L.bajada("La flota congeladora tangonera no salió a pescar por conflictos "
             "laborales y estuvo prácticamente detenida de abril a julio.")
    L.cifra(P["tang_caida"], "cayó la captura tangonera",
            "de %s a %s kt entre 2024 y 2025 · dato oficial SSPyA"
            % (P["tang_2024"], P["tang_2025"]), M, 3.85, 8.6, tam=126)
    L.cifra(P["total_caida"], "cayó el desembarque total",
            "de %s a %s kt · la fresquera, en cambio, creció %s"
            % (P["desem_2024_total"], P["total_desem"], P["fresq_var"]),
            10.42, 3.85, 8.4, tam=126)
    L.remate("Todo lo que ocurre en 2025 —menos volumen exportado, derrumbe del "
             "entero— se lee como oferta faltante. La única excepción es España: "
             "esa pérdida viene de antes del conflicto y sí es competitiva (lámina 17).",
             y=8.35)
    L.pie("Secciones 1 y 11 · desembarques SSPyA por puerto, flota y mes.")
    L.notas("Vale aclararlo antes de que lo pregunten: casi todos los indicadores "
            "de 2025 están contaminados por el parate. Las conclusiones "
            "estructurales se apoyan en la serie larga.")

    # ---------- 05 · el producto ----------
    L = Lamina(prs)
    L.encabezado("El producto", 5, TOTAL)
    L.titulo("Dos flotas, dos cadenas de valor distintas", tam=57)
    L.bajada("La diferencia no es sólo tecnológica: define productos, plantas y "
             "mercados propios.")
    mitad = (CW - 0.55) / 2
    L.tarjeta(M, 3.90, mitad, 4.15, "Congeladora tangonera",
              "Congela a bordo en las horas siguientes a la captura: corta temprano "
              "la degradación y minimiza la melanosis. Produce esencialmente entero "
              "en bloque por calibre (L1 a L5) en cajas de 2 kg, y algo de sin "
              "cabeza. Opera en aguas nacionales y exporta directo, sin pasar por "
              "planta.", kicker="Congelado a bordo · sufijo SA01", acento=AZUL1)
    L.tarjeta(M + mitad + 0.55, 3.90, mitad, 4.15, "Fresquera",
              "Mantiene la captura en hielo y metabisulfito durante mareas de 3 a 10 "
              "días y congela recién en planta: más riesgo de melanosis y textura más "
              "blanda. A cambio, la planta hace lo que el buque no puede —pelado, "
              "desvenado, easy peel, cocido, IQF— y con eso accede a EE.UU. Opera "
              "fuerte en aguas provinciales de Chubut.",
              kicker="Congelado en tierra", acento=AZUL3)
    L.remate("Las dos flotas casi no compiten entre sí: hacen productos distintos, "
             "para clientes distintos y en meses distintos del año. Casi todo lo que "
             "sigue —precio, destino, estacionalidad, aranceles— se ordena por esta "
             "división.", y=8.45, tam=22.5)
    L.pie("Sección 2 del estudio · producto y proceso por flota.")
    L.notas("Es la lámina de encuadre: si esta división queda clara, el resto del "
            "deck se lee solo. La congeladora despacha el grueso de su volumen entre "
            "junio y octubre; la fresquera, en el verano.")

    # ---------- 06 · las dos flotas ----------
    L = Lamina(prs)
    L.encabezado("Las dos flotas", 6, TOTAL)
    L.titulo("La tangonera genera el doble de valor por tonelada", tam=57)
    L.bajada("Y la brecha no es sólo mezcla de producto: el mismo talle vale más si "
             "lo trae el tangonero.")
    L.cifra(P["brecha_2025"], "la brecha de valor por tonelada",
            "US$%s por kilo desembarcado la tangonera contra ~US$3,3 la fresquera "
            "en 2025 · la escasez de entero premium ensanchó la diferencia"
            % P["tang_kg"], M, 3.85, 8.6, tam=120)
    L.cifra(P["brecha_l1"], "vale el entero L1 tangonero",
            "US$%s contra %s el fresquero en 2025 · mismo calibre, misma unidad · "
            "en cola la diferencia es de +22%% en C1"
            % (P["l1_tang"], P["l1_fresq"]), 10.42, 3.85, 8.4, tam=120)
    L.remate("Dónde vive la brecha: donde las dos flotas compiten de verdad casi no "
             "hay diferencia (Japón −0,19, China +0,20, Italia +0,35 dólares por "
             "kilo). La brecha sale de España, donde la diferencia es de US$%s. El "
             "problema de la fresquera no es el producto: es que manda el %s de su "
             "volumen a un solo comprador y ahí cobra el precio más bajo de la "
             "matriz." % (P["brecha_espana"], P["fresq_conc"]), y=8.20, tam=21)
    L.pie("Sección 6 · aduana argentina (sufijo SA) ÷ desembarques SSPyA · el "
          "rendimiento de entero a cola se toma en 0,55 para las dos flotas, así que "
          "la brecha es de precio y no de supuesto.")
    L.notas("La tangonera reparte entre cuatro mercados grandes: España %s, Italia "
            "21,1%%, China 13,6%% y Japón 11,5%%. La fresquera concentra."
            % P["tang_espana"])

    # ---------- 07 · presentación y talle ----------
    L = Lamina(prs)
    L.encabezado("Presentación y talle", 7, TOTAL)
    L.titulo("El entero grande es el mejor uso del calibre grande", tam=57)
    L.bajada("Ingreso neto por kilo de langostino desembarcado: precio de aduana × "
             "rendimiento. No es lo mismo que el precio del kilo vendido.")
    filas = [(f[0], num(f[3]), f[3]) for f in t_talle[1:]]
    L.barras(filas, M, 3.95, ancho_etiqueta=3.05, ancho_pista=6.3, alto=0.50,
             paso=0.745, tam_etiqueta=27, tam_valor=31, ancho_valor=1.6,
             colores=[AZUL1, AZUL2, AZUL2, AZUL3, AZUL4, AZUL4, AZUL5])
    L.texto("US$ por kilo desembarcado", M, 3.50, 8.0, 0.42, fuente=BODY, tam=18.75,
            color=MUTED)
    L.regla(13.45, 4.05, 5.38, AZUL3, grosor=0.03)
    L.texto("31% menos", 13.45, 4.32, 5.4, 1.1, fuente=HEAD, tam=78, color=AZUL1)
    L.texto("rinde la mejor cola P&D que el entero L1, por kilo capturado — aunque "
            "el kilo de P&D se venda a US$12,4 y el de entero a US$7,0.",
            13.45, 5.45, 5.3, 1.5, fuente=BODY, tam=20.25, color=MUTED,
            interlinea=1.18)
    L.texto("De un kilo capturado quedan 1,00 kg de entero, 0,55 de cola y 0,385 de "
            "pelado y devenado. Cada paso deja menos kilos vendibles aunque suba el "
            "precio del kilo vendido.", 13.45, 7.05, 5.3, 1.8, fuente=BODY, tam=21,
            color=INK, interlinea=1.18)
    L.remate("Cómo clasifica la industria: grande (L1) → entero a España e Italia · "
             "con proceso → cola P&D a EE.UU. · cola → Asia, el canal de menor valor. "
             "La decisión es por calibre, no por mercado.", y=9.05, w=11.9, tam=21)
    L.pie("Sección 5 · FOB real de exportación argentina 2025-26. No contempla el "
          "glaseo: si las presentaciones glasean distinto, parte de la diferencia "
          "por kilo es agua y el orden puede cambiar.", y_regla=9.95)
    L.notas("La tabla no dice que convenga dejar de pelar: dice que el calibre grande "
            "rinde más entero, y que el pelado es el uso correcto del calibre chico.")

    # ---------- 08 · precio y estacionalidad ----------
    L = Lamina(prs)
    L.encabezado("Precio y estacionalidad", 8, TOTAL)
    L.titulo("Estacional en origen, y la mitad de eso es mezcla de flota", tam=54)
    L.bajada("El precio en destino no reproduce el perfil de origen: el CIF llega con "
             "rezago, mezcla embarques de meses distintos y agrupa calibres que la "
             "partida no separa.")
    L.cifra(P["amplitud"], "de amplitud dentro del año",
            "el FOB del entero toca piso en febrero (US$%s/kg) y máximo en junio "
            "(US$%s), y se sostiene sobre US$6,26 hasta octubre"
            % (P["fob_min"], P["fob_max"]), M, 3.85, 8.6, tam=126)
    L.cifra(P["mix_44"], "de esa brecha es mezcla de flota",
            "con el mix fijo desaparece: la congeladora despacha el %s de su volumen "
            "entre junio y octubre y la fresquera el %s entre diciembre y febrero"
            % (P["cong_jun_oct"], P["fresq_dic_feb"]), 10.42, 3.85, 8.4, tam=126)
    L.remate("Dentro de cada flota la estacionalidad es moderada —14% la congeladora, "
             "22% la fresquera— y ninguna muestra relación clara entre precio y "
             "volumen del mes. Los meses de verano se ven baratos porque exporta la "
             "flota que cobra menos, no porque el mercado pague menos.", y=8.30,
             tam=21.5)
    L.pie("Secciones 3 y 7 · serie mensual de aduana y base de comercio "
          "(transaccional): entero L1, 2018-2026, %s despachos depurados."
          % P["despachos"])
    L.notas("Ojo con leer la curva agregada como si fuera una oportunidad de "
            "arbitraje temporal: casi la mitad es composición.")

    # ---------- 09 · destinos ----------
    L = Lamina(prs)
    L.encabezado("Destinos", 9, TOTAL)
    L.titulo("España se lleva el volumen y aparece pagando menos", tam=57)
    L.bajada("Entero L1, el producto insignia. La barra es el porcentaje del volumen; "
             "al lado, el FOB promedio de ese destino.")
    filas = []
    for f in t_dest[1:-1]:
        filas.append((f[0].split(" (")[0], num(f[2]), "%s%%  ·  US$%s" % (f[2], f[1])))
    L.barras(filas, M, 4.35, ancho_etiqueta=2.3, ancho_pista=5.3, alto=0.58,
             paso=1.02, tam_etiqueta=30, tam_valor=27, ancho_valor=3.2,
             colores=[AZUL2, AZUL3, AZUL4, AZUL1, AZUL5])
    L.texto("% del volumen de entero L1  ·  FOB US$/kg", M, 3.88, 9.0, 0.42,
            fuente=BODY, tam=18.75, color=MUTED)
    L.columna(12.55, 3.95, 6.28, [
        {"txt": "La mitad de la brecha es ruta de proceso", "fuente": HEAD,
         "tam": 42, "color": AZUL1, "interlinea": 0.95, "gap": 0.38},
        {"txt": "España es el único que compra L1 procesado en tierra en volumen "
                "—el %s de su L1, contra 2,4%% de Italia, 4,2%% de China y 1,5%% de "
                "Japón— y ese producto vale un dólar menos por kilo."
                % P["es_l1_planta"], "tam": 20.25, "gap": 0.38},
        {"txt": "Comparando sólo congelado a bordo el panel se aplana: Italia "
                "US$%s, China 6,38, España US$%s, Japón 6,31. Lo que queda —la "
                "ventaja de Italia, que se repite en siete de los nueve años— sí es "
                "mercado." % (P["abordo_it"], P["abordo_es"]),
         "tam": 21, "color": INK},
    ])
    L.pie("Sección 7 · base de comercio (transaccional), entero L1 2018-2026. El FOB "
          "no está controlado por el momento de compra ni por la ruta de proceso.")
    L.notas("Italia concentra el 48% de su compra en septiembre-octubre, justo los "
            "meses del precio máximo, y aun así paga la prima: compra la calidad del "
            "pico, no oportunidad.")

    # ---------- 10 · flujo comercial ----------
    L = Lamina(prs)
    L.encabezado("Flujo comercial", 10, TOTAL)
    L.titulo("España es la puerta de Europa; EE.UU. es otro negocio", tam=54)
    L.bajada("El langostino entra a la UE sobre todo directo a España e Italia; "
             "España re-despacha al resto y eso oculta el origen argentino en las "
             "estadísticas de Francia e Italia, que registran por procedencia.")
    ancho = (CW - 2 * 0.55) / 3
    L.tarjeta(M, 3.95, ancho, 4.40, "España · el hub",
              "Casi la mitad del entero L1 y un tercio de la exportación total. Es "
              "también el único que compra volumen de L1 procesado en tierra, el "
              "único que sostiene compra en verano y el comprador más estacional "
              "(26% entre pico y piso).", kicker="Destino 1", acento=AZUL1)
    L.tarjeta(M + ancho + 0.55, 3.95, ancho, 4.40, "Italia · compra directo",
              "El 18,4% del L1 y el destino que mejor paga a igual ruta de proceso. "
              "Es 88% tangonero, el más parejo del año (14% de amplitud) y compra en "
              "el pico de precio sin pedir descuento.", kicker="Destino 2",
              acento=AZUL2)
    L.tarjeta(M + 2 * (ancho + 0.55), 3.95, ancho, 4.40, "EE.UU. · otro producto",
              "Cerca de un tercio del volumen europeo y paga un %s más por kilo en la "
              "misma moneda — pero compra cola pelada, no entero: 67%% pelado y 33%% "
              "con cáscara, contra 90%% pelado de India y 52%% con cáscara de Ecuador."
              % P["eeuu_prima"], kicker="Destino 3", acento=AZUL3)
    L.remate("Los dos mapas son, en el fondo, el mismo: Japón compra 99% tangonera, "
             "Italia 88% y España 71%, mientras el circuito de cola y reproceso es "
             "casi enteramente fresquero. Destino y flota son la misma variable.",
             y=8.55, tam=21.5)
    L.pie("Secciones 4, 5 y 7 · NOAA FOSS (EE.UU.) · Comext (UE-27) · aduana "
          "argentina oficial · base de comercio (origen España).")
    L.notas("Que EE.UU. pague más por kilo no significa que convenga: paga más por un "
            "producto que rinde 31% menos por kilo capturado.")

    # ---------- 11 · el fasón ----------
    L = Lamina(prs)
    L.encabezado("El fasón", 11, TOTAL)
    L.titulo("Dos de cada tres kilos argentinos en EE.UU. no salen de Argentina",
             tam=51)
    L.bajada("La aduana estadounidense registra ORIGEN, no procedencia — y pelar no "
             "cambia el origen. Por eso su dato incluye producto argentino "
             "reprocesado en terceros países.")
    L.cifra(P["eeuu_origen"], "registra EE.UU. de origen argentino",
            "contra %s despachadas directo desde Argentina en 2025 (INDEC): una "
            "brecha de 11,8 kt" % P["eeuu_directo"], M, 3.85, 8.6, tam=120)
    L.cifra(P["via_terceros"], "llegó por reprocesado en otros mercados",
            "era el 56%% en 2024 · el circuito documentado mueve unas 9,6 kt al año",
            10.42, 3.85, 8.4, tam=120)
    L.remate("Y es un circuito exclusivamente fresquero: la cola que va a los países "
             "de reproceso —Perú, Tailandia, Vietnam, Indonesia— es %s de origen "
             "fresquero. La tangonera no participa: vende entero premium directo a "
             "mercados finales. La discusión sobre el margen que se pela afuera es, "
             "en rigor, una discusión sobre la cadena fresquera y su capacidad de "
             "planta." % P["fason_fresquero"], y=8.15, tam=21.5)
    L.pie("Sección 4 · aduana argentina (INDEC y sufijo SA) · NOAA FOSS por país de "
          "origen · acumulado 2023-2025 para el corte por flota.")
    L.notas("El dato de 2024 y 2025 está en la tabla del estudio: 6,4 contra 14,5 kt "
            "el primer año, 5,3 contra 17,0 el segundo.")

    # ---------- 12 · el fasón, probado ----------
    L = Lamina(prs)
    L.encabezado("El fasón · la prueba", 12, TOTAL)
    L.titulo("Perú lo declara por nombre, y las dos aduanas cierran", tam=57)
    L.bajada("El fenómeno era inexistente hasta 2021, arranca en 2022 y hoy es "
             "estructural.")
    ancho = (CW - 2 * 0.55) / 3
    L.tarjeta(M, 3.90, ancho, 4.55, "La aduana peruana nombra la especie",
              "En la descripción aduanera aparece literalmente «Pleoticus muelleri»: "
              "pasó de 0 a %s, el %s de toda la exportación peruana de langostino. De "
              "las 8,47 kt que Perú despachó a EE.UU. en 2025, el %s era langostino "
              "argentino." % (P["peru_kt"], P["peru_share"], P["peru_eeuu"]),
              kicker="Probado", acento=AZUL1)
    L.tarjeta(M + ancho + 0.55, 3.90, ancho, 4.55, "Nadie más lo pesca",
              "Según FAO FishStat, Argentina es el %s de la captura mundial de la "
              "especie. Perú captura cero. Cada kilo que despacha bajo ese nombre es "
              "necesariamente argentino reprocesado: no hay explicación alternativa."
              % P["fao_share"], kicker="Sin ambigüedad", acento=AZUL2)
    L.tarjeta(M + 2 * (ancho + 0.55), 3.90, ancho, 4.55, "Y el margen es fino",
              "Entre 2023 y 2025 Argentina despachó %s de cola a Perú y Perú "
              "despachó %s de pelado: usa el 97%% de su capacidad teórica. La "
              "diferencia bruta es US$%s por kilo de cola, un %s sobre el insumo — "
              "antes del flete, del pelado y del margen del reprocesador."
              % (P["cola_a_peru"], P["peru_pelado"], P["margen_kg"],
                 P["margen_pct"]), kicker="Sin gran despojo", acento=AZUL3)
    L.remate("China, en cambio, queda descartada como hub: entre 2012 y 2018 sus "
             "compras a Argentina crecieron 1452%% mientras sus envíos a la UE caían "
             "27%% (correlación −0,73). Importa 989 kt al año y exporta 199: absorbe "
             "producto, no lo recicla. En la UE el reprocesado es %s de la "
             "importación directa — marginal en volumen, pero ×4 desde 2022."
             % P["reproceso_ue"], y=8.58, tam=20)
    L.pie("Sección 4 · base de comercio (importación y exportación) · INDEC · EUMOFA "
          "CN8 · FAO FishStat.", y_regla=9.78)
    L.notas("El circuito tiene un costo nuevo desde 2025: la cola que se pela en un "
            "tercer país pierde la certificación MSC si la planta de fasón no está "
            "certificada, porque se rompe la cadena de custodia.")

    # ---------- 13 · aranceles EE.UU. ----------
    L = Lamina(prs)
    L.encabezado("Aranceles · EE.UU.", 13, TOTAL)
    L.titulo("Un cambio de reglas que deja a Argentina en el piso", tam=57)
    L.bajada("Hasta 2024 el langostino entraba a EE.UU. con arancel cero para todos "
             "los orígenes. Desde el 24 de julio de 2026 la carga tiene dos capas: "
             "Sección 301 y antidumping/compensatorios.")
    filas = [(f[0].split(" (")[0], num(f[3]), f[3]) for f in t_eeuu[1:]]
    L.barras(filas, M, 4.14, ancho_etiqueta=2.5, ancho_pista=5.4, alto=0.46,
             paso=0.665, tam_etiqueta=26, tam_valor=28, ancho_valor=1.8,
             colores=[AZUL1, AZUL2, AZUL2, AZUL3, AZUL3, AZUL4, AZUL5, AZUL5])
    L.texto("Carga arancelaria total, agosto de 2026", M, 3.70, 9.0, 0.42,
            fuente=BODY, tam=18.75, color=MUTED)
    L.columna(12.55, 4.02, 6.28, [
        {"txt": "Ventaja sobre India: %s" % P["ventaja_india"], "fuente": HEAD,
         "tam": 48, "color": AZUL1, "interlinea": 0.95, "gap": 0.38},
        {"txt": "Llegó a ser de ~47 puntos con los recíprocos de 2025-26, hasta que "
                "la Corte Suprema los anuló en febrero de 2026. Sirve como ventana "
                "de oportunidad, no como base estructural.",
         "tam": 20.25, "gap": 0.38},
        {"txt": "Argentina es el único oferente grande sin antidumping — no porque "
                "el producto esté excluido, sino porque nunca fue país investigado. "
                "Y la Sección 301 le puso 12,5% a Perú: el pelado de fasón ahora "
                "paga más que el despacho directo.", "tam": 21, "color": INK},
    ], limite=9.50)
    L.pie("Sección 8 · Federal Register 2026-15181 (S.301 por país) · fallo de la "
          "Corte Suprema 20-feb-2026 · órdenes AD/CVD del Departamento de Comercio de "
          "diciembre de 2024, tasas «all others».", y_regla=9.62)
    L.notas("Dos reservas: el arancel se aplica sobre el valor y el langostino entra "
            "caro ($11,92/kg), así que en dólares por kilo pesa más; y es política "
            "comercial reciente y volátil.")

    # ---------- 14 · aranceles UE ----------
    L = Lamina(prs)
    L.encabezado("Aranceles · UE", 14, TOTAL)
    L.titulo("En Europa, de 12% a cero antes de 2030", tam=57)
    L.bajada("Argentina pagaba el 12% pleno desde 2014, cuando quedó fuera del SGP. "
             "El Acuerdo Interino UE-Mercosur rige desde el 1 de mayo de 2026.")
    filas = [(f[0].replace(" (entrada en vigor del Acuerdo Interino)", "")
              .replace(" en adelante", ""), num(f[1]), f[1]) for f in t_ue[1:]]
    L.barras(filas, M, 4.20, ancho_etiqueta=4.5, ancho_pista=5.2, alto=0.58,
             paso=0.86, tam_etiqueta=27, tam_valor=33, ancho_valor=1.6,
             maximo=12.0,
             colores=[AZUL1, AZUL2, AZUL3, AZUL4, AZUL5, AZUL6])
    L.texto("Arancel del congelado 0306.17", M, 3.78, 9.0, 0.42, fuente=BODY,
            tam=18.75, color=MUTED)
    L.columna(12.55, 4.20, 6.28, [
        {"txt": "2,4 puntos de margen por año", "fuente": HEAD, "tam": 48,
         "color": AZUL1, "interlinea": 0.95, "gap": 0.38},
        {"txt": "en el principal destino del entero premium, y ya firmados. El "
                "elaborado de la partida 1605 (20%) también se desgrava.",
         "tam": 20.25, "gap": 0.38},
        {"txt": "Hoy Argentina todavía carga el peor arancel del pelotón —9,6% "
                "contra 0% de Ecuador y Vietnam y 4,2% de India e Indonesia—. En "
                "2030 el mapa se invierte respecto de 2024: la UE a 0% y EE.UU. en "
                "un 10% discrecional, renovable a voluntad.",
         "tam": 21, "color": INK},
    ], limite=9.50)
    L.pie("Sección 8 · Acuerdo Interino UE-Mercosur, DOUE abril 2026, vigencia "
          "provisional 1-may-2026 · Access2Markets.")
    L.notas("Es la mejora de margen más previsible del informe: no depende de "
            "negociar precio, ya está en el calendario.")

    # ---------- 15 · el competidor ----------
    L = Lamina(prs)
    L.encabezado("El competidor", 15, TOTAL)
    L.titulo("Vannamei: una marea de cultivo, no una pesquería", tam=57)
    L.bajada("A diferencia de una pesquería, el cultivo se expande a voluntad. Desde "
             "2015 Ecuador triplicó su producción (+202%), India casi (+184%) y "
             "Vietnam también (+175%).")
    filas = [(f[0], num(f[1]), f[1]) for f in t_vanna[1:-1]]
    L.barras(filas, M, 4.35, ancho_etiqueta=2.3, ancho_pista=5.3, alto=0.58,
             paso=1.02, tam_etiqueta=30, tam_valor=31, ancho_valor=2.6,
             colores=[AZUL1, AZUL2, AZUL3, AZUL4, AZUL5])
    L.texto("Producción 2024 · millones de toneladas · cinco países son el 85% del "
            "mundo", M, 3.88, 10.0, 0.42, fuente=BODY, tam=18.75, color=MUTED)
    L.columna(12.55, 3.95, 6.28, [
        {"txt": P["vannamei_mt"], "fuente": HEAD, "tam": 108, "color": AZUL1,
         "interlinea": 0.9, "gap": 0.26},
        {"txt": "de vannamei de cultivo en 2024 — %s la captura argentina de "
                "langostino, y %s lo que era en 2010."
                % (P["vannamei_34"], P["vannamei_x"]), "tam": 20.25, "gap": 0.38},
        {"txt": "Entre los salvajes, en cambio, el langostino es una categoría de "
                "uno: está entre los cinco más capturados del mundo y es el único "
                "con escala exportable en el nicho premium. Su competencia real no "
                "es salvaje.", "tam": 21, "color": INK},
    ], limite=9.50)
    L.pie("Secciones 9 y 10 · FAO FishStat, producción de acuicultura y capturas, "
          "descarga 2026.")
    L.notas("Sus pares de segmento —gamba roja y blanca mediterráneas— son más caros "
            "pero marginales en volumen; nórdico y tigre son otro producto.")

    # ---------- 16 · el competidor, el costo ----------
    L = Lamina(prs)
    L.encabezado("El competidor · el costo", 16, TOTAL)
    L.titulo("Ecuador no baja el precio: le baja el costo", tam=57)
    L.bajada("Y se movió al formato que el langostino consideraba terreno propio.")
    L.cifra("US$%s" % P["granja_2024"], "vale el kilo en la granja ecuatoriana",
            "bajó %s desde 2015 (US$%s) mientras triplicaba la producción · es el "
            "productor más barato del mundo a escala, por debajo de Indonesia 4,11, "
            "Tailandia 4,32 e India 4,34"
            % (P["granja_caida"], P["granja_2015"]), M, 3.80, 8.6, tam=120)
    L.cifra("×35", "creció su exportación de entero",
            "de %s en 2013 a %s en 2025 · hoy es el 15%% de su exportación contra el "
            "4%% de hace doce años, y con el precio bajando de US$%s a US$%s"
            % (P["ec_entero_2013"], P["ec_entero_2025"], P["ec_precio_2013"],
               P["ec_precio_2025"]), 10.42, 3.80, 8.4, tam=120)
    L.remate("Una granja baja su costo con genética, densidad y alimento; una "
             "pesquería no puede pescar más barato. Cuando Ecuador baja el precio no "
             "resigna margen: traslada una caída de costo. Competir por precio es "
             "competir en la cancha del otro.", y=8.25, tam=22.5)
    L.pie("Sección 9 · FAO FishStat (valor de granja = valor de producción ÷ "
          "toneladas, 2015-2024) · aduana de Ecuador, subpartida 0306.17.11.00.")
    L.notas("Su fragilidad es el destino: China pasó del 4,4%% de sus exportaciones en "
            "2013 al %s hoy. Cualquier recorte chino vuelca volumen a Europa, que es "
            "donde Argentina defiende su margen." % P["ec_china"])

    # ---------- 17 · España ----------
    L = Lamina(prs)
    L.encabezado("España", 17, TOTAL)
    L.titulo("La cuota se pierde hace diez años, no desde el conflicto", tam=54)
    L.bajada("Con la serie larga de EUMOFA el desplazamiento aparece como tendencia "
             "estructural: Ecuador cruzó a Argentina en 2020, cinco años antes del "
             "conflicto gremial.")
    L.cifra("%s → %s" % (P["ec_cuota_ini"], P["ec_cuota_fin"]),
            "pasó Ecuador en el mercado español",
            "mientras Argentina venía del 25%% en 2012, tocaba 35%% en 2016-17 y hoy "
            "está en %s del langostino congelado" % P["ar_cuota_fin"],
            M, 3.85, 8.6, tam=90)
    L.cifra("41 : 1  →  1,6 : 1", "se cerró la brecha en entero",
            "Argentina despachaba %s kt contra %s de Ecuador en 2018; en 2025 son %s "
            "contra %s. Argentina perdió el %s de su volumen y Ecuador multiplicó el "
            "suyo por diez, en el mismo producto y el mismo mercado."
            % (P["es_ent_ar_2018"], P["es_ent_ec_2018"], P["es_ent_ar_2025"],
               P["es_ent_ec_2025"], P["ar_perdida"]), 10.42, 3.85, 8.4, tam=72)
    L.remate("El matiz que sostiene el diagnóstico: el precio del langostino en "
             "España subió durante la caída de 2025 (%s a %s), señal de escasez y no "
             "de producto invendible. Pero la cuota se pierde hace diez años a precio "
             "estable. Y la ventaja de Ecuador no es sólo precio: es continuidad — "
             "reparte entre 5,0%% y 11,2%% por mes (CV %s) mientras Argentina "
             "concentra el 17,6%% en septiembre y cae a 2,5%% en marzo (CV %s)."
             % (P["es_precio_ini"], P["es_precio_fin"], P["cv_ec"], P["cv_ar"]),
             y=7.95, tam=21)
    L.pie("Sección 9 · EUMOFA CN8 2012-2025 · aduanas de origen (NCM 0306.17.10 y "
          "0306.17.11.00) · INDEC mensual 2013-2026.")
    L.notas("Con el INDEC se ve el espejo: Argentina no se retiró de España, dejó de "
            "crecer ahí mientras el mercado crecía. Ese estancamiento es lo que "
            "Ecuador convirtió en cuota.")

    # ---------- 18 · el atributo salvaje ----------
    L = Lamina(prs)
    L.encabezado("El atributo salvaje", 18, TOTAL)
    L.titulo("El premium aguanta, y ahora es auditable", tam=57)
    L.bajada("Siete años de datos sin dirección sostenida, y desde 2026 un sello que "
             "el cultivo no puede obtener.")
    ancho = (CW - 2 * 0.55) / 3
    L.tarjeta(M, 3.90, ancho, 4.60, "%sx sobre el vannamei" % P["premium"],
              "El premium en EE.UU. se movió entre %s veces desde 2020, sin "
              "tendencia. El pico de 2023-24 no fue una mejora del langostino sino el "
              "derrumbe del vannamei por sobreoferta; cuando el sustituto se "
              "recuperó, el ratio volvió a su rango." % P["premium_rango"],
              kicker="No se erosiona", acento=AZUL1)
    L.tarjeta(M + ancho + 0.55, 3.90, ancho, 4.60, "MSC en dos etapas",
              "La pesquería costera de Chubut certificó en abril de 2025 y la de "
              "aguas nacionales en febrero de 2026, por cinco años con auditorías "
              "anuales. Como Argentina es el %s de la captura mundial, es en la "
              "práctica el único langostino salvaje certificado que existe: una "
              "granja puede certificar ASC, nunca MSC-salvaje." % P["fao_share"],
              kicker="La llave", acento=AZUL2)
    L.tarjeta(M + 2 * (ancho + 0.55), 3.90, ancho, 4.60, "La puerta recién se entreabre",
              "Los mercados que pagan por el sello siguen recibiendo el %s de la "
              "exportación, y la cola certificada sigue yendo a China, Perú y "
              "Tailandia, que no pagan por MSC. Llevar el norte del 2%% al 10%% al "
              "diferencial observado movería %s — techo ilustrativo, porque hereda "
              "el efecto mezcla." % (P["msc_share"], P["msc_upside"]),
              kicker="Todavía sin monetizar", acento=AZUL3)
    L.remate("El candidato natural para cobrar el sello es el entero tangonero: "
             "cadena corta buque-retail europeo, certificado desde febrero de 2026, "
             "con su primera temporada certificada en curso (julio-octubre de 2026).",
             y=8.72, tam=21.5)
    L.pie("Sección 9 · NOAA (serie anual 2020-2026, langostino AR ÷ canasta vannamei "
          "de Ecuador, India e Indonesia) · base de comercio para los mercados "
          "MSC-sensibles.")
    L.notas("La cola que entra al circuito de fasón puede perder la etiqueta: la "
            "cadena de custodia se rompe salvo que la planta peruana también "
            "certifique.")

    # ---------- 19 · la góndola ----------
    L = Lamina(prs)
    L.encabezado("La góndola", 19, TOTAL)
    L.titulo("El sello ya llegó al lineal; la prima todavía no", tam=57)
    L.bajada("Relevamiento propio del precio final al consumidor, agosto de 2026.")
    L.cifra("×1,8 a ×2,0", "multiplica la góndola al FOB de origen",
            "el gambón entero se vende a %s en España (FOB ~€6,5) y el pelado "
            "wild-caught de Kroger a ~%s en EE.UU. (FOB ~$12,7). El salto "
            "entero→cola reaparece en el lineal: Mercadona vende el entero a €12,00 "
            "y las colas a €24,60." % (P["gondola_es"], P["gondola_us"]),
            M, 3.72, 8.6, tam=78)
    L.cifra("Sin prima estable", "por el atributo salvaje",
            "en La Sirena, mismo calibre 30-40, entero crudo y glaseado 0%% en ambos: "
            "langostino argentino %s frente a vannamei %s — el de cultivo cuesta un "
            "18%% más, y el argentino de ese par está rotulado MSC."
            % (P["sirena_ar"], P["sirena_ec"]), 10.42, 3.72, 8.4, tam=66)
    L.columna(M, 8.05, CW, [
        {"txt": "La prima del salvaje que sí existe en aduana —%s en el calibre "
                "15/20 con cáscara, la única celda donde argentino y vannamei se "
                "comparan cabeza a cabeza en el dato de NOAA— no se traslada al "
                "lineal: el posicionamiento depende de la cadena y del calibre, no "
                "del atributo. La señal a seguir es que La Sirena ya rotula MSC toda "
                "su línea de gambón argentino y el vannamei se rotula ASC — la "
                "góndola española ya habla el idioma de la certificación."
                % P["prima_1520"], "tam": 21, "color": INK},
    ], limite=9.85, acento_regla=False)
    L.pie("Sección 12 · relevamiento propio 2026-08-04: scraping Mercadona, Dia y La "
          "Sirena (ES) más la API oficial de Kroger (US), con ficha reglamentaria y "
          "peso de envase verificado.", y_regla=9.95)
    L.notas("No permite todavía medir volumen: es una cadena, observada en agosto de "
            "2026, con formatos distintos entre productos comparados.")

    # ---------- 20 · tendencia ----------
    L = Lamina(prs)
    L.encabezado("Tendencia", 20, TOTAL)
    L.titulo("Pesquería post-pico, y un corrimiento del entero a la cola", tam=54)
    L.bajada("La exportación tocó máximo en 2018 con %s y ronda los 120 kt en 2025. "
             "Pero el segundo mensaje importa más que el primero." % P["expo_pico"])
    filas = [(f[0], num(f[4]), f[4]) for f in t_serie[1:]]
    L.barras(filas, M, 4.35, ancho_etiqueta=1.8, ancho_pista=5.6, alto=0.58,
             paso=0.90, tam_etiqueta=30, tam_valor=33, ancho_valor=1.8,
             maximo=100.0,
             colores=[AZUL1, AZUL2, AZUL2, AZUL3, AZUL3, AZUL4])
    L.texto("Participación del entero en la exportación oficial", M, 3.88, 10.0, 0.42,
            fuente=BODY, tam=18.75, color=MUTED)
    L.columna(12.30, 3.95, 6.53, [
        {"txt": "La flota explica el producto", "fuente": HEAD, "tam": 48,
         "color": AZUL1, "interlinea": 0.95, "gap": 0.38},
        {"txt": "El corrimiento no fue una decisión comercial: es composición de "
                "flota. La tangonera —que congela entero a bordo— pasó del %s de "
                "los desembarques en 2013 al %s en 2024, mientras la fresquera se "
                "multiplicó por 4,5. La correlación entre las dos series es %s."
                % (P["tang_share_2013"], P["tang_share_2024"], P["correl"]),
         "tam": 20.25, "gap": 0.38},
        {"txt": "Primera señal de normalización: la tangonera lleva %s entre enero "
                "y julio de 2026, por encima de las 55,3 kt de 2024 y contra apenas "
                "0,5 kt en 2025. Con la capacidad debería volver el share de entero "
                "y, con él, el valor por kilo capturado." % P["tang_2026"],
         "tam": 21, "color": INK},
    ], limite=9.85)
    L.pie("Sección 11 · aduana argentina oficial, NCM 0306.17.10 (entero) y "
          "0306.17.90 (cola). 2020-2026 son piso por secreto estadístico; 2026 es "
          "parcial. Desembarques SSPyA para el corte por flota.", y_regla=9.98)
    L.notas("En 2025 la relación se invirtió por primera vez en la serie: la "
            "fresquera exportó 70.300 toneladas contra 49.233 de la congeladora.")

    # ---------- 21 · cierre ----------
    L = Lamina(prs, BG_DARK, oscura=True)
    L.encabezado("Cierre", 21, TOTAL)
    L.titulo("Cuatro conclusiones", tam=72, y=1.75)
    conclusiones = [
        ("El volumen no es la palanca; el valor por tonelada sí.",
         "La base productiva se achica y el sustituto se expande a voluntad: la "
         "pregunta no es cuánto se pesca, sino cuánto valor deja cada tonelada."),
        ("La flota y el calibre ya son la ventaja: falta cobrarla.",
         "La tangonera genera %s el valor por tonelada de la fresquera, su entero L1 "
         "vale %s a igual calibre y rinde 31%% más que la mejor cola P&D."
         % (P["brecha_2025"], P["brecha_l1"])),
        ("España es el problema competitivo, y viene de antes de 2025.",
         "Ecuador pasó del %s al %s del mercado español y cruzó a Argentina en 2020; "
         "en entero, la brecha se cerró de 41 a 1 a 1,6 a 1."
         % (P["ec_cuota_ini"], P["ec_cuota_fin"])),
        ("Las dos buenas noticias son de calendario, no de mercado.",
         "El arancel europeo baja 2,4 puntos por año hasta 0%% en 2030 y el MSC "
         "habilita el sello sobre el entero tangonero: hoy los mercados que lo pagan "
         "reciben el %s de la exportación." % P["msc_share"]),
    ]
    y = 3.08
    PASO = 1.80
    for i, (tit, cuerpo) in enumerate(conclusiones):
        L.regla(M, y, CW, RULE_D, grosor=0.010)
        L.texto(str(i + 1), M, y + 0.26, 1.33, 0.85, fuente=HEAD, tam=60,
                color=AZUL5)
        L.texto(tit, 2.83, y + 0.28, CW - 1.66, 0.66, fuente=HEAD, tam=37,
                color=INK_D)
        h = alto_texto(cuerpo, 15.4, 19.5, 1.18)
        if 0.98 + h > PASO - 0.14:
            raise SystemExit("Conclusion %d se pasa de su banda (%.2f)"
                             % (i + 1, 0.98 + h))
        L.texto(cuerpo, 2.83, y + 0.98, 15.4, h + 0.1, fuente=BODY, tam=19.5,
                color=MUTED_D, interlinea=1.18)
        y += PASO
    L.regla(M, y, CW, RULE_D, grosor=0.010)
    L.texto("%s · %s" % (AUTOR, FECHA), M, 10.52, CW, 0.46, fuente=HEAD, tam=19.5,
            color=EYEBROW_D)
    L.notas("Cierre. Las dos primeras conclusiones son de gestión comercial; la "
            "tercera es el problema a resolver; la cuarta, las dos ventanas que ya "
            "están abiertas.")

    # ---------- 22 · notas de dato ----------
    L = Lamina(prs, BG_ANEXO)
    L.encabezado("Notas de dato y fuentes", 22, TOTAL)
    L.titulo("De dónde sale cada número", tam=57)
    L.bajada("Todas las cifras del estudio salen de registros oficiales, del dato "
             "transaccional depurado y del relevamiento propio de góndola.")
    mitad = (CW - 0.55) / 2
    L.parrafos([
        ("Volumen", True),
        "Aduana argentina oficial (NCM 0306.17.10 entero y 0306.17.90 cola), "
        "validado contra la captura de FishStat. La base de comercio se usa sólo "
        "para precio, calibre y destino.",
        ("Serie oficial 2013-2026", True),
        "2013-2019 es dato completo. 2020-2026 proviene del portal de aduana por "
        "país y mes, donde el secreto estadístico suprime los flujos chicos: esos "
        "años son un piso y subestiman el total. 2026 es parcial.",
        ("Precios y rendimientos", True),
        "Conversión EUR→USD ≈ 1,08. El margen por talle usa un rendimiento único de "
        "entero a cola de 0,55, igual para el congelado a bordo y para el procesado "
        "en tierra, y de entero a cola P&D de 0,385 (0,55 × 0,70).",
    ], M, 3.95, mitad, 5.2, tam=20.25, color=INK, interlinea=1.18, espacio=7)
    L.parrafos([
        ("Contexto estructural", True),
        "FishStat y FAOSTAT son anuales, hasta 2024: sirven para el encuadre, no "
        "para el detalle comercial.",
        ("Aranceles", True),
        "Tasas por norma: HTS/USITC, Federal Register, DOUE y Access2Markets.",
        ("Fuentes primarias", True),
        "Desembarques SSPyA (puerto × flota × especie × mes, 2013-2026) · aduana "
        "argentina oficial (exportación por NCM) · base de comercio (importación y "
        "exportación) · NOAA FOSS · Comext DS-045409 · EUMOFA CN8 · FAO FishStat "
        "Global Production 2025.1.0 · relevamiento propio de góndola (scraping ES "
        "más API de Kroger).",
    ], M + mitad + 0.55, 3.95, mitad, 5.2, tam=20.25, color=INK, interlinea=1.18,
        espacio=7)
    L.pie("Resumen de «Estudio de mercado · Langostino argentino · Precio, comercio y "
          "posición competitiva», versión 08.09.26. %s · %s." % (AUTOR, FECHA))
    L.notas("Las advertencias de método que conviene tener a mano si preguntan por "
            "el detalle.")

    # Propiedades del archivo: nada de nombres de libreria en material que circula.
    cp = prs.core_properties
    cp.title = "Estudio de mercado · Langostino argentino · Resumen ejecutivo"
    cp.subject = "Precio, comercio y posición competitiva · versión 08.09.26"
    cp.author = "Lic. Fabián Pettigrew"
    cp.last_modified_by = "Lic. Fabián Pettigrew"
    cp.category = "Estudio de mercado"
    cp.comments = ("Resumen del estudio de mercado de langostino argentino, "
                   "versión 08.09.26.")

    prs.save(DESTINO)
    print("Escrito: %s (%d laminas)" % (DESTINO, len(prs.slides._sldIdLst)))


if __name__ == "__main__":
    construir()
