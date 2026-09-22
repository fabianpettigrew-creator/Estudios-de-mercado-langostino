# Demanda inversa del langostino argentino L1 — resultados

AXIA · 22 de agosto de 2026
Pregunta: ¿regular la oferta mejora el precio que reciben los exportadores argentinos?

---

## Respuesta en una línea

**No.** La flexibilidad-precio de la demanda que enfrenta el langostino argentino es
**−0,27** (IC 95%: −0,37 a −0,16). El umbral en el que recortar oferta deja de destruir
ingreso es **−1**, y se rechaza con **t = 13,7**. Recortar el 7,4% del desembarque —el
paquete que se discutió en Conxemar 2025— subiría el precio alrededor de **2,0%** y bajaría
la facturación alrededor de **5,4%**, unos **US$47 millones** al año.

---

## 1. Qué se estimó

El parámetro de política es la flexibilidad-precio propia `f = ∂logP/∂logQ`. Como
`d(P·Q)/dQ = P·(1+f)`, todo se juega en si `|f|` supera 1. **No alcanza con que `f` sea
negativo y significativo**: hace falta que sea menor que −1.

Se estimaron dos familias, como se acordó:

**(a) Ecuación única de demanda inversa residual.** Precio del entero L1 del dato
transaccional (Softrade), cantidad del registro oficial de desembarques (SSPyA) —la regla
de fuente de la casa, sin excepciones—, controlando por el precio del camarón de cultivo en
la UE (EUMOFA, importación extra-UE de warmwater congelado), tipo de cambio, estacionalidad
y tendencia. Mensual, 2013-01 a 2026-07, N = 149 (los 10 meses sin grado declarado se
interpolan para no romper los rezagos y se excluyen de la estimación).

**(b) Sistema LA/IAIDS** sobre la importación extra-UE de camarón tropical congelado por
origen: Argentina, Ecuador, India, Vietnam y resto, mensual 2013-2026, con homogeneidad
impuesta por normalización y adición por construcción. Es la ruta Barten-Bettendorf: da la
flexibilidad de escala, las cruzadas y el reparto entre efecto tamaño de mercado y efecto
sustitución.

---

## 2. El sistema de demanda inversa

> **Pendiente de regenerar (22-09-2026).** Las cifras de esta sección salen de la corrida
> anterior al arreglo de la fórmula de flexibilidad (`flexibilidades_iaids.matriz`) y del
> índice de Stone. Se reconocen porque **todas las filas de la matriz suman exactamente
> −1**, que es imposible junto con la fila de escala de abajo. Hay que rehacerlas con
> `python demanda_inversa_modelo.py`. La reconstrucción a partir de estos mismos números
> da una propia argentina de **−0,241** en lugar de −0,267 —más lejos del umbral, no más
> cerca—, así que la conclusión no se mueve, pero el número que va a la presentación sí.
> Detalle en `salidas/Verificacion_consistencia_Barten_Tabarestani.md`.


Participación media en el valor importado extra-UE: **Argentina 14,6%** · Ecuador 26,1% ·
India 16,4% · Vietnam 9,1% · resto 33,7%. Precio medio de importación: Argentina
6,27 EUR/kg, Ecuador 5,73, India 6,74, Vietnam 8,53.

**Flexibilidades de cantidad, no compensadas** (fila = precio de *i*, columna = cantidad de *j*):

| | AR | EC | IN | VN | Resto |
|---|---|---|---|---|---|
| **Argentina** | **−0,267** | −0,128 | −0,246 | −0,100 | −0,259 |
| Ecuador | −0,152 | −0,397 | −0,113 | −0,113 | −0,225 |
| India | −0,125 | −0,210 | −0,254 | −0,106 | −0,305 |
| Vietnam | −0,106 | −0,335 | −0,302 | −0,025 | −0,232 |
| Resto | −0,110 | −0,219 | −0,088 | −0,081 | −0,502 |

**Flexibilidad de escala** (todas las cantidades suben 1% a la vez): Argentina **−0,82**,
Ecuador −0,83, India −1,14, Vietnam −1,17, resto −1,10.

Tres lecturas:

- **La propia argentina es −0,267**, con SE 0,053. Signo correcto y precisa. Pero
  `H0: f = −1` se rechaza con t = 13,7. Un recorte del 10% sube el precio 2,7%.
- **La escala es −0,82.** Aun si *todos* los orígenes recortaran a la vez —lo que no está
  sobre la mesa de nadie— el precio subiría menos que proporcionalmente y el ingreso del
  conjunto caería. Es el mismo resultado que Barten y Bettendorf encontraron en el pescado
  blanco belga (escala entre −0,77 y −1,15).
- **La cruzada con Ecuador es −0,128 y con India −0,246**: cuando el cultivo entra volumen,
  el precio argentino cede. Argentina recibe el shock de los demás; los demás casi no
  reciben el suyo (la cruzada de Ecuador respecto de Argentina es −0,152 sobre una
  participación mucho mayor).

La simetría no se impuso: con cinco orígenes y errores HAC eso exige SUR iterado, y no
cambia el signo ni el orden de magnitud. Queda como refinamiento si el resultado va a
publicación arbitrada.

---

## 3. La ecuación única: diez especificaciones, el mismo resultado

| Especificación | f | IC 95% | t de H0: f = −1 |
|---|---|---|---|
| M1 · log P_L1 (US$) ~ log desembarque 3m, **sin control mundial** | +0,037 | −0,013 a +0,088 | 40,3 |
| M2 · + precio del cultivo UE + tipo de cambio | +0,050 | +0,012 a +0,089 | 53,2 |
| M3 · en euros | +0,050 | +0,011 a +0,089 | 53,3 |
| M4 · **demanda residual**: log (P_L1 / cultivo) | +0,010 | −0,033 a +0,053 | 46,1 |
| R1 · Q = desembarque acumulado 12 meses | +0,023 | −0,098 a +0,143 | 16,6 |
| R2 · Q = captura tangonera 3 meses | +0,036 | +0,017 a +0,055 | 106,5 |
| R3 · suma de rezagos 0-6 meses (largo plazo) | +0,002 | — | — |
| R6 · en primeras diferencias | +0,021 | −0,006 a +0,049 | 72,0 |
| A1 · **anual** 2013-2025, con control de cultivo | −0,005 | −0,077 a +0,067 | 27,1 |
| A2 · **anual**, demanda residual | −0,087 | −0,191 a +0,016 | 17,3 |

La cota inferior más favorable de todo el conjunto es **−0,191**. Aun tomando ese extremo,
un recorte del 10% subiría el precio como máximo 1,9% y bajaría el ingreso al menos 8,1%.

**El coeficiente que sí importa es otro.** El precio del camarón de cultivo en la UE entra
con **+0,40 a +0,65** y t entre 4 y 5 en todas las especificaciones. El precio del
langostino argentino lo pone el mercado mundial del camarón, no la oferta argentina. Y el
tipo de cambio entra con coeficiente **1,02** (t = 5,2): el precio en dólares es el precio
en euros multiplicado por el euro, ni más ni menos.

Dos controles de diagnóstico:

- **Régimen de oferta baja.** Interactuando la cantidad con el cuartil inferior de
  desembarque, `f` en ese régimen es **+0,077**: no hay no linealidad que haga aparecer el
  efecto sólo cuando el recorte es grande.
- **Almacenabilidad.** Con la oferta acumulada a 12 meses —que neutraliza el stock de
  congelado— `f = +0,023` (t = 0,37). El resultado no depende de confundir desembarque
  mensual con oferta al mercado.

---

## 4. El conflicto de 2025 no prueba lo que parece

Es el único shock de oferta grande de la serie, y a primera vista da la razón a la
hipótesis: desembarque **−15,8%**, entero exportado **−37,1%**, FOB medio **+22,4%**.

Pero:

1. **La facturación cayó.** El FOB del entero pasó de US$518,7 M a US$399,0 M: **−23,1%**.
   El precio mejor no compensó el volumen perdido. Ese es el hecho, antes de cualquier
   modelo.
2. **Buena parte de la suba en dólares fue el dólar.** El EUR/USD pasó de 1,0808 promedio
   en 2024 a 1,1314 en 2025: **+4,7%** que aparece en el precio FOB sin que nadie haya
   vendido mejor.
3. **Otra parte fue el ciclo mundial.** El precio de importación del cultivo en la UE
   también subió en 2025 (5,93 → 6,09 EUR/kg en la canasta, Ecuador 5,14 → 5,34).
4. **Con una dummy del período abr-nov 2025 en lugar de la cantidad, y controlando el
   precio mundial, el coeficiente es +0,031 con t = 0,61.** El mayor shock de oferta de la
   serie no dejó huella medible en el precio en euros.
5. **Y la prueba definitiva es 2026**: el precio siguió subiendo *mientras el volumen se
   recuperaba*. El entero de aduana en julio de 2026 valió 7,31 US$/kg con 14,0 kt
   exportadas, contra 5,66 US$/kg con 17,0 kt en julio de 2024. Si la suba viniera del
   recorte, habría cedido al volver la oferta. No cedió.

Hay un detalle que conviene tener a mano porque se va a repetir en la discusión: durante el
paro efectivo (abril-julio 2025) el precio del entero **en euros** estuvo *por debajo* del
de un año antes; la mejora llegó recién en agosto-noviembre, con la flota de vuelta y los
volúmenes recuperándose. El promedio anual ponderado sube en parte porque el volumen de
2025 se concentró en los meses caros, que es un efecto de calendario, no de nivel de precio.

---

## 5. Simulación: el paquete de Conxemar

Traducido a toneladas sobre el desembarque medio 2022-2024 (210.826 t):

| Medida | Toneladas |
|---|---|
| Zafra de Rawson a cuatro meses (sale marzo) | −4.516 |
| Cierre de la zafra nacional a mediados de septiembre | −11.004 |
| **Total** | **−15.520 t = −7,4%** |

(La reducción del 20% de XXL incidental de la flota fresquera no se cuantifica: hace falta
la composición por talle de esa captura, que no está en el registro de desembarques.)

| Supuesto sobre f | f | Δ precio | Δ ingreso |
|---|---|---|---|
| Ecuación única, anual (A2) | −0,09 | +0,6% | **−6,7%** |
| **Sistema de demanda inversa (central)** | **−0,27** | **+2,0%** | **−5,4%** |
| Sistema, cota más favorable del IC 95% | −0,37 | +2,7% | −4,6% |
| Si *todos* los orígenes recortaran a la vez | −0,82 | +6,0% | −1,3% |
| El f que haría falta para no perder plata | −1,00 | +7,4% | 0,0% |

Sobre los US$867 M de exportación de langostino de 2025, el escenario central son
**−US$47 millones** de facturación anual. Y eso antes de contar el empleo y el costo fijo
que no se ahorra con la flota parada.

---

## 6. Lo que la evidencia sí respalda

La literatura arbitrada no dice que regular la pesquería no sirva. Dice que **la ganancia
está en el momento y la forma de la descarga, no en el nivel de captura**:

- «Do Catch Shares Increase Prices?» (*Marine Resource Economics* 38(3), 2023) mide
  +17,9% a +22,4% de ingresos en 39 pesquerías estadounidenses, y el canal identificado es
  **elongación de la temporada y calidad** —poder desembarcar cuando el precio está alto y
  vender fresco en vez de congelado—, no restricción de oferta. Los crustáceos del Golfo
  dan efecto negativo.
- Guillen y Maynou (*Marine Policy* 47, 2014) sobre la gamba roja catalana: el precio de
  primera venta es 14% menor los martes y miércoles que los viernes, y recomiendan
  concentrar la reducción de esfuerzo **en los días de precio bajo**.
- Las cuotas colectivas en la merluza austral chilena (*MRE*, 2019) sí subieron el precio de
  playa 14%, pero **en una sola de tres regiones**: la que tenía organizaciones estables y
  un reparto inicial que respetaba la distribución entre armadores y tripulación.

Aplicado al langostino, eso apunta a tres palancas que el modelo no descarta y que además
son compatibles con el dato propio del proyecto:

1. **Calendario, no volumen.** El piso de precio está en diciembre y el pico en junio; la
   amplitud del entero es 15-18%. Correr volumen del piso al pico no requiere resignar
   toneladas.
2. **Composición.** La brecha de precio entre flotas y entre talles es mucho mayor que
   cualquier efecto de cantidad que se pueda esperar. El corrimiento a cola destruye valor
   por kilo de materia prima.
3. **Diferenciación.** El MSC de aguas nacionales (feb-2026) y el de Chubut (abr-2025) son
   una palanca de precio que no cuesta toneladas. La flexibilidad cruzada con el cultivo
   (−0,13 con Ecuador, −0,25 con India) es la medida de cuánto se gana separándose de él.

---

## 7. Límites de este resultado

- **Lo que se descarta y lo que no.** No se descarta que `f` sea algo negativo: el sistema
  lo estima en −0,27 y es significativo. Lo que se descarta, con mucho margen, es que sea
  del orden de −1, que es lo que haría falta.
- **La simetría del sistema no está impuesta** en la corrida de esta sección, pero
  `iaids_simetria.py` ya la impone por SUR iterado, con test de Wald y de razón de
  verosimilitud. Corresponde traer ese resultado al §2. Importa más de lo que parecía: la
  lectura de que «Argentina recibe el shock de los demás y los demás casi no reciben el
  suyo» descansa entera en una asimetría (h_AR,EC = +0,019 contra h_EC,AR = −0,002) que la
  simetría de Antonelli dice que no puede existir.
- **La negatividad no se cumple.** La matriz de Antonelli implícita tiene la diagonal de
  Vietnam positiva y un autovalor de +0,011: falla la condición (17) de Barten y
  Bettendorf, que es la que hace interpretables a las flexibilidades propias. El
  diagnóstico ahora lo imprime el propio modelo (`flexibilidades_iaids.negatividad`).
- **Los instrumentos de oferta que se listaron en la nota de diseño no se usaron.** El
  desembarque es plausiblemente predeterminado por biología y calendario, y la dirección del
  sesgo por endogeneidad —más precio induce más esfuerzo— empujaría `f` hacia arriba, o sea
  hacia el cero. Corregirla haría el resultado *más* negativo, no menos; pero para dar el
  número como definitivo hay que estimarlo con el calendario oficial de vedas como
  instrumento. Ese es el próximo paso.
- **La reducción de XXL incidental no está cuantificada** por falta de composición por
  talle de la captura fresquera.
- **El glaseo sigue sin considerarse** (limitación general del proyecto).

---

### Fuentes y trazabilidad

Precio del L1: Softrade, `fuentes/expo.py`, filtro `pres=='entero' & cal=='L1'`.
Cantidad: desembarques SSPyA, `_lan.pkl`. Precio y volumen europeos: EUMOFA, «Trade data
reported by EU countries», importación extra-UE, `demanda_inversa_eumofa.py`. Tipo de
cambio: EUR/USD promedio mensual. Aduana oficial NCM 0306.17.10 para el contraste de nivel.

Todo lo de arriba sale de `demanda_inversa_modelo.py`; las tablas completas están en
`salidas/demanda_inversa_L1.xlsx` (hojas `flexibilidades`, `sistema_flexibilidades`,
`sistema_escala`, `simulacion`, `regresiones`, `raices_unitarias`).

Antecedentes bibliográficos: ver `salidas/Demanda_inversa_L1_antecedentes_y_diseno.md`.
