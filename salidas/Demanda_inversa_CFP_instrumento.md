# ¿Sirve el calendario del CFP como instrumento?

AXIA · 1 de septiembre de 2026 · nota de método

**Veredicto en una línea.** El calendario del CFP mueve la cantidad con fuerza y en todos los años —eso está probado—, pero no mueve el precio, y la mitad de la evidencia dice que no es exógeno. No es el segundo instrumento que el §11 pedía. Lo que sí deja es una confirmación más fuerte de la conclusión de política: bajo el calendario, la flexibilidad queda entre −0,20 y +0,12, todavía más lejos de −1 que la estimación preferida.

---

## 1. Qué se hizo

Se codificaron a mano las 547 actas del Consejo Federal Pesquero de 2013 a 2026 —2.884 párrafos que mencionan langostino— en **289 decisiones de oferta** con fecha, subárea, cita literal y grado de confianza. De ahí sale, año por año, la temporada en aguas nacionales dentro del Área de Veda Permanente de Juveniles de Merluza (AVPJM), que es donde pesca la flota tangonera de mayo a octubre: fecha de la primera apertura comercial y fecha de la suspensión del despacho.

| Año | Apertura AVPJM | Fin AVPJM | Largo (días) | Captura tangonera (t) |
|---|---|---|---|---|
| 2013 | 29-may | 08-nov | 163 | 72.130 |
| 2014 | 29-may | 31-oct | 155 | 78.139 |
| 2015 | 12-jun* | 02-nov* | 143 | 89.399 |
| 2016 | 31-may | 27-oct† | 149 | 100.691 |
| 2017 | 19-may | 21-oct | 155 | 109.540 |
| 2018 | 24-may* | 31-oct | 160 | 119.777 |
| 2019 | 13-jun | 15-oct | 124 | 100.171 |
| 2020 | 18-jun | 10-oct | 114 | 55.430 |
| 2021 | 05-jun* | 23-sep | 110 | 86.941 |
| 2022 | 08-jun | 21-sep | 105 | 90.471 |
| 2023 | 02-jun | 25-sep | 115 | 80.877 |
| 2024 | 29-may | 19-sep | 113 | 90.095 |
| 2025 | 09-jul | 04-oct | 87 | 48.284 |
| 2026 | 29-may | en curso | — | — |

\* fecha aproximada: no está en el texto del acta, sale de una nota de la Autoridad de Aplicación citada después o de la habilitación de buques. † imputada: ninguna acta registra el fin de 2016 (delegado a la Autoridad de Aplicación).

Dos cosas se ven a simple vista. La temporada se acortó de 155-163 días (2013-2018) a 105-115 (2021-2024) sin que la captura cayera en proporción: la flota pesca lo mismo en menos días. Y el 87 de 2025 no es una decisión biológica: la apertura del 9 de julio se demoró porque el conflicto dejó sin buques a las prospecciones —el 12 de mayo había un solo congelador despachado y la prospección del 28 de mayo se suspendió con dos buques nominados.

Con eso se construyeron tres instrumentos mensuales, en ventana móvil de doce meses para emparejar con el desembarque acumulado que usa el modelo: **Z1**, días con el AVPJM abierto; **Z2**, días con alguna agua nacional abierta; **Z3**, saldo de aperturas menos cierres de subárea. Y se corrieron las cuatro pruebas que corresponden: primera etapa, permutación del calendario entre años, IV solo y junto al conflicto, y exclusión.

## 2. Relevancia: sí, y sin depender de 2025

Ésta es la parte que funciona.

| Primera etapa de log(desembarque 12m) sobre log(Z1) | Coeficiente | t | R² parcial |
|---|---|---|---|
| Muestra completa, N = 138 | +2,03 | 6,9 | 0,60 |
| Sin 2025-2026, N = 124 | +1,34 | 3,5 | 0,40 |
| Sólo pre-pandemia (hasta feb-2020), N = 63 | +0,87 | 4,3 | — |
| Sin tendencia lineal | +0,83 | 3,2 | — |

Y bajo inferencia de diseño, que es la vara del §9.5: barajando mil veces las fechas de apertura y cierre entre años, **ningún calendario falso produce una primera etapa como la real** —mediana de placebos −0,02, percentil 95 +1,02, real +2,03; p = 0,000—. Sin 2025 igual: p = 0,000. A diferencia de la ventana del conflicto, acá la relevancia no cuelga de un episodio.

Z2 y Z3 no sirven: Z2 es en la práctica una indicadora del cambio de régimen de 2019-2020 (fuera del AVPJM se pescaba todo el año hasta la suspensión provisoria de noviembre de 2019), y Z3 cambia de signo según la muestra (−0,024 con t −2,0; +0,029 con t +2,6 sin 2025). Lo que sigue es sobre Z1.

## 3. El precio no responde

| Especificación | Forma reducida (precio sobre Z1) | f por IV | IC 95% |
|---|---|---|---|
| Base | −0,086 (t −0,5) | **−0,042** | [−0,20, +0,12] |
| Sin 2025-2026 | +0,216 (t +0,9) | +0,162 | [−0,21, +0,53] |
| Pre-pandemia | +0,477 (t +1,3) | +0,552 | [−0,24, +1,35] |
| Desde 2018 (con marcador SA01) | −0,003 (t 0,0) | −0,002 | [−0,25, +0,24] |
| Sin ventana de pandemia | −0,130 (t −0,7) | −0,064 | [−0,24, +0,11] |
| Con precio relativo rezagado 12 meses | −0,205 (t −1,6) | −0,094 | [−0,21, +0,02] |
| **Referencia: ventana del conflicto** | — | **−0,184** | [−0,34, −0,03] |

El calendario mueve la cantidad y el precio no se mueve. La forma reducida bajo permutación da p = 0,23 en la muestra completa: el efecto del calendario real sobre el precio es indistinguible del de un calendario barajado.

Y cuando se meten los dos instrumentos juntos, el test de sobreidentificación de Sargan **rechaza que identifiquen el mismo parámetro** (p = 0,020): −0,18 con el conflicto, −0,04 con el calendario, y el modelo dice que la diferencia no es azar.

## 4. Exclusión: la mitad de la evidencia está en contra

Para que el calendario sirva, tiene que mover la oferta por biología y no por el mercado. Tres piezas:

**A favor.** La fecha de apertura no responde al precio de la campaña anterior: +35 días por unidad de log del precio, t = 0,7, correlación +0,23. Y los criterios que las actas invocan para abrir y cerrar son biológicos: porcentaje de juveniles, relación macho/hembra, captura incidental de merluza.

**En contra, uno.** El largo de la temporada sí correlaciona con el precio de la campaña anterior: **−157 días por unidad de log, t = −2,4, correlación −0,58**. Las temporadas se acortaron en los mismos años en que el precio relativo subió. Buena parte de eso es tendencia común, y con tendencia la relación anual desaparece. Pero es exactamente el tipo de correlación que un instrumento no debería tener, y con trece temporadas no se puede separar tendencia de causalidad.

**En contra, dos, y es el que más pesa.** Sin 2025, la forma reducida es **positiva y significativa bajo permutación**: +0,216, p = 0,030. Más días de temporada, precio más alto. Un instrumento de oferta no puede producir ese signo; sólo lo produce un instrumento que lleva adentro información de demanda —por ejemplo, si la Autoridad de Aplicación mantiene abiertas las subáreas mientras el mercado absorbe y las cierra cuando deja de hacerlo.

## 5. Cómo leer la discrepancia entre −0,18 y −0,04

Hay dos explicaciones y no se pueden distinguir con estos datos.

**La económica.** El calendario es anticipado. Las decisiones del CFP son públicas, la apertura se conoce en mayo y el cierre se decide con semanas de aviso; flota, plantas y compradores lo incorporan a existencias y contratos antes de que llegue al precio spot. El conflicto de 2025 fue una sorpresa. En un bien almacenable, sólo el componente no anticipado de la oferta mueve el precio de la ventana de venta. Bajo esta lectura los dos instrumentos miden cosas distintas —y para la pregunta de política, que es un recorte *regulado* y por lo tanto anticipado, el relevante sería el calendario, que dice que el precio no se mueve y la facturación cae uno a uno con la cantidad.

**La econométrica.** El calendario viola la exclusión por el canal del punto 4, y el −0,04 está sesgado hacia cero. Con el precio rezagado como control —que absorbe parte de ese canal— la estimación baja a −0,09 con intervalo [−0,21, +0,02], a un paso del −0,18.

Las dos llevan al mismo lugar respecto de −1.

## 6. Lo que esto cambia en el informe

Tres cosas.

Primero, el §11 no puede seguir diciendo que el calendario del CFP es «la condición para que el parámetro sea estimable con precisión». Ya está codificado y no lo es: da relevancia, no identificación. Hay que reescribir ese pedido.

Segundo, la convergencia de la sección 9 y del Anexo A.8 gana una fila y una salvedad: el calendario da f entre −0,20 y +0,12, confirma el rechazo de −1 con más margen que ninguna otra construcción, y no confirma el valor puntual de −0,18.

Tercero, lo que sí falta ahora tiene nombre más preciso. No son las disposiciones de la DNCyFP —la precisión de las fechas no es el problema—. Es un desplazador de oferta que no pase por ninguna decisión de nadie: el **índice de biomasa o de reclutamiento pre-temporada del INIDEP**, que es lo que efectivamente decide cuánto hay para pescar y no lleva adentro ni al mercado ni a la Autoridad de Aplicación. Está en los informes de evaluación, campaña por campaña, y ya figura en la lista de pedidos.

## 7. Un hallazgo lateral

Las actas de las prospecciones reportan composición por talla del recurso en el agua: Acta 21/2025, SA 7, 68,1% L1 y 25,7% L2; Acta 22/2025, SA 14, 36,3% L1 y 4,4% L2. Es la variable que en su momento se pidió y se dio por inexistente. No sirve para el instrumento; sirve como lectura del recurso independiente del despacho de exportación.

---

*Reproducibilidad: `demanda_inversa_cfp.py`, con el calendario anual y sus fuentes escritos en el código; libro `cfp_calendario_codificado.xlsx` con las 289 decisiones, la cita literal de cada fecha, el resumen por año, las variables mensuales y la salida completa.*
