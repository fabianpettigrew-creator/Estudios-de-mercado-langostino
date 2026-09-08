# -*- coding: utf-8 -*-
"""SUPERADO — no correr. Desde el 2 de septiembre de 2026 el anexo
se genera dentro de «deck_ceo.js», junto con el resto del deck. Volver a correr
este script duplicaría las placas del anexo y borraría la placa de destinos.

Edita el PPT «Langostino tangonero CEO»:
  1. saca la placa 2 (precio por destino)
  2. arregla lo que esa placa dejaba colgando: «tres palancas» → dos, y la numeración
  3. agrega el anexo metodológico y el resumen de los estudios de la placa 3
Respeta el diseño existente: mismas coordenadas, colores y tipografías que el resto del deck."""
import copy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree

SRC, OUT = '/tmp/lango/deck.pptx', '/tmp/lango/out/Langostino_tangonero_CEO.pptx'
AZUL, GRIS, NARANJA = '12333F', '5C6B73', 'E2703A'
TEXTO, PIE, CREMA = '3E4E55', '94A2A8', 'F4EFE6'
CLARO, BLANCO = 'BFD3DA', 'FFFFFF'
NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NSA = 'http://schemas.openxmlformats.org/drawingml/2006/main'

prs = Presentation(SRC)
LAYOUT = prs.slide_masters[0].slide_layouts[0]


# ---------------------------------------------------------------- utilidades
def texto_de(shape):
    return shape.text_frame.text.strip()


def buscar(slide, frag):
    for sh in slide.shapes:
        if sh.has_text_frame and frag in sh.text_frame.text:
            return sh
    return None


def reescribir(shape, nuevo):
    """Cambia el texto conservando el formato del primer run."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    if not p0.runs:
        return
    p0.runs[0].text = nuevo
    for r in p0.runs[1:]:
        r._r.getparent().remove(r._r)
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)


def borrar_slide(idx):
    xml = prs.slides._sldIdLst
    slide_id = list(xml)[idx]
    rId = slide_id.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
    prs.part.drop_rel(rId)
    xml.remove(slide_id)


def nueva(fondo=BLANCO):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    bg = etree.SubElement(s._element.find(f'{{{NS}}}cSld'), f'{{{NS}}}bg')
    s._element.find(f'{{{NS}}}cSld').remove(bg)
    s._element.find(f'{{{NS}}}cSld').insert(0, bg)
    pr = etree.SubElement(bg, f'{{{NS}}}bgPr')
    fill = etree.SubElement(pr, f'{{{NSA}}}solidFill')
    etree.SubElement(fill, f'{{{NSA}}}srgbClr').set('val', fondo)
    etree.SubElement(pr, f'{{{NSA}}}effectLst')
    return s


def txt(s, x, y, w, h, contenido, size=11.5, color=TEXTO, bold=False,
        align=PP_ALIGN.LEFT, espacio=1.25):
    caja = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = caja.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lineas = contenido if isinstance(contenido, list) else [contenido]
    for i, linea in enumerate(lineas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = espacio
        partes = linea if isinstance(linea, list) else [(linea, bold, color)]
        for t, b, c in partes:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = b
            r.font.name = 'Calibri'
            r.font.color.rgb = RGBColor.from_string(c)
    return caja


def tarjeta(s, x, y, w, h, relleno=CREMA):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(relleno)
    sh.line.fill.background()
    sh.shadow.inherit = False
    for gd in sh._element.findall(f'.//{{{NSA}}}gd'):
        gd.set('fmla', 'val 5233')
    return sh


def circulo(s, x, y, n, d=0.60):
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(NARANJA)
    sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = n
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.name = 'Calibri'
    r.font.color.rgb = RGBColor.from_string(BLANCO)
    return sh


def cabecera(s, titulo, bajada=None, oscuro=False):
    txt(s, 0.70, 0.45, 11.90, 0.95, titulo, 34, BLANCO if oscuro else AZUL, True, espacio=1.0)
    if bajada:
        txt(s, 0.70, 1.40, 11.90, 0.55, bajada, 15, CLARO if oscuro else GRIS, espacio=1.15)


def pie(s, t):
    txt(s, 0.70, 6.88, 11.90, 0.32, t, 9.5, PIE)


# ============================================================ 1. consistencia
# (la placa se borra al final, en un segundo pase sobre el archivo ya guardado: si se borra
#  antes de agregar, PowerPoint reutiliza el nombre de la parte XML y el paquete queda con dos
#  slides18.xml)
s = next(s for s in prs.slides if buscar(s, '¿dónde está el valor?'))
reescribir(buscar(s, 'muestra tres que sí'),
           'Si la palanca del volumen no rinde, el mismo trabajo muestra dos que sí. '
           'Ninguna cuesta toneladas.')
print('2. «tres que sí» → «dos que sí»')

s = next(s for s in prs.slides if buscar(s, 'La flota y la talla ya son una ventaja'))
for sh in s.shapes:
    if sh.has_text_frame and texto_de(sh) == '3':
        reescribir(sh, '2')
print('   la palanca de talla pasa a ser la 2')

s = next(s for s in prs.slides if buscar(s, 'Tres conclusiones'))
reescribir(buscar(s, 'El valor está en el canal, el destino y la talla.'),
           'El valor está en el canal y en la talla.')
reescribir(buscar(s, 'trece puntos de diferencia entre destinos'),
           'La actividad de restauración mueve el precio más que la propia captura, y el entero '
           'grande se vende con descuento contra camarón de tamaño equivalente.')
print('   conclusión 3 reescrita sin la referencia a los destinos')

# ============================================================ 3. anexo
print('3. anexo metodológico')

# --- portadilla
s = nueva(AZUL)
txt(s, 0.70, 2.50, 10.50, 1.30, 'Anexo metodológico', 40, BLANCO, True, espacio=1.0)
txt(s, 0.70, 3.90, 9.50, 0.90,
    'Cómo está construido el número, con qué datos, y qué dice la literatura que lo respalda.',
    17, CLARO, espacio=1.2)

# --- A1 qué se estima
s = nueva()
cabecera(s, 'Qué se estima, y contra qué umbral',
         'Un solo parámetro ordena toda la discusión.')
tarjeta(s, 0.70, 2.25, 5.55, 3.30)
txt(s, 1.10, 2.50, 4.75, 0.45, 'La flexibilidad-precio', 17, AZUL, True)
txt(s, 1.10, 3.05, 4.75, 2.30,
    ['Mide en cuánto por ciento se mueve el precio cuando la cantidad ofrecida se mueve un uno '
     'por ciento. Es negativa por definición: más mercadería, menos precio.',
     '',
     'Se estima sobre el precio del langostino relativo al camarón de cultivo, para que el ciclo '
     'mundial no se cuele en el resultado.'], 11.5, TEXTO)
tarjeta(s, 6.85, 2.25, 5.55, 3.30)
txt(s, 7.25, 2.50, 4.75, 0.45, 'El umbral no es cero, es 1', 17, NARANJA, True)
txt(s, 7.25, 3.05, 4.75, 2.30,
    ['Como la facturación es precio por cantidad, recortar oferta la aumenta sólo si el precio '
     'sube MÁS de lo que cae el volumen. En términos del parámetro: sólo si es menor que −1.',
     '',
     [('Con −0,2, sacar 10 toneladas del mercado sube el precio 2% y baja la facturación 8%.',
       True, AZUL)]], 11.5, TEXTO)
pie(s, 'No alcanza con que el parámetro sea negativo y estadísticamente significativo: '
       'tiene que ser mayor que uno en valor absoluto.')

# --- A2 datos
s = nueva()
cabecera(s, 'Qué entra al modelo',
         'Series mensuales de enero de 2013 a julio de 2026. Todo es registro oficial o base '
         'comercial de despachos.')
CAJAS = [
    (0.70, 2.25, 'Precio', 'Valor unitario FOB del entero L1 congelado a bordo, despacho por '
                           'despacho. La flota se identifica por la marca de congelado a bordo: '
                           'lo que la lleva es tangonera, lo que no la lleva es fresquera.'),
    (6.85, 2.25, 'Cantidad', 'Desembarque oficial por puerto, flota y mes. Es la variable que la '
                             'política mueve, y es exógena: no la decide el que vende.'),
    (0.70, 4.35, 'Competidor', 'Precio del camarón de cultivo importado por la Unión Europea, y '
                               'exportación ecuatoriana por subpartida y país de destino, para '
                               'comparar contra el mismo mercado y el mismo mes.'),
    (6.85, 4.35, 'Demanda', 'Índice mensual de actividad del canal de restauración en España, '
                            'Italia, China y Japón, construido con estadística oficial de los '
                            'cuatro países.'),
]
for x, y, tit, cuerpo in CAJAS:
    tarjeta(s, x, y, 5.55, 1.85)
    txt(s, x + 0.40, y + 0.22, 4.75, 0.40, tit, 15, AZUL, True)
    txt(s, x + 0.40, y + 0.70, 4.75, 1.00, cuerpo, 11.5, TEXTO)
pie(s, 'El desembarque de la flota tangonera es producto final que va directo a exportación, sin '
       'reproceso: por eso su composición por talla se observa en el despacho.')

# --- A3 identificación
s = nueva()
cabecera(s, 'Por qué hace falta un experimento',
         'Precio y cantidad se determinan juntos. Cruzarlos sin más no mide la demanda: mide una '
         'mezcla.')
tarjeta(s, 0.70, 2.25, 5.55, 2.05)
txt(s, 1.10, 2.48, 4.75, 0.40, '2020 · un shock de DEMANDA', 15, AZUL, True)
txt(s, 1.10, 2.98, 4.75, 1.20,
    'Con el canal de restauración cerrado, precio y cantidad cayeron juntos. Leído sin '
    'distinguir, ese año «demuestra» que menos oferta baja el precio. Es exactamente el sesgo '
    'que hay que sacar.', 11.5, TEXTO)
tarjeta(s, 6.85, 2.25, 5.55, 2.05)
txt(s, 7.25, 2.48, 4.75, 0.40, '2025 · un shock de OFERTA', 15, NARANJA, True)
txt(s, 7.25, 2.98, 4.75, 1.20,
    'La flota parada cuatro meses por un conflicto gremial, con la captura de campaña 46% abajo. '
    'La cantidad se movió por un motivo ajeno al mercado: eso es lo que traza la curva de '
    'demanda.', 11.5, TEXTO)
tarjeta(s, 0.70, 4.60, 11.70, 1.55, CREMA)
txt(s, 1.10, 4.85, 10.90, 0.40, 'Cómo se usa', 15, AZUL, True)
txt(s, 1.10, 5.35, 10.90, 0.70,
    'El parate entra como instrumento: se usa sólo la parte de la captura que se movió por el '
    'conflicto. La primera etapa da F = 61, muy por encima del umbral de 10 que se exige para '
    'que el instrumento sea fuerte. El cierre del canal entra como control, con índice observado '
    'y no supuesto.', 11.5, TEXTO)

# --- A4 convergencia
s = nueva()
cabecera(s, 'Siete caminos, un número',
         'Se estimó por vías deliberadamente distintas —otras bases, otras unidades de '
         'observación, otros métodos— para ver si el resultado dependía de la construcción.')
FILAS = [
    ('Instrumental mensual, precio transaccional con marca de flota', '−0,184'),
    ('Instrumental mensual, agregado de las dos tallas grandes', '−0,219'),
    ('Proxy sobre aduana oficial, sin marca de flota, trece campañas', '−0,234'),
    ('Sistema de demanda inversa por origen, importación europea', '−0,267'),
    ('Sistema de dos flotas, recompuesto', '−0,212'),
    ('Ecuación incondicional con desembarques por flota', '−0,239'),
    ('Contra el competidor ecuatoriano en el mismo mercado', '−0,209 a −0,274'),
]
y = 2.30
for i, (nom, val) in enumerate(FILAS):
    if i % 2 == 0:
        tarjeta(s, 0.70, y - 0.06, 8.60, 0.48, CREMA)
    txt(s, 1.05, y + 0.04, 7.90, 0.35, nom, 12, TEXTO)
    txt(s, 6.60, y + 0.04, 2.50, 0.35, val, 12.5, AZUL, True, align=PP_ALIGN.RIGHT)
    y += 0.55
tarjeta(s, 9.70, 2.24, 2.70, 3.55)
txt(s, 10.00, 2.50, 2.10, 0.45, 'Todas rechazan', 15, NARANJA, True)
txt(s, 10.00, 3.00, 2.10, 2.60,
    ['el umbral de −1 con holgura.',
     '',
     'El rango va de −0,18 a −0,30: el precio se mueve entre la quinta y la tercera parte de lo '
     'que se mueve la cantidad.',
     '',
     'Ninguna construcción se acerca al valor que haría conveniente recortar.'], 11.5, TEXTO)
pie(s, 'Bases, unidades de observación y métodos distintos. La convergencia es el argumento: el '
       'número no es un artefacto de una construcción particular.')

# --- A5 limitaciones
s = nueva()
cabecera(s, 'Lo que el trabajo no puede afirmar',
         'Conviene tenerlo a mano antes de que lo pregunte otro.')
LIM = [
    ('Glaseo', 'No está considerado y no puede estarlo con dato de aduana: sobre 47.000 '
               'despachos, dos mencionan si el producto está glaseado, y el nomenclador oficial '
               'no tiene código para declararlo.'),
    ('Existencias', 'No se miden. Lo que llega al mercado difiere de lo que se pescó entre −19% '
                    'y +24% según la campaña, y esa brecha es error de medición en la cantidad.'),
    ('El valor exacto', 'La identificación se apoya en un solo episodio. El signo y el orden de '
                        'magnitud son firmes; los decimales y el intervalo, no.'),
    ('La tendencia', 'El precio relativo sube 1,1% por año contra el mismo mercado y esa mitad '
                     'todavía no tiene explicación. Los candidatos son certificación y '
                     'posicionamiento en góndola.'),
]
y = 2.30
for tit, cuerpo in LIM:
    tarjeta(s, 0.70, y, 11.70, 0.95)
    txt(s, 1.10, y + 0.18, 2.60, 0.35, tit, 14, NARANJA, True)
    txt(s, 3.90, y + 0.16, 8.10, 0.70, cuerpo, 11.5, TEXTO)
    y += 1.12
pie(s, 'Ninguna de estas limitaciones cambia el signo del resultado: cambian su precisión.')

# --- A6 y A7 estudios
def placa_estudios(titulo, bajada, items, nota=None):
    s = nueva()
    cabecera(s, titulo, bajada)
    y = 2.25
    for autor, revista, cuerpo in items:
        tarjeta(s, 0.70, y, 11.70, 1.85)
        txt(s, 1.10, y + 0.20, 5.20, 0.40, autor, 14.5, AZUL, True)
        txt(s, 1.10, y + 0.68, 5.20, 0.28, revista, 11, NARANJA, True)
        txt(s, 6.60, y + 0.20, 5.40, 1.45, cuerpo, 11.5, TEXTO)
        y += 2.05
    if nota:
        pie(s, nota)
    return s


placa_estudios(
    'Los estudios que fijan el método',
    'Los dos primeros de la placa 3, en detalle.',
    [('Barten y Bettendorf (1989)', 'European Economic Review',
      'El trabajo fundacional de la demanda inversa aplicada a pescado. Muestra que en productos '
      'pesqueros hay que dar vuelta el análisis: la captura llega al mercado ya decidida por el '
      'recurso y el calendario, y es el precio el que se acomoda para vaciarlo. De ahí sale el '
      'sistema de ecuaciones que se usa acá para estimar varias especies o flotas a la vez '
      'respetando que el gasto total tiene que cerrar.'),
     ('Tabarestani, Keithly y Marzoughi-Ardakani (2017)', 'Marine Resource Economics',
      'Lleva ese enfoque al mercado del camarón en Estados Unidos, que es el mercado de '
      'referencia mundial. Trata el desembarque salvaje del Golfo de México como cantidad ya '
      'dada y el precio del camarón de cultivo importado como dato externo. El resultado es el '
      'antecedente más directo de este trabajo: un cambio de 1% en el precio del importado mueve '
      '0,98% el precio doméstico. El salvaje casi no tiene autonomía de precio frente al cultivo.')],
    'Es el enfoque que corresponde cuando la cantidad no la decide el que vende.')

placa_estudios(
    'Los estudios que acotan la expectativa',
    'Los dos últimos de la placa 3, más el aporte del INIDEP.',
    [('Guillen y Maynou (2014)', 'Scientia Marina',
      'Estudia cómo se forma el precio en primera venta en pesquerías mediterráneas, con la '
      'gamba roja catalana. Separa qué pesa el volumen del día y qué pesa la temporada, y '
      'encuentra que el precio de primera venta es 14% menor los martes y miércoles. La '
      'recomendación es de calendario, no de recorte: concentrar la reducción de esfuerzo en los '
      'días de precio bajo. Es el antecedente de la palanca 1 de este trabajo.'),
     ('Asche y otros (2017)', 'Marine Resource Economics',
      'Documenta que los distintos camarones del mundo suelen moverse como un solo mercado. Ese '
      'supuesto se testeó acá y NO se cumple entre el langostino argentino y el vannamei de '
      'cultivo: son productos diferenciados, no sustitutos perfectos. Es lo que deja lugar a la '
      'palanca de talla y diferenciación, y lo que impide tratar al langostino como una '
      'commodity más dentro del agregado camarón.')],
    'Se sumó el INIDEP para la biología de la especie: el langostino renueva casi toda su '
    'población entre temporadas, y por eso la captura de un año no sirve para predecir la del '
    'siguiente — un instrumento que se probó y se descartó.')

TMP = '/tmp/lango/_deck_tmp.pptx'
prs.save(TMP)

# ============================================================ 4. sacar la placa de destinos
prs = Presentation(TMP)
i_destino = next(i for i, s in enumerate(prs.slides)
                 if buscar(s, 'vale distinto según a dónde va'))
xml = prs.slides._sldIdLst
sid = list(xml)[i_destino]
rId = sid.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
prs.part.drop_rel(rId)
xml.remove(sid)
prs.save(OUT)
print(f'4. borrada la placa de destinos (índice {i_destino})')
print(f'\nplacas finales: {len(list(prs.slides))}')
print('guardado en', OUT)
