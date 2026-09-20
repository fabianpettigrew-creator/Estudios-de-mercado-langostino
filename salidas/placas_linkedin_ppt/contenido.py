# -*- coding: utf-8 -*-
"""Contenido de las placas del resumen ejecutivo (PPT ver08.09.26).

Filminas del PPT: 1, 2, 3, 5, 6, 9, 10, 11, 13+14 (fusionadas), 15, 16
y el cierre (filmina 21, agregado).

Toda cifra fue auditada contra ../Estudio_mercado_langostino_ver08.09.26.docx.
Correcciones respecto del PPT, documentadas en NOTAS_DE_AUDITORIA.md:
  - filmina 2: Ecuador "×5,5 en producción" no figura en el estudio (dice ×3,0
    entre 2015 y 2024). Se usa la exportación ×9,3, que sí está.
  - filmina 2: "#6 mundial" -> el estudio dice "entre los cinco salvajes más
    capturados del mundo".
  - filmina 11: "era el 56% en 2024" no figura en el estudio. Se omite.
  - filmina 21: "rinde 31% más que la mejor cola P&D" invierte el cálculo;
    el estudio dice que la P&D rinde 31% MENOS por kilo capturado.
"""

BANCO = [

    dict(id="portada", tipo="portada", ppt=1,
         kicker="ESTUDIO DE MERCADO &middot; LANGOSTINO ARGENTINO",
         titulo="Precio, comercio<br>y posici&oacute;n<br>competitiva",
         subtitulo="Resumen ejecutivo",
         lead="Un producto salvaje de nicho, sobre una base productiva que se achica, compitiendo contra una marea de langostino de cultivo. Su valor no est&aacute; en el precio-commodity sino en lo que es &mdash;salvaje, entero, premium&mdash;.",
         fuente=""),

    dict(id="cinco_numeros", tipo="lista", ppt=2,
         kicker="EL CUADRO",
         headline="El estudio en cinco n&uacute;meros",
         intro="D&oacute;nde est&aacute; parado hoy el langostino argentino, antes de entrar en el detalle.",
         items=[
             ("1,6&times;", "Premium sobre el vannamei en EE.UU.", "oscil&oacute; entre 1,3 y 1,8 desde 2020"),
             ("US$7,0", "Mejor uso del calibre grande: entero L1 a la UE", "por kilo de producto, 2025-26"),
             ("&minus;13%", "Desembarques contra el pico de 2018", "255 a 222 kt en 2024; 2025 cay&oacute; a 187 por el conflicto gremial"),
             ("&times;2,9", "Marea de vannamei de cultivo, 2010-2024", "Ecuador multiplic&oacute; &times;9,3 su exportaci&oacute;n desde 2013"),
             ("Ninguno", "Competidor salvaje directo a escala", "entre los cinco salvajes m&aacute;s capturados: categor&iacute;a de uno"),
         ],
         fuente="aduana argentina &middot; SSPyA &middot; NOAA FOSS &middot; FishStat"),

    dict(id="tesis", tipo="puntos", ppt=3,
         kicker="LA TESIS",
         headline="No se compite por volumen ni por precio",
         intro="Una conclusi&oacute;n atraviesa las doce secciones del estudio y ordena todo lo que viene despu&eacute;s.",
         puntos=[
             ("La base productiva se achica",
              "La captura toc&oacute; m&aacute;ximo en 2018 (255 kt) y en 2024 est&aacute; 13% por debajo (222 kt). Una pesquer&iacute;a no se expande a voluntad: cada tonelada es m&aacute;s escasa que la anterior."),
             ("El sustituto crece y abarata",
              "El vannamei de cultivo se multiplic&oacute; &times;2,9 desde 2010 y hoy son 7,66 Mt, 34 veces la captura argentina. Y no baja el precio resignando margen: baja porque le baja el costo."),
             ("El valor est&aacute; en el atributo",
              "Salvaje, entero, calibre grande, origen identificable y &mdash;desde 2026&mdash; certificado MSC. Es lo &uacute;nico que el cultivo no puede replicar."),
         ],
         remate="No hay que buscar m&aacute;s toneladas: hay que capturar m&aacute;s valor en cada tonelada, eligiendo flota, formato, calibre, destino y momento.",
         fuente="Secciones 1, 9 y 10 del estudio"),

    dict(id="dos_flotas", tipo="tarjetas", ppt=5,
         kicker="EL PRODUCTO",
         headline="Dos flotas, dos cadenas de valor distintas",
         intro="La diferencia no es s&oacute;lo tecnol&oacute;gica: define productos, plantas y mercados propios.",
         tarjetas=[
             ("CONGELADO A BORDO &middot; SUFIJO SA01", "Congeladora tangonera",
              "Congela en las horas siguientes a la captura: corta temprano la degradaci&oacute;n y minimiza la melanosis. Produce esencialmente entero en bloque por calibre (L1 a L5). Opera en aguas nacionales y exporta directo, sin pasar por planta."),
             ("CONGELADO EN TIERRA", "Fresquera",
              "Mantiene la captura en hielo durante mareas de 3 a 10 d&iacute;as y congela reci&eacute;n en planta: m&aacute;s riesgo de melanosis. A cambio, la planta hace pelado, desvenado, cocido e IQF &mdash;y con eso accede a EE.UU.&mdash;. Opera fuerte en aguas de Chubut."),
         ],
         remate="Casi no compiten entre s&iacute;: hacen productos distintos, para clientes distintos y en meses distintos del a&ntilde;o. Todo lo dem&aacute;s &mdash;precio, destino, estacionalidad, aranceles&mdash; se ordena por esta divisi&oacute;n.",
         fuente="Secci&oacute;n 2 &middot; producto y proceso por flota"),

    dict(id="flotas_valor", tipo="dos_stats", ppt=6,
         kicker="LAS DOS FLOTAS",
         headline="La tangonera genera el doble de valor por tonelada",
         intro="Y la brecha no es s&oacute;lo mezcla de producto: el mismo talle vale m&aacute;s si lo trae el tangonero.",
         stats=[
             ("2,15&times;", 150, "la brecha de valor por tonelada",
              "US$7,08 por kilo desembarcado la tangonera contra ~US$3,3 la fresquera en 2025"),
             ("+25%", 150, "vale el entero L1 tangonero",
              "US$7,23 contra US$5,80 el fresquero, mismo calibre &middot; en cola, +22% en C1"),
         ],
         remate="Donde las dos flotas compiten de verdad casi no hay diferencia (Jap&oacute;n &minus;0,19, China +0,20, Italia +0,35 d&oacute;lares por kilo). La brecha sale de Espa&ntilde;a, donde es de US$1,01: la fresquera manda el 60% de su volumen a un solo comprador y ah&iacute; cobra el precio m&aacute;s bajo de la matriz.",
         fuente="Secci&oacute;n 6 &middot; aduana argentina (SA) &divide; SSPyA"),

    dict(id="destinos", tipo="barras", ppt=9,
         kicker="DESTINOS",
         headline="Espa&ntilde;a se lleva el volumen y aparece pagando menos",
         intro="Entero L1, el producto insignia. La barra es el porcentaje del volumen; al lado, el FOB promedio de ese destino.",
         barras=[
             ("Espa&ntilde;a", 46.0, "46,0%", "US$6,2", True),
             ("Italia", 18.4, "18,4%", "US$6,6", False),
             ("Resto", 13.8, "13,8%", "US$6,3", False),
             ("China", 12.0, "12,0%", "US$6,4", False),
             ("Jap&oacute;n", 9.9, "9,9%", "US$6,3", False),
         ],
         pie_grafico="% del volumen de entero L1 &middot; FOB US$/kg",
         remate="La mitad de la brecha es ruta de proceso: Espa&ntilde;a es el &uacute;nico que compra L1 procesado en tierra en volumen &mdash;19,8% de su L1, contra 2,4% de Italia&mdash; y ese producto vale un d&oacute;lar menos. Comparando s&oacute;lo congelado a bordo el panel se aplana: Italia 6,59, China 6,38, Espa&ntilde;a 6,37, Jap&oacute;n 6,31.",
         fuente="Secci&oacute;n 7 &middot; base de comercio, entero L1 2018-2026"),

    dict(id="flujo", tipo="tarjetas", ppt=10,
         kicker="FLUJO COMERCIAL",
         headline="Espa&ntilde;a es la puerta de Europa; EE.UU. es otro negocio",
         intro="Espa&ntilde;a re-despacha al resto del continente, y eso oculta el origen argentino en las estad&iacute;sticas de Francia e Italia, que registran por procedencia.",
         tarjetas=[
             ("DESTINO 1", "Espa&ntilde;a &middot; el hub",
              "Casi la mitad del entero L1 y un tercio de la exportaci&oacute;n total. Es el &uacute;nico que compra volumen de L1 procesado en tierra y el &uacute;nico que sostiene compra en verano."),
             ("DESTINO 2", "Italia &middot; compra directo",
              "El 18,4% del L1 y el destino que mejor paga a igual ruta de proceso. Es 88% tangonero y compra en el pico de precio sin pedir descuento."),
             ("DESTINO 3", "EE.UU. &middot; otro producto",
              "Paga un 60% m&aacute;s por kilo en la misma moneda, pero compra cola pelada, no entero: 67% pelado y 33% con c&aacute;scara, contra 90% pelado de India."),
         ],
         remate="Jap&oacute;n compra 99% tangonera, Italia 88% y Espa&ntilde;a 71%, mientras el circuito de cola y reproceso es casi enteramente fresquero. Destino y flota son, en el fondo, la misma variable.",
         fuente="Secciones 4, 5 y 7 &middot; NOAA FOSS &middot; Comext &middot; aduana"),

    dict(id="fason", tipo="dos_stats", ppt=11,
         kicker="EL FAS&Oacute;N",
         headline="Dos de cada tres kilos argentinos en EE.UU. no salen de Argentina",
         intro="La aduana estadounidense registra ORIGEN, no procedencia &mdash; y pelar no cambia el origen.",
         stats=[
             ("17,0 kt", 132, "registra EE.UU. de origen argentino",
              "contra 5,3 kt despachadas directo desde Argentina en 2025 (INDEC): una brecha de 11,8 kt"),
             ("69%", 150, "lleg&oacute; por reprocesado en otros mercados",
              "el circuito documentado mueve unas 9,6 kt al a&ntilde;o"),
         ],
         remate="Y es un circuito exclusivamente fresquero: la cola que va a Per&uacute;, Tailandia, Vietnam e Indonesia es 99,6% de origen fresquero. La tangonera no participa: vende entero premium directo a mercados finales.",
         fuente="Secci&oacute;n 4 &middot; INDEC &middot; NOAA FOSS por pa&iacute;s de origen"),

    dict(id="aranceles", tipo="aranceles", ppt="13+14",
         kicker="ARANCELES",
         headline="Un cambio de reglas que deja a Argentina en el piso",
         titulo_us="EE.UU. &middot; carga total, agosto de 2026",
         us=[
             ("India", 10.0, 7.1, "17,1%", False),
             ("Vietnam", 12.5, 2.8, "15,3%", False),
             ("Indonesia", 10.0, 3.9, "13,9%", False),
             ("Ecuador", 10.0, 3.8, "13,8%", False),
             ("Tailandia", 12.5, 0.0, "12,5%", False),
             ("Per&uacute;", 12.5, 0.0, "12,5%", False),
             ("Argentina", 10.0, 0.0, "10%", True),
             ("M&eacute;xico", 10.0, 0.0, "10%", False),
         ],
         leyenda_us="Secci&oacute;n 301 (jul-2026) + antidumping y compensatorios",
         titulo_ue="UE &middot; arancel al congelado 0306.17",
         ue=[("hasta abr-26", 12.0, "12%"), ("may-26", 9.6, "9,6%"), ("ene-27", 7.2, "7,2%"),
             ("ene-28", 4.8, "4,8%"), ("ene-29", 2.4, "2,4%"), ("ene-30", 0.0, "0%")],
         leyenda_ue="Acuerdo Interino UE-Mercosur &middot; 2,4 puntos de margen por a&ntilde;o, ya firmados",
         remate="Ventaja sobre India: ~7 puntos &mdash;lleg&oacute; a ser de ~47 con los rec&iacute;procos, hasta que la Corte Suprema los anul&oacute; en febrero de 2026&mdash;. Argentina es el &uacute;nico oferente grande sin antidumping: nunca fue pa&iacute;s investigado.",
         fuente="Secci&oacute;n 8 &middot; Federal Register &middot; DOUE UE-Mercosur"),

    dict(id="vannamei", tipo="barras", ppt=15,
         kicker="EL COMPETIDOR",
         headline="Vannamei: una marea de cultivo, no una pesquer&iacute;a",
         stat_previo=("7,66 Mt", "de vannamei de cultivo en 2024 &mdash; 34 veces la captura argentina de langostino, y &times;2,9 lo que era en 2010"),
         barras=[
             ("China", 2.374, "2,374 Mt", "31%", False),
             ("Ecuador", 1.218, "1,218 Mt", "16%", False),
             ("India", 1.183, "1,183 Mt", "15%", False),
             ("Vietnam", 0.934, "0,934 Mt", "12%", False),
             ("Indonesia", 0.786, "0,786 Mt", "10%", False),
         ],
         pie_grafico="Producci&oacute;n 2024 &middot; cinco pa&iacute;ses son el 85% del mundo",
         remate="A diferencia de una pesquer&iacute;a, el cultivo se expande a voluntad: desde 2015 Ecuador triplic&oacute; su producci&oacute;n, India casi y Vietnam tambi&eacute;n. Entre los salvajes, en cambio, el langostino es una categor&iacute;a de uno: su competencia real no es salvaje.",
         fuente="Secciones 9 y 10 &middot; FAO FishStat, descarga 2026"),

    dict(id="ecuador_costo", tipo="dos_stats", ppt=16,
         kicker="EL COMPETIDOR &middot; EL COSTO",
         headline="Ecuador no baja el precio: le baja el costo",
         intro="Y se movi&oacute; al formato que el langostino consideraba terreno propio.",
         stats=[
             ("US$3,60", 132, "vale el kilo en la granja ecuatoriana",
              "baj&oacute; 35% desde 2015 (US$5,50) mientras triplicaba la producci&oacute;n: el m&aacute;s barato del mundo a escala, por debajo de Indonesia 4,11 e India 4,34"),
             ("&times;35", 150, "creci&oacute; su exportaci&oacute;n de entero",
              "de 5,9 kt en 2013 a 202,4 kt en 2025, con el precio bajando de US$6,90 a US$4,91"),
         ],
         remate="Una granja baja su costo con gen&eacute;tica, densidad y alimento; una pesquer&iacute;a no puede pescar m&aacute;s barato. Cuando Ecuador baja el precio no resigna margen: traslada una ca&iacute;da de costo. Competir por precio es competir en la cancha del otro.",
         fuente="Secci&oacute;n 9 &middot; FAO FishStat &middot; aduana de Ecuador"),

    dict(id="cierre", tipo="puntos", ppt=21, oscuro=True,
         kicker="CIERRE",
         headline="Cuatro conclusiones",
         puntos=[
             ("El volumen no es la palanca; el valor por tonelada s&iacute;",
              "La base productiva se achica y el sustituto se expande a voluntad: la pregunta no es cu&aacute;nto se pesca, sino cu&aacute;nto valor deja cada tonelada."),
             ("La flota y el calibre ya son la ventaja: falta cobrarla",
              "La tangonera genera 2,15&times; el valor por tonelada de la fresquera y su entero L1 vale +25% a igual calibre; la mejor cola P&amp;D rinde 31% menos por kilo capturado."),
             ("Espa&ntilde;a es el problema competitivo, y viene de antes de 2025",
              "Ecuador pas&oacute; del 14% al 49% del mercado espa&ntilde;ol y cruz&oacute; a Argentina en 2020; en entero, la brecha se cerr&oacute; de 41 a 1 a 1,6 a 1."),
             ("Las dos buenas noticias son de calendario, no de mercado",
              "El arancel europeo baja 2,4 puntos por a&ntilde;o hasta 0% en 2030 y el MSC habilita el sello sobre el entero tangonero: hoy los mercados que lo pagan reciben el 1-2% de la exportaci&oacute;n."),
         ],
         cta="Lic. Fabi&aacute;n Pettigrew &middot; Axia Consultora",
         fuente=""),
]

# --- Selección publicada -------------------------------------------------
SELECCION = [
    "portada",        # PPT 1
    "cinco_numeros",  # PPT 2
    "tesis",          # PPT 3
    "dos_flotas",     # PPT 5
    "flotas_valor",   # PPT 6
    "destinos",       # PPT 9
    "flujo",          # PPT 10
    "fason",          # PPT 11
    "aranceles",      # PPT 13 + 14 fusionadas
    "vannamei",       # PPT 15
    "ecuador_costo",  # PPT 16
    "cierre",         # PPT 21 — agregado, sacalo de esta lista si no lo querés
]

_POR_ID = {d["id"]: d for d in BANCO}
SLIDES = [_POR_ID[k] for k in SELECCION]
