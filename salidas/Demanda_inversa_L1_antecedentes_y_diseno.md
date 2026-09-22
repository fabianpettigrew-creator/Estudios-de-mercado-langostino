# Demanda inversa del langostino argentino L1

## Antecedentes, diagnóstico del dato y diseño del modelo

AXIA · nota de método · 22 de agosto de 2026
Objetivo del encargo: estimar `P = f(Q)` para el L1 argentino y evaluar si regular la
oferta mejora el ingreso de los exportadores.

---

## 1. Por qué demanda inversa, y qué se estima exactamente

La forma inversa no es una preferencia de estilo: en pesca la cantidad llega al mercado
predeterminada por la biología, la flota y el calendario regulatorio, y el precio es el que
ajusta. Es el argumento fundacional de **Barten y Bettendorf (1989)**, que estimaron un
sistema Rotterdam inverso sobre ocho especies de pescado blanco en puertos belgas (169
meses de serie, dic-1973 a dic-1987; 168 observaciones en diferencias): *«los operadores fijan los precios en función de las
cantidades; la causalidad va de la cantidad al precio»*.

El parámetro de interés es la **flexibilidad-precio propia**

    f = ∂ log P / ∂ log Q

y el umbral de política es **|f| = 1**:

| Si… | Un recorte de oferta… | Porque |
|---|---|---|
| \|f\| > 1 | **sube** el ingreso total | el precio sube más que proporcionalmente |
| \|f\| < 1 | **baja** el ingreso total | el precio no compensa el volumen perdido |

Formalmente, `d(P·Q)/dQ = P·(1 + f)`. Todo el encargo se reduce a estimar `f` con un
intervalo de confianza y ver de qué lado del −1 cae. **No alcanza con que `f` sea negativo
y significativo.**

El antecedente no es alentador: Barten y Bettendorf reportan flexibilidades propias
compensadas de **−0,09 a −0,37** (la raya el mayor, gallineta el menor) y una flexibilidad
de escala cercana a **−1,0**. Cuidado con comparar ese rango contra el umbral: son
elasticidades de sustitución propia *compensadas*, y lo que se contrasta acá es una
flexibilidad *no compensada*. El objeto comparable es `h_i + h_ii/w_i`, que en su cuadro 2
va de **−0,11** (gallineta) a **−0,57** (lenguado, el 47% del valor y el análogo más cercano
a la posición del L1 en su nicho). Sigue muy por encima de −1, que es lo que importa. Con esos órdenes de magnitud, restringir la oferta de una
especie destruye ingreso. La pregunta abierta es si el L1 argentino, que es un nicho
diferenciado y no un pescado blanco genérico, se comporta distinto.

---

## 2. Antecedentes en fuentes arbitradas

### 2.1 Metodología: la familia de sistemas de demanda inversa

- **Barten, A.P. y Bettendorf, L.J. (1989)**, «Price formation of fish: An application of an
  inverse demand system», *European Economic Review* 33(8). Rotterdam inversa. Es la
  referencia obligada y la que ya cita el `pronostico.py` del proyecto.
- **Holt y Bishop; Eales y Unnevehr** — familia del **AIDS inverso (IAIDS)** y su versión
  lineal aproximada. Permite imponer y testear homogeneidad y simetría, y descomponer el
  efecto en escala (volumen total del mercado) y sustitución (composición).
- **Modeling Inverse Demands for Fish: Empirical Welfare Measurement in Gulf and South
  Atlantic Fisheries**, *Marine Resource Economics* 19(3), 2004. Uso del sistema inverso para
  medir bienestar ante cambios de captura: exactamente el ejercicio de política que acá
  interesa.
- **An Inverse Demand System for the Differentiated Blue Crab Market in Chesapeake Bay**,
  *MRE* 30(2), 2015, y su versión en dos etapas (*Welfare Analysis in a Two-Stage Inverse
  Demand Model*). Producto **diferenciado por calibre y presentación** — el análogo más
  cercano a la estructura L1-L5 / entero-cola.
- **Testing Structural Changes in the U.S. Whitefish Import Market: An Inverse Demand System
  Approach**, *Agricultural and Resource Economics Review*. Aplicación a un mercado de
  **importación por origen**, que es el formato natural para modelar España e Italia.
- **A semiflexible normalized quadratic inverse demand system** — alternativa funcional
  cuando la Rotterdam inversa impone demasiado.

### 2.2 Camarón específicamente

- **Tabarestani, Keithly y Marzoughi-Ardakani (2017)**, «An Analysis of the US Shrimp Market:
  A Mixed Demand Approach», *MRE* 32(4). El más pertinente al caso argentino: tratan los
  **desembarques salvajes del Golfo como cantidad predeterminada** (forma inversa) y los
  **precios de las importaciones de cultivo como predeterminados** (forma directa), en un
  sistema de **demanda mixta**. Resultado: un cambio simultáneo de 1% en **todos** los
  precios de importación mueve 0,98% el precio doméstico. La palabra «todos» es la que hace
  útil a la cita: para un origen solo los números son otros y apuntan al mismo lado —
  Tailandia, con más del 35% del volumen importado, tiene una flexibilidad precio-precio de
  apenas **0,02**, porque cuando sube su precio los otros siete orígenes amortiguan casi
  todo el ajuste. Es decir, el salvaje casi no tiene autonomía de precio frente al
  cultivo. Si eso vale para el L1 frente al vannamei, la palanca de la oferta argentina es
  débil por construcción.
- **Price flexibility and international shrimp supply** — flexibilidades de precio del
  camarón en el comercio internacional.
- **U.S. Shrimp Market Integration** (*MRE* 27(2), 2012) y **Market Integration of Cold and
  Warmwater Shrimp in Europe** (*MRE* 32(4), 2017). Definen si el salvaje y el de cultivo son
  el mismo mercado. **Este test es previo al modelo**: si el L1 está integrado con el
  vannamei, la demanda relevante no es la del langostino argentino sino la del camarón, y la
  flexibilidad propia colapsa. El proyecto ya tiene un resultado propio en esa dirección —
  el FOB del L1 **no cointegra con el vannamei** y el premium es cíclico (1,34-1,77×) sin
  tendencia —, lo que sugiere separación de mercados y deja lugar para un efecto propio.
- **Guillen, J. y Maynou, F. (2014)**, «Importance of temporal and spatial factors in the
  ex-vessel price formation for red shrimp and management implications», *Marine Policy* 47.
  Gamba roja (*Aristeus antennatus*), precios diarios de primera venta en puertos catalanes
  2000-2012, función hedónica. Encuentran que el precio es **14% menor los martes y
  miércoles** que los viernes y recomiendan que la reducción de esfuerzo se concentre
  justamente en los días de precio bajo, para minimizar el costo económico del recorte.
  Es el antecedente de **«dosificar cuándo», no «cuánto»**.

### 2.3 Regular la oferta para mejorar el precio: qué muestra la evidencia

- **Do Catch Shares Increase Prices? Evidence from US Fisheries**, *MRE* 38(3), 2023.
  Diferencias en diferencias más control sintético sobre 39 pesquerías estadounidenses con
  derechos de captura, 1990-2016. Efecto agregado **+17,9%** de los ingresos previos por el
  método DiD (IC 95%: US$17,2-59,4 M) y **+22,4%** por control sintético, pero **con evidencia
  mixta a nivel pesquería** (20 de 29 positivas en DiD; sólo 2 de 36 significativas y positivas
  en el control sintético). **El canal identificado no es la restricción de oferta: es la
  elongación de la temporada y la calidad** — poder desembarcar cuando el precio está alto y
  vender fresco en vez de congelado. Los crustáceos del Golfo, justamente, dan efecto
  negativo.
- **Collective Share Quotas and the Role of Fishermen's Organizations**, *MRE*, 2019
  (merluza austral chilena). Cuotas asignadas a organizaciones de pescadores en lugar de a
  individuos, con asambleas mensuales de negociación de precio. **Sólo una de tres regiones
  logró subir el precio de playa (+14%)**, y fue la que tenía organizaciones estables y un
  reparto inicial que respetaba la distribución tradicional entre armadores y tripulación.
  Donde la asignación generó conflicto distributivo, no hubo mejora de precio. La
  concentración de la demanda (exportadores e importadores mayoristas) limitó el poder de
  negociación en el resto.
- **Norges Råfisklag / Norges Sildesalgslag** (Noruega). El caso extremo institucional:
  organizaciones de venta de primera mano con **monopolio legal** y facultad de fijar precios
  mínimos y regular el flujo de desembarques. Muestran que el modelo existe y es legal en
  algún marco, pero **descansa en una ley específica**, no en un acuerdo privado entre
  exportadores.

**Síntesis de la evidencia**: donde hay mejoras de precio documentadas, vienen del
**momento y la forma** de la descarga (temporada más larga, más fresco, mejor calidad,
evitar el pico de oferta) mucho más que del **nivel** de captura. Y cuando vienen de
coordinación, requieren una institución con dientes y un reparto inicial que los
participantes acepten.

### 2.4 El precedente argentino, que ya está sobre la mesa

- **Conxemar 2025 (Vigo)**: CEOs del bloque tangonero discutieron abiertamente *dosificar el
  volumen* para sostener precios por encima de US$7/kg, con el langostino arriba de US$9 en
  ese momento. Las medidas concretas propuestas fueron **acortar la zafra de Rawson a cuatro
  meses**, eliminar la pesca al norte durante la veda, reducir 20% la captura incidental de
  XXL de la flota fresquera y cerrar la zafra nacional a mediados de septiembre.
- **Cuotificación (CITC)**: debate abierto sobre llevar al langostino al régimen de cuotas
  individuales transferibles que ya rige para la merluza, bajo la Ley Federal de Pesca
  24.922, con la asignación ponderada por historia de captura, empleo e inversión.

Es decir: el encargo no es hipotético, y el modelo tiene que poder pronunciarse sobre
medidas de este tipo específico, no sobre un recorte abstracto de toneladas.

---

## 3. Diagnóstico del dato: por qué no se puede estimar esto ingenuamente

Corrida exploratoria sobre la serie que ya está armada en el proyecto: FOB del entero
(NCM 0306.17.10, aduana oficial empalmada con INDEC 2013-01/2017-01) y desembarques
mensuales de la SSPyA por flota, 2013-01 a 2026-07.

**Regresiones mensuales de `log P` contra volumen** (HAC, 6 rezagos):

| Especificación | Coef. de la cantidad | t | N |
|---|---|---|---|
| A1 · log Q exportado + tendencia | **+0,059** | 4,04 | 163 |
| A2 · A1 + 11 dummies de mes | **+0,069** | 3,14 | 163 |
| B1 · log desembarque 3 meses + mes + tendencia | **+0,057** | 2,48 | 161 |
| B2 · log captura tangonera 3 meses + mes + tendencia | **+0,029** | 3,84 | 161 |

**Las cuatro dan el signo equivocado y significativo.** No es un problema de
especificación: es que a frecuencia mensual la oferta y la demanda se mueven juntas. La
zafra coincide con la compra europea de fin de año, y el dato ya lo sabía —
`corr(precio, volumen) = +0,55` sobre el agregado oficial es un resultado propio del informe
de mercado, no una anomalía de esta corrida.

**Flexibilidades de arco año contra año** (2014-2025), calculadas como
`Δlog P / Δlog Q`:

Mediana **+0,52** sobre volumen exportado y **+0,21** sobre desembarques, con un rango que va
de −1,15 a +5,6. Once de trece años dan valores sin sentido económico. La serie anual
completa en regresión da `f = −0,045` (t = −0,38) con tendencia y `−0,085` (t = −1,37) sin
ella: **negativo pero indistinguible de cero, con N = 13**.

**El único episodio con algo parecido a una fuente de variación exógena es 2025**, el
conflicto gremial que detuvo la flota tangonera de abril a julio:

| | 2024 | 2025 | Variación |
|---|---|---|---|
| Desembarque total (t) | 222.163 | 187.030 | −15,8% |
| Entero exportado (t) | 92.732 | 58.300 | −37,1% |
| FOB medio (US$/kg) | 5,59 | 6,84 | **+22,4%** |
| **Ingreso FOB del entero (US$ M)** | **518,7** | **399,0** | **−23,1%** |

La flexibilidad de arco de ese episodio es **−0,43** medida sobre el volumen exportado y
**−1,17** medida sobre desembarques. Es decir: **el único experimento disponible deja el
resultado justo encima y justo debajo del umbral de −1, según qué cantidad se use.** Y el
hecho crudo es que el ingreso cayó 23%.

Con una advertencia que invalida la lectura directa: **en 2026 el precio siguió subiendo
mientras el volumen se recuperaba** (julio 2026: 7,31 US$/kg con 14,0 kt exportadas, contra
5,66 con 17,0 kt en julio 2024). Si el precio alto de 2025-2026 fuera consecuencia del
recorte argentino, habría cedido al volver la oferta. No cedió. Lo más probable es que
buena parte de la suba sea **recuperación del ciclo mundial del camarón**, y que 2025
sobrestime el efecto del recorte. Sin un control del precio mundial, el episodio no sirve
como evidencia.

---

## 4. Diseño propuesto

### 4.1 Qué hay que resolver antes de estimar

1. **Definición del mercado.** Si el L1 está integrado con el vannamei, no hay demanda
   propia que estimar. Test de cointegración e integración de mercado (Asche/Johansen) entre
   FOB L1, precio del vannamei ecuatoriano y precio de importación europea, previo al modelo.
2. **Identificación.** Hace falta variación de oferta que no mueva la demanda. Candidatos de
   instrumento, todos disponibles o conseguibles:
   - fechas de apertura y cierre de zafra y vedas (aguas nacionales y provinciales);
   - el conflicto gremial de 2025 como dummy de shock;
   - anomalías de temperatura del mar (NOAA, ya está en el proyecto) y reclutamiento INIDEP;
   - precio del gasoil marino y tipo de cambio real / retenciones, que mueven el esfuerzo
     sin mover la demanda europea.
3. **Almacenabilidad.** El producto es congelado. Los desembarques de un mes no son la
   oferta de ese mes: hay stock. Eso es lo que rompe la regresión mensual. Se resuelve
   agregando a frecuencia de campaña o incorporando un proxy de existencias.
4. **Escala del jugador.** Argentina exporta del orden de 90-120 kt sobre un mercado mundial
   de camarón de ~7,7 Mt. La flexibilidad relevante no es la del camarón mundial sino la de
   la **demanda residual que enfrenta Argentina en su nicho** (salvaje premium en España e
   Italia, donde sí tiene 20-35% del mercado).

### 4.2 Especificación

**Modelo principal — demanda inversa residual, ecuación única con variable instrumental:**

    log P_L1,t = α + f · log Q_AR,t + β · log P_vannamei,t + γ · log Y_UE,t
                 + δ · TCR_EUR/USD,t + estacionalidad + ε_t

con `Q_AR` instrumentada por los shifters de oferta de arriba. `f` es el número que decide
la política. Se reporta con IC y con el test de `H₀: f = −1`.

**Modelo de contraste — sistema de demanda inversa (IAIDS o Rotterdam inversa)** sobre las
importaciones europeas de camarón por origen (Argentina, Ecuador, India, Vietnam, resto),
con datos Comext. Entrega flexibilidad de escala y flexibilidades cruzadas, permite testear
homogeneidad y simetría, y dice cuánto del efecto es escala del mercado y cuánto es
sustitución hacia Ecuador. Es la ruta Barten-Bettendorf y la que exige la literatura para
que el resultado sea publicable.

**Simulación de política.** Sobre `f` estimado, la grilla de escenarios que interesa no es
«recortar X%» en abstracto sino las medidas concretas de Conxemar: zafra de Rawson a cuatro
meses, cierre nacional a mediados de septiembre, corte de XXL incidental. Cada una se
traduce a toneladas por mes y flota con la base de desembarques, y de ahí a precio e
ingreso, separando **efecto nivel** (menos toneladas) de **efecto composición** (menos
fresquero, más entero tangonero, mejor mix de calibre) y de **efecto calendario** (correr el
volumen fuera del piso de diciembre). Los tres son distintos y sólo el primero depende de
`f`.

### 4.3 Lo que hace falta conseguir

| Dato | Para qué | Dónde |
|---|---|---|
| Precio mundial del camarón, mensual | Control imprescindible; sin él 2025 no es interpretable | NOAA import price (ya hay módulo), Urner Barry, FAO GLOBEFISH |
| Comext **mensual** por origen y CN8 | Sistema de demanda inversa europeo | El consolidado que hay es anual (2019-2025): 7 puntos no alcanzan |
| Calendario oficial de vedas y aperturas 2013-2026 | Instrumento de oferta | CFP / SSPyA, resoluciones |
| Existencias / stock de congelado | Cerrar la brecha desembarque-oferta | Declaraciones de planta, o proxy desembarque menos exportación acumulada |

---

## 5. Advertencia previa al resultado

Tres cosas conviene decirlas antes de estimar, no después:

1. **La literatura no respalda el mecanismo que se busca.** Donde hay ganancias de precio
   documentadas por regulación, el canal es el momento y la calidad de la descarga, no el
   nivel de captura. Y las flexibilidades propias estimadas en pesca están casi siempre muy
   por debajo de 1 en valor absoluto.
2. **El único episodio argentino disponible dio ingreso más bajo.** 2025: menos volumen,
   mejor precio, US$120 M menos de facturación en el entero.
3. **Aunque `f` diera menor que −1, el resultado sería un óptimo colectivo con incentivo
   individual a desviarse.** El caso chileno lo muestra con precisión: la mejora aparece sólo
   donde la organización era estable y el reparto inicial fue aceptado. Sin eso, el recorte
   lo pagan unos y lo cobran otros, y no se sostiene. Y una coordinación privada de volumen
   entre exportadores tiene un problema de defensa de la competencia que la vía regulatoria
   (veda, cuota, CITC) no tiene.

Nada de esto cierra la pregunta. La cierra el número, con su intervalo. Pero el diseño
tiene que estar hecho para poder decir «no» si el dato dice que no.

---

### Fuentes

Barten y Bettendorf (1989), *European Economic Review*, «Price formation of fish: An
application of an inverse demand system» · Tabarestani, Keithly y Marzoughi-Ardakani (2017),
*Marine Resource Economics* 32(4), «An Analysis of the US Shrimp Market: A Mixed Demand
Approach» · Guillen y Maynou (2014), *Marine Policy* 47, «Importance of temporal and spatial
factors in the ex-vessel price formation for red shrimp and management implications» ·
«Do Catch Shares Increase Prices? Evidence from US Fisheries», *MRE* 38(3), 2023 ·
«Collective Share Quotas and the Role of Fishermen's Organizations», *MRE*, 2019 ·
«Modeling Inverse Demands for Fish», *MRE* 19(3), 2004 · «An Inverse Demand System for the
Differentiated Blue Crab Market in Chesapeake Bay», *MRE* 30(2), 2015 · «U.S. Shrimp Market
Integration», *MRE* 27(2), 2012 · «Market Integration of Cold and Warmwater Shrimp in
Europe», *MRE* 32(4), 2017 · Punto Noticias, «Langostino 2026: el desafío de dosificar el
volumen para mantener mejores precios» · Pescare, «Langostino. La cuotificación abre debate
sobre recurso, empleo y exportaciones».

Cálculos propios sobre `datos/aduana_langostino_total.pkl`, `datos/indec_entero_2013_2017.pkl`
y `_lan.pkl` (SSPyA), script `demanda_inversa_explora.py`.
