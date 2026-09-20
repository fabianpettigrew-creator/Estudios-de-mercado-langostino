# -*- coding: utf-8 -*-
"""Contenido de las placas para LinkedIn.

Toda cifra sale del estudio ver08.09.26 y fue verificada contra su texto.
Fuente: ../Estudio_mercado_langostino_ver08.09.26.docx
"""

BANCO = [
    dict(id="portada", tipo="portada",
         kicker="ESTUDIO DE MERCADO &middot; 2026",
         titulo="Langostino<br>argentino",
         subtitulo="Precio, comercio y posici&oacute;n competitiva",
         lead="Diez hallazgos sobre datos oficiales de aduana, FAO, NOAA y relevamiento propio de g&oacute;ndola.",
         fuente=""),

    dict(id="punto_partida", tipo="dato",
         kicker="EL PUNTO DE PARTIDA",
         headline="Una pesquer&iacute;a post-pico frente a una marea de cultivo",
         stat="&times;34", stat_size=200,
         stat_label="es el vannamei de cultivo (7,66 Mt) sobre la captura argentina de langostino (222 kt) en 2024",
         body="La captura toc&oacute; m&aacute;ximo en 2018 (255 kt) y en 2024 est&aacute; 13% por debajo. El sustituto de cultivo se multiplic&oacute; &times;2,9 desde 2010. No se puede competir por volumen ni por precio-commodity.",
         fuente="FAO FishStat 2025.1.0"),

    dict(id="eeuu", tipo="dato",
         tema="ESTADOS UNIDOS",
         headline="El langostino argentino que no sale de Argentina",
         stat="69%", stat_size=210,
         stat_label="del langostino de origen argentino que entr&oacute; a EE.UU. en 2025 lleg&oacute; reprocesado desde terceros pa&iacute;ses",
         body="Argentina despach&oacute; 5,3 kt directo (INDEC), pero la aduana estadounidense registr&oacute; 17,0 kt de origen argentino. La brecha es de 11,8 kt. EE.UU. registra origen, no procedencia: pelar no cambia el origen.",
         fuente="INDEC &middot; NOAA FOSS, 2025"),

    dict(id="peru", tipo="cita",
         tema="EL CIRCUITO",
         headline="Per&uacute; lo declara por nombre en su propia aduana",
         stat="34%", stat_size=210,
         stat_label="de toda la exportaci&oacute;n peruana de langostino es, por descripci&oacute;n aduanera, langostino argentino",
         cita="COLAS DE LANGOSTINO P&amp;D 40-70 (PLEOTICUS MUELLERI) EN CAJAS X 12 KGS",
         body="Inexistente hasta 2021, hoy estructural: pas&oacute; de 0 a 8,6 kt. Per&uacute; no captura la especie &mdash;FishStat registra cero&mdash;, as&iacute; que cada kilo es necesariamente argentino.",
         fuente="base de comercio &middot; FAO FishStat"),

    dict(id="origen", tipo="dato",
         tema="EL ORIGEN",
         headline="Si aparece en un tercer pa&iacute;s, s&oacute;lo pudo salir de Argentina",
         stat="99,5%", stat_size=185,
         stat_label="de la captura mundial de Pleoticus muelleri es argentina: 222.163 t en 2024",
         body="Brasil captura 1.153 t y Uruguay nada desde 2017. Las flotas de bandera lejana que operan en el &aacute;rea 41 &mdash;Espa&ntilde;a, Taiw&aacute;n, China, Corea&mdash; pescan calamar y merluza: de langostino, cero.",
         fuente="FAO FishStat, capturas 2024 &middot; &aacute;rea 41"),

    dict(id="valor_kilo", tipo="dato",
         tema="VALOR POR KILO",
         headline="El entero grande rinde m&aacute;s que el pelado premium",
         stat="$7,0<span class=\"vs\">vs</span>$4,8", stat_size=145,
         stat_label="de ingreso por kilo de langostino desembarcado: entero L1 a Espa&ntilde;a/Italia contra la mejor cola P&amp;D",
         body="La P&amp;D se vende a $12,4 por kilo de producto &mdash;casi el doble que el entero&mdash; pero de un kilo capturado salen apenas 385 gramos de carne. Rinde 31% menos por kilo pescado.",
         fuente="FOB real de exportaci&oacute;n argentina 2025-26"),

    dict(id="flotas", tipo="dato",
         tema="LAS DOS FLOTAS",
         headline="La tangonera genera el doble de valor por tonelada",
         stat="2,15&times;", stat_size=185,
         stat_label="de brecha entre flotas por kilo desembarcado en 2025: US$7,08 la tangonera contra ~US$3,3 la fresquera",
         body="El mismo talle vale m&aacute;s si lo trae el tangonero: el entero L1 sali&oacute; a US$7,23 contra US$5,80 (+25%). Y la brecha se abre: dentro de Espa&ntilde;a pas&oacute; de US$0,24 en 2019 a US$1,41 en 2026.",
         fuente="aduana argentina (sufijo SA) &middot; desembarques SSPyA"),

    dict(id="ecuador", tipo="dato",
         tema="EL COMPETIDOR",
         headline="Ecuador no baja el precio: baja el costo",
         stat="&minus;35%", stat_size=200,
         stat_label="cay&oacute; el valor de granja ecuatoriano entre 2015 y 2024 (US$5,50 &rarr; 3,60/kg) mientras triplicaba su producci&oacute;n",
         body="Una granja baja su costo con gen&eacute;tica, densidad y alimento; una pesquer&iacute;a no puede pescar m&aacute;s barato. Cuando Ecuador baja el precio no resigna margen: traslada una ca&iacute;da de costo. Competir por precio es jugar en la cancha del otro.",
         fuente="FAO FishStat, valor de acuicultura 2015-2024"),

    dict(id="espana", tipo="dato",
         tema="ESPA&Ntilde;A",
         headline="La cuota se pierde hace una d&eacute;cada, no desde el conflicto gremial",
         stat="41 a 1<span class=\"arrow\">&rarr;</span>1,6 a 1", stat_size=112,
         stat_label="entero argentino contra entero ecuatoriano en el mercado espa&ntilde;ol: 2018 frente a 2025",
         body="Ecuador pas&oacute; del 14% al 49% del mercado espa&ntilde;ol de langostino congelado y cruz&oacute; a Argentina en 2020, cinco a&ntilde;os antes del conflicto. Argentina no se retir&oacute; de Espa&ntilde;a: dej&oacute; de crecer mientras el mercado crec&iacute;a.",
         fuente="EUMOFA CN8 2012-2025 &middot; aduanas de origen"),

    dict(id="aranceles", tipo="dato",
         tema="ARANCELES",
         headline="Por primera vez, las reglas juegan a favor",
         stat="10%", stat_size=210,
         stat_label="paga Argentina en EE.UU., el piso del esquema, contra ~17% de India. Es el &uacute;nico oferente grande sin antidumping",
         body="En la UE, el Acuerdo Interino Mercosur baj&oacute; el congelado de 12% a 9,6% en mayo de 2026, con cortes de 2,4 puntos por a&ntilde;o hasta 0% en 2030. Pero es ventana, no base estructural: el fallo de la Corte Suprema de febrero achic&oacute; la ventaja sobre India de ~47 a ~7 puntos en cinco meses.",
         fuente="Federal Register 2026-15181 &middot; DOUE UE-Mercosur"),

    dict(id="msc", tipo="dato",
         tema="EL SELLO",
         headline="El &uacute;nico langostino salvaje certificado que existe",
         stat="1-2%", stat_size=200,
         stat_label="de la exportaci&oacute;n va hoy a los mercados que pagan por el sello MSC. La llave existe; la puerta reci&eacute;n se entreabre",
         body="Certificado en dos etapas: costera de Chubut (abril 2025) y aguas nacionales (febrero 2026). Una granja de vannamei puede certificar ASC, nunca MSC-salvaje. Llevar el norte europeo del 2% al 10% de la exportaci&oacute;n mover&iacute;a US$15-30 millones al a&ntilde;o.",
         fuente="MSC &middot; base de comercio &middot; relevamiento propio"),

    dict(id="gondola", tipo="dato",
         tema="G&Oacute;NDOLA",
         headline="El sello ya lleg&oacute; al lineal, pero no cobra prima",
         stat="&euro;11,00<span class=\"vs\">vs</span>&euro;12,99", stat_size=110,
         stat_label="mismo calibre en La Sirena: langostino argentino MSC contra vannamei de cultivo. El salvaje cuesta 18% menos",
         body="En agosto de 2026 la cadena vend&iacute;a cinco productos de gamb&oacute;n argentino rotulados MSC. Pero donde compiten calibre a calibre, el atributo salvaje no cobra una prima sistem&aacute;tica: el posicionamiento depende de la cadena y del calibre.",
         fuente="relevamiento propio de g&oacute;ndola, 2026-08-04"),

    dict(id="cierre", tipo="cierre",
         kicker="LA CONCLUSI&Oacute;N",
         titulo="El valor no est&aacute;<br>en el precio.",
         lead="Un producto salvaje de nicho, sobre una base productiva que se achica, compitiendo contra una marea de cultivo. Lo que queda del lado argentino es el atributo que el cultivo no puede replicar: <strong>salvaje, calibre grande, origen identificable</strong>.",
         cta="Estudio completo disponible &middot; Axia Consultora",
         fuente=""),
]

# --- Selección publicada -------------------------------------------------
# El carrusel usa sólo estos ocho. Los cinco restantes quedan en BANCO:
# para sumarlos, agregar su id acá y volver a correr generar_placas.py.
#   Disponibles sin usar: origen (99,5%), valor_kilo ($7,0 vs $4,8),
#   flotas (2,15x), aranceles (10%), gondola (11,00 vs 12,99 euros).
SELECCION = [
    "portada",
    "punto_partida",   # x34  . el rival es 34 veces más grande
    "eeuu",            # 69%  . el gancho
    "peru",            # 34%  . la prueba del anterior
    "ecuador",         # -35% . por qué no se puede competir por precio
    "espana",          # 41 a 1 -> 1,6 a 1 . la consecuencia medible
    "msc",             # 1-2% . la palanca que queda
    "cierre",
]

_POR_ID = {d["id"]: d for d in BANCO}
SLIDES = [_POR_ID[k] for k in SELECCION]
