# -*- coding: utf-8 -*-
"""Correcciones sobre el .docx que editó Fabián. Se parchea EN SU ARCHIVO, no se regenera:
regenerar perdería sus cuatro ediciones a mano del 23-ago."""
import copy, sys
from docx import Document
from docx.text.paragraph import Paragraph

SRC = '/tmp/lango/doc_base.docx'
OUT = '/tmp/lango/out/Demanda_inversa_langostino_metodologia_y_resultados.docx'
d = Document(SRC)
P = d.paragraphs

def buscar(frag, desde=0):
    for i in range(desde, len(P)):
        if frag in P[i].text:
            return i
    raise SystemExit(f'NO ENCONTRADO: {frag!r}')

def reemplazar_texto(par, viejo, nuevo):
    """Sustituye un fragmento respetando los runs; si cruza runs, lo mete en el primero."""
    for r in par.runs:
        if viejo in r.text:
            r.text = r.text.replace(viejo, nuevo)
            return True
    txt = par.text
    if viejo not in txt:
        return False
    txt = txt.replace(viejo, nuevo)
    par.runs[0].text = txt
    for r in par.runs[1:]:
        r.text = ''
    return True

def escribir(par, piezas):
    """piezas = [(texto, negrita), ...]. Reusa run0 como plantilla de formato."""
    base = par.runs[0]
    par.runs[0].text = piezas[0][0]
    par.runs[0].bold = piezas[0][1]
    for j, (t, b) in enumerate(piezas[1:], start=1):
        if j < len(par.runs):
            par.runs[j].text = t
            par.runs[j].bold = b
        else:
            nr = par.add_run(t)
            nr.bold = b
            nr.font.name = base.font.name
            nr.font.size = base.font.size
            if base.font.color and base.font.color.rgb:
                nr.font.color.rgb = base.font.color.rgb
    for j in range(len(piezas), len(par.runs)):
        par.runs[j].text = ''

def insertar_despues(par, piezas):
    nuevo = copy.deepcopy(par._p)
    par._p.addnext(nuevo)
    np_ = Paragraph(nuevo, par._parent)
    escribir(np_, piezas)
    return np_

# ---------------------------------------------------------------- 1. §1 Conxemar
i = buscar('Conxemar 2025')
assert reemplazar_texto(P[i], 'Aplicado al paquete de medidas discutido en Conxemar 2025',
                        'Aplicado a un paquete hipotético de medidas'), 'fallo §1'
print('§1 corregido:', P[i].text[:160])

# ---------------------------------------------------------------- 2. §8 la tendencia
i = buscar('La tendencia.')
escribir(P[i], [
    ('La tendencia, corregida. ', True),
    ('Medido contra la canasta de camarón de cultivo de EUMOFA, el precio relativo del L1 sube '
     '2,13% por año con t = 4,93, y esa tendencia se lleva cincuenta puntos de R². Pero buena '
     'parte de eso no es el langostino subiendo: es el control bajando. Entre 2013 y 2026 Ecuador '
     'multiplicó por 5,6 su exportación de camarón —de 144 mil a cerca de 1.400 mil toneladas— y '
     'reorientó la mitad de ese volumen a China, donde hoy coloca a 4,64 dólares por kilo contra '
     '6,19 en la Unión Europea. Ese caudal de talla chica y precio bajo hunde la canasta de EUMOFA '
     'más rápido de lo que arrastra al langostino salvaje. La comparación limpia es contra el '
     'camarón ecuatoriano embarcado a España —mismo mercado, mismo mes—: ahí la prima del L1 sube '
     '1,11% por año con t = 2,43, la mitad. La conclusión es de dos partes: la mitad del '
     'ensanchamiento de la prima es artefacto del control y la otra mitad es real. En el modelo de '
     'campaña, incorporar la tendencia lleva el R² de 0,29 a 0,79 y la flexibilidad de −0,247 a '
     '−0,186.', False)])
print('§8 tendencia reescrito')

# ---------------------------------------------------------------- 3. banda de f
p2 = insertar_despues(P[i], [
    ('La flexibilidad no depende de la referencia. ', True),
    ('Reestimando el modelo instrumental contra las tres definiciones del competidor sobre los '
     'mismos 136 meses, f queda entre −0,19 y −0,40: −0,219 contra la canasta de EUMOFA, −0,257 '
     'contra el precio ecuatoriano en España, Italia y Francia, y −0,188 contra España sola, las '
     'tres con la tendencia incluida. Ninguna se acerca al umbral de −1. La conclusión de política '
     'es la misma con cualquiera de los tres controles, y eso es lo que hacía falta verificar.',
     False)])

# ---------------------------------------------------------------- 4. descuento por talla
insertar_despues(p2, [
    ('El descuento por talla, una línea nueva. ', True),
    ('Los despachos ecuatorianos a España, transacción por transacción, permiten medir por primera '
     'vez cuánto vale el tamaño: la elasticidad del precio a las piezas por kilo es −0,277 con '
     't = −9,65, sobre 716 despachos con talla declarada. Ecuador embarca a España un promedio de '
     '52 piezas por kilo; el L1 argentino son 11 a 20, o sea unas 3,3 veces más grande. Con ese '
     'gradiente, un camarón ecuatoriano del tamaño del L1 valdría un 40% más que el promedio '
     'ecuatoriano a España, y contra ese precio ajustado el L1 argentino queda en torno a 0,80: el '
     'langostino argentino se estaría vendiendo como si fuera camarón chico. Es una extrapolación '
     'fuera de muestra —el gradiente se mide entre 20 y 100 piezas por kilo— y sobre un flujo '
     'mayormente intra-grupo, ya que Promarisco embarca el 76% de esos kilos y Pescanova España '
     'recibe el 74%. Indicativo, no establecido; pero es la primera medición directa de la brecha '
     'y merece trabajo propio.', False)])
print('§8: dos párrafos nuevos insertados')

# ---------------------------------------------------------------- 5. §11.2 nueva viñeta
i = buscar('Serie de restauración para China y Japón')
insertar_despues(P[i], [
    ('Precio del competidor emparejado por talla. ', True),
    ('El control ecuatoriano resuelve el mercado y la presentación, no el calibre: es un promedio '
     'sobre tallas dentro de los embarques a cada destino. La talla aparece en la descripción '
     'comercial de apenas el 3,4% de los kilos y la cobertura se desploma después de 2021, así que '
     'no alcanza para armar una serie. Hace falta el precio europeo de importación por rango de '
     'calibre.', False)])
print('§11.2: viñeta de talla agregada')

# ---------------------------------------------------------------- 6. §12 fuentes
i = buscar('Precio y calibre: base de despachos')
P[i].runs[0].text = P[i].runs[0].text.rstrip() + (
    ' Competencia ecuatoriana: estadísticas de comercio exterior del Ecuador, exportaciones por '
    'subpartida y país de destino, mensuales de enero de 2013 a junio de 2026, y despachos '
    'transacción por transacción de Ecuador a España de la subpartida 0306.17.99 entre enero de '
    '2020 y julio de 2026.')
i = buscar('Reproducibilidad:')
P[i].runs[0].text = (
    'Reproducibilidad: todos los números de este documento salen de los guiones '
    '«demanda_inversa_tangonera.py», «demanda_inversa_l1l2.py», «demanda_inversa_flotas.py», '
    '«demanda_inversa_sistema_flotas.py», «demanda_inversa_ecuador.py», '
    '«demanda_inversa_modelo.py» y «demanda_inversa_eumofa.py», y las tablas completas están en '
    'los libros «demanda_inversa_tangonera.xlsx», «demanda_inversa_l1l2.xlsx», '
    '«demanda_inversa_sistema_flotas.xlsx», «ecuador_competidor.xlsx» y '
    '«demanda_inversa_L1.xlsx».')
print('§12 fuentes y reproducibilidad actualizados')

d.save(OUT)
print('guardado en', OUT)
