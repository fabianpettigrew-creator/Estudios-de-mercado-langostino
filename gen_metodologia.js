/*
 * Genera salidas/Metodologia_modelo_precios.docx (metodología y resultados del
 * modelo de anticipación del precio del entero: agregado, L1 y España).
 *
 * Uso:
 *     npm install          # una sola vez; baja la librería docx a node_modules/
 *     node gen_metodologia.js
 *
 * El destino se puede pisar con la variable de entorno OUT_DOCX.
 *
 * Los números NO se leen de los pkl: están escritos a mano en este archivo, así
 * que después de correr `python pronostico.py --l1 --es` hay que actualizarlos
 * acá. Los que vienen del pronóstico son la tabla 2.1 (backtest), la 2.2
 * (pronóstico vigente, incluido el último dato de cada serie), la 2.3
 * (sensibilidad, que sale de salidas/sensibilidad_desembarques.xlsx) y el
 * párrafo de cierre de la sección 3.
 *
 * Ojo con los horizontes: el pronóstico de España arranca un mes antes que el
 * del entero y el L1, porque el INDEC publica con un mes más de rezago que la
 * base de aduana. Toda tabla que ponga las series en paralelo tiene que decir
 * el mes calendario de cada columna (ver 2.3).
 */
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  Footer, PageNumber, TabStopType, Tab, LevelFormat, convertMillimetersToTwip,
} = require("docx");
const fs = require("fs");

// ---------- helpers ----------
const FUENTE = "Calibri";
const AZUL = "1F3864";
const GRIS = "595959";

const p = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: 120, line: 276 },
    ...opts.para,
    children: [new TextRun({ text, font: FUENTE, size: 22, ...opts.run })],
  });

const rico = (runs, opts = {}) =>
  new Paragraph({
    spacing: { after: 120, line: 276 },
    ...opts,
    children: runs.map(r => new TextRun({ font: FUENTE, size: 22, ...r })),
  });

const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 160 }, children: [new TextRun({ text: t, font: FUENTE, size: 28, bold: true, color: AZUL })] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 }, children: [new TextRun({ text: t, font: FUENTE, size: 24, bold: true, color: AZUL })] });

const vineta = t =>
  new Paragraph({
    numbering: { reference: "vinetas", level: 0 },
    spacing: { after: 80, line: 276 },
    children: [new TextRun({ text: t, font: FUENTE, size: 22 })],
  });
const vinetaRica = runs =>
  new Paragraph({
    numbering: { reference: "vinetas", level: 0 },
    spacing: { after: 80, line: 276 },
    children: runs.map(r => new TextRun({ font: FUENTE, size: 22, ...r })),
  });

function tabla(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const celda = (txt, esHeader, w, alineado) =>
    new TableCell({
      width: { size: w, type: WidthType.DXA },
      shading: esHeader ? { type: ShadingType.CLEAR, fill: "1F3864" } : undefined,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      children: [new Paragraph({
        alignment: alineado || AlignmentType.LEFT,
        children: [new TextRun({ text: txt, font: FUENTE, size: 20, bold: esHeader, color: esHeader ? "FFFFFF" : "000000" })],
      })],
    });
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => celda(h, true, widths[i])) }),
      ...rows.map(r => new TableRow({
        children: r.map((c, i) => celda(String(c), false, widths[i], i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER)),
      })),
    ],
  });
}

const espacio = () => new Paragraph({ spacing: { after: 120 }, children: [] });

// ---------- contenido ----------
const cuerpo = [
  new Paragraph({
    spacing: { after: 60 },
    children: [new TextRun({ text: "Modelo de anticipación del precio del langostino entero", font: FUENTE, size: 36, bold: true, color: AZUL })],
  }),
  new Paragraph({
    spacing: { after: 320 },
    children: [new TextRun({ text: "Metodología y resultados — agosto de 2026", font: FUENTE, size: 24, color: GRIS })],
  }),

  h1("1. Metodología"),
  p("El objetivo es pronosticar el FOB de exportación del langostino entero argentino (agregado y calibre L1) a uno, dos y tres meses, midiendo la capacidad predictiva contra el punto de referencia obligado —el paseo aleatorio: “el mejor pronóstico es el precio de hoy”— y traduciéndola a valor económico mediante una regla de decisión comercial."),

  h2("1.1 Datos"),
  tabla(
    ["Serie", "Fuente", "Período", "Uso"],
    [
      ["FOB entero (0306.17.10), USD/kg mensual", "INDEC base usuaria mensual (2013-2017, sin secreto) empalmada con base agregada de aduana (2017-02 en adelante); pu idéntico al 4º decimal en el solape", "2013-01 a 2026-07", "Serie objetivo principal"],
      ["FOB por calibre (L1/L2/L3) y destino", "Base de comercio transaccional (depurada). El grado viaja en prosa —«de 11 hasta 20 piezas por kg»— hasta 2017 y como código AI(L1) desde 2017-10; ambos se resuelven con los mismos tramos oficiales del NCM", "2013-01 a 2026-07", "Serie objetivo L1; índice de composición"],
      ["FOB entero a España (destino 410)", "INDEC base usuaria mensual por destino (0% secreto, sin huecos)", "2013-01 a 2026-06", "Serie objetivo España"],
      ["Captura tangonera mensual", "Desembarques SSPyA", "2013-2026", "Driver de oferta"],
      ["CIF España: langostino AR (CN 03061799) y vannamei Ecuador (03061792)", "EUMOFA / Comext", "2012-2025 (168 meses)", "Test de integración con el cultivo"],
    ],
    [2700, 2400, 1800, 2126],
  ),
  espacio(),

  h2("1.2 Capa 1 — ¿La serie mide precio o mezcla?"),
  p("Antes de modelar el FOB promedio hay que descartar que sus movimientos reflejen cambios de composición (más calibre chico, más participación de un destino barato) y no de precio. Se estimó un índice de precio puro por el método time-product-dummy: una regresión ponderada por kilos del logaritmo del precio sobre efectos fijos de celda (calibre × destino) y de mes; el índice es la exponencial de los efectos de mes. Se descartó el Laspeyres mensual encadenado porque exhibió deriva de encadenamiento (+15 puntos en cuatro años contra las celdas observadas directamente), un defecto conocido de encadenar con pesos de cantidad en frecuencia mensual."),
  rico([
    { text: "Resultado: correlación 0,991 entre el índice puro y el FOB promedio crudo; efecto composición de ±0,05 USD/kg. " },
    { text: "El FOB promedio del entero es un índice de precio válido sin ajuste.", bold: true },
  ]),
  p("La base transaccional entra al análisis ya depurada según el método documentado del estudio (duplicados exactos por 7 campos, subítems, filas vacías) más una regla nueva incorporada al extender la serie a 2013: los despachos fraccionados sin prorratear, donde el FOB total corresponde a la cantidad completa de la operación pero los kilos netos son solo la fracción despachada (FOB = unitario × cantidad, exacto), lo que infla el precio implícito hasta 100 veces. Se detectaron 208 casos en 2018, 31 en 2019 y 3 en 2022; se excluyen, no se reconstruyen."),
  p("Control de robustez: se verificó con histogramas finos del FOB unitario ponderados por kilos que no existe amontonamiento de declaraciones en torno a ningún valor puntual (bunching). No se detectan puntos de masa: la serie se comporta como precio de mercado puro."),

  h2("1.3 Capa 2 — Estructura"),
  rico([{ text: "Integración con el vannamei (Engle-Granger). ", bold: true },
    { text: "Sobre 168 meses de CIF España, ambas series son I(1) al borde de la estacionariedad; la regresión de cointegración arroja una elasticidad de largo plazo de 0,13 y el ADF sobre el residuo (−2,89) no rechaza al valor crítico de cointegración (−3,37). El test restringido sobre el premium (cociente langostino/vannamei) tampoco resulta estacionario (ADF −2,06). Conclusión: no hay ancla de largo plazo del langostino entero al camarón de cultivo en España, contra lo que la literatura de integración de mercados (Asche et al., 2017) documenta para otros pares de camarones. El traspaso de corto plazo existe pero es menor (0,16; t=2,1). El veredicto se re-verificó con la maquinaria completa (Johansen, statsmodels): el par langostino-vannamei no coíntegra (traza 15,05 contra un crítico de 15,49) y el premium es claramente no estacionario (p=0,77). En el sistema trivariado que agrega el CIF de Italia aparece un único vector de cointegración —y es revelador: relaciona España con Italia (elasticidad 0,81) con peso nulo del vannamei. El langostino entero está anclado a sí mismo en los distintos mercados europeos (ley de un precio intra-UE, con Italia haciendo el grueso del ajuste, t=3,9), no al camarón de cultivo. Ese equilibrio de destino, sin embargo, no anticipa el FOB de origen (correlación −0,09): no se incorpora al modelo de pronóstico." }]),
  rico([{ text: "Orden de integración: ADF y KPSS, nunca uno solo. ", bold: true },
    { text: "Los dos tests tienen hipótesis nulas opuestas —el ADF supone raíz unitaria, el KPSS supone estacionariedad— y por eso se leen cruzados: coinciden o el resultado no es concluyente. Aplicados a todas las series del modelo, el veredicto es nítido y tiene tres consecuencias. Primera: los tres FOB de origen (agregado, L1 y España) son estacionarios en niveles por ambos tests (ADF p≤0,002; KPSS sin rechazo), lo que valida la especificación —incluir el precio rezagado en niveles es correcto precisamente porque la serie revierte—. Segunda: el premium langostino/vannamei es I(1) por ambos tests (ADF p=0,77; KPSS p<0,01), de modo que la ausencia de anclaje al camarón de cultivo queda confirmada por partida doble. Tercera: el spread España-Italia es estacionario por ambos tests (ADF p<0,001; KPSS sin rechazo) incluso imponiendo elasticidad unitaria, una versión más exigente que la que estimó Johansen (0,81): la ley de un precio intra-UE sale reforzada." }]),
  p("El único signo de alarma fue la serie de Italia por separado, donde los dos tests se contradicen —señal típica de quiebre estructural—. El diagnóstico lo confirma y lo desactiva a la vez: hay un salto de nivel en febrero de 2021 (+18,5%), pero España tiene el suyo dos meses después y de magnitud casi igual (+15,5%), mientras que el vannamei quiebra en otro momento y en sentido contrario (abril de 2020, −12%). Es un shock común a los dos mercados europeos que se cancela en el spread, cuyo propio quiebre es de orden menor (F de 10,6 contra 94 y 117 en los niveles). Es exactamente lo que significa que dos series coíntegren, y refuerza la lectura de que el langostino europeo se ancla a sí mismo y no al cultivo."),
  rico([{ text: "Demanda inversa (Barten y Bettendorf, 1989). ", bold: true },
    { text: "En pesca la causalidad va de la cantidad al precio: la captura la determinan la biología, la administración del recurso y la flota, y el precio ajusta para vaciar el mercado. La ecuación estimada es:" }]),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 120 },
    children: [new TextRun({ text: "Δlog P(t) = a + b·log P(t−1) + c·log Tan3(t−1) + d·zafra(t) + e·dic_ene(t)", font: "Cambria Math", size: 22, italics: true })],
  }),
  p("donde Tan3 es la captura tangonera acumulada de tres meses (con un piso de 500 t para acotar los ceros del paro de 2025), zafra es una variable indicadora de noviembre a marzo y dic_ene captura la resaca post-fiestas: la demanda europea pica para las fiestas de fin de año pero se embarca en septiembre-noviembre; para diciembre-enero la compra ya está hecha y el precio afloja más de lo que la zafra sola explica (t=−3,1). La estimación es por mínimos cuadrados con errores Newey-West. La regresión anual precio-cantidad se descartó explícitamente por simultaneidad (arroja signo positivo: los años de buena captura coincidieron con demanda global fuerte); la identificación válida es mensual, con la oferta rezagada, que es predeterminada respecto del precio."),
  vinetaRica([{ text: "La oferta es significativa en el FOB de origen ", bold: false }, { text: "(t = −3,8 a −4,4 según la serie; flexibilidad de largo plazo ≈ −0,2: un 10% más de captura reduce el precio un 2%)." }]),
  vineta("El descuento de zafra es de 2 a 5% mensual entre noviembre y marzo."),
  vineta("El vannamei no es significativo en el FOB de origen: su influencia, débil, opera en el CIF de destino."),
  vineta("Se probó además una proxy de demanda observada (importaciones españolas de camarón congelado, EUMOFA 2012-2025, en variación interanual): no es significativa (t=0,6) y empeora el pronóstico en todos los horizontes. La estacionalidad de calendario le gana a la demanda medida: el dato de importaciones llega tarde y con ruido; el calendario de las fiestas se conoce perfecto y gratis."),

  h2("1.4 Capa 3 — Backtest y valor económico"),
  p("El backtest del entero corre ahora sobre 127 meses de prueba (2016-01 a 2026-07): una década que incluye la pandemia y el paro de 2025. Backtest rolling one-step-ahead: mínimo de 36 meses de entrenamiento, reestimación completa en cada paso y pronóstico iterado a 1-3 meses congelando la captura en el último dato conocido (el calendario de zafra sí se conoce hacia adelante). Ningún dato futuro entra en ninguna estimación. Las métricas:"),
  vinetaRica([{ text: "U de Theil", bold: true }, { text: " = RMSE del modelo / RMSE del naive (U < 1 significa ganarle al paseo aleatorio), desdoblado en subperíodos pre-paro (2023-01 a 2025-03) y paro+rebote (2025-04 a 2026-07) para verificar que el filo no dependa de un único episodio." }]),
  vinetaRica([{ text: "Acierto direccional", bold: true }, { text: " a un mes (¿el modelo acierta si el precio sube o baja?)." }]),
  vinetaRica([{ text: "Regla de timing", bold: true }, { text: ": cada mes se vende al contado salvo que el pronóstico a un mes supere el precio actual más un costo de espera del 1% mensual (financiero + frío); el ingreso acumulado se compara contra vender siempre al contado y contra el timing perfecto." }]),
  p("Las bandas de pronóstico (80%) surgen del RMSE empírico del backtest (±1,28·RMSE), no de supuestos distribucionales. Todo el circuito está implementado en pronostico.py (la opción --l1 corre además la serie del calibre L1), que imprime el backtest junto a cada pronóstico: ningún número se reporta sin su U de Theil al lado."),
  rico([{ text: "Límites. ", bold: true },
    { text: "La captura futura se congela en el último dato: un paro, una veda anticipada o un cierre de zafra atípico invalidan el pronóstico hasta recalcular. La banda a tres meses (±0,60 USD/kg) sirve para presupuestar y para la señal de timing, no para fijar precio de contrato. La muestra de test son 43 meses: suficiente para el veredicto general, corta para discriminar entre especificaciones parecidas." }]),

  h1("2. Resultados"),
  h2("2.1 Backtest (2023-01 a 2026-07)"),
  tabla(
    ["Serie / horizonte", "U total", "U pre-paro", "U paro+rebote", "Direccional 1m"],
    [
      ["Entero agregado — 1 mes", "0,88", "0,92", "0,78", "61%"],
      ["Entero agregado — 2 meses", "0,78", "0,84", "0,64", ""],
      ["Entero agregado — 3 meses", "0,72", "0,80", "0,51", ""],
      ["L1 — 1 mes", "0,94", "0,96", "0,80", "63%"],
      ["L1 — 2 meses", "0,87", "0,91", "0,68", ""],
      ["L1 — 3 meses", "0,83", "0,90", "0,56", ""],
      ["España — 1 mes", "0,85", "0,88", "0,75", "64%"],
      ["España — 2 meses", "0,69", "0,74", "0,57", ""],
      ["España — 3 meses", "0,64", "0,71", "0,40", ""],
    ],
    [2726, 1400, 1500, 1750, 1650],
  ),
  espacio(),
  p("El veredicto sobre el L1 pasó por tres etapas y vale contarlo porque ilustra el riesgo central de este estudio. Con la muestra 2020-2026 parecía que todo su filo provenía del episodio del paro. Al cargar lo que se creyó la serie transaccional completa, el veredicto pareció refutado — pero esa serie arrancaba en octubre de 2017, no en 2013: antes de esa fecha las descripciones aduaneras no traen el código de grado. Recuperado el calibre de los años previos a partir de la prosa («de 11 hasta 20 piezas por kg», que corresponde a los mismos tramos oficiales del NCM), la serie llega a 117 meses de prueba y vuelve la lectura original, esta vez con evidencia suficiente: en tiempos normales el L1 apenas le gana al paseo aleatorio a un mes (U de 0,96) y modestamente a dos y tres (0,91 y 0,90). Su filo real está en el shock de oferta, donde el U cae a 0,80 / 0,68 / 0,57. Uso correcto: el nivel se toma del agregado; el L1 sirve como señal direccional (acierta el signo en el 63% de los meses) y como alarma de oferta."),
  p("La reconstrucción de los años tempranos se validó por tres vías antes de adoptarla: el orden de precios por grado se replica casi idéntico en ambas notaciones (L1 6,56 contra 6,33 USD/kg; L5 4,07 contra 3,73), la serie reconstruida es menos volátil que la moderna (5,8% contra 6,6% mensual) y el modelo no rinde peor en ella. Quedan 10 meses sin ninguna fila con grado declarado (enero a junio de 2016 y junio a septiembre de 2017): se interpolan para no romper la estructura de rezagos y se excluyen de la puntuación del backtest."),
  p("El FOB a España —modelado por separado sobre el detalle mensual por destino de INDEC, donde España, por ser destino grande, no tiene una sola celda bajo secreto estadístico en toda la serie 2013-2026— resultó la serie más predecible de las tres: U de 0,85/0,69/0,64. La zafra pesa más que en el agregado (t=−5,7): España es el gran comprador de temporada. El desvío del precio España respecto del agregado, probado como término de corrección de error, no aporta (t=−1,4) y no se incluye. El pronóstico España corre con un mes más de rezago (el INDEC publica después que la base de aduana): con dato a jun-2026 (7,37 USD/kg), proyecta 7,33 / 7,30 / 7,27 para jul-sep."),
  p("Los tres modelos del entero le ganan al paseo aleatorio en el conjunto de la muestra, pero con reparos distintos según la serie, que se detallan a continuación."),

  h2("2.2 Pronóstico vigente (dato a julio de 2026)"),
  tabla(
    ["Mes", "Entero agregado (USD/kg)", "Banda 80%", "L1 (USD/kg)", "Banda 80%"],
    [
      ["Último dato (jul-26)", "7,31", "—", "7,26", "—"],
      ["ago-2026", "7,27", "6,89 – 7,67", "7,12", "6,60 – 7,68"],
      ["sep-2026", "7,24", "6,71 – 7,82", "7,00", "6,31 – 7,77"],
      ["oct-2026", "7,21", "6,58 – 7,91", "6,90", "6,13 – 7,76"],
    ],
    [1900, 2050, 1750, 1576, 1750],
  ),
  espacio(),
  rico([{ text: "Señal de timing: vender ahora. ", bold: true },
    { text: "La regla, aplicada mes a mes en el backtest extendido, habría rendido +0,9% de ingreso (entero) y +1,1% (L1) contra vender siempre al contado; el timing perfecto era +1,7% y +2,1% respectivamente." }]),

  h2("2.3 Sensibilidad a las toneladas desembarcadas"),
  p("Escenarios multiplicativos sobre la captura tangonera acumulada de tres meses (Tan3), sostenidos a lo largo del horizonte, aplicados sobre el modelo de producción reestimado en la muestra completa. Los valores son el tercer mes de pronóstico de cada serie, que no es el mismo mes calendario: el entero parte del dato de julio de 2026 y proyecta a octubre, mientras que España parte del dato de junio —el INDEC publica con un mes más de rezago que la base de aduana— y proyecta a septiembre. Las dos columnas se leen en paralelo como respuesta a la oferta, no como precios comparables del mismo mes:"),
  tabla(
    ["Escenario de captura", "Entero oct-26 (USD/kg)", "vs. base", "España sep-26 (USD/kg)", "vs. base"],
    [
      ["Paro (Tan3 al piso de 500 t)", "7,95", "+10,2%", "8,22", "+13,0%"],
      ["−50%", "7,32", "+1,4%", "7,42", "+2,0%"],
      ["−30%", "7,27", "+0,7%", "7,35", "+1,1%"],
      ["−15%", "7,24", "+0,3%", "7,31", "+0,5%"],
      ["Base (56,7 kt / 33,3 kt)", "7,21", "—", "7,27", "—"],
      ["+15%", "7,19", "−0,3%", "7,24", "−0,4%"],
      ["+30%", "7,17", "−0,5%", "7,22", "−0,8%"],
      ["+50%", "7,15", "−0,8%", "7,19", "−1,2%"],
    ],
    [2476, 1700, 1350, 1750, 1750],
  ),
  espacio(),
  vineta("La sensibilidad es fuertemente asimétrica: con la oferta en logaritmo, un ±30% de captura mueve el precio menos de 1% a tres meses, pero un colapso tipo paro lo dispara +10% (entero) y +13% (España). El precio no responde a las variaciones normales de zafra; responde a las rupturas de oferta — exactamente lo observado en 2025 y el escenario que el modelo mejor anticipa (U de 0,40-0,51 durante el paro)."),
  vineta("El ajuste es lento: la flexibilidad de largo plazo es ≈ −0,13 en ambas series (+10% de captura sostenida → −1,3% de precio en equilibrio), pero a tres meses solo se materializa −0,2/−0,3%. Esa digestión lenta de la oferta es la fuente del poder predictivo del modelo."),
  vineta("España amplifica: su coeficiente de oferta (−0,0105) es un 45% mayor que el del agregado (−0,0072). Ante una ruptura de oferta, el precio sube antes y más en España, el comprador de temporada."),
  p("Advertencia de uso: los escenarios de ±15/30/50% interpolan dentro del rango histórico observado; el escenario de paro está anclado en el episodio real de 2025, presente en la muestra. Lecturas más extremas extrapolarían la forma log-lineal fuera de lo visto. Detalle completo por horizonte en salidas/sensibilidad_desembarques.xlsx."),

  h2("2.4 Hipótesis testeadas y descartadas"),
  p("Un modelo vale tanto por lo que incorpora como por lo que probó y dejó afuera. Estas son las hipótesis evaluadas formalmente que no sobrevivieron, con el criterio de rechazo en cada caso."),
  rico([{ text: "Umbral de desembarques. ", bold: true },
    { text: "Referentes de la industria señalan que los compradores extranjeros miran los desembarques oficiales de la flota tangonera y, por encima de cierto volumen, ofrecen menos precio. La hipótesis implica que la respuesta del precio a la oferta no es continua —como la tiene el modelo— sino escalonada, y eso se testea con regresión de umbral: se busca por grilla el nivel de captura que mejor parte la muestra y se evalúa con sup-F, con p-valor por bootstrap wild. El bootstrap es imprescindible: buscar el mejor corte entre veintenas de candidatos infla el estadístico, y el p-valor convencional daría significativo casi siempre. Se probaron tres formas del umbral:" }]),
  vineta("Nivel absoluto de captura (acumulada de tres meses y mensual): sin quiebre en el rango alto (p=0,25 en el agregado; 0,25 y 0,30 en España)."),
  vineta("Anomalía respecto de la expectativa —«viene un N% arriba de lo normal para esta altura del año», con la norma estacional calculada solo con información pasada—: el peor resultado de los tres (p entre 0,34 y 0,85), y en el rango alto el coeficiente aparece con signo positivo, contrario a la hipótesis."),
  vineta("Acumulado de temporada (zafra tangonera de abril a noviembre): el único que roza la significancia, con un umbral en torno a 70 kt en el agregado y 66 kt en España, coeficiente de −0,02 y p de 0,100 y 0,113. Se verificó que no fuera calendario disfrazado: en 3 de 14 temporadas el umbral nunca se cruza y el mes de cruce varía entre agosto y noviembre."),
  p("El juez fuera de muestra descarta incluso esta última versión. Reestimando el umbral en cada ventana del backtest, el pronóstico empeora en los tres horizontes y en las dos series (agregado: 0,88 → 0,92, 0,78 → 0,83 y 0,72 → 0,76; España: 0,85 → 0,89, 0,69 → 0,76 y 0,64 → 0,68). Y un placebo de calendario —una simple variable indicadora de temporada avanzada, septiembre a noviembre, que no mira un solo dato de volumen— rinde igual o mejor que el modelo base: lo poco que el umbral capturaba era estacionalidad ya presente en el modelo."),
  p("La lectura no es que los referentes se equivoquen sobre lo que ocurre en la mesa de negociación. El comprador que ve desembarques fuertes efectivamente ofrece menos; el punto es que ese «menos» es proporcional y continuo —ya recogido por el término de oferta en logaritmo— y no tiene escalón. Lo refuerza que el efecto sea un 45% más fuerte en España, donde está la mayoría de esos compradores. Queda una versión sin testear: que el umbral opere por comprador o por contrato, invisible en el promedio agregado; exigiría dato transaccional identificado por comprador, que ninguna de las bases disponibles ofrece."),
  rico([{ text: "Nota sobre un falso positivo recurrente. ", bold: true },
    { text: "Con la grilla completa siempre aparece un umbral muy significativo en el extremo bajo de la distribución (6 a 12 kt, p<0,01). No es «mucho volumen»: es el interruptor entre flota parada y flota pescando, es decir veda o paro. Es un efecto real, pero distinto del que postula la hipótesis, y agregarlo al modelo también deteriora el pronóstico a dos y tres meses." }]),
  rico([{ text: "Proxy de demanda observada. ", bold: true },
    { text: "Las importaciones españolas de camarón congelado (EUMOFA 2012-2025, en variación interanual) no resultan significativas (t=0,6) y empeoran el pronóstico en todos los horizontes; el calendario de las fiestas, que se conoce de antemano y sin costo, hace mejor ese trabajo. Detalle en la capa 2." }]),
  rico([{ text: "Corrección de error contra el vannamei y contra el mercado europeo. ", bold: true },
    { text: "Ni el desvío respecto del camarón de cultivo (que no coíntegra) ni el equilibrio España-Italia hallado por Johansen (correlación de −0,09 con el FOB de origen) ni el desvío del precio a España respecto del agregado (t=−1,4) anticipan el precio de exportación. Ninguno se incorpora." }]),

  h1("3. Resumen en términos llanos"),
  p("¿Se puede predecir el precio del langostino? Un poco, y ese poco vale plata. El intento anterior había concluido que no: el precio mensual parecía una moneda al aire. El error estaba en qué serie se miraba —el promedio de todo junto (entero, colas, pelado)—. Al aislar el entero solo, apareció la señal."),
  p("La regla de oro es simple: mirar cuánto pescaron los tangoneros en los últimos tres meses. Si las bodegas vienen llenas, el precio va a aflojar; si la captura viene corta, va a firmar. El mercado no ajusta de golpe —tarda meses en digerir la oferta— y esa lentitud es exactamente lo que el modelo aprovecha. A eso se suma que en plena zafra (noviembre a marzo) el precio siempre cede un 2-5% mensual por la avalancha de mercadería. Con esas dos piezas se le gana al “va a valer lo mismo que hoy” por un margen amplio: a tres meses, el error de pronóstico se achica más de 40%."),
  p("También quedó claro lo que no funciona. El vannamei ecuatoriano, que uno imaginaría marcando el techo, resultó no mandar sobre el entero argentino: en España conviven hace catorce años sin que el precio de uno arrastre al del otro. Son negocios distintos: el entero se vende solo, contra su propia oferta. Y la vieja idea de que “el precio vuelve solo a su promedio” tampoco aporta nada por sí misma."),
  p("Los números de hoy, con dato a julio de 2026: el entero está en 7,31 USD/kg y el modelo lo ve apenas cediendo hasta octubre (~7,20). El L1 está en 7,26 y lo ve cayendo hacia ~6,90: está caro respecto de lo que la captura récord de este año justifica, y el pico estacional de septiembre-noviembre llegaría debilitado. La señal práctica es vender ahora, no guardar esperando suba. Esa regla de “vender o esperar”, aplicada mes a mes en el backtest, habría dejado un 1% más de ingreso; sobre un negocio de 900 millones de dólares, no es un decimal."),
  p("Una nota final sobre el L1, que es también la mejor moraleja del trabajo. Con pocos años de datos parecía que para ese calibre el modelo solo servía cuando la oferta se sacudía. Con más años pareció lo contrario. Y al reconstruir de verdad la serie completa —los años viejos declaraban el calibre en palabras, «de 11 hasta 20 piezas por kilo», no con el código que se usa hoy— volvió la primera lectura, ahora con el doble de evidencia: en años tranquilos el L1 es prácticamente impredecible mes a mes, y donde el modelo vale es cuando la oferta se rompe. Tres vueltas para la misma pregunta. Por eso la regla de la casa es no dar por buena ninguna conclusión sacada de una ventana corta, y por eso conviene mirar siempre el dato de contexto: no cuánto acierta un modelo, sino sobre cuántos meses se lo midió."),
];

// ---------- documento ----------
const doc = new Document({
  numbering: {
    config: [{
      reference: "vinetas",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 420, hanging: 210 } } },
      }],
    }],
  },
  styles: { default: { document: { run: { font: FUENTE, size: 22 } } } },
  sections: [{
    properties: {
      page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } }, // A4 por defecto
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: 9026 }],
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" } },
          children: [
            new TextRun({ text: "Lic. Fabián Pettigrew", font: FUENTE, size: 18, color: GRIS }),
            new TextRun({ children: [new Tab(), PageNumber.CURRENT], font: FUENTE, size: 18, color: GRIS }),
          ],
        })],
      }),
    },
    children: cuerpo,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = process.env.OUT_DOCX || String.raw`C:\Users\fmpet\OneDrive\IA agentes\Estudios de mercado langostino\salidas\Metodologia_modelo_precios.docx`;
  fs.writeFileSync(out, buf);
  console.log("OK ->", out);
});
