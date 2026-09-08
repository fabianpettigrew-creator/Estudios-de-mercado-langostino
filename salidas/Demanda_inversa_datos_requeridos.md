# Qué datos faltan para mejorar las estimaciones

AXIA · 23 de agosto de 2026 · reemplaza la versión anterior del mismo día · actualizado el 2 de septiembre de 2026 con el resultado del CFP

La lista se acortó de seis puntos a tres. Salieron dos por decisión de alcance —el costo
evitable del buque y el bloque de controles de composición, que no tienen fuente— y uno se
resolvió con el dato que ya está en la carpeta, sin pedirle nada a nadie: la composición por
talla. Queda lo que sigue, con la medición que justifica cada punto.

---

## 1. La composición por talla: resuelta adentro, no se pide

El problema era real: el modelo cruzaba el precio del **L1** con la captura **total** de la
flota tangonera, y el peso del L1 dentro del entero congelado a bordo se mueve entre 61,7% y
82,8% según la campaña. Esa variación entraba al modelo como si fuera cantidad.

**La salida no era pedir la composición del desembarque, era ampliar el producto.** El
congelado a bordo es producto final: lo que la flota desembarca es exactamente lo que exporta,
sin reproceso en tierra. Entonces la composición por talla del desembarque **ya está observada
en el despacho de exportación**. Y tomando L1 y L2 juntos se cubre casi todo:

| Talla | Kilos de entero a bordo, 2013-2026 | Participación |
|---|---|---|
| L1 | 719,9 kt | 72,9% |
| L2 | 214,8 kt | 21,7% |
| L3 | 37,2 kt | 3,8% |
| L4 y L5 | 1,9 kt | 0,2% |
| Sin declarar | 14,1 kt | 1,4% |
| **L1 + L2** | **934,7 kt** | **94,6%** |

Al agregarlas, la mezcla deja de moverse:

| | Rango entre campañas | Desvío estándar |
|---|---|---|
| Participación del L1 solo | 61,7% – 82,8% | 7,3 puntos |
| Participación del L1+L2 | 88,2% – 97,7% | **2,9 puntos** |

Y las dos tallas se comportan como un solo producto: el L2 cotiza **6,0% por debajo** del L1,
la correlación mensual de los dos precios en logaritmos es **0,852** y la elasticidad del precio
del L2 al del L1 es **+0,867** (error estándar 0,058). No son dos mercados, es uno.

**Lo que cambia en el resultado: casi nada, y ése es el punto.**

| Especificación | L1 solo | L1+L2, valor unitario | L1+L2, peso fijo |
|---|---|---|---|
| Mensual, MCO sobre precio relativo | −0,151 | −0,163 | −0,123 |
| Mensual, IV con la ventana del conflicto | −0,184 | −0,219 | −0,116 |
| Campaña, con tendencia | −0,192 | −0,196 | −0,196 |

Las tres construcciones de campaña dan lo mismo hasta el tercer decimal. Agregando además el
share de L2 como control explícito, entra con coeficiente −0,43 y t = −1,54 —no
significativo— y la flexibilidad queda en −0,208. El *leave-one-out* del agregado se mueve
entre −0,112 y −0,254.

**Conclusión.** El agregado L1+L2 es la unidad correcta de análisis, elimina el error de
medición por mezcla de tallas y confirma el resultado en vez de cambiarlo. **Este punto sale de
la lista de pedidos.** Queda una salvedad de nomenclatura que conviene chequear: en nuestra
lectura del nomenclador, `NA01` = 11 a 20 piezas por kilo = L1, y sobre esa base el L1 es el
72,9% del entero de la flota congeladora y el L2 el 21,7%. Si en la mesa «L2» designa otro
rango, hay que reasignar la etiqueta —el agregado no cambia, la descripción sí.

*Único residuo abierto:* el índice de **peso fijo** —el que purga por completo la mezcla— da
una flexibilidad algo menor y pierde significatividad en la versión instrumental (−0,116, con
el intervalo cruzando el cero). No cambia la conclusión de política, pero conviene decirlo:
parte de la señal mensual viene de la mezcla, no sólo del nivel de precios.

---

## 2. Prioridad 1 — Existencias mensuales de congelado

Se sabía que faltaba. Ahora se sabe cuánto pesa. Comparando lo que se exporta en la ventana de
venta contra lo que se capturó en la campaña, sobre los años con volumen confiable:

| Campaña | Captura abr-oct (t) | Entero a bordo exportado (t) | Exportado / capturado |
|---|---|---|---|
| 2020/2021 | 54.244 | 81.350 | **1,50** |
| 2021/2022 | 86.937 | 80.645 | 0,93 |
| 2022/2023 | 90.469 | 82.731 | 0,91 |
| 2023/2024 | 80.876 | 68.936 | 0,85 |
| 2024/2025 | 90.092 | 63.267 | **0,70** |
| 2025/2026 | 48.282 | 53.913 | 1,12 |

La razón se mueve entre **0,70 y 1,50**, con desvío de 0,28. En 2020/2021 se vendió una vez y
media lo pescado —se descargó el stock acumulado durante la pandemia— y en 2024/2025 se vendió
apenas siete décimos: se acumuló. Lo que llega al mercado no es lo que se pescó, y esa
diferencia es exactamente el error de medición de `Q`.

Que el producto sea final ayuda pero no alcanza: elimina el reproceso, no el almacenamiento.

**Qué se necesita.** Existencias mensuales de congelado —a bordo, en planta y en cámara de
terceros— por presentación y talla. Sin esto, el modelo mide la respuesta del precio al
*desembarque*, no a la *oferta*, que es la variable de política.

**Y hay un atajo parcial que ya podemos usar.** Desde 2020 el volumen del despacho es confiable
y el producto es final, así que los kilos exportados **son** la cantidad ofrecida. Sobre las
seis campañas disponibles, medir `Q` sobre el producto exportado en vez de sobre la captura
lleva la flexibilidad de −0,341 a −0,472. Son seis puntos: es un contraste de orden de
magnitud, no una estimación. Pero apunta en la dirección esperada —el sesgo de medir la
cantidad equivocada atenúa `f` hacia cero— y se vuelve una estimación en regla apenas haya
existencias para cerrar la brecha en los años anteriores.

---

## 3. Prioridad 2 — La mitad de la tendencia que sigue sin explicar

Este punto se resolvió a medias con la exportación ecuatoriana, y conviene decir con precisión
qué quedó cerrado y qué no.

**Lo que se cerró.** El precio del L1 relativo al camarón de cultivo subía 2,13% por año contra
la canasta de EUMOFA, con t = 4,93 y cincuenta puntos de R². Buena parte de eso no era el
langostino subiendo sino el control bajando: Ecuador multiplicó por 5,6 su exportación entre
2013 y 2026 y reorientó la mitad del volumen a China, donde coloca a 4,64 dólares por kilo
contra 6,19 en la Unión Europea. Ese caudal de talla chica y precio bajo hunde la canasta más
rápido de lo que arrastra al langostino salvaje.

| Referencia del competidor | Tendencia | f (IV), con tendencia |
|---|---|---|
| Canasta EUMOFA (el control anterior) | +2,13%/año (t = 4,93) | −0,219 |
| Ecuador a España, Italia y Francia | −0,14% (t = −0,21) | −0,257 |
| **España contra España — la limpia** | **+1,11%/año (t = 2,43)** | **−0,188** |

**Lo que queda abierto.** Contra el camarón ecuatoriano embarcado a España —mismo mercado, mismo
mes— la prima sigue subiendo **1,11% por año**, la mitad de lo que marcaba EUMOFA pero
significativo. Esa mitad es real y no tiene explicación. Dos candidatos:

1. **Certificación MSC**: fecha de certificación por pesquería y subárea, y participación
   certificada en el volumen exportado, campaña por campaña. La campaña 2025/2026 es la primera
   que rompe la paridad con el cultivo y coincide con el MSC de aguas nacionales de febrero de
   2026, no con el conflicto.
2. **El relevamiento propio de góndola.** Si la prima se ensanchó en el mostrador y no sólo en
   aduana, es de demanda y no de mezcla. Es el único que ya está en la carpeta.

**Y un pedido nuevo que salió de todo esto: precio del competidor por calibre.** El control
ecuatoriano empareja mercado y presentación, no talla. Con los despachos de Ecuador a España se
pudo medir el gradiente —la elasticidad del precio a las piezas por kilo es −0,254, con t =
−8,54 sobre 597 despachos— pero no armar una serie: la talla aparece en la descripción comercial
de apenas el 3,4% de los kilos y la cobertura se desploma después de 2021. Hace falta el precio
europeo de importación por rango de calibre. La cuenta que habilitaría: Ecuador embarca a España
52 piezas por kilo y el L1 argentino son 11 a 20 —3,4 veces más grande—, así que ajustado por
talla el L1 estaría vendiéndose con un descuento del orden del 21% contra producto comparable.

**Y hay un problema de unidad que condiciona todo lo anterior.** Ninguna fila declara si el
conteo va por kilo o por libra, y en la misma serie conviven las dos convenciones: el 93,7% de
los kilos está en bandas de decena —20/30 a 80/100, la forma europea, por kilo—, el 4,8% en la
escalera estándar de Estados Unidos —16/20, 21/25 hasta 71/90, que se cuenta por libra— y el
1,5% en bandas irregulares con errores de tipeo visibles. El gradiente de arriba se estima sólo
sobre las bandas de decena, que es la lectura que no obliga a decidir; leyendo todo como por
kilo daría −0,277 y un descuento del 23%, y convirtiendo la escalera a piezas por kilo, −0,112 y
6%. El descuento va de 6% a 23% según cómo se lean 108 filas. Así que al pedido de precio por
calibre hay que sumarle la unidad del conteo y la presentación —HOSO o HLSO—, que tampoco viene
declarada en ninguna fila. Los dos están en «Pedido_a_Softrade.md».

---

## 4. Prioridad 3 — Instrumentos de oferta para todos los años

Hoy toda la identificación causal cuelga de **un solo episodio**: la ventana del conflicto de
2025. La primera etapa es fuerte (F = 61,1), pero es un instrumento, un año.

1. **Precio mensual del gasoil marino y retenciones vigentes mes a mes.** Es un desplazador
   de costo: mueve cuánto sale a pescar la flota sin que el recurso ni el comprador intervengan.
   De la lista original es el único que no puede ser síntoma del estado del recurso. Fuente
   pública, serie larga.
2. **Paros y conflictos gremiales fechados, 2013-2026.** Más de lo mismo que ya
   identifica: si hubo episodios menores en otros años, el conflicto de 2025 deja de ser un
   shock aislado y pasa a ser una serie.

   **El método que sirve no es buscar la palabra en un texto sino la anomalía en la serie.**
   Comparando cada mes contra la mediana histórica de ese mismo mes calendario aparecen cinco
   meses de zafra con desembarque tangonero por debajo del 35% de lo normal que no son el
   episodio de 2025:

   | Mes | Tangonera (t) | Mediana del mes | Ratio | Qué es |
   |---|---|---|---|---|
   | 2024-10 | 0 | 12.961 | 0,00 | hueco entre zafras, no conflicto |
   | 2020-06 | 172 | 13.367 | 0,01 | coincide con el pozo del canal |
   | 2020-07 | 900 | 18.712 | 0,05 | coincide con el pozo del canal |
   | 2026-08 | 2.378 | 19.114 | 0,12 | último mes, posible dato parcial |
   | 2022-10 | 4.220 | 12.961 | 0,33 | la zafra se corrió: octubre se vació |

   Octubre de 2024 cae entre el cierre de la zafra en la zona de veda de juveniles, el 19 de
   septiembre, y la apertura de Rawson, el 2 de noviembre. Los dos meses de 2020 están
   contaminados por el shock de demanda, que es justo del que el modelo se cuida.

   **Y octubre de 2022 no es un episodio sino una tendencia.** La zafra nacional se corrió
   hacia adelante: el desembarque tangonero de octubre a diciembre pasó del 25% del año en
   2016-2018 al 5-7% en 2021-2023 y a cero en 2024, mientras el total anual no cayó en esa
   proporción. El último mes con más de mil toneladas se movió de noviembre a septiembre. La
   serie de octubre lo dice sola: 21.853 t en 2018, 16.996 en 2019, 10.724 en 2020, 6.157 en
   2021, 4.220 en 2022. El IPI pesquero de INDEC —grupo crustáceos— dibuja la misma bajada.

   **Advertencia de método, para la próxima detección.** Comparar cada mes contra la mediana
   de catorce años hace que un desplazamiento estructural del calendario aparezca como si
   fuera un evento: la mediana de octubre está dominada por 2016-2019, cuando octubre todavía
   era mes de pesca. Un detector que sirva tiene que comparar contra el nivel reciente del
   mismo mes, no contra la mediana de toda la serie.

   **Las actas del CFP sí aportan, por una vía que no era la esperada.** Los conflictos no
   aparecen como decisión del Consejo sino dentro de los expedientes de justificación de
   inactividad comercial, con fechas documentadas. El texto completo de las 547 da veinte
   menciones en catorce actas, y de ahí quedan fechados: el conflicto de 2012 (marzo a agosto,
   fuera de la muestra), huelgas en marzo y abril de 2019, un paro de 76 días entre el 30 de
   agosto y el 16 de noviembre de 2023, y un conflicto de la flota de Rawson desde marzo de
   2024. Son de buque y en su mayoría de la flota merlucera, así que hay que cruzarlos contra
   el desembarque tangonero antes de darlos por shocks de oferta del langostino. Hecho el
   cruce, sólo octubre de 2023 muestra caída, al 45% de su mediana.

   **La prensa sectorial acota el resultado.** Confirma 2025 como el único paro que amarró la
   flota tangonera entera —113 barcos desde el 17 de marzo— y no registra otro equivalente
   entre 2013 y 2024: la paritaria de 2018 cerró con acuerdo y los conflictos de 2023 y 2024
   son de la flota amarilla de Rawson, que es fresquera.
3. **Días de puerto cerrado por Prefectura y días no operables por clima.** Exógenos y
   mensuales: nadie cierra el puerto mirando el precio del langostino.
4. **Esfuerzo efectivo mensual: buques tangoneros activos y días de pesca.** Baja de
   instrumento a control. Responde al precio, así que no sirve para identificar; sí para
   absorber variación.

Con un desplazador de costo o de días de mar hay variación exógena todos los años en vez de en
uno. El sesgo que corrige —más precio induce más esfuerzo— empuja f hacia cero, así que el
número esperado es más negativo, no menos.

**Lo que ya se obtuvo y se probó, y no resolvió el problema.** Las actas del CFP se descargaron íntegras —547, 2013-2026— y se leyeron: 165 decisiones
resolutivas de oferta, 55 con fecha de vigencia. Construido el instrumento como suma móvil de
doce meses de decisiones, la primera etapa es nula en los cierres (F = 0,0) e invertida en las
aperturas (t = −6,7 con los eventos de fecha propia): más decisiones de apertura, menos captura.
Combinado con la ventana del conflicto, el test de Hansen rechaza con p = 0,000. La razón está
en las propias actas —el Acta 37/2013 dice que la caída de la CPUE «obliga a evaluar un
cierre»—: el Consejo decide siguiendo al recurso, que es lo mismo que mueve el precio. No es un
desplazador exógeno. Detalle en la sección 9.6 del anexo metodológico e «iv_cfp.xlsx». Los
índices de biomasa del INIDEP se obtuvieron del repositorio institucional en dos tramos que no
encadenan: 2013-2019 sobre el sur del Golfo San Jorge (17 a 30 kt) y 2020-2025 sobre el área
total evaluada (73 a 99 kt), sin informe de biomasa en 2014-2016, período en que el propio
INIDEP señaló que la interpretación del índice había cambiado de naturaleza. Son anuales, así
que no identifican un modelo mensual; quedan como control, no incorporados todavía.

*(La captura rezagada se probó como instrumento y no sirve, F = 0,1; el calendario del CFP, tampoco, ver arriba. El langostino tiene
reemplazo casi total de ejemplares entre campañas, según el INIDEP, así que un año no informa
sobre el siguiente.)*

---

## Resumen

| # | Qué | A quién | Qué cambia |
|---|---|---|---|
| 1 | Existencias mensuales de congelado, por presentación y talla | Empresas / cámara | Hoy la oferta que llega al mercado difiere de la captura entre −30% y +50% |
| 2 | MSC por campaña · góndola · precio del competidor por calibre, con su unidad de conteo | Mixto (uno ya está en la carpeta) | La mitad de la tendencia era el control; falta explicar la otra mitad, 1,11% por año |
| 3 | Gasoil y retenciones · paros fechados · puerto cerrado · esfuerzo como control | Energía, cámaras y actas, Prefectura, SSPyA | un instrumento ajeno al recurso; el CFP se probó y no lo es |

Y un pendiente que no es de dato sino de método: **imponer simetría al sistema IAIDS** por SUR
iterado. Hoy el sistema se estima ecuación por ecuación. Es un refinamiento a hacer si el
trabajo va a arbitraje.

---

### Lo que salió de la lista, y por qué

- **Composición por talla de la captura.** Resuelta con el dato propio: el agregado L1+L2 cubre
  el 94,6% del producto de la flota, la mezcla se aquieta y la flexibilidad no cambia.
- **Costo evitable del buque tangonero.** Fuera del alcance del análisis por decisión de AXIA.
- **Controles de composición** —razón social del exportador, spot contra contrato, rendimientos
  reales, condición de venta de 2023—. No hay datos.
- **Índice mensual de actividad HORECA.** Construido y en el modelo desde ayer.
- **Marca de flota antes de 2018.** Recuperada de la prosa del despacho; la serie arranca en 2013.
- **Tramos sin descripción de 2016 y 2017.** Limitación del registro de origen, no se pueden
  recuperar. Cubiertos por el proxy de temporada.
- **Porcentaje de glaseo.** Dos menciones en cuarenta y siete mil despachos, y el nomenclador
  oficial confirma que no existe sufijo para declararlo. Tiene que venir de la industria.
- **Las actas del CFP como instrumento.** Obtenidas y probadas: F = 0,0 en cierres, signo invertido en aperturas, Hansen p = 0,000. El Consejo decide siguiendo al recurso. Ver 9.6 del anexo e `iv_cfp.xlsx`.
- **La captura rezagada como instrumento.** F = 0,1, por la biología de la especie.
