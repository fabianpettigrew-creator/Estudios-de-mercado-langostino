# -*- coding: utf-8 -*-
"""Tercera pasada sobre el .docx de metodología: agrega el Anexo A con el sistema de
ecuaciones explícito y la técnica de estimación. Mantiene la maqueta del documento
(Heading 1/2, cuerpo justificado 1A1A1A, tablas con encabezado 1F4E79 y bandeo F2F5F8)."""
from __future__ import annotations
import copy, re
from docx import Document
from docx.shared import Pt, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

RUTA = "/tmp/lango/out/Demanda_inversa_langostino_metodologia_y_resultados.docx"
AZUL, TXT, GRIS, BANDA, BORDE = "1F4E79", "1A1A1A", "5A5A5A", "F2F5F8", "D9DEE4"
ANCHO = 9100                     # twips, el mismo de las tablas existentes
CENTRO, DERECHA = 4550, 9100     # tabuladores para numerar ecuaciones

doc = Document(RUTA)
body = doc.element.body


def _add(p_new):
    """Agrega al final del cuerpo, antes de sectPr."""
    sect = body.find(qn("w:sectPr"))
    if sect is not None:
        sect.addprevious(p_new)
    else:
        body.append(p_new)


def _nuevo(style="Normal"):
    p = doc.add_paragraph(style=style)
    return p


def H1(t):
    p = _nuevo("Heading 1")
    r = p.add_run(t); r.font.bold = True; r.font.size = Pt(13.5)
    r.font.color.rgb = RGBColor.from_string(AZUL)
    p.paragraph_format.space_before = Pt(16.5); p.paragraph_format.space_after = Pt(6.5)
    return p


def H2(t):
    p = _nuevo("Heading 2")
    r = p.add_run(t); r.font.bold = True; r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor.from_string(AZUL)
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(6.5)
    return p


def P(*trozos):
    """P('texto normal', ('negrita', 'b'), ('cursiva', 'i'))"""
    p = _nuevo()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6.5)
    for t in trozos:
        est = ""
        if isinstance(t, tuple):
            t, est = t
        r = p.add_run(t)
        r.font.color.rgb = RGBColor.from_string(TXT)
        if "b" in est: r.font.bold = True
        if "i" in est: r.font.italic = True
        if "m" in est: r.font.name = "Consolas"; r.font.size = Pt(9)
    return p


def EQ(texto, num=None, sangria=False):
    """Ecuación centrada; si num, el rótulo va alineado al margen derecho."""
    p = _nuevo()
    pf = p.paragraph_format
    pf.space_before = Pt(3); pf.space_after = Pt(7)
    pf.tab_stops.add_tab_stop(Twips(CENTRO), WD_TAB_ALIGNMENT.CENTER)
    pf.tab_stops.add_tab_stop(Twips(DERECHA), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run("\t" + texto)
    r.font.bold = True; r.font.color.rgb = RGBColor.from_string(TXT)
    if num:
        r2 = p.add_run("\t(" + num + ")")
        r2.font.color.rgb = RGBColor.from_string(GRIS); r2.font.size = Pt(9)
    return p


def NOTA(texto):
    p = _nuevo()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(texto); r.font.italic = True; r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor.from_string(GRIS)
    return p


def _shd(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), color)
    tcPr.append(s)


def _mar(celda):
    tcPr = celda._tc.get_or_add_tcPr()
    m = OxmlElement("w:tcMar")
    for lado, v in (("top", 55), ("left", 90), ("bottom", 55), ("right", 90)):
        e = OxmlElement("w:" + lado); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa")
        m.append(e)
    tcPr.append(m)
    va = OxmlElement("w:vAlign"); va.set(qn("w:val"), "center"); tcPr.append(va)


def TABLA(encabezado, filas, anchos, negrita_col0=False):
    t = doc.add_table(rows=1 + len(filas), cols=len(encabezado))
    t.style = doc.tables[0].style
    # tblPr calcado del resto del documento
    tblPr = t._tbl.tblPr
    for hijo in list(tblPr):
        if hijo.tag in (qn("w:tblW"), qn("w:tblBorders"), qn("w:tblCellMar"), qn("w:tblLook")):
            tblPr.remove(hijo)
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), str(ANCHO)); w.set(qn("w:type"), "dxa")
    tblPr.append(w)
    bd = OxmlElement("w:tblBorders")
    for lado, sz in (("top", 2), ("bottom", 2), ("insideH", 1)):
        e = OxmlElement("w:" + lado)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), BORDE)
        bd.append(e)
    tblPr.append(bd)
    cm = OxmlElement("w:tblCellMar")
    for lado in ("left", "right"):
        e = OxmlElement("w:" + lado); e.set(qn("w:w"), "10"); e.set(qn("w:type"), "dxa")
        cm.append(e)
    tblPr.append(cm)
    lk = OxmlElement("w:tblLook")
    lk.set(qn("w:val"), "0000")
    for k in ("firstRow", "lastRow", "firstColumn", "lastColumn"): lk.set(qn("w:" + k), "0")
    for k in ("noHBand", "noVBand"): lk.set(qn("w:" + k), "0")
    tblPr.append(lk)
    grid = t._tbl.find(qn("w:tblGrid"))
    for gc, a in zip(grid.findall(qn("w:gridCol")), anchos):
        gc.set(qn("w:w"), str(a))

    for j, h in enumerate(encabezado):
        c = t.rows[0].cells[j]
        c.width = Twips(anchos[j]); _shd(c, AZUL); _mar(c)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h); r.font.bold = True; r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor.from_string("FFFFFF")
    for i, fila in enumerate(filas):
        for j, v in enumerate(fila):
            c = t.rows[1 + i].cells[j]
            c.width = Twips(anchos[j]); _mar(c)
            if i % 2: _shd(c, BANDA)
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
            r = p.add_run(v); r.font.size = Pt(9)
            r.font.color.rgb = RGBColor.from_string(TXT)
            if j == 0 and negrita_col0: r.font.bold = True
            if j == 0 and "_" in v: r.font.name = "Consolas"
    return t


# ═══════════════════════════════════════════════════════════════════ 1. puntero en §6
anchor = None
for p in doc.paragraphs:
    if p.text.startswith("con homogeneidad impuesta por normalización y adición"):
        anchor = p
if anchor is None:
    raise SystemExit("no se encontró el cierre de 6.3")
nuevo = copy.deepcopy(anchor._p)
for r in nuevo.findall(qn("w:r")): nuevo.remove(r)
anchor._p.addnext(nuevo)
from docx.text.paragraph import Paragraph
pp = Paragraph(nuevo, anchor._parent)
for t, est in [("Las tres construcciones —y el sistema de dos flotas que las reconcilia— están "
                "escritas en forma explícita, con notación unificada y numeración de ecuaciones, "
                "en el ", ""), ("Anexo A", "b"), (".", "")]:
    r = pp.add_run(t); r.font.color.rgb = RGBColor.from_string(TXT)
    if est == "b": r.font.bold = True

print("puntero agregado en §6.3")

# ═══════════════════════════════════════════════════════════════════ 2. Anexo A
H1("Anexo A. El sistema de ecuaciones y la técnica de estimación")

P("La flexibilidad que este trabajo reporta no sale de una ecuación sino de tres "
  "construcciones que se estiman por separado y tienen que coincidir. Este anexo las escribe "
  "en forma explícita, con notación unificada, y deja asentado qué estimador y qué matriz de "
  "varianzas se usó en cada una. Las ecuaciones numeradas son las que efectivamente se llevan "
  "a los datos; las restricciones teóricas se listan aparte para que se vea cuáles se imponen "
  "y cuáles se testean.")

# ---------------------------------------------------------------- A.1 notación
H2("A.1 Notación")
TABLA(["Símbolo", "Qué es", "Fuente"], [
    ("p_t", "Valor unitario FOB del entero L1 congelado a bordo, US$/kg, mensual",
     "Base de comercio (transaccional), partida 0306.17, sufijo SA01"),
    ("e_t", "Tipo de cambio euro/dólar", "BCE"),
    ("p*_t", "Precio del camarón de cultivo en la UE, €/kg — el bien de afuera",
     "EUMOFA; contraste con Ecuador a España"),
    ("Q_t", "Desembarque tangonero, suma móvil de doce meses, en toneladas", "SSPyA"),
    ("D_t^G", "Desembarque total de langostino, todas las flotas, suma móvil 12 meses", "SSPyA"),
    ("q_tan, q_fre", "Kilos exportados de entero L1+L2 por flota, ventana móvil 12 meses",
     "Base de comercio"),
    ("w_tan", "Participación de la tangonera en el valor del grupo argentino", "Base de comercio"),
    ("s_tan", "Participación de la tangonera en el volumen del grupo", "Base de comercio"),
    ("h_t", "Brecha del índice de actividad HORECA respecto de su propia tendencia",
     "Eurostat CNAE/Ateco 56 + OxCGRT"),
    ("z_t", "Instrumento: ventana en que el conflicto gremial deprime la captura de 12 meses",
     "Construida"),
    ("D_mt, t", "Once dummies de mes y tendencia lineal en años", "—"),
], [1500, 4700, 2900])
P()

# ---------------------------------------------------------------- A.2 capa 1
H2("A.2 Capa 1 — la ecuación única de demanda inversa residual")

P("Es la que produce el número que se cita. El precio se toma relativo al camarón de cultivo, "
  "lo que neutraliza a la vez el ciclo mundial del camarón y el tipo de cambio:")
EQ("log (p_t / e_t) − log p*_t  =  α + f · log Q_t + φ · h_t + τ · t + Σ_m δ_m·D_mt + ε_t", "A.1")
P("Dividir por el precio del competidor no es una conveniencia de escala: ",
  ("impone que el coeficiente del precio del cultivo sea exactamente +1", "b"),
  ". La versión sin esa restricción —log p contra log Q y log p* por separado— también está "
  "estimada y da el mismo resultado, de modo que la restricción no está haciendo el trabajo.")
P("El parámetro de interés es f = ∂ log p / ∂ log Q, la flexibilidad-precio. El umbral que "
  "decide la política no es cero sino −1, porque el ingreso de la industria es P(Q)·Q:")
EQ("∂ log (p·Q) / ∂ log Q  =  1 + f", "A.2")
P("Con f > −1 un recorte de cantidad sube el precio menos que proporcionalmente y la "
  "facturación cae. Con f < −1 la sube. Toda la discusión de política se reduce a de qué lado "
  "de −1 está el intervalo de confianza.")

# ---------------------------------------------------------------- A.3 identificación
H2("A.3 Identificación: por qué no alcanza con mínimos cuadrados")

P("Precio y cantidad se determinan simultáneamente, y la serie contiene dos episodios de signo "
  "contrario que, mezclados, se cancelan. En ", ("2020", "b"), " el canal HORECA estuvo cerrado: "
  "precio y cantidad caen juntos, y leído como si fuera un movimiento de oferta el año "
  "«demuestra» una curva de pendiente positiva. Se controla con h_t y se verifica excluyendo la "
  "ventana mar-2020 a mar-2022. En ", ("2025", "b"), " el conflicto gremial paró la flota de "
  "abril a julio, al inicio de la temporada, y la captura de campaña cayó 46%: ése es un "
  "desplazamiento de oferta puro y es el que traza la demanda.")
P("El instrumento es la ventana en que ese paro deprime la captura acumulada de doce meses:")
EQ("z_t  =  1{ abr-2025 ≤ t ≤ mar-2026 }", "A.3")
P("y el modelo se estima por mínimos cuadrados en dos etapas:")
EQ("log Q_t  =  π₀ + π₁·z_t + φ·h_t + τ·t + Σ_m δ_m·D_mt + v_t", "A.4")
EQ("log (p_t/e_t) − log p*_t  =  α + f · log Q̂_t + φ·h_t + τ·t + Σ_m δ_m·D_mt + ε_t", "A.5")
P("La primera etapa da F = 61,1 en la especificación base y F = 40,3 en la versión con "
  "desembarques por flota. La restricción de exclusión se apoya en la naturaleza del episodio: "
  "un conflicto gremial argentino mueve la oferta embarcada, no la disposición a pagar del "
  "comprador europeo, que además está controlada por h_t y por el precio del cultivo.")
NOTA("La captura rezagada se probó como instrumento alternativo y no sirve: primera etapa "
     "F = 0,1. El langostino tiene ciclo de vida corto y reemplazo casi total de ejemplares "
     "entre temporadas (INIDEP), de modo que no hay persistencia de biomasa que explotar. Es la "
     "razón por la que toda la identificación causal descansa hoy en un solo episodio, y el "
     "motivo del pedido de actas del CFP y esfuerzo mensual del §11.")

# ---------------------------------------------------------------- A.4 campaña
H2("A.4 El modelo de campaña")

P("El congelado a bordo se pesca entre abril y octubre y se vende a lo largo de los doce meses "
  "siguientes, así que la unidad temporal correcta no es el mes sino la campaña. Sobre la "
  "sección cruzada de campañas completas, con el precio ponderado por kilos de la ventana de "
  "venta de julio de Y a junio de Y+1 contra la captura de abril-octubre de Y:")
EQ("log rel_Y  =  α + f · log Cap_Y + φ · h_Y + τ · Y + u_Y", "A.6")
P("Es una muestra chica —doce campañas— pero empareja la unidad temporal y no depende del "
  "instrumento. Que dé lo mismo que la versión mensual instrumentada es parte de la evidencia.")

# ---------------------------------------------------------------- A.5 sistema flotas
H2("A.5 Capa 2 — el sistema de dos flotas, en dos etapas")

P("Este sistema nace de un problema concreto. Metida como regresor suelto en (A.1), la cantidad "
  "fresquera entra con signo ", ("positivo", "b"), " —+0,063, con t = 2,45—: más oferta "
  "fresquera, mayor precio tangonero. Un sustituto no hace eso. Lo que ese coeficiente captura "
  "es un desplazamiento de demanda común a las dos flotas, es decir que la fresquera es tan "
  "endógena como la tangonera. El sistema lo resuelve por construcción: el término de escala "
  "absorbe el movimiento común y los coeficientes de cantidad quedan midiendo sustitución.")
P("La estructura en dos etapas es la que corresponde cuando un grupo de bienes compite contra "
  "un bien de afuera —acá, el camarón de cultivo.")

H2("A.5.1 Etapa de grupo")
P("Cuánto cae el precio argentino agregado, relativo al cultivo, cuando sube la oferta argentina "
  "total. Es la flexibilidad que manda para la política, porque es la que responde a la "
  "pregunta que el regulador puede efectivamente hacerse:")
EQ("log (P_t^G / p*_t)  =  α_G + f_G · log D_t^G + φ·h_t + τ·t + Σ_m δ_m·D_mt + u_t", "A.7")
P("con P^G el valor unitario del entero L1+L2 de las dos flotas juntas y D^G el desembarque "
  "total de todas las flotas. Se estima por MCO con errores HAC y por variable instrumental con "
  "el mismo z_t de (A.3). Resultado: ", ("f_G = −0,196", "b"), ".")
P("La distinción entre desembarque y kilos exportados no es menor. El desembarque es la cantidad "
  "exógena, la que la política mueve. Los kilos embarcados llevan adentro la decisión de la "
  "empresa sobre cuándo vender, y por eso arrastran la demanda al lado derecho.")

H2("A.5.2 Etapa interna: sistema LA/IAIDS de dos bienes")
P("Dado el total, cómo se reparte entre flotas. El sistema de demanda inversa casi-ideal en su "
  "forma general, con i, j sobre {tangonera, fresquera}:")
EQ("w_i  =  α_i + Σ_j γ_ij · log q_j + β_i · log Q*", "A.8")
P("sujeto a las restricciones de la teoría:")
EQ("agregación:  Σ_i α_i = 1 ,  Σ_i γ_ij = 0 ,  Σ_i β_i = 0", "A.9a")
EQ("homogeneidad:  Σ_j γ_ij = 0        ·        simetría:  γ_ij = γ_ji", "A.9b")
P("Con ", ("dos", "b"), " bienes esto colapsa a una sola ecuación estimable, y algo notable "
  "ocurre en el camino. Homogeneidad da γ₁₁ = −γ₁₂; agregación da γ₂₁ = −γ₁₁; juntas implican "
  "γ₁₂ = γ₂₁. ", ("La simetría no hay que imponerla: es una consecuencia", "b"), ". Es el único "
  "caso en que sale gratis, y es una de las razones por las que agrupar las flotas de a dos "
  "vale la pena. La forma que se lleva a los datos:")
EQ("w_tan,t = α + γ · log(q_tan,t / q_fre,t) + β · log Q*_t + θ · log p*_t + φ·h_t + τ·t "
   "+ Σ_m δ_m·D_mt + ε_t", "A.10")
EQ("log Q*_t  =  w̄_tan · log q_tan,t + w̄_fre · log q_fre,t", "A.11")
P("Dos decisiones de construcción que no son cosméticas. Escribir el regresor como el ",
  ("cociente", "b"), " de cantidades es lo que impone homogeneidad. Y el índice de cantidad de "
  "Stone en (A.11) va con participaciones ", ("medias", "b"), ", no corrientes: con las "
  "corrientes el regresor lleva adentro la variable dependiente.")
P("Estimación: γ = 0,1081 con t = 12,5, sobre N = 138 meses, R² = 0,932, con participación media "
  "de la tangonera de 84,2% del valor y 82,1% del volumen.")

H2("A.5.3 De coeficientes a flexibilidades")
P("Las flexibilidades de cantidad no compensadas y la de escala se recuperan como:")
EQ("f_ij  =  γ_ij / w_i  +  β_i · w_j / w_i  −  δ_ij        ·        "
   "f_i^escala  =  β_i / w_i − 1", "A.12")
P("con δ_ij la delta de Kronecker. El término β_i·w_j/w_i es el pedazo del efecto escala que "
  "le toca a cada casilla, y omitirlo no es inocuo: como la homogeneidad da Σ_j γ_ij = 0, sin "
  "ese término ", ("toda fila suma exactamente −1", "b"), " y la matriz contradice a la columna "
  "de escala del mismo cuadro. La identidad que hay que poder verificar siempre es "
  "Σ_j f_ij = f_i^escala. La matriz condicional resultante —fila: precio de i; columna: "
  "cantidad de j— es:")
TABLA(["", "Cantidad tangonera", "Cantidad fresquera"], [
    ("Precio tangonero", "−0,872", "−0,128"),
    ("Precio fresquero", "−0,685", "−0,315"),
], [3100, 3000, 3000], negrita_col0=True)
P(("PENDIENTE DE REGENERAR: ", "b"), "estas dos filas y las cifras de A.14 y A.6 salen de la "
  "corrida anterior al arreglo de A.12 —se reconocen porque suman exactamente −1— y hay que "
  "rehacerlas con demanda_inversa_sistema_flotas.py y demanda_inversa_modelo.py. La fórmula de "
  "arriba ya es la correcta.")
P()

H2("A.5.4 Recomposición: el paso donde es fácil equivocarse")
P("El IAIDS no estima la flexibilidad del precio a secas. Estima la del precio ",
  ("normalizado por el gasto del grupo", "b"), ", p_i/E con E = P^G·Q^G. Para volver al precio "
  "hay que devolver las dos piezas que la normalización sacó —el efecto escala y la propia "
  "respuesta del grupo—:")
EQ("∂ log p_i / ∂ log q_i  =  f_ii  +  s_i · (1 + f_G)", "A.13")
P(("No", "b"), " es f_ii + s_i·f_G. Esa forma, que es el error natural, da −0,88 y no reconcilia "
  "con ninguna de las otras construcciones; la de (A.13) sí. Con f_ii = −0,872, s_tan = 0,821 y "
  "f_G = −0,196:")
EQ("f_tangonera  =  −0,872 + 0,821 · (1 − 0,196)  =  −0,212", "A.14")
P("El contraste directo —ecuación incondicional con los desembarques de cada flota por separado, "
  "instrumentada— da ", ("−0,239", "b"), " con error estándar 0,078 y primera etapa F = 40,3. "
  "Las dos vías coinciden entre sí y con la ecuación única.")
P("Y ahí se resuelve el signo perverso que motivó todo el ejercicio: medida por ",
  ("desembarque", "b"), " en lugar de kilos embarcados, la cantidad fresquera entra en +0,012 "
  "con t = 0,28, es decir cero. No era un efecto de demanda: era la empresa eligiendo el momento "
  "del embarque.")

# ---------------------------------------------------------------- A.6 origen
H2("A.6 Capa 3 — el sistema por origen en el mercado europeo")

P("Anterior y complementario: un LA/IAIDS de cinco bienes sobre la importación extra-UE de "
  "camarón tropical y misceláneo congelado, mensual 2013-2026, con los orígenes agrupados en "
  "Argentina, Ecuador, India, Vietnam y un residual:")
EQ("w_i  =  α_i + Σ_j γ_ij · [ log q_j − log q_RE ] + β_i · log Q* + τ·t + Σ_m δ_m·D_mt + ε_it",
   "A.15")
P("La homogeneidad se impone por normalización contra el grupo residual —de ahí la resta dentro "
  "del corchete— y la ecuación del residual se recupera por agregación, γ_RE,j = −Σ_i γ_ij. "
  "Con cinco bienes la simetría ya no sale gratis: acá ", ("no se impone, se testea", "b"), ". "
  "Se estiman las cuatro ecuaciones independientes una por una.")
P("Flexibilidad propia de Argentina: ", ("−0,267", "b"), "; flexibilidad de escala −0,819; "
  "participación media en el valor importado 14,6%. Es una base de datos distinta (Eurostat "
  "COMEXT vía EUMOFA), un mercado distinto (la UE entera, no el producto argentino) y un método "
  "distinto, y llega al mismo orden de magnitud.")

# ---------------------------------------------------------------- A.7 estimadores
H2("A.7 Estimadores y matrices de varianzas")

TABLA(["Bloque", "Estimador", "Errores estándar", "Por qué"], [
    ("Ecuación única mensual (A.1)", "MCO", "Newey-West HAC, 6 rezagos",
     "Autocorrelación residual en serie mensual"),
    ("Etapas de grupo e interna (A.7, A.10)", "MCO ecuación por ecuación",
     "Newey-West HAC, 18 rezagos",
     "Las ventanas móviles de 12 meses se solapan: el error es MA(11) por construcción"),
    ("Todas las versiones instrumentadas", "IV 2SLS (linearmodels)",
     "HAC con núcleo de Bartlett", "Consistencia bajo heterocedasticidad y autocorrelación"),
    ("Modelo de campaña (A.6)", "MCO, sección cruzada de 12", "HC1",
     "Muestra chica: corrección de grados de libertad"),
    ("Sistema por origen (A.15)", "MCO ecuación por ecuación", "Newey-West HAC, 6 rezagos",
     "Simetría testeada, no impuesta"),
    ("Flexibilidades derivadas (A.12, A.13)", "Método delta", "w tratado como fijo",
     "Las participaciones se estiman con precisión de orden mayor"),
], [2600, 2100, 2100, 2300])
P()

# ---------------------------------------------------------------- A.8 convergencia
H2("A.8 Convergencia de las construcciones")

P("La razón para creerle al número no es ninguna estimación en particular sino que siete "
  "construcciones con datos, unidades temporales y métodos distintos caen en la misma franja:")
TABLA(["Construcción", "f"], [
    ("Mensual instrumentada, L1 solo", "−0,184"),
    ("Mensual instrumentada, L1+L2", "−0,219"),
    ("Campaña, con tendencia", "−0,196"),
    ("L1+L2 con la participación del L2 como control explícito", "−0,208"),
    ("Sistema de dos flotas, recompuesto por (A.13)", "−0,212"),
    ("Incondicional con desembarques por flota, instrumentada", "−0,239"),
    ("Sistema por origen, IAIDS de cinco bienes en la UE", "−0,267"),
], [6600, 2500])
P()
P("Ninguna se acerca a −1; el extremo más negativo de todos los intervalos de confianza al 95% "
  "llega a −0,39. La conclusión de política no depende de cuál se elija.")

# ---------------------------------------------------------------- A.9 pendientes
H2("A.9 Lo que este anexo no resuelve")

P(("Uno.", "b"), " El sistema por origen se estima ecuación por ecuación, de modo que la "
  "simetría se testea pero no se impone. Imponerla por SUR iterado es el refinamiento que "
  "corresponde si el trabajo va a arbitraje. En el sistema de dos flotas el punto no se plantea, "
  "porque ahí la simetría es una consecuencia y no un supuesto.")
P(("Dos.", "b"), " Toda la identificación causal descansa en un episodio. Sin 2025 no hay "
  "instrumento, y (A.4) no tiene con qué. Es la limitación estructural del trabajo y no se "
  "arregla con método: se arregla con las series de apertura, cierre y esfuerzo que se piden "
  "en el §11.")

# ═══════════════════════════════════════════════════════════════════ 3. TOC al día
st = doc.settings.element
uf = st.find(qn("w:updateFields"))
if uf is None:
    uf = OxmlElement("w:updateFields"); st.append(uf)
uf.set(qn("w:val"), "true")

doc.save(RUTA)
print("guardado:", RUTA)
