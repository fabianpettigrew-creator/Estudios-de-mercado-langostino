# Verificación de consistencia del estudio econométrico del langostino

Contraste contra Barten y Bettendorf (1989) y Tabarestani, Keithly y Marzoughi-Ardakani (2017)

AXIA · nota de auditoría · 21 de septiembre de 2026
Alcance: `salidas/Demanda_inversa_L1_antecedentes_y_diseno.md`,
`salidas/Demanda_inversa_L1_resultados.md`, `demanda_inversa_modelo.py`,
`iaids_simetria.py` y el anexo metodológico (`salidas/correcciones_docx_3.py`, A.5–A.6).
Reproducible con `python verificar_sistema_inverso.py` (corre sin las bases).

---

## Veredicto en una línea

**La conclusión de política resiste; la tabla que la sostiene, no.** El resultado —que
`|f|` está muy por debajo de 1 y que recortar oferta destruye ingreso— sobrevive a todas
las correcciones que pude aplicar, y de hecho sale reforzado. Pero la matriz de
flexibilidades del §2 contiene un error de fórmula que la vuelve **internamente
contradictoria con la fila de escala publicada en el mismo párrafo**, y el sistema no
cumple la condición de negatividad que es el requisito central de Barten. Hay además una
inversión de supuestos respecto de Tabarestani que el informe cita como su antecedente más
cercano y luego no sigue.

Nueve hallazgos. Tres son errores de fórmula o de especificación; cuatro son de lectura o
de reporte; dos son de cita.

---

## 1. Error de fórmula: la flexibilidad omite el término de escala

**Dónde.** `demanda_inversa_modelo.py:386`, `iaids_simetria.py:193`, y el anexo como
ecuación **A.12**. Los tres escriben:

    f_ij  =  γ_ij / w_i − δ_ij                    ← usada
    f_ij  =  γ_ij / w_i + β_i·w_j / w_i − δ_ij    ← correcta

La forma correcta es la del AIDS inverso (Eales-Unnevehr; es el análogo inverso de la
ecuación (20) de Barten, `dw_i = c_i·dlnQ + Σ_j c_ij·dlnq_j`). Sale de que
`w_i = π_i·q_i` implica `dlnπ_i = dw_i/w_i − dlnq_i`, y `dlnQ = Σ_k w_k·dlnq_k` mete
`β_i·w_j/w_i` en cada casilla.

**Cómo se detecta sin datos.** La teoría obliga a que la suma de cada fila sea la
flexibilidad de escala de esa fila:

    Σ_j f_ij  =  Σ_j γ_ij/w_i + β_i/w_i − 1  =  β_i/w_i − 1  =  f_i^escala

Con la fórmula usada, `Σ_j γ_ij = 0` por homogeneidad y **toda fila suma exactamente −1**.
Es justo lo que pasa en la tabla publicada:

| origen | suma de la fila | escala publicada | brecha |
|---|---|---|---|
| Argentina | −1,000 | −0,82 | −0,18 |
| Ecuador | −1,000 | −0,83 | −0,17 |
| India | −1,000 | −1,14 | +0,14 |
| Vietnam | −1,000 | −1,17 | +0,17 |
| Resto | −1,000 | −1,10 | +0,10 |

Las dos mitades del §2 no pueden ser ciertas a la vez. La adición, en cambio, sí se cumple
(`Σ_i w_i·f_ij = −w_j` en las cinco columnas, a cuatro decimales): el error está en el
término de escala, no en la estimación.

**Qué cambia.** Reconstruyendo `γ_ij` y `β_i` desde lo publicado:

| | AR | EC | IN | VN | Resto | suma = escala |
|---|---|---|---|---|---|---|
| **Argentina** | **−0,241** | −0,081 | −0,216 | −0,084 | −0,198 | −0,820 |
| Ecuador | −0,127 | −0,353 | −0,085 | −0,098 | −0,168 | −0,830 |
| India | −0,145 | −0,247 | −0,277 | −0,119 | −0,352 | −1,140 |
| Vietnam | −0,131 | −0,379 | −0,330 | −0,040 | −0,289 | −1,170 |
| Resto | −0,125 | −0,245 | −0,104 | −0,090 | −0,536 | −1,100 |

La propia argentina pasa de **−0,267 a −0,241**: se aleja del umbral, no se acerca. La
simulación del §5 queda algo más adversa, no menos. El titular no se toca.

La misma omisión está en la tabla de dos flotas del anexo (A.5.3): sus dos filas,
(−0,872, −0,128) y (−0,685, −0,315), también suman exactamente −1,000. Ahí importa menos
porque A.13 recompone después, pero la fila de partida es la misma fórmula incompleta.

---

## 2. El sistema no cumple negatividad — y nadie lo testeó

Barten dedica la condición **(17)** a esto y verifica explícitamente que su matriz de
Antonelli resultó semidefinida negativa *sin* haberlo impuesto. Es lo que hace que la
flexibilidad propia sea interpretable: sin negatividad no hay función de utilidad
cuasicóncava detrás y los números son correlaciones, no elasticidades.

Reconstruyendo `H = γ_ij − w_i·δ_ij + w_i·w_j` desde lo publicado:

- **La diagonal de Vietnam es positiva**: `h_VN,VN = +0,0060`. En la lengua de Barten, «un
  bien es sustituto de sí mismo» y ese elemento tiene que ser negativo. Se ve a simple
  vista en la tabla original: la propia de Vietnam es **−0,025**, o sea cero. Que el
  volumen vietnamita no mueva en absoluto el precio vietnamita no es un hallazgo, es el
  síntoma.
- **La matriz no es semidefinida negativa**: el mayor autovalor de su parte simétrica es
  **+0,0109**. Falla la condición (17).

Ninguno de los dos controles aparece en el informe ni en el código.

---

## 3. El índice de Stone usa participaciones corrientes

El anexo lo dice con todas las letras en A.11: el índice va con participaciones **medias**,
«con las corrientes el regresor lleva adentro la variable dependiente».
`demanda_inversa_sistema_flotas.py:109` lo hace bien. Pero el sistema de cinco orígenes
—el que produce el número del titular— hace lo contrario:

```python
lnQ = (W * X).sum(axis=1)     # demanda_inversa_modelo.py, y idéntico en iaids_simetria.py:82
```

`W` son las participaciones corrientes y `w_i` es la variable dependiente. El regresor
contiene la izquierda. Eso sesga `β_i`, y `β_i` es exactamente lo que produce la
**flexibilidad de escala de −0,82**, que es la segunda cifra del §2 y una fila de la
simulación del §5. El proyecto ya tiene la regla escrita y la aplica en otra capa; acá no.

---

## 4. La asimetría que se está leyendo es la que la teoría prohíbe

El §2 concluye: *«Argentina recibe el shock de los demás; los demás casi no reciben el
suyo»*. Esa lectura descansa enteramente en que `f_AR,EC ≠ f_EC,AR`. En términos de
Antonelli:

    h_AR,EC = +0,0194        h_EC,AR = −0,0016

Signos opuestos, y una discrepancia máxima de **0,0210** contra una diagonal cuyo menor
valor absoluto es 0,0060. La asimetría es más grande que los elementos que compara.

La simetría de Antonelli (`γ_ij = γ_ji`) dice que esa diferencia no puede existir. Barten
la impone por máxima verosimilitud; Tabarestani la impone por ISUR (`θ_ij = θ_ji`,
`γ_rs = γ_sr`, su ec. 5b). Los dos antecedentes citados hacen lo mismo y el informe hace lo
contrario.

**Dato de gestión:** el §7 lista esto como «refinamiento pendiente», pero
`iaids_simetria.py` ya lo resuelve por SUR iterado, con test de Wald y de razón de
verosimilitud. El informe de resultados está desactualizado respecto de su propio
repositorio. Corresponde traer ese resultado al §2 y bajar el hallazgo de la asimetría, o
sostenerlo con el test.

---

## 5. Leer las cruzadas no compensadas como sustitución es lo que Barten prohíbe

El §2 dice: *«la cruzada con Ecuador es −0,128 y con India −0,246: cuando el cultivo entra
volumen, el precio argentino cede»*. Y el §6.3 va más lejos: *«La flexibilidad cruzada con
el cultivo es la medida de cuánto se gana separándose de él»*.

Barten dedica su sección 4 a advertir contra exactamente eso. Los `h_ij` son «medidas
imperfectas de la interacción» porque la adición `Σ_i h_ij = 0` junto con `h_jj < 0`
**fuerza** `Σ_{i≠j} h_ij > 0`: el predominio «no proviene de la estructura de las
preferencias, sino de la condición `π'q = 1`».

Acá es peor, porque las cruzadas publicadas son **no compensadas**: están dominadas por el
término de escala, que vale aproximadamente `−w_j`. Que las veinticinco casillas sean
negativas no informa nada sobre sustitución; es aritmética de participaciones. Convertida a
Antonelli, la cruzada Argentina-Ecuador es **+0,019**, o sea complementariedad en el sentido
de Barten — el signo contrario al que el informe está leyendo.

La herramienta correcta existe y el estudio tiene todos los insumos: los **coeficientes de
Allais** de Barten (su ec. 27) y las intensidades `α_ij = a_ij/√(a_ii·a_jj)` (ec. 28), que
son ordinales y van entre −1 y +1. Requieren antes resolver los puntos 2 y 4 — sin simetría
ni negatividad no se pueden calcular con sentido.

---

## 6. El sistema hace lo contrario de lo que prescribe Tabarestani

El diseño (§2.2) presenta a Tabarestani como *«el más pertinente al caso argentino»* y
resume bien su aporte: desembarques salvajes del Golfo como cantidad predeterminada (forma
inversa), precios de las importaciones de cultivo como predeterminados (forma directa),
sistema de **demanda mixta**.

Y después estima un sistema **inverso puro** sobre la importación europea por origen, o sea
tratando como predeterminadas las cantidades de Ecuador, India, Vietnam y resto. Para cuatro
de los cinco bienes es el supuesto polar opuesto al del antecedente.

No es una discusión de escuela. Tabarestani dedica su Apéndice A a testearlo —Hausman,
Wald por variable y razón de verosimilitud conjunta— y encuentra que los precios de
importación son exógenos (LR = 6,23 contra χ²₇ = 14,1) y las cantidades importadas
endógenas, mientras que los desembarques del Golfo sí son exógenos (LR = 0,44 contra
χ²₃ = 7,81). Es el test que decide la forma del modelo, y es previo a estimarlo.

En este repositorio no hay nada equivalente (`grep -ri hausman` sólo toca
`elasticidad_sustitucion_es.py`). El §7 lo reconoce a medias —«los instrumentos de oferta
que se listaron en la nota de diseño no se usaron»— pero lo plantea como una cuestión de
precisión de la ecuación única, cuando además invalida la forma funcional del sistema.

**La especificación que pide el antecedente** es la que el propio informe argumenta en
todas partes: Argentina en forma inversa (salvaje, predeterminado por biología y calendario
— el análogo exacto del desembarque del Golfo) y los orígenes de cultivo en forma directa
(precio exógeno, cantidad endógena). Es un Rotterdam mixto de cinco bienes, y es el trabajo
que Tabarestani ya dejó hecho.

---

## 7. La simulación mezcla tres cantidades distintas

`d(P·Q)/dQ = P·(1+f)` sólo vale si las tres Q son la misma. En el §5 son tres:

| pieza | qué cantidad es | fuente |
|---|---|---|
| `f = −0,27` | volumen de importación **extra-UE desde Argentina** | sistema EUMOFA, §2 |
| `ΔQ = −7,4%` | desembarque de langostino de **todas las flotas** | `recorte_conxemar.py`, base 2022-24 |
| base US$ 867 M | exportación **total** de langostino, todos los productos y destinos | `recorte_conxemar.EXPO_2025` |

Un recorte del 7,4% del desembarque nacional no es un recorte del 7,4% del embarque a la
UE: Argentina también vende a Estados Unidos y Asia, y hay stock de congelado de por medio
(que es el argumento con que el propio §3 justifica la especificación a 12 meses). Y la
base relevante para una flexibilidad del entero en el mercado europeo no son los US$ 867 M
del total exportado sino algo del orden de los **US$ 399 M** de FOB del entero que el §4
reporta para 2025.

La dirección del resultado no cambia. La cifra de **US$ 47 millones** no es defendible tal
como está construida.

---

## 8. Dos citas de Barten para corregir, y una que conviene usar mejor

**8.1 El pescado equivocado.** El diseño (§1) dice: *«flexibilidades propias compensadas de
−0,09 a −0,37 (lenguado el mayor, gallineta el menor)»*. El rango está bien y gallineta es
el menor (−0,09), pero el lenguado es **−0,11**. El mayor en valor absoluto es la **raya**
(−0,37), seguida del rodaballo (−0,35). Cuadro 3 de Barten.

**8.2 Objetos distintos comparados contra el mismo umbral.** El −0,09/−0,37 de Barten son
elasticidades de sustitución propia **compensadas** (Antonelli). El −0,267 del informe es
una flexibilidad **no compensada**. Ponerlos al lado del umbral de −1 mezcla dos cosas.

El objeto comparable es la no compensada de Barten, `h_i + h_ii/w_i`:

| especie | w | compensada (cuadro 3) | escala | **no compensada** |
|---|---|---|---|---|
| Eglefino | 3% | −0,12 | −0,82 | **−0,14** |
| Bacalao | 23% | −0,12 | −1,00 | **−0,35** |
| Merlán | 4% | −0,13 | −1,15 | **−0,18** |
| Gallineta | 3% | −0,09 | −0,77 | **−0,11** |
| Platija | 13% | −0,19 | −1,02 | **−0,32** |
| Lenguado | 47% | −0,11 | −0,99 | **−0,57** |
| Raya | 4% | −0,37 | −1,14 | **−0,42** |
| Rodaballo | 3% | −0,35 | −1,06 | **−0,39** |

Conviene usar estos números porque son el argumento más fuerte, no el más débil: el
**lenguado**, que concentra el 47% del valor y es el pescado insignia de la flota belga —el
análogo más cercano a la posición del L1 en su nicho—, llega apenas a **−0,57**. Ni siquiera
la especie dominante de un mercado de subasta con oferta rígida se acerca a −1. Y el rango
completo, −0,11 a −0,57, encierra cómodamente al −0,241 corregido.

**8.3 Menor.** «169 observaciones mensuales» (diseño §1): 169 es el largo de la serie
(dic-1973 a dic-1987); la estimación corre sobre **168** observaciones en diferencias
(cuadro 2: enero 1974 – diciembre 1987; Barten lo dice al comentar los errores estándar).

---

## 9. La cita de Tabarestani pierde la palabra que la hace útil

El diseño (§2.2) dice: *«un cambio de 1% en el precio de importación mueve 0,98% el precio
doméstico»*. El paper dice: *«una variación simultánea del 1% en **todos** los precios de
importación»*.

Sin «todos» la frase queda al revés de la conclusión del paper. Para un origen individual
los números son otros: Tailandia, con más del 35% del volumen importado, tiene una
flexibilidad precio-precio de **0,02** — un aumento del 10% del precio tailandés mueve el
precio del Golfo un 0,2%. Y el mecanismo es el que interesa acá: el 10% tailandés baja las
importaciones desde Tailandia 3,54%, pero las de los otros siete orígenes suben 3,43% y
**amortiguan casi todo el ajuste**.

Corregida, la cita es la mejor que tiene el estudio, porque es exactamente su tesis y con
la misma estructura de dos filas que el §5 ya construyó:

| | Tabarestani (EE.UU.) | Este estudio (UE) |
|---|---|---|
| un solo origen recorta | 0,02 (Tailandia, 35% del volumen) | **−0,24** (Argentina, 14,6% del valor) |
| todos los orígenes a la vez | 0,98 | **−0,82** (escala) |

Y trae de arriba la conclusión de política de Tabarestani, que es literalmente la del
encargo: *«imponer un arancel o una cuota sólo a un país específico o a un grupo reducido
tendrá escaso efecto sobre los precios en muelle»*.

---

## Lo que sí resiste

Para que quede claro qué no hay que rehacer:

- **La adición del sistema se cumple** en las cinco columnas a cuatro decimales. La
  homogeneidad entra bien por normalización contra el residual. El armado del sistema es
  correcto; el error está en el paso de coeficientes a flexibilidades.
- **La aritmética del §3 cierra en las diez filas.** Verifiqué los diez estadísticos `t`
  contra `H0: f = −1` desde los IC publicados: M1 40,3 · M2 53,2 · A2 17,3, todos
  reproducen.
- **La aritmética del §5 cierra.** `Δp = f·ΔQ`, `Δingreso = (1+f)·ΔQ` y los US$ 47 M son
  exactos dados sus insumos. El problema es de qué son esos insumos (punto 7), no de la
  cuenta.
- **El rango de escala de Barten está bien citado** (−0,77 a −1,15, cuadro 3).
- **La caracterización de Tabarestani es correcta** en lo metodológico: salvaje
  predeterminado, precios de cultivo predeterminados, demanda mixta.
- **La conclusión de política queda más firme, no menos.** La propia corregida es −0,241,
  más lejos de −1 que la publicada. La comparación correcta con Barten (−0,11 a −0,57)
  encierra al resultado en vez de tensionarlo. Y Tabarestani bien citado lo respalda de
  frente.

---

## Orden sugerido de corrección

| # | Qué | Estado | Mueve el resultado |
|---|---|---|---|
| 1 | Arreglar A.12 y la fórmula en los tres scripts (`+ β_i·w_j/w_i`) | **hecho** | −0,267 → −0,241 |
| 2 | Índice de Stone con participaciones medias en el sistema de origen | **hecho** | mueve la escala (−0,82) |
| 3 | Traer `iaids_simetria.py` al §2 y actualizar el §7 | §7 actualizado; falta correr | probablemente poco |
| 4 | Testear negatividad y reportarla (Barten ec. 17) | **hecho**, lo imprime el modelo | no, pero la diagonal de Vietnam necesita explicación |
| 5 | Reexpresar el §5 sobre una base coherente (embarque a la UE, FOB del entero) | pendiente | baja la cifra de US$ 47 M |
| 6 | Cruzadas: intensidades de Allais en lugar de `f_ij` crudas, o bajar la afirmación del §6.3 | pendiente | cambia una conclusión cualitativa |
| 7 | Test de exogeneidad tipo Hausman antes de fijar la forma del sistema | pendiente | podría cambiar el modelo |
| 8 | Correcciones de cita (raya, «todos los precios», 168 obs.) | **hecho** | no |

Los puntos 1 a 4 son de higiene y no tocan el mensaje. El 7 es el que decide si el sistema
por origen es un Rotterdam inverso o el **mixto** que el antecedente prescribe, y es el
único que puede cambiar el número.

### Qué quedó aplicado (22-09-2026)

La fórmula vivía en **tres** copias, no dos: se sumó
`demanda_inversa_sistema_flotas.py`, donde alimenta la recomposición A.13 y por lo tanto
sí mueve el −0,212 de la cadena de dos flotas. Las tres pasaron a
`flexibilidades_iaids.py`, módulo nuevo con una sola definición —el mismo criterio con que
`recorte_conxemar.py` unificó el recorte— más `verificar()`, que corta la corrida si
`Σ_j f_ij ≠ f_i^escala`, y `negatividad()`, que informa la condición (17) de Barten.

El guardarraíl está probado en las dos direcciones: acepta la fórmula corregida y corta
con la vieja, con el mensaje `fila AR: Σ_j f_ij = −1,000000 contra escala −0,820000`. El
circuito completo se corrió sobre un panel sintético de 163 meses, porque las bases no
están en el repositorio: la identidad cierra a seis decimales sobre un ajuste real de MCO.

**Lo que falta es correrlo con el dato real.** Las cifras publicadas del §2, de A.6 y de
A.14 son todas de la corrida anterior y quedaron marcadas como tales en los tres
documentos. Se reconocen a simple vista: suman exactamente −1.

---

### Fuentes

Barten, A.P. y Bettendorf, L.J. (1989), «Price formation of fish: An application of an
inverse demand system», *European Economic Review* 33(8), 1509-1525 — secciones 3, 4 y 6,
ecuaciones (14)-(20), (27)-(28), condición (17), cuadros 2 y 3.
Tabarestani, M., Keithly, W.R. y Marzoughi-Ardakani, H. (2017), «An Analysis of the US
Shrimp Market: A Mixed Demand Approach», *Marine Resource Economics* 32(4), 411-429 —
ecuaciones (5a)-(6b), cuadros 4b y 5, Apéndice A.

Verificación numérica: `verificar_sistema_inverso.py`. Corre sin acceso a las bases; los
insumos son las cifras publicadas en `salidas/Demanda_inversa_L1_resultados.md` §2. Las
matrices corregidas y la matriz de Antonelli se reconstruyen desde esas cifras redondeadas,
de modo que los decimales finos pueden moverse; los signos y los órdenes de magnitud, no.
