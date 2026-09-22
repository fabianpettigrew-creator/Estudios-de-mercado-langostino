# Demanda inversa del L1 tangonero — versión con la serie larga

## Serie 2013-2026, marca de flota recuperada de la prosa, y un instrumento menos

AXIA · 22 de agosto de 2026 · reemplaza a la versión de esta misma fecha basada en 2018-2026

---

## Qué cambió y qué pasó con el número

Tres cosas, en orden:

1. **La serie de flota se extendió de 2018 a 2013.** Antes de que existiera el sufijo SIM
   SA01, la leyenda **«CONGELADO A BORDO»** viaja en prosa en la descripción del despacho.
   Cubre el 68-70% de los kilos de entero de 2013-2016. Con eso el modelo de campaña pasa de
   **N = 8 a N = 11**.
2. **La captura rezagada dejó de servir como instrumento.** El langostino tiene ciclo de vida
   corto y «reemplazo casi total de la cantidad de ejemplares» entre temporadas (INIDEP): no
   hay persistencia de biomasa que explotar. Empíricamente da primera etapa **F = 0,1**. Se
   descarta. Queda un solo instrumento válido: la ventana en que el conflicto gremial deprime
   la captura acumulada — que en la serie larga sí es fuerte, **F = 61,1**.
3. **Con la serie larga, el efecto se achica.** La estimación preferida pasa de −0,35 a
   **−0,18**.

**Estimación preferida — IV mensual sobre el precio relativo al camarón de cultivo,
cantidad instrumentada por la ventana del conflicto, N = 138:**

> **f = −0,184**   ·   SE 0,081   ·   IC 95% **[−0,342, −0,026]**   ·   primera etapa F = 61,1
> **H0: f = −1 → t = +10,1**

Negativa y significativa, pero chica. Y la conclusión de política queda **más firme** que
antes, no menos: hay todavía menos respuesta de precio de la que estimábamos.

---

## Por qué se achicó: hay una tendencia que antes no se veía

En la ventana corta (2018-2026) el precio relativo al cultivo y la captura se movían en
sentidos opuestos, y eso se leía como demanda inversa. Con trece años a la vista se ve que
buena parte de ese movimiento es una **tendencia**: el precio del L1 tangonero relativo al
camarón de cultivo sube **+2,6% por año** (t = 5,0) a lo largo de toda la serie, mientras la
captura baja. En el modelo de campaña, meter la tendencia lleva el R² de 0,29 a 0,79 y `f` de
−0,247 a −0,186.

Esa tendencia es real y es una buena noticia, pero no es demanda inversa: es la **prima del
salvaje ensanchándose** frente al cultivo. Atribuirla a la cantidad sería un error.

**Y el leave-one-out lo confirma.** En la serie larga, sacar la campaña 2025/2026 —la del
conflicto, que además coincide con el MSC de aguas nacionales— lleva `f` de −0,247 a **−0,024**.
Es decir: en el modelo de campaña sin instrumentar, casi todo el efecto lo pone ese único año. La
robustez que mostraba la versión de ocho campañas era un artefacto de la ventana.

Por eso la estimación que hay que citar es la **IV**, que usa el shock de oferta
explícitamente y con toda la serie mensual detrás, y no el ajuste de once puntos.

---

## El empalme de la marca de flota está validado

La pregunta obligada es si el precio medido cambia de nivel cuando cambia el marcador (prosa
hasta 2017, sufijo desde 2018), ya que la cobertura es distinta: 68-70% de los kilos en la
primera mitad, 78-91% en la segunda.

El testigo es el FOB del entero de aduana oficial, que es el mismo dato en las dos épocas. La
prima del L1 a bordo sobre ese entero:

| 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1,124 | 1,071 | 1,101 | 1,022 | 1,072 | 1,076 | 1,062 | 1,083 | 1,073 | 1,088 | 1,022 | 1,083 | 1,093 |

Media 2013-2016 (prosa) **1,080** contra media 2018-2024 (sufijo) **1,070**: **−0,9%**. No hay
quiebre. Las dos mitades de la serie son comparables.

**Dónde no hay serie**: enero a junio de 2016 (ningún despacho con grado declarado) y junio a
octubre de 2017 (la descripción viene con el literal «No disponible»). Por eso las campañas
2015/2016 y 2017/2018 quedan afuera del modelo con marcador: su ventana de venta no llega a
nueve meses con dato. **Es una limitación del registro de origen, no de la extracción**, así
que no hay nada que pedirle al proveedor. La sección siguiente muestra cómo se recuperan esas
dos campañas por otra vía.

---

## Todas las especificaciones

| Especificación | f | IC 95% | t de H0: f = −1 | N |
|---|---|---|---|---|
| T1 · mensual, **sin** control de HORECA | −0,095 | −0,212 a +0,021 | 15,2 | 138 |
| T2 · mensual, con la brecha del índice HORECA | −0,107 | −0,219 a +0,006 | 15,6 | 138 |
| T3 · mensual, **excluyendo** los meses de cierre | −0,112 | −0,240 a +0,016 | 13,6 | 113 |
| T4 · mensual, precio relativo + HORECA | −0,151 | −0,261 a −0,041 | 15,1 | 138 |
| **T5 · IV 2SLS, precio relativo (preferida)** | **−0,184** | **−0,342 a −0,026** | **10,1** | 138 |
| C1 · campaña, precio en euros + cultivo + HORECA | −0,107 | −0,339 a +0,124 | 7,6 | 11 |
| C2 · campaña, precio relativo + HORECA | −0,247 | −0,544 a +0,050 | 5,0 | 11 |
| C3 · C2 + tendencia | −0,186 | −0,339 a −0,032 | 10,4 | 11 |

Todo converge en la banda **−0,10 a −0,25**, y el sistema LA/IAIDS por origen del modelo
general —base y método distintos— da **−0,267** [−0,371, −0,162]. `H0: f = −1` se rechaza en
todas con |t| ≥ 4,4.

---

## El canal HORECA, ahora con dato observado

El índice construido a mano de la primera versión fue reemplazado por el observado de los
cuatro destinos: **INE** para España (cifra de negocios de la CNAE 56, mensual y completa
desde 2013), **ISTAT** para Italia (Ateco 56; mensual desde 2021, trimestral antes),
**la Oficina Nacional de Estadística** para China (ingresos de restauración, valor corriente)
y el **METI** para Japón (índice de actividad terciaria, rama restauración). Los cuatro en base
2019 = 100 y combinados por media geométrica ponderada por volumen. Lo arma
`demanda_inversa_horeca.py` desde `HORECA_indice_mensual.xlsx`.

Lo que el supuesto anterior no podía representar: **en abril de 2020 el índice marcó 16,9,
una caída del 83,1% contra 2019.** Ninguna variable binaria captura eso.

En el modelo de campaña sobre el precio en euros el coeficiente es **+0,248 con t = 2,02**:
un 10% de actividad de restauración por debajo de su tendencia baja el precio del L1
alrededor de **2,5%** — más de lo que produciría un recorte de oferta del 10%, que da 1,8%.
**La palanca del canal es más grande que la de la oferta, y no cuesta toneladas.**

Sobre el precio *relativo* al cultivo el efecto es menor y no significativo, y la razón es
informativa: cuando cerró el servicio de comidas también cayó el precio del camarón de
cultivo, de modo que la prima del salvaje quedó prácticamente intacta —el relativo promedió
0,864 en las campañas de pandemia contra 0,775 en 2013-2019—. Vale contrastarlo con el
relevamiento propio de góndola: es compatible con que el producto argentino se haya corrido
al canal minorista mientras el servicio estuvo cerrado.

Supuestos que quedan, declarados: China no publica enero ni febrero por separado —los difunde
acumulados y acá se reparten por mitades— e Italia entra como escalón trimestral hasta 2020.

---

## El contraste sin marcador: trece campañas, sin huecos

La industria aporta una regla que el dato confirma: **la cola se procesa casi toda en tierra y
el entero que se exporta durante la temporada de la flota congeladora es casi todo congelado a
bordo.** Verificado sobre 2018-2026, donde el sufijo SA01 está a la vista:

| Mes de embarque | may | jun | jul | ago | sep | oct | abr | nov | dic | ene | feb | mar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| % del entero L1 congelado a bordo | 95,4 | 96,3 | 93,6 | 96,8 | 96,1 | 95,9 | 80,4 | 81,6 | 48,2 | 21,9 | 22,2 | 42,0 |

Y en la cola (0306.17.90), entre el 85% y el 95% de los kilos con marcador salen procesados en
tierra, todos los años desde 2017.

Eso habilita un **proxy que no depende del marcador**: el FOB del entero del registro oficial de
aduana embarcado entre mayo y octubre, que por la regla es 94-97% tangonero. La ventaja es
decisiva: **no tiene huecos**, así que recupera las campañas 2015/2016 y 2017/2018 y da
**N = 13** en vez de 11, sobre dato oficial y sin ninguna dependencia de cómo esté redactada la
descripción del despacho.

| Especificación | f | IC 95% | t de H0: f = −1 | N |
|---|---|---|---|---|
| P1 · log (P/cultivo) ~ log captura + HORECA | −0,282 | −0,591 a +0,026 | 4,6 | 13 |
| **P2 · P1 + tendencia** | **−0,234** | **−0,380 a −0,089** | **10,3** | 13 |
| P3 · log P (EUR) ~ log captura + cultivo + HORECA | −0,110 | −0,378 a +0,158 | 6,5 | 13 |

**Y es la estimación más estable de todo el trabajo.** El leave-one-out sobre P2 se mueve entre
**−0,181 y −0,277**: ninguna campaña la maneja. Compárese con el modelo con marcador, donde
sacar 2025/2026 llevaba la flexibilidad de −0,247 a −0,024.

Con esto hay tres construcciones independientes que convergen: la instrumental sobre el precio
de Softrade con marcador de flota da **−0,184**; el proxy oficial sin marcador da **−0,234**; y
el sistema de demanda inversa por origen sobre importación europea da **−0,267**. Tres bases de
datos y tres métodos distintos, todos entre −0,18 y −0,27, y todos rechazando `f = −1` con
holgura.

---

## Lo que confirma el nomenclador oficial

Del `NCM Completo ver 07.2026`, hoja de sufijos, para las partidas 0306.17.10 y 0306.17.90:

- **`SA01` = «CONGELADO A BORDO»**, y **no existe un `SA00` en la norma**. O sea que el único
  código declarable es afirmativo: el `SA00` que aparece en las descripciones es el relleno de
  «no corresponde». Eso valida la regla que ya estaba en el código —la marca «a bordo» es
  afirmativa y el resto no se infiere por descarte— y conviene dejarlo dicho así.
- **El calibre tiene sufijo oficial**: `NA01` = de 11 hasta 20 piezas por kilo, que es
  exactamente el L1; `NA02` 21-30, `NA03` 31-40, `NA04` 41-60, `NA05` 61-80, `NA06` más de 80.
  Para la cola, `NB01` 30-55, `NB02` 56-100, `NB03` 101-150.
- **Hay sufijos oficiales para producto defectuoso**: `NA03` rotos en bloque, `NA04` melanósicos
  en bloque, `NC01` rotos. Se usan: 67,9 kt declaradas como rotas y 2,9 kt como melanósicas en
  toda la serie. **Pero cero kilos en el entero**: están todas en cola y pelado. La serie de
  precio del L1 entero no tiene contaminación de calidad, que era la duda.
- **No existe sufijo de glaseo.** Los códigos `CA01` (venta al por menor), `CB01` (hielo en
  escamas) y `CB02` (gel refrigerante) son de acondicionamiento, no de glaseo. Queda cerrado:
  el porcentaje de glaseo no se puede obtener del registro aduanero por ninguna vía.

---

## Lo que implica para la política

Recorte del 7,4% del desembarque (Rawson a cuatro meses más cierre nacional a mediados de
septiembre, −15.520 t):

| Supuesto sobre f | f | Δ precio | Δ facturación | Costo evitable mínimo para que convenga |
|---|---|---|---|---|
| **IV, preferida** | −0,184 | +1,4% | **−6,0%** | **c/P > 0,816 · US$5,34/kg** |
| IV, cota más favorable del IC | −0,342 | +2,5% | −4,8% | c/P > 0,658 · US$4,31/kg |
| Campaña con tendencia (C3) | −0,186 | +1,4% | −6,0% | c/P > 0,814 · US$5,33/kg |
| Proxy sin marcador, 13 campañas (P2) | −0,234 | +1,7% | −5,6% | c/P > 0,766 · US$5,02/kg |
| Sistema IAIDS | −0,267 | +2,0% | −5,4% | c/P > 0,733 · US$4,80/kg |
| Umbral de facturación | −1,000 | +7,4% | 0,0% | — |

Sobre US$867 M de exportación de langostino de 2025, la estimación preferida son
**−US$52 millones** de facturación por año.

> **Pendiente de regenerar (22-09-2026).** Las `f` de este cuadro salen del FOB argentino
> a todos los destinos, así que su ámbito es el total y `(1+f)` es la elasticidad
> correcta: el cuadro no tiene el error de base que sí tenía el §5 del informe general.
> Cambian dos cosas menores igual. El valor exportado ahora se calcula del registro
> oficial en lugar de estar escrito a mano, y la fila prestada del sistema IAIDS pasa a
> **−0,241** —la propia argentina corregida— y se evalúa con ámbito europeo, donde el
> umbral de facturación no es −1 sino cerca de −2. Ver `recorte_conxemar.simular()`.

Y el test que decide sigue siendo el del margen, no el de la facturación: con `f = −0,184`,
recortar conviene sólo si el costo que se ahorra por no pescar supera el **81,6% del FOB**
—unos **US$5,34 por kilo**—. Ese umbral es ahora **más alto** que con la estimación anterior
(era 64,7%), o sea que el recorte tiene que ahorrar más costo para justificarse. Sigue
faltando el dato de costo.

---

## Novedades de los dos documentos nuevos de la carpeta

**`Documentos/ACTA CFP 10-2026.pdf`** (15 de abril de 2026, punto 2.1) es exactamente el tipo
de fuente que pedimos para armar los instrumentos. De ahí salen dos fechas duras:

- **Apertura de la pesca de langostino en aguas nacionales fuera del AVPJM: 15 de abril de
  2026**, por nota INIDEP DNI 31/2026, decidida por unanimidad.
- **Cierre reproductivo desde comienzos de octubre de 2025**, que el INIDEP evalúa como
  contribución a reducir la mortalidad por pesca en ese período.

Cuadra con el dato: la captura tangonera de abril de 2026 fue de 865 t, la de mayo 4.873 t y
la de junio 27.548 t — el arranque de una temporada que se abrió a mediados de abril. **Con la
serie completa de actas 2013-2026 se puede construir la fecha de apertura y de cierre de cada
temporada**, que es un instrumento de oferta limpio: lo decide el CFP sobre asesoramiento
biológico del INIDEP, no sobre la demanda europea.

**`Documentos/inidep_infografia_langostino.pdf`** confirma el calendario biológico (captura
habitual en jurisdicción nacional de marzo a octubre, veda de noviembre a febrero para
proteger la reproducción en el golfo San Jorge) y aporta el dato que **invalidó un
instrumento**: «ciclo de vida corto, existe un reemplazo casi total de la cantidad de
ejemplares disponibles». Sin persistencia de biomasa entre temporadas, la captura rezagada no
puede predecir la de hoy — y en efecto no lo hace (F = 0,1).

---

## Advertencia sobre `fuentes/expo.py`

El respaldo por prosa se agregó **dentro de `fuentes/expo.py`**, en el bloque que arma la
columna `ruta`, con el mismo criterio que ya existía para el calibre. Consecuencia: **cualquier
salida del proyecto que abra por flota ahora incluye 2013-2017**, donde antes esos años venían
todos como «s/d». Si algún cuadro o gráfico del informe se regenera sin filtro de año, va a
cambiar.

La regla que quedó escrita en el código y que conviene no romper: **la marca «a bordo» es
afirmativa**. Sin sufijo y sin leyenda el registro queda en «s/d», nunca en «en tierra». En
2013-2016 no existe leyenda para el procesado en tierra, así que el residuo es *desconocido*,
no *fresquero*.

---

## Límites que quedan

- **El instrumento es uno solo.** Toda la identificación causal cuelga del conflicto de 2025.
  Con el calendario de aperturas y cierres del CFP se puede tener variación exógena todos los
  años; ése es el próximo paso y ahora sabemos que la fuente existe y es accesible.
- **El índice de HORECA ya no es un supuesto.** Se reemplazó por el observado de los cuatro
  destinos —INE para España, ISTAT para Italia, la Oficina Nacional de Estadística para China y
  el METI para Japón—, base 2019 = 100, ponderado por volumen. En abril de 2020 marcó 16,9,
  una caída del 83,1% contra 2019. En el modelo de campaña sobre el precio en euros entra con
  coeficiente **+0,248 (t = 2,02)**: un 10% de actividad por debajo de tendencia baja el precio
  del L1 alrededor de 2,5%. Queda un supuesto menor: China no publica enero ni febrero por
  separado y se reparten por mitades, e Italia entra como escalón trimestral hasta 2020.
- **La campaña 2025/2026 mezcla el conflicto con el MSC** de aguas nacionales de febrero de
  2026. En la serie larga el leave-one-out muestra que el modelo de campaña depende de ella;
  la IV no, porque usa la variación mensual.
- **Sigue faltando el costo evitable**, que es lo único que puede cambiar el signo de la
  recomendación.

---

### Trazabilidad

`demanda_inversa_tangonera.py` corre todo. Tablas en
`salidas/demanda_inversa_tangonera.xlsx` (hojas `campanas`, `flexibilidades`,
`leave_one_out`, `regresiones`, `simulacion`), figura en
`salidas/demanda_inversa_tangonera.svg`. El respaldo por prosa está en `fuentes/expo.py`.
