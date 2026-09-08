// Presentación para CEO de la industria tangonera. Sin jerga econométrica.
//
// Uso:  node deck_ceo.js "salidas/Langostino_tangonero_CEO.pptx"
//
// Este script ES la fuente del entregable: si hay que cambiar algo de la
// presentación, se cambia acá y se regenera. Para comprobar que el archivo de
// salidas/ sigue siendo lo que produce este código, correr:
//
//     python verificar_deck.py
//
// No comparar tamaños de archivo: pptxgenjs escribe con compresión mínima y
// PowerPoint recomprime, así que el entregable pesa ~170 KB y lo que sale de acá
// ~560 KB siendo el mismo contenido (descomprimidos, 520 contra 539 KB). Guardar
// desde PowerPoint también agrega partes propias —changesInfos, revisionInfo, un
// segundo theme, webextensions— y elimina los runs de texto vacíos. Nada de eso es
// una diferencia de contenido; verificar_deck.py las ignora y compara texto,
// gráficos, notas y medios.
const pptx = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Placa de destinos: las barras las calcula premium_destino_placa15.py, no se
// escriben acá. Si cambia el dato, correr ese script y regenerar.
const PREMIUM = JSON.parse(fs.readFileSync(
  path.join(__dirname, "salidas", "premium_destino_placa15.json"), "utf8"));
// Placa del canal: las series y las cifras las calcula horeca_placa.py.
const HORECA = JSON.parse(fs.readFileSync(
  path.join(__dirname, "salidas", "horeca_placa.json"), "utf8"));
const MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
  "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
const _hoy = new Date();
const FECHA = MESES[_hoy.getMonth()] + " de " + _hoy.getFullYear();

const p = new pptx();
p.layout = "LAYOUT_WIDE";              // 13.3 x 7.5
p.author = "Lic. Fabián Pettigrew";
p.company = "Lic. Fabián Pettigrew";
p.title = "Langostino tangonero: pescar menos no vende mejor";

const MAR = "12333F";   // azul profundo, dominante
const COR = "E2703A";   // coral del langostino, acento
const AREN = "F4EFE6";  // arena, fondo claro
const TEAL = "2E7D8F";  // apoyo
const GRIS = "5C6B73";
const BL = "FFFFFF";
const TIT = "Cambria", CUE = "Calibri";

const W = 13.3, H = 7.5, M = 0.7;

// ---------- helpers ----------
function fondoClaro(s) { s.background = { color: BL }; }
function fondoOscuro(s) { s.background = { color: MAR }; }

function titulo(s, t, oscuro) {
  s.addText(t, {
    x: M, y: 0.45, w: W - 2 * M, h: 0.95, isTextBox: true, margin: 0,
    fontFace: TIT, fontSize: 34, bold: true, color: oscuro ? BL : MAR,
    valign: "middle",
  });
}

function bajada(s, t, oscuro) {
  s.addText(t, {
    x: M, y: 1.4, w: W - 2 * M, h: 0.55, isTextBox: true, margin: 0,
    fontFace: CUE, fontSize: 15, color: oscuro ? "BFD3DA" : GRIS, italic: true,
    valign: "top",
  });
}

// círculo con número: el motivo que se repite en las láminas de contenido
function chapa(s, n, x, y, d) {
  d = d || 0.5;
  s.addShape(p.ShapeType.ellipse, {
    x: x, y: y, w: d, h: d, fill: { color: COR },
  });
  s.addText(String(n), {
    x: x, y: y, w: d, h: d, isTextBox: true, margin: 0,
    fontFace: CUE, fontSize: 15, bold: true, color: BL,
    align: "center", valign: "middle",
  });
}

function tarjeta(s, x, y, w, h, relleno) {
  s.addShape(p.ShapeType.roundRect, {
    x: x, y: y, w: w, h: h, rectRadius: 0.09,
    fill: { color: relleno || AREN },
    shadow: { type: "outer", angle: 90, blur: 8, offset: 0.05,
              color: "9AA5AA", opacity: 0.35 },
  });
}

function pie(s, t) {
  s.addText(t, {
    x: M, y: H - 0.62, w: W - 2 * M, h: 0.32, isTextBox: true, margin: 0,
    fontFace: CUE, fontSize: 9.5, color: "94A2A8", valign: "middle",
  });
}

// ============================================================ 1 · portada
let s = p.addSlide(); fondoOscuro(s);
s.addShape(p.ShapeType.ellipse, { x: 10.4, y: -1.5, w: 5.2, h: 5.2,
  fill: { color: "1B4657" } });
s.addShape(p.ShapeType.ellipse, { x: 11.9, y: 4.6, w: 3.4, h: 3.4,
  fill: { color: "1B4657" } });
s.addText("Consultoría económica y de comercio exterior", {
  x: M, y: 1.15, w: 9, h: 0.35, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 13, color: COR, bold: true });
s.addText("¿Conviene pescar menos\npara vender mejor?", {
  x: M, y: 1.75, w: 9.2, h: 2.1, isTextBox: true, margin: 0,
  fontFace: TIT, fontSize: 44, bold: true, color: BL, lineSpacing: 46 });
s.addText("Qué pasa con el precio del langostino cuando cambia la cantidad "
  + "que sale al mercado. Trece años de datos y un experimento natural.", {
  x: M, y: 4.0, w: 8.4, h: 0.9, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 16, color: "BFD3DA" });
s.addText(FECHA[0].toUpperCase() + FECHA.slice(1) + " · Lic. Fabián Pettigrew", {
  x: M, y: 5.5, w: 8, h: 0.35, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 13, color: "8FA9B3" });
s.addNotes("Objetivo: contestar si regular la oferta mejora lo que cobra la "
  + "flota. La respuesta corta es que no, y hay un lugar mejor donde buscar valor.");

// ============================================================ 2 · la pregunta
s = p.addSlide(); fondoClaro(s);
titulo(s, "La pregunta que contesta este trabajo");
bajada(s, "Dos creencias razonables, opuestas entre sí. Sólo una resiste el dato.");
[["Si sale menos mercadería,\nel precio sube y ganamos más",
  "Es la idea detrás de acortar zafras o cerrar temporadas antes. Vale sólo si el "
  + "precio sube MÁS de lo que cae el volumen.", "A"],
 ["El precio no lo ponemos nosotros:\nlo pone el mercado mundial",
  "Argentina es un jugador chico dentro del mercado global del camarón. Si es así, "
  + "recortar oferta resigna toneladas sin recuperar precio.", "B"]
].forEach(function (c, i) {
  const x = M + i * 6.15;
  tarjeta(s, x, 2.25, 5.55, 3.15, i === 1 ? "E8EFF1" : AREN);
  chapa(s, c[2], x + 0.35, 2.6, 0.52);
  s.addText(c[0], { x: x + 1.05, y: 2.58, w: 4.2, h: 0.95, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 17, bold: true, color: MAR });
  s.addText(c[1], { x: x + 0.35, y: 3.75, w: 4.9, h: 1.4, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 13.5, color: "3E4E55" });
});
s.addText("El trabajo mide cuál de las dos describe al langostino argentino, "
  + "y con qué margen.", {
  x: M, y: 5.75, w: W - 2 * M, h: 0.5, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 15, bold: true, color: MAR });
s.addNotes("No es una pregunta retórica: hay medidas concretas sobre la mesa "
  + "—acortar la zafra de Rawson, cerrar antes la zafra nacional— que asumen la A.");

// ============================================================ 3 · antecedentes
s = p.addSlide(); fondoClaro(s);
titulo(s, "Cómo se estudia esto en el mundo");
bajada(s, "La pregunta no es nueva. Hay literatura específica de pesquerías, y "
  + "de crustáceos en particular, que fija el método y da con qué comparar.");
const REF = [
  ["Barten y Bettendorf (1989)", "European Economic Review",
   "El trabajo fundacional: la cantidad llega al mercado ya decidida y el precio es "
   + "el que se acomoda."],
  ["Tabarestani y otros (2017)", "Marine Resource Economics",
   "Lleva ese enfoque al camarón en Estados Unidos, el mercado de referencia "
   + "mundial del producto."],
  ["Guillen y Maynou (2014)", "Scientia Marina",
   "Cómo se forma el precio en primera venta: qué pesa el volumen del día y qué "
   + "pesa la temporada."],
  ["Asche y otros (2017)", "Marine Resource Economics",
   "Los camarones del mundo suelen moverse juntos. Acá se testeó y NO se cumple "
   + "entre langostino y vannamei."],
  ["Huang (2015)", "Marine Resource Economics",
   "Cangrejo azul de Chesapeake: un recurso, varias calidades. Casi ninguna "
   + "responde al volumen, igual que acá."],
  ["Sun y otros (2019)", "PLOS ONE",
   "Atún rojo, la misma pregunta al revés. Ahí recortar sí puede pagar: el método "
   + "no trae el resultado adentro."],
];
REF.forEach(function (r, i) {
  const x = M + (i % 2) * 6.15, y = 2.12 + Math.floor(i / 2) * 1.56;
  tarjeta(s, x, y, 5.55, 1.42);
  s.addText(r[0], { x: x + 0.35, y: y + 0.13, w: 4.9, h: 0.32, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 14, bold: true, color: MAR });
  s.addText(r[1], { x: x + 0.35, y: y + 0.47, w: 4.9, h: 0.26, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 10.5, color: COR, bold: true });
  s.addText(r[2], { x: x + 0.35, y: y + 0.76, w: 4.9, h: 0.58, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 11, color: "3E4E55" });
});
pie(s, "Se sumó el INIDEP para la biología de la especie: el langostino renueva "
  + "casi toda su población entre temporadas, dato que condiciona el análisis.");
s.addNotes("El punto de esta lámina: el método no se inventó para este trabajo, "
  + "es el estándar de la disciplina, y uno de los supuestos de la literatura se "
  + "testeó y se rechazó.");

// ============================================================ 4 · el modelo
s = p.addSlide(); fondoClaro(s);
titulo(s, "El modelo: demanda inversa");
bajada(s, "Se llama así porque da vuelta la pregunta habitual. Y esa vuelta es "
  + "la que corresponde en una pesquería.");
[["La demanda común pregunta", "E8EFF1", MAR,
  "«A cada precio, ¿cuánto se vende?» Sirve cuando el que produce decide cuánto "
  + "sacar al mercado mirando el precio. Una fábrica, por ejemplo."],
 ["La demanda inversa pregunta", "FBEDE6", COR,
  "«Dada la cantidad que llegó, ¿a qué precio se vacía el mercado?» Sirve cuando "
  + "la cantidad viene dada: la deciden el recurso, la flota y el calendario."]
].forEach(function (c, i) {
  const x = M + i * 6.15;
  tarjeta(s, x, 2.2, 5.55, 1.95, c[1]);
  s.addText(c[0], { x: x + 0.35, y: 2.4, w: 4.9, h: 0.42, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 16, bold: true, color: c[2] });
  s.addText(c[3], { x: x + 0.35, y: 2.85, w: 4.9, h: 1.1, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12.5, color: "3E4E55" });
});
s.addText("El número que se estima se llama flexibilidad-precio: cuánto se mueve "
  + "el precio cuando la cantidad se mueve 1%. El umbral de decisión no es cero, "
  + "es 1 — recortar oferta sube el ingreso sólo si el precio se mueve más que "
  + "proporcionalmente.", {
  x: M, y: 4.35, w: W - 2 * M, h: 0.85, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 14, color: "3E4E55" });
[["−0,18", "ecuación instrumental,\nprecio transaccional"],
 ["−0,23", "registro oficial de aduana,\nsin marca de flota"],
 ["−0,27", "sistema de demanda inversa\nsobre importación europea"]
].forEach(function (c, i) {
  const x = M + i * 4.05;
  tarjeta(s, x, 5.3, 3.7, 1.35);
  s.addText(c[0], { x: x + 0.25, y: 5.45, w: 1.3, h: 0.65, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 24, bold: true, color: COR });
  s.addText(c[1], { x: x + 1.6, y: 5.48, w: 1.95, h: 0.95, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 10.5, color: GRIS });
});
pie(s, "Tres estimaciones con bases y métodos distintos. Ninguna se acerca al "
  + "umbral de 1: el más alto está a un cuarto del camino.");
s.addNotes("El marco es el de Barten y Bettendorf. Si preguntan por qué no una "
  + "demanda común: daría el signo al revés, porque los años de buena captura "
  + "coincidieron con años de demanda mundial fuerte.");

// ============================================================ 5 · la técnica
s = p.addSlide(); fondoClaro(s);
titulo(s, "La técnica: variable instrumental");
bajada(s, "Cruzar precio y captura no alcanza, y el motivo es concreto.");
tarjeta(s, M, 2.15, 5.55, 1.75, "FBEDE6");
s.addText("El problema", { x: M + 0.35, y: 2.33, w: 4.9, h: 0.4,
  isTextBox: true, margin: 0, fontFace: TIT, fontSize: 16, bold: true,
  color: COR });
s.addText("Los años de buena captura fueron también años de demanda mundial "
  + "fuerte. Precio y cantidad suben juntos por un tercer motivo, y la "
  + "correlación cruda da el signo al revés.", {
  x: M + 0.35, y: 2.75, w: 4.9, h: 1.05, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 12.5, color: "3E4E55" });
tarjeta(s, M + 6.15, 2.15, 5.55, 1.75, "E8EFF1");
s.addText("La solución", { x: M + 6.5, y: 2.33, w: 4.9, h: 0.4,
  isTextBox: true, margin: 0, fontFace: TIT, fontSize: 16, bold: true,
  color: MAR });
s.addText("Usar sólo la parte de la captura que se movió por un motivo ajeno al "
  + "mercado. Ese motivo se llama instrumento, y acá es el conflicto gremial "
  + "de 2025, que impidió que la flota zarpara a pescar.", {
  x: M + 6.5, y: 2.75, w: 4.9, h: 1.05, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 12.5, color: "3E4E55" });
[["Primera etapa", "Se aísla cuánto cayó la captura por el conflicto y no por "
  + "otra cosa."],
 ["Segunda etapa", "Se mide cómo se movió el precio ante esa parte, y sólo "
  + "ante esa parte."]
].forEach(function (c, i) {
  const x = M + i * 6.15;
  chapa(s, i + 1, x, 4.2, 0.55);
  s.addText(c[0], { x: x + 0.75, y: 4.21, w: 4.6, h: 0.55, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 14.5, bold: true, color: MAR,
    valign: "middle" });
  s.addText(c[1], { x: x + 0.75, y: 4.85, w: 4.6, h: 0.7, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12, color: GRIS });
});
[["138", "meses de serie"], ["2013-2026", "período estimado"],
 ["2 etapas", "mínimos cuadrados"], ["robustos", "errores estándar"]
].forEach(function (c, i) {
  const x = M + i * 3.05;
  tarjeta(s, x, 5.75, 2.75, 0.95, "E8EFF1");
  s.addText(c[0], { x: x + 0.15, y: 5.85, w: 2.45, h: 0.42, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 17, bold: true, color: MAR,
    align: "center" });
  s.addText(c[1], { x: x + 0.15, y: 6.26, w: 2.45, h: 0.3, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 10.5, color: GRIS, align: "center" });
});
s.addNotes("En la jerga: mínimos cuadrados en dos etapas, con la ventana del "
  + "conflicto como instrumento de la cantidad y errores robustos a "
  + "autocorrelación. No hace falta decirlo así salvo que lo pregunten.");

// ============================================================ 6 · datos
s = p.addSlide(); fondoClaro(s);
titulo(s, "Con qué datos");
bajada(s, "Todo lo que entra al modelo es registro oficial o base comercial de "
  + "despachos. Nada es estimación de escritorio.");
[["14", "fuentes primarias", "aduana, INDEC, SSPyA, Eurostat,\nEUMOFA, NOAA, FAO"],
 ["2013-2026", "trece años y medio", "mes a mes, sin huecos en\nla serie principal"],
 ["68.000", "despachos, uno por uno", "con precio, talla, destino\ny flota"],
 ["547", "actas del CFP", "descargadas y leídas:\n165 decisiones de oferta"],
 ["5", "flotas identificadas", "la tangonera se separa\ndel resto por el registro"]
].forEach(function (c, i) {
  const x = M + i * 2.42;
  tarjeta(s, x, 2.35, 2.2, 2.75);
  s.addText(c[0], { x: x + 0.12, y: 2.6, w: 1.96, h: 0.75, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 24, bold: true, color: COR,
    align: "center" });
  s.addText(c[1], { x: x + 0.12, y: 3.38, w: 1.96, h: 0.55, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12, bold: true, color: MAR,
    align: "center" });
  s.addText(c[2], { x: x + 0.12, y: 3.95, w: 1.96, h: 1.0, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 10, color: GRIS, align: "center" });
});
s.addText("Un detalle que importa: el registro aduanero marca el congelado a "
  + "bordo, así que se puede aislar el producto de la flota tangonera y no "
  + "mezclarlo con el de la fresquera, que es otro negocio y otro precio.", {
  x: M, y: 5.4, w: W - 2 * M, h: 0.8, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 14, color: "3E4E55" });
s.addNotes("Las fuentes están listadas una por una, con cobertura, unidad y "
  + "limitaciones, en un documento aparte. Las actas del CFP se incorporaron "
  + "en agosto de 2026 y todavía se están codificando.");

// ============================================================ 7 · el recurso
s = p.addSlide(); fondoClaro(s);
titulo(s, "El recurso en catorce años");
bajada(s, "Desembarque de langostino por flota. El total creció y después se "
  + "amesetó; lo que cambió de fondo es quién lo pesca.");
s.addChart(p.ChartType.bar, [
  { name: "Congeladora tangonera",
    labels: ["2013","2014","2015","2016","2017","2018","2019","2020","2021",
             "2022","2023","2024","2025","2026*"],
    values: [72130,78139,89399,100691,109540,119777,100171,55430,86941,90471,
             80877,90095,48284,59962] },
  { name: "Resto de la flota",
    labels: ["2013","2014","2015","2016","2017","2018","2019","2020","2021",
             "2022","2023","2024","2025","2026*"],
    values: [29631,50921,53398,77763,133622,135149,115367,128474,136539,119309,
             119658,132068,138746,84174] },
], {
  x: M, y: 2.4, w: 8.5, h: 3.5, barDir: "col", barGrouping: "stacked",
  chartColors: [COR, TEAL],
  showLegend: true, legendPos: "t", legendFontSize: 11, legendColor: GRIS,
  showTitle: false,
  catAxisLabelColor: GRIS, catAxisLabelFontSize: 9.5,
  valAxisLabelColor: GRIS, valAxisLabelFontSize: 9.5,
  valGridLine: { color: "E4E9EB", size: 1 }, catGridLine: { style: "none" },
  valAxisTitle: "toneladas desembarcadas", showValAxisTitle: true,
  valAxisTitleColor: GRIS, valAxisTitleFontSize: 10,
});
[["254.926 t", "el pico, en 2018", MAR],
 ["187.030 t", "2025: el 73% de ese pico", MAR],
 ["70,9% → 25,8%", "la participación tangonera,\nde 2013 a 2025", COR]
].forEach(function (c, i) {
  const y = 2.55 + i * 1.15;
  tarjeta(s, 9.5, y, 3.1, 1.0, i === 2 ? "FBEDE6" : AREN);
  s.addText(c[0], { x: 9.72, y: y + 0.1, w: 2.7, h: 0.42, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 17, bold: true, color: c[2] });
  s.addText(c[1], { x: 9.72, y: y + 0.5, w: 2.7, h: 0.45, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 10.5, color: GRIS });
});
pie(s, "SSPyA, planillas por puerto, flota, especie y mes. Auditado contra la "
  + "columna Total de cada hoja: diferencia máxima 0,0 t. (*) 2026 llega hasta "
  + "agosto.");
s.addNotes("El dato de fondo: la tangonera pesca hoy la misma cantidad que en "
  + "2015 pero pesa la mitad dentro del total, porque la fresquera se "
  + "multiplicó. Son dos negocios distintos y conviene no leerlos juntos.");

// ============================================================ 6 · el experimento
s = p.addSlide(); fondoClaro(s);
titulo(s, "El experimento que nadie quiso hacer");
bajada(s, "En 2025 el conflicto gremial dejó la flota parada cuatro meses. "
  + "Es la prueba que el dato no suele regalar: una caída de oferta que no la "
  + "causó el mercado.");
s.addChart(p.ChartType.bar, [
  { name: "2024", labels: ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],
    values: [0,0,0,6144,3291,22409,23418,22203,12627,0,0,0] },
  { name: "2025", labels: ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],
    values: [0,0,0,106,150,103,157,20889,21214,5663,0,0] },
], {
  x: M, y: 2.35, w: 8.1, h: 3.75,
  barDir: "col", barGrouping: "clustered",
  chartColors: [TEAL, COR],
  showLegend: true, legendPos: "t", legendFontSize: 11, legendColor: GRIS,
  showTitle: false,
  catAxisLabelColor: GRIS, catAxisLabelFontSize: 10,
  valAxisLabelColor: GRIS, valAxisLabelFontSize: 10,
  valGridLine: { color: "E4E9EB", size: 1 },
  catGridLine: { style: "none" },
  valAxisTitle: "toneladas desembarcadas", showValAxisTitle: true,
  valAxisTitleColor: GRIS, valAxisTitleFontSize: 10,
});
tarjeta(s, 9.2, 2.6, 3.4, 3.2, "E8EFF1");
s.addText("Abril a julio\nde 2025", { x: 9.5, y: 2.85, w: 2.8, h: 0.8,
  isTextBox: true, margin: 0, fontFace: TIT, fontSize: 17, bold: true,
  color: MAR });
s.addText("106 · 150 · 103 · 157", { x: 9.5, y: 3.7, w: 2.8, h: 0.45,
  isTextBox: true, margin: 0, fontFace: CUE, fontSize: 17, bold: true,
  color: COR });
s.addText("toneladas por mes, contra miles en cualquier año normal. La flota "
  + "no pescó menos: no salió.", { x: 9.5, y: 4.2, w: 2.8, h: 1.3,
  isTextBox: true, margin: 0, fontFace: CUE, fontSize: 12, color: "3E4E55" });
pie(s, "Desembarques de la flota congeladora tangonera. Fuente: Subsecretaría "
  + "de Pesca y Acuicultura.");
s.addNotes("La clave metodológica: el parate no lo causó el precio, así que "
  + "sirve para aislar el efecto de la cantidad sobre el precio.");

// ============================================================ 7 · el resultado
s = p.addSlide(); fondoOscuro(s);
titulo(s, "Qué pasó con el precio", true);
bajada(s, "La respuesta, en dos números que se leen sin econometría.", true);
[["−46%", "la captura tangonera", "de 90.095 a 48.284 toneladas entre 2024 y 2025"],
 ["+3,1%", "el precio del langostino", "medido contra el camarón de cultivo, para "
  + "descontar lo que hizo el mercado mundial"]
].forEach(function (c, i) {
  const x = M + i * 6.15;
  s.addShape(p.ShapeType.roundRect, { x: x, y: 2.5, w: 5.55, h: 2.6,
    rectRadius: 0.09, fill: { color: "1B4657" } });
  s.addText(c[0], { x: x + 0.4, y: 2.75, w: 4.75, h: 1.1, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 52, bold: true,
    color: i === 0 ? COR : "7FD1C0" });
  s.addText(c[1], { x: x + 0.4, y: 3.85, w: 4.75, h: 0.35, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 15, bold: true, color: BL });
  s.addText(c[2], { x: x + 0.4, y: 4.2, w: 4.75, h: 0.7, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12, color: "BFD3DA" });
});
s.addText("Se partió la oferta al medio y el precio se movió tres puntos. "
  + "Ese contraste no depende de ningún modelo: son los dos datos, uno al lado "
  + "del otro.", {
  x: M, y: 5.5, w: W - 2 * M, h: 0.8, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 16, color: BL });
pie(s, "Cómo se calcula: es el precio del langostino argentino dividido por el "
  + "precio del camarón de cultivo, 2025 contra 2024. Ese cociente subió 3,1%. "
  + "Al mirar el cociente y no el precio en dólares por kilo, queda descontado "
  + "lo que hizo el mercado mundial del camarón y sólo queda el movimiento "
  + "propio del langostino. Es dato observado, no salida de un modelo.");
s.addNotes("Este es el corazón del trabajo. Todo lo demás confirma o matiza "
  + "esta comparación.");

// ============================================================ 8 · el umbral
s = p.addSlide(); fondoClaro(s);
titulo(s, "¿Cuánto debería haber subido para que convenga?");
bajada(s, "Para que recortar oferta deje MÁS plata, el precio tiene que "
  + "compensar todo el volumen que se resigna. La cuenta es de almacenero.");
tarjeta(s, M, 2.35, 5.55, 2.9, AREN);
s.addText("86,6%", { x: M + 0.4, y: 2.6, w: 4.75, h: 1.15, isTextBox: true,
  margin: 0, fontFace: TIT, fontSize: 50, bold: true, color: MAR });
s.addText("lo que tendría que haber subido el precio", { x: M + 0.4, y: 3.75,
  w: 4.75, h: 0.4, isTextBox: true, margin: 0, fontFace: CUE, fontSize: 13.5,
  bold: true, color: MAR });
s.addText("sólo para que la facturación quedara igual que antes del parate",
  { x: M + 0.4, y: 4.15, w: 4.75, h: 0.7, isTextBox: true, margin: 0,
    fontFace: CUE, fontSize: 12, color: GRIS });
tarjeta(s, M + 6.15, 2.35, 5.55, 2.9, "E8EFF1");
s.addText("3,1%", { x: M + 6.55, y: 2.6, w: 4.75, h: 1.15, isTextBox: true,
  margin: 0, fontFace: TIT, fontSize: 50, bold: true, color: COR });
s.addText("lo que efectivamente subió", { x: M + 6.55, y: 3.75, w: 4.75,
  h: 0.4, isTextBox: true, margin: 0, fontFace: CUE, fontSize: 13.5,
  bold: true, color: MAR });
s.addText("veintiocho veces menos de lo necesario", { x: M + 6.55, y: 4.15,
  w: 4.75, h: 0.7, isTextBox: true, margin: 0, fontFace: CUE, fontSize: 12,
  color: GRIS });
s.addText("No es que el precio no reaccione. Reacciona, y en la dirección "
  + "esperada. Pero reacciona muchísimo menos de lo que haría falta para que "
  + "pescar menos sea negocio.", {
  x: M, y: 5.6, w: W - 2 * M, h: 0.8, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 15, bold: true, color: MAR });
pie(s, "El 3,1% es el cambio observado del precio del langostino medido contra "
  + "el camarón de cultivo, 2025 contra 2024. El 86,6% es aritmética pura: con "
  + "la captura en 48.284 t contra 90.095 t, el precio debería multiplicarse "
  + "por 90.095 ÷ 48.284 para que la facturación quedara igual.");
s.addNotes("Si alguien pide el número técnico: la flexibilidad-precio da "
  + "alrededor de −0,18, y el umbral para que convenga recortar es −1.");

// ============================================================ 9 · simulación
s = p.addSlide(); fondoClaro(s);
titulo(s, "Qué pasaría con un paquete de medidas concreto");
bajada(s, "Zafra de Rawson acortada a cuatro meses y cierre de la zafra "
  + "nacional a mediados de septiembre.");
[["−15.520 t", "de desembarque", "el 7,4% del total", MAR],
 ["+1,4%", "el precio", "proyectado, y relativo al camarón de cultivo", TEAL],
 ["−6,0%", "la facturación", "lo que se pierde en total", COR],
 ["−52", "millones de dólares", "por año, para el sector", COR]
].forEach(function (c, i) {
  const x = M + i * 3.05;
  tarjeta(s, x, 2.35, 2.75, 2.65);
  s.addText(c[0], { x: x + 0.2, y: 2.6, w: 2.35, h: 0.8, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 27, bold: true, color: c[3],
    align: "center" });
  s.addText(c[1], { x: x + 0.2, y: 3.4, w: 2.35, h: 0.35, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 13, bold: true, color: MAR,
    align: "center" });
  s.addText(c[2], { x: x + 0.2, y: 3.8, w: 2.35, h: 0.9, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 11, color: GRIS, align: "center" });
});
s.addText("El precio sube, sí. Pero sube 1,4% mientras el volumen cae 7,4%: "
  + "la cuenta da negativa por unos 52 millones de dólares al año.", {
  x: M, y: 5.4, w: W - 2 * M, h: 0.8, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 15, bold: true, color: MAR });
pie(s, "El precio proyectado es relativo al camarón de cultivo: mide cuánto se "
  + "despega el langostino argentino del referente mundial, no el precio en "
  + "dólares por kilo. Surge de aplicar la flexibilidad estimada (−0,184) al "
  + "recorte de volumen, no de una observación: el signo y el orden de magnitud "
  + "son firmes, la cifra exacta no.");
s.addNotes("El paquete es hipotético, construido sobre el desembarque medio "
  + "2022-2024. Sirve para dar orden de magnitud, no para pronosticar una "
  + "medida puntual.");

// ============================================================ 10 · franqueza
s = p.addSlide(); fondoClaro(s);
titulo(s, "Qué tan firme es esto");
bajada(s, "Conviene decirlo antes de que lo diga otro.");
[["Lo que está sólido", MAR, AREN,
  "El parate de 2025 fue un shock de oferta genuino, no un efecto del precio: "
  + "se verificó contra todas las ventanas alternativas posibles de la serie.\n\n"
  + "Las dos magnitudes del episodio —46% menos de captura, 3,1% más de precio— "
  + "son observación directa. No dependen de ningún modelo.\n\n"
  + "Tres estimaciones distintas, con bases y métodos distintos, dan lo mismo: "
  + "entre −0,18 y −0,27, todas lejísimos del umbral de −1."],
 ["Lo que no conviene afirmar", COR, "FBEDE6",
  "El valor exacto del parámetro. La estimación se apoya en un solo episodio, y "
  + "una prueba de robustez muestra que con un único shock no se puede defender "
  + "el número con decimales ni su intervalo.\n\n"
  + "Lo que se sostiene es el orden de magnitud y la conclusión de política, no "
  + "la precisión.\n\n"
  + "Para cerrarlo haría falta otro shock ajeno al mercado. El calendario del "
  + "CFP se probó y no sirve: sus decisiones siguen al recurso."]
].forEach(function (c, i) {
  const x = M + i * 6.15;
  tarjeta(s, x, 2.25, 5.55, 3.85, c[2]);
  s.addText(c[0], { x: x + 0.4, y: 2.48, w: 4.75, h: 0.45, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 17, bold: true, color: c[1] });
  s.addText(c[3], { x: x + 0.4, y: 3.0, w: 4.75, h: 2.9, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 11.5, color: "3E4E55",
    lineSpacing: 15 });
});
s.addNotes("Esta lámina es deliberada. Si el estudio se discute con un "
  + "tercero, la objeción del único episodio va a aparecer; es mejor haberla "
  + "puesto nosotros y haberla acotado.");

// ============================================================ 11 · transición
s = p.addSlide(); fondoOscuro(s);
s.addShape(p.ShapeType.ellipse, { x: -1.6, y: 3.9, w: 4.6, h: 4.6,
  fill: { color: "1B4657" } });
s.addText("Entonces, ¿dónde está el valor?", {
  x: M, y: 2.5, w: 10.5, h: 1.3, isTextBox: true, margin: 0,
  fontFace: TIT, fontSize: 40, bold: true, color: BL });
s.addText("Si la palanca del volumen no rinde, el mismo trabajo muestra tres "
  + "que sí. Ninguna cuesta toneladas.", {
  x: M, y: 3.9, w: 9.5, h: 0.9, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 17, color: "BFD3DA" });
s.addNotes("Bisagra de la presentación. De acá en adelante es agenda comercial.");

// ============================================================ 12 · palanca 1
s = p.addSlide(); fondoClaro(s);
chapa(s, 1, M, 0.5, 0.6);
s.addText("El canal manda más que la cantidad", {
  x: M + 0.85, y: 0.45, w: 11, h: 0.7, isTextBox: true, margin: 0,
  fontFace: TIT, fontSize: 32, bold: true, color: MAR, valign: "middle" });
bajada(s, "El langostino entero se come afuera de casa: restaurante, hotel, "
  + "catering. Cuando ese canal se mueve, el precio se mueve más que con la oferta.");
s.addChart(p.ChartType.bar, [{
  name: "Efecto sobre el precio",
  labels: ["Si HORECA cae 10%", "Si la captura cae 10%"],
  values: [-2.5, 1.8],
}], {
  x: M, y: 2.5, w: 7.6, h: 3.0, barDir: "bar",
  chartColors: [COR, TEAL], varyColors: true,
  showLegend: false, showTitle: false, showValue: true,
  dataLabelPosition: "outEnd", dataLabelColor: MAR, dataLabelFontSize: 13,
  dataLabelFormatCode: '+0.0"%";-0.0"%"',
  // sin esto las etiquetas se dibujan pegadas al eje cero y quedan ENCIMA de
  // la barra negativa; 'low' las manda al borde izquierdo del gráfico
  catAxisLabelPos: "low",
  catAxisLabelColor: MAR, catAxisLabelFontSize: 12,
  valAxisLabelColor: GRIS, valAxisLabelFontSize: 10,
  valGridLine: { color: "E4E9EB", size: 1 }, catGridLine: { style: "none" },
});
tarjeta(s, 8.7, 2.6, 3.9, 2.8, "E8EFF1");
s.addText("Qué hacer con esto", { x: 9.0, y: 2.82, w: 3.3, h: 0.4,
  isTextBox: true, margin: 0, fontFace: TIT, fontSize: 15, bold: true,
  color: MAR });
s.addText("Seguir la actividad HORECA de España, Italia, China y "
  + "Japón es más útil para anticipar el precio que seguir el propio "
  + "desembarque. Y no requiere resignar un solo kilo.", {
  x: 9.0, y: 3.3, w: 3.3, h: 1.9, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 12, color: "3E4E55" });
pie(s, "Las dos barras no están medidas contra la misma referencia: el efecto de "
  + "la captura es sobre el precio relativo al camarón de cultivo y el del canal "
  + "sobre el precio en euros. Sobre el precio relativo el canal pesa menos, "
  + "porque cuando cerró el canal HORECA también cayó el precio del cultivo. "
  + "Índice construido con estadística oficial de los cuatro destinos: INE, "
  + "ISTAT, Oficina Nacional de Estadística de China y METI.");
s.addNotes("Dato duro: en abril de 2020 el índice cayó 83% contra 2019. "
  + "Ninguna variable de oferta explica lo que pasó con el precio ese año.");

// ============================================ 12 bis · el canal, en detalle
s = p.addSlide(); fondoClaro(s);
titulo(s, "No todos los canales volvieron igual");
bajada(s, "Actividad HORECA en los cuatro destinos del L1, base 2019 = "
  + "100. El canal ya está por encima de la prepandemia. En uno, no.");
s.addChart(p.ChartType.line, [
  { name: HORECA.combinado.name, labels: HORECA.labels,
    values: HORECA.combinado.values },
  { name: HORECA.tarjetas[HORECA.tarjetas.length - 1].mercado, labels: HORECA.labels,
    values: HORECA.series.filter(function (x) {
      return x.name === HORECA.tarjetas[HORECA.tarjetas.length - 1].mercado;
    })[0].values },
], {
  x: M, y: 2.2, w: 8.5, h: 3.5,
  chartColors: [MAR, COR], lineSize: 1.75, lineDataSymbol: "none",
  showLegend: true, legendPos: "b", legendColor: GRIS, legendFontSize: 10,
  showTitle: false, valAxisMinVal: 0, valAxisMaxVal: 160,
  catAxisLabelColor: GRIS, catAxisLabelFontSize: 9,
  valAxisLabelColor: GRIS, valAxisLabelFontSize: 9,
  valGridLine: { color: "E4E9EB", size: 1 }, catGridLine: { style: "none" },
});
tarjeta(s, 9.35, 2.2, 3.25, 3.7, AREN);
s.addText("Dónde está cada mercado", { x: 9.62, y: 2.4, w: 2.75, h: 0.35,
  isTextBox: true, margin: 0, fontFace: TIT, fontSize: 14, bold: true,
  color: MAR });
s.addText("promedio de los últimos doce meses, y cuánto pesa en el volumen del L1", {
  x: 9.62, y: 2.76, w: 2.75, h: 0.55, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 9.5, color: GRIS });
HORECA.tarjetas.forEach(function (t, i) {
  const y = 3.35 + i * 0.50, ultimo = i === HORECA.tarjetas.length - 1;
  s.addText(t.mercado, { x: 9.62, y: y, w: 1.25, h: 0.3, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12, bold: ultimo,
    color: ultimo ? COR : MAR });
  s.addText(t.nivel.toFixed(1).replace(".", ","), { x: 10.85, y: y, w: 0.8, h: 0.3,
    isTextBox: true, margin: 0, fontFace: TIT, fontSize: 13, bold: true,
    color: ultimo ? COR : MAR, align: "right" });
  s.addText(t.peso_pct.toString().replace(".", ",") + "%", { x: 11.72, y: y + 0.03,
    w: 0.65, h: 0.28, isTextBox: true, margin: 0, fontFace: CUE, fontSize: 10,
    color: GRIS, align: "right" });
});
s.addText("Japón sigue " + Math.abs(HORECA.tarjetas[HORECA.tarjetas.length - 1]
  .brecha_pct).toFixed(0).replace(".", ",") + "% abajo de 2019 y no se recupera. "
  + "Es uno de cada nueve kilos de L1.", {
  x: 9.62, y: 5.15, w: 2.75, h: 0.62, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 10.5, bold: true, color: MAR });
pie(s, "En " + HORECA.pozo.mes + " el índice combinado tocó "
  + HORECA.pozo.nivel.toFixed(1).replace(".", ",") + ", un "
  + HORECA.pozo.caida_pct.toFixed(1).replace(".", ",") + "% por debajo de 2019, y no "
  + "volvió al nivel de 2019 hasta " + HORECA.vuelta_a_100 + ". Por eso el modelo "
  + "usa el índice observado y no una marca de pandemia. " + HORECA.pie);
s.addNotes("La placa no dice «dejemos Japón»: dice que el canal explica el precio y "
  + "que hay un mercado donde el canal no volvió. Sirve para leer la demanda de los "
  + "próximos meses sin esperar el dato propio, que llega más tarde.");

// ============================================================ 13 · palanca 2
s = p.addSlide(); fondoClaro(s);
chapa(s, 2, M, 0.5, 0.6);
s.addText("El mismo producto vale distinto según a dónde va", {
  x: M + 0.85, y: 0.45, w: 11, h: 0.7, isTextBox: true, margin: 0,
  fontFace: TIT, fontSize: 32, bold: true, color: MAR, valign: "middle" });
bajada(s, "Diferencia de precio del entero L1 contra España, a igual mes y "
  + "producto. España ancla el volumen al precio más bajo.");
s.addChart(p.ChartType.bar, [{
  name: "Diferencia contra España",
  labels: PREMIUM.labels,
  values: PREMIUM.values,
}], {
  x: M, y: 2.4, w: 7.9, h: 3.4, barDir: "col",
  chartColors: [TEAL], showLegend: false, showTitle: false, showValue: true,
  dataLabelPosition: "outEnd", dataLabelColor: MAR, dataLabelFontSize: 11,
  dataLabelFormatCode: '+0.0"%"',
  catAxisLabelColor: MAR, catAxisLabelFontSize: 10,
  valAxisLabelColor: GRIS, valAxisLabelFontSize: 10,
  valGridLine: { color: "E4E9EB", size: 1 }, catGridLine: { style: "none" },
});
tarjeta(s, 9.0, 2.6, 3.6, 3.0, AREN);
s.addText(PREMIUM.dispersion_txt, { x: 9.3, y: 2.82, w: 3.0, h: 0.4,
  isTextBox: true, margin: 0, fontFace: TIT, fontSize: 16, bold: true,
  color: COR });
s.addText("separan el destino más caro del más barato, sobre el mismo "
  + "producto físico y el mismo mes.\n\nEspaña se lleva el volumen: es el "
  + "comprador grande y paga el precio más bajo de la tabla. Ahí hay una "
  + "decisión comercial, no un dato de la naturaleza.", {
  x: 9.3, y: 3.3, w: 3.0, h: 2.1, isTextBox: true, margin: 0, fontFace: CUE,
  fontSize: 11.5, color: "3E4E55" });
pie(s, PREMIUM.pie);
s.addNotes(PREMIUM.nota_orador);

// ============================================================ 14 · palanca 3
s = p.addSlide(); fondoClaro(s);
chapa(s, 3, M, 0.5, 0.6);
s.addText("La flota y la talla ya son una ventaja: falta cobrarla", {
  x: M + 0.85, y: 0.45, w: 11, h: 0.7, isTextBox: true, margin: 0,
  fontFace: TIT, fontSize: 30, bold: true, color: MAR, valign: "middle" });
bajada(s, "El producto tangonero es otro negocio, y el entero grande es el "
  + "activo diferencial frente al camarón de cultivo.");
[["+25%", "vale el entero L1 tangonero\nsobre el mismo talle fresquero",
  "7,23 contra 5,80 dólares por kilo en 2025. Es congelado a bordo contra "
  + "procesado en tierra: distinto producto, distinto cliente."],
 ["3,4 veces", "más grande que el camarón\necuatoriano que llega a España",
  "El langostino entero L1 es un producto que el cultivo no replica. Ese "
  + "tamaño tiene un precio y hoy no se está cobrando entero."],
 ["−21%", "el descuento con que se vende\najustado por talla",
  "Contra camarón ecuatoriano equivalente en el mismo mercado. Es la brecha "
  + "que el trabajo mide por primera vez, y merece verificación propia."]
].forEach(function (c, i) {
  const x = M + i * 4.05;
  tarjeta(s, x, 2.4, 3.7, 3.3);
  s.addText(c[0], { x: x + 0.3, y: 2.62, w: 3.1, h: 0.75, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 28, bold: true, color: COR });
  s.addText(c[1], { x: x + 0.3, y: 3.4, w: 3.1, h: 0.75, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12.5, bold: true, color: MAR });
  s.addText(c[2], { x: x + 0.3, y: 4.2, w: 3.1, h: 1.35, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 11, color: "3E4E55" });
});
pie(s, "El descuento sale de 6,48 ÷ (6,01 × 1,36): entero L1 congelado a bordo "
  + "contra camarón ecuatoriano al mismo mercado y mes, ajustado por talla con "
  + "la elasticidad precio–piezas por kilo de −0,254 aplicada a 52 contra 15,5 "
  + "piezas por kilo. La unidad del conteo está inferida y el ajuste extrapola "
  + "fuera de muestra: según cómo se lea, el descuento va de 6% a 23%. "
  + "Indicativo, no establecido.");
s.addNotes("La tangonera pasó del 71% del desembarque total en 2013 al 26% en "
  + "2025. La participación cae, pero el valor por tonelada es el doble.");

// ============================================================ 15 · qué falta
s = p.addSlide(); fondoClaro(s);
titulo(s, "Qué falta para afinar el número");
bajada(s, "El primero se probó y no resuelve el problema. Los otros dos dependen "
  + "del sector.");
[["Calendario oficial de aperturas y cierres — PROBADO, NO ALCANZA",
  "Las 547 actas del CFP están leídas: 165 decisiones, 55 fechadas. Como "
  + "instrumento no identifican: el Consejo cierra cuando cae el rendimiento y "
  + "abre de a poco en años flojos, así que sus decisiones siguen al recurso en "
  + "vez de moverlo.", "probado"],
 ["Existencias mensuales de congelado",
  "Cuánto producto hay en cámara, por presentación y talla. Hoy medimos la "
  + "respuesta del precio al desembarque, no a lo que efectivamente llega al "
  + "mercado.", "Empresas"],
 ["Precio del competidor por calibre",
  "Precio europeo de importación abierto por rango de talla, con la unidad del "
  + "conteo declarada. Cierra la comparación con el vannamei.", "Proveedor"]
].forEach(function (c, i) {
  const y = 2.3 + i * 1.32;
  tarjeta(s, M, y, W - 2 * M, 1.15);
  chapa(s, i + 1, M + 0.3, y + 0.3, 0.55);
  s.addText(c[0], { x: M + 1.05, y: y + 0.14, w: 7.4, h: 0.42, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 15, bold: true, color: MAR });
  s.addText(c[1], { x: M + 1.05, y: y + 0.56, w: 7.4, h: 0.5, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 11.5, color: "3E4E55" });
  s.addText(c[2], { x: M + 8.75, y: y + 0.35, w: 2.6, h: 0.45, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 12, bold: true, color: COR,
    align: "right" });
});
s.addText("El paro de 2025 sigue siendo el único shock ajeno al recurso y al "
  + "mercado. Lo que se sostiene son sus magnitudes, no un parámetro preciso.", {
  x: M, y: 6.35, w: W - 2 * M, h: 0.5, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 13.5, color: GRIS });
s.addNotes("El primero es el más importante y el más barato: son documentos "
  + "públicos que hay que sistematizar.");

// ============================================================ 16 · cierre
s = p.addSlide(); fondoOscuro(s);
s.addShape(p.ShapeType.ellipse, { x: 10.9, y: 4.9, w: 4.2, h: 4.2,
  fill: { color: "1B4657" } });
titulo(s, "Tres conclusiones", true);
[["Recortar oferta no mejora el ingreso.",
  "Se partió la captura al medio y el precio subió 3,1%. Para que la cuenta "
  + "cerrara tendría que haber subido 86,6%."],
 ["El precio lo pone el mercado mundial, no la flota.",
  "El langostino argentino es tomador de precio dentro del mercado global del "
  + "camarón. La palanca del volumen es corta por definición."],
 ["El valor está en el canal, el destino y la talla.",
  "La actividad HORECA mueve el precio más que la propia captura, y "
  + "hay " + PREMIUM.dispersion_txt.toLowerCase() + " de diferencia entre "
  + "destinos por el mismo producto."]
].forEach(function (c, i) {
  const y = 2.1 + i * 1.42;
  chapa(s, i + 1, M, y + 0.08, 0.58);
  s.addText(c[0], { x: M + 0.85, y: y, w: 10.6, h: 0.45, isTextBox: true,
    margin: 0, fontFace: TIT, fontSize: 18, bold: true, color: BL });
  s.addText(c[1], { x: M + 0.85, y: y + 0.48, w: 10.6, h: 0.7, isTextBox: true,
    margin: 0, fontFace: CUE, fontSize: 13, color: "BFD3DA" });
});
s.addText("Lic. Fabián Pettigrew · " + FECHA, {
  x: M, y: 6.55, w: 8, h: 0.35, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 12, color: "8FA9B3" });
s.addNotes("Cierre: la recomendación no es hacer nada, es mover las palancas "
  + "que efectivamente pagan.");


// ============================================================================
// ANEXO METODOLÓGICO  (placas 19 a 26)
// Contenido portado de «salidas/ppt_anexo.py», que lo generaba en un segundo
// pase con python-pptx. Acá va en el mismo generador que el resto del deck,
// con los mismos helpers, para que haya una sola fuente reproducible.
// ============================================================================

// texto de anexo: interlineado 1,25 y párrafos separados con línea en blanco
function tx(s, x, y, w, h, t, size, color, bold, align) {
  const partes = (typeof t === "string") ? [t] : t;
  const runs = [];
  partes.forEach(function (linea, i) {
    if (i > 0) runs.push({ text: "", options: { breakLine: true } });
    if (typeof linea === "string") {
      runs.push({ text: linea, options: { breakLine: true } });
    } else {
      linea.forEach(function (q) {
        runs.push({ text: q[0], options: { bold: q[1], color: q[2], breakLine: true } });
      });
    }
  });
  s.addText(runs, {
    x: x, y: y, w: w, h: h, isTextBox: true, margin: 0, valign: "top",
    fontFace: CUE, fontSize: size, bold: !!bold, color: color,
    align: align || "left", lineSpacingMultiple: 1.25,
  });
}

function cabecera(s, t, b) { titulo(s, t); if (b) bajada(s, b); }

// ---------------------------------------------------------- 19 · portadilla
s = p.addSlide(); fondoOscuro(s);
s.addShape(p.ShapeType.ellipse, { x: 10.6, y: -1.2, w: 4.6, h: 4.6,
  fill: { color: "1B4657" } });
s.addText("Anexo metodológico", {
  x: M, y: 2.5, w: 10.5, h: 1.3, isTextBox: true, margin: 0,
  fontFace: TIT, fontSize: 40, bold: true, color: BL });
s.addText("Cómo está construido el número, con qué datos, y qué dice la "
  + "literatura que lo respalda.", {
  x: M, y: 3.9, w: 9.5, h: 0.9, isTextBox: true, margin: 0,
  fontFace: CUE, fontSize: 17, color: "BFD3DA" });
s.addNotes("De acá en adelante es material de respaldo: no se pasa en la "
  + "presentación, se usa para contestar preguntas.");

// ---------------------------------------------------- 20 · qué se estima
s = p.addSlide(); fondoClaro(s);
cabecera(s, "Qué se estima, y contra qué umbral",
  "Un solo parámetro ordena toda la discusión.");
tarjeta(s, M, 2.25, 5.55, 3.30);
tx(s, 1.10, 2.50, 4.75, 0.45, "La flexibilidad-precio", 17, MAR, true);
tx(s, 1.10, 3.05, 4.75, 2.30,
  ["Mide en cuánto por ciento se mueve el precio cuando la cantidad ofrecida se "
   + "mueve un uno por ciento. Es negativa por definición: más mercadería, "
   + "menos precio.",
   "Se estima sobre el precio del langostino relativo al camarón de cultivo, "
   + "para que el ciclo mundial no se cuele en el resultado."], 11.5, "3E4E55");
tarjeta(s, 6.85, 2.25, 5.55, 3.30);
tx(s, 7.25, 2.50, 4.75, 0.45, "El umbral no es cero, es 1", 17, COR, true);
tx(s, 7.25, 3.05, 4.75, 2.30,
  ["Como la facturación es precio por cantidad, recortar oferta la aumenta sólo "
   + "si el precio sube MÁS de lo que cae el volumen. En términos del "
   + "parámetro: sólo si es menor que −1.",
   [["Con −0,2, sacar el 10% de las toneladas sube el precio 2% y baja la "
     + "facturación 8%.", true, MAR]]], 11.5, "3E4E55");
pie(s, "No alcanza con que el parámetro sea negativo y estadísticamente "
  + "significativo: tiene que ser mayor que uno en valor absoluto.");

// ---------------------------------------------------------- 21 · qué entra
s = p.addSlide(); fondoClaro(s);
cabecera(s, "Qué entra al modelo",
  "Series mensuales de enero de 2013 a julio de 2026. Todo es registro oficial "
  + "o base comercial de despachos.");
[[M, 2.25, "Precio",
  "Valor unitario FOB del entero L1 congelado a bordo, despacho por despacho. "
  + "La flota se identifica por la marca de congelado a bordo: lo que la lleva "
  + "es tangonera, lo que no la lleva es fresquera."],
 [6.85, 2.25, "Cantidad",
  "Desembarque oficial por puerto, flota y mes. Es la variable que la política "
  + "mueve, y es exógena: no la decide el que vende."],
 [M, 4.35, "Competidor",
  "Precio del camarón de cultivo importado por la Unión Europea, y exportación "
  + "ecuatoriana por subpartida y país de destino, para comparar contra el "
  + "mismo mercado y el mismo mes."],
 [6.85, 4.35, "Demanda",
  "Índice mensual de actividad del canal HORECA en España, Italia, "
  + "China y Japón, construido con estadística oficial de los cuatro países."]
].forEach(function (c) {
  tarjeta(s, c[0], c[1], 5.55, 1.85);
  tx(s, c[0] + 0.40, c[1] + 0.22, 4.75, 0.40, c[2], 15, MAR, true);
  tx(s, c[0] + 0.40, c[1] + 0.70, 4.75, 1.00, c[3], 11.5, "3E4E55");
});
pie(s, "El desembarque de la flota tangonera es producto final que va directo a "
  + "exportación, sin reproceso: por eso su composición por talla se observa "
  + "en el despacho.");

// -------------------------------------------------- 22 · identificación
s = p.addSlide(); fondoClaro(s);
cabecera(s, "Por qué hace falta un experimento",
  "Precio y cantidad se determinan juntos. Cruzarlos sin más no mide la "
  + "demanda: mide una mezcla.");
tarjeta(s, M, 2.25, 5.55, 2.05);
tx(s, 1.10, 2.48, 4.75, 0.40, "2020 · un shock de DEMANDA", 15, MAR, true);
tx(s, 1.10, 2.98, 4.75, 1.20,
  "Con el canal HORECA cerrado, precio y cantidad cayeron juntos. "
  + "Leído sin distinguir, ese año «demuestra» que menos oferta baja el precio. "
  + "Es exactamente el sesgo que hay que sacar.", 11.5, "3E4E55");
tarjeta(s, 6.85, 2.25, 5.55, 2.05);
tx(s, 7.25, 2.48, 4.75, 0.40, "2025 · un shock de OFERTA", 15, COR, true);
tx(s, 7.25, 2.98, 4.75, 1.20,
  "La flota parada cuatro meses por un conflicto gremial, con la captura de "
  + "del año 46% abajo. La cantidad se movió por un motivo ajeno al mercado: "
  + "eso es lo que traza la curva de demanda.", 11.5, "3E4E55");
tarjeta(s, M, 4.60, 11.70, 1.55);
tx(s, 1.10, 4.85, 10.90, 0.40, "Cómo se usa", 15, MAR, true);
tx(s, 1.10, 5.35, 10.90, 0.70,
  "El conflicto entra como instrumento: se usa sólo la parte de la captura que "
  + "se movió por el parate de la flota. La primera etapa da F = 61, muy por "
  + "encima del umbral de 10 que se exige para que el instrumento sea fuerte. "
  + "El cierre del canal entra como control, con índice observado y no "
  + "supuesto.", 11.5, "3E4E55");

// ----------------------------------------------------- 23 · convergencia
s = p.addSlide(); fondoClaro(s);
cabecera(s, "Siete caminos, un número",
  "Se estimó por vías deliberadamente distintas —otras bases, otras unidades "
  + "de observación, otros métodos— para ver si el resultado dependía de la "
  + "construcción.");
// las siete de A.8 del anexo metodológico, en el mismo orden
[["Instrumental mensual, precio transaccional del L1", "−0,184"],
 ["Instrumental mensual, agregado de las dos tallas grandes", "−0,219"],
 ["Nivel campaña, con tendencia", "−0,196"],
 ["Las dos tallas grandes, con la participación del L2 como control", "−0,208"],
 ["Sistema de dos flotas, recompuesto", "−0,212"],
 ["Ecuación incondicional con desembarques por flota", "−0,239"],
 ["Sistema de demanda inversa por origen, importación europea", "−0,267"]
].forEach(function (f, i) {
  const y = 2.30 + i * 0.55;
  if (i % 2 === 0) tarjeta(s, M, y - 0.06, 8.60, 0.48);
  tx(s, 1.05, y + 0.04, 7.90, 0.35, f[0], 12, "3E4E55");
  tx(s, 6.60, y + 0.04, 2.50, 0.35, f[1], 12.5, MAR, true, "right");
});
tarjeta(s, 9.70, 2.24, 2.70, 4.45);
tx(s, 10.00, 2.50, 2.10, 0.45, "Todas rechazan", 15, COR, true);
tx(s, 10.00, 3.00, 2.10, 3.50,
  ["el umbral de −1 con holgura.",
   "El rango va de −0,18 a −0,27: el precio se mueve entre un quinto y "
   + "algo más de un cuarto de lo que se mueve la cantidad.",
   "Ninguna construcción se acerca al valor que haría conveniente recortar.",
   "Al sistema por origen se le impuso además la simetría teórica: da −0,282 "
   + "en vez de −0,267."],
  11.5, "3E4E55");
pie(s, "Bases, unidades de observación y métodos distintos. La convergencia es "
  + "el argumento: el número no es un artefacto de una construcción particular.");

// ----------------------------------------------------- 24 · limitaciones
s = p.addSlide(); fondoClaro(s);
cabecera(s, "Lo que el trabajo no puede afirmar",
  "Conviene tenerlo a mano antes de que lo pregunte otro.");
[["Glaseo",
  "No está considerado y no puede estarlo con dato de aduana: sobre los 67.844 "
  + "despachos de la base, siete mencionan glaseo y ninguno de ellos es entero "
  + "L1, y el nomenclador oficial no tiene código para declararlo."],
 ["Existencias",
  "No se miden. Lo que llega al mercado difiere de lo que se pescó entre −19% "
  + "y +24% según la campaña, y esa brecha es error de medición en la cantidad."],
 ["El valor exacto",
  "La identificación se apoya en un solo episodio. El signo y el orden de "
  + "magnitud son firmes; los decimales y el intervalo, no."],
 ["La tendencia",
  "Contra el mismo mercado, el precio relativo sube 1,1% por año. Comparar "
  + "España contra España explicó la mitad de la tendencia; esta otra mitad "
  + "todavía no. Los candidatos son certificación y góndola."]
].forEach(function (c, i) {
  const y = 2.30 + i * 1.12;
  tarjeta(s, M, y, 11.70, 0.95);
  tx(s, 1.10, y + 0.18, 2.60, 0.35, c[0], 14, COR, true);
  tx(s, 3.90, y + 0.16, 8.10, 0.70, c[1], 11.5, "3E4E55");
});
pie(s, "Ninguna de estas limitaciones cambia el signo del resultado: cambian "
  + "su precisión.");

// -------------------------------------------------- 25 y 26 · los estudios
function placaEstudios(t, b, items, nota) {
  const s2 = p.addSlide(); fondoClaro(s2);
  cabecera(s2, t, b);
  items.forEach(function (it, i) {
    const y = 2.25 + i * 2.05;
    tarjeta(s2, M, y, 11.70, 1.85);
    tx(s2, 1.10, y + 0.20, 5.20, 0.40, it[0], 14.5, MAR, true);
    tx(s2, 1.10, y + 0.68, 5.20, 0.28, it[1], 11, COR, true);
    tx(s2, 6.60, y + 0.20, 5.40, 1.45, it[2], 11.5, "3E4E55");
  });
  // la nota de estas dos placas ocupa dos renglones: arranca más arriba
  if (nota) s2.addText(nota, {
    x: M, y: H - 0.78, w: W - 2 * M, h: 0.5, isTextBox: true, margin: 0,
    fontFace: CUE, fontSize: 9.5, color: "94A2A8", valign: "top" });
  return s2;
}

placaEstudios("Los estudios que fijan el método",
  "Los dos primeros de la placa 3, en detalle.",
  [["Barten y Bettendorf (1989)", "European Economic Review",
    "El trabajo fundacional de la demanda inversa aplicada a pescado. Muestra "
    + "que en productos pesqueros hay que dar vuelta el análisis: la captura "
    + "llega al mercado ya decidida por el recurso y el calendario, y es el "
    + "precio el que se acomoda para vaciarlo. De ahí sale el sistema de "
    + "ecuaciones que se usa acá para estimar varias especies o flotas a la vez "
    + "respetando que el gasto total tiene que cerrar."],
   ["Tabarestani, Keithly y Marzoughi-Ardakani (2017)", "Marine Resource Economics",
    "Lleva ese enfoque al mercado del camarón en Estados Unidos, que es el "
    + "mercado de referencia mundial. Trata el desembarque salvaje del Golfo de "
    + "México como cantidad ya dada y el precio del camarón de cultivo "
    + "importado como dato externo. El resultado es el antecedente más directo "
    + "de este trabajo: un cambio de 1% en el precio del importado mueve 0,98% "
    + "el precio doméstico. El salvaje casi no tiene autonomía de precio frente "
    + "al cultivo."]],
  "Es el enfoque que corresponde cuando la cantidad no la decide el que vende.");

placaEstudios("Los estudios que acotan la expectativa",
  "Los dos últimos de la placa 3, más el aporte del INIDEP.",
  [["Guillen y Maynou (2014)", "Scientia Marina",
    "Estudia cómo se forma el precio en primera venta en pesquerías "
    + "mediterráneas, con la gamba roja catalana. Separa qué pesa el volumen "
    + "del día y qué pesa la temporada, y encuentra que el precio de primera "
    + "venta es 14% menor los martes y miércoles. La recomendación es de "
    + "calendario, no de recorte: concentrar la reducción de esfuerzo en los "
    + "días de precio bajo. Es el antecedente de la palanca del canal en este "
    + "trabajo."],
   ["Asche y otros (2017)", "Marine Resource Economics",
    "Documenta que los distintos camarones del mundo suelen moverse como un "
    + "solo mercado. Ese supuesto se testeó acá y NO se cumple entre el "
    + "langostino argentino y el vannamei de cultivo: son productos "
    + "diferenciados, no sustitutos perfectos. Es lo que deja lugar a la "
    + "palanca de talla y diferenciación, y lo que impide tratar al langostino "
    + "como una commodity más dentro del agregado camarón."]],
  "Se sumó el INIDEP para la biología de la especie: el langostino renueva casi "
  + "toda su población entre temporadas, y por eso la captura de un año no "
  + "sirve para predecir la del siguiente — un instrumento que se probó y se "
  + "descartó.");

p.writeFile({ fileName: process.argv[2] })
 .then(function (f) { console.log("escrito: " + f); });
