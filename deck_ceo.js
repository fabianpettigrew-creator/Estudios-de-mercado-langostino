// Generador del deck del langostino tangonero.
//
// Uso:  node deck_ceo.js "salidas/Estudio econométrico - testeo reducción  de captura.pptx"
//
// ATENCIÓN, LEER ANTES DE EDITAR. Este archivo NO es la fuente de autor del diseño.
// El deck se diseña en PowerPoint y este generador lo REPRODUCE: lo emite
// `extraer_deck.py`, que lee el PPT vigente y vuelca placa por placa la geometría, los
// rellenos y el formato del texto. Se hizo así porque el diseño nuevo tiene 639 formas
// sobre un lienzo de 20 x 11,25 pulgadas, con los gráficos rehechos como formas
// nativas: transcribirlo a mano sería adivinar coordenadas.
//
// En consecuencia:
//   · para cambiar el DISEÑO, se edita el PPT y se vuelve a correr `extraer_deck.py`;
//   · para cambiar un TEXTO puntual, se puede editar acá, en la constante PLACAS, y
//     regenerar — pero el cambio se pierde en la próxima extracción, así que conviene
//     hacerlo también en el PPT;
//   · `python verificar_deck.py` compara el entregable contra lo que sale de acá.
//
// Fuente del diseño: Estudio econométrico - testeo reducción  de captura.pptx
// Generado por extraer_deck.py el 09 de September de 2026
const pptxgen = require("pptxgenjs");
const path = require("path");

const MEDIA = path.join(__dirname, "salidas", "media_deck");

const PLACAS = [
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.0,
    "w": 9.68,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "LANGOSTINO ARGENTINO · FLOTA TANGONERA",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.784,
    "w": 9.064,
    "h": 3.471,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "¿Conviene pescar menos para vender mejor?",
        "sz": 84.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -1.68
       }
      ],
      "algn": "l",
      "lns": 0.735
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 6.672,
    "w": 2.083,
    "h": 0.021,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.067,
    "w": 8.798,
    "h": 1.492,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué pasa con el precio del langostino cuando cambia la cantidad que sale al mercado. Trece años de datos y un experimento natural.",
        "sz": 24.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.914,
    "w": 9.68,
    "h": 0.461,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SEPTIEMBRE DE 2026 · LIC. FABIÁN PETTIGREW",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 1.95
       }
      ],
      "algn": "l",
      "lns": 1.2594
     }
    ]
   },
   {
    "tipo": "img",
    "x": 10.806,
    "y": 1.542,
    "w": 8.028,
    "h": 8.243,
    "src": "image1.jpeg"
   }
  ],
  "notas": "Objetivo: contestar si regular la oferta mejora lo que cobra la flota. La respuesta corta es que no, y hay un lugar mejor donde buscar valor."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.627,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EL PLANTEO",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.001,
    "y": 0.708,
    "w": 0.915,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "02 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La pregunta que contesta este trabajo",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 19.433,
    "h": 0.495,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Dos creencias razonables, opuestas entre sí. Sólo una resiste el dato.",
        "sz": 22.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1821
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.757,
    "w": 8.542,
    "h": 5.546,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.633,
    "y": 4.224,
    "w": 8.369,
    "h": 0.708,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "A",
        "sz": 48.0,
        "c": "5980A6",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.633,
    "y": 5.099,
    "w": 7.837,
    "h": 1.086,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Si sale menos mercadería, el precio sube y ganamos más",
        "sz": 33.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.855
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.633,
    "y": 6.352,
    "w": 7.837,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Es la idea detrás de acortar zafras o cerrar temporadas antes. Vale sólo si el precio sube MÁS de lo que cae el volumen.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.292,
    "y": 3.757,
    "w": 8.542,
    "h": 5.546,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.758,
    "y": 4.224,
    "w": 8.369,
    "h": 0.708,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "B",
        "sz": 48.0,
        "c": "5980A6",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.758,
    "y": 5.099,
    "w": 7.837,
    "h": 1.086,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El precio no lo ponemos nosotros: lo pone el mercado mundial",
        "sz": 33.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.855
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.758,
    "y": 6.352,
    "w": 7.837,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Argentina es un jugador chico dentro del mercado global del ",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       },
       {
        "t": "camarón ",
        "sz": 20.25,
        "c": "2C455D",
        "f": "Barlow",
        "b": true
       },
       {
        "t": ". Si es así, recortar oferta resigna toneladas sin recuperar precio.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.804,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.104,
    "w": 18.197,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El trabajo mide cuál de las dos describe al langostino argentino, y con qué margen.",
        "sz": 21.75,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   }
  ],
  "notas": "No es una pregunta retórica: hay medidas concretas sobre la mesa —acortar la zafra de Rawson, cerrar antes la zafra nacional— que asumen la A."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 2.045,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANTECEDENTES",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.0,
    "y": 0.708,
    "w": 0.917,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "03 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cómo se estudia esto en el mundo",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 15.557,
    "h": 0.918,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La pregunta no es nueva. Hay literatura específica de pesquerías, y de crustáceos en particular, que fija el método y da con qué comparar.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.139,
    "w": 5.611,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.405,
    "w": 6.172,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Barten y Bettendorf (1989)",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.966,
    "w": 6.172,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EUROPEAN ECONOMIC REVIEW",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 1.8
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.561,
    "w": 5.779,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El trabajo fundacional: la cantidad llega al mercado ya decidida y el precio es el que se acomoda.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 7.194,
    "y": 4.139,
    "w": 5.611,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 4.405,
    "w": 6.172,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Tabarestani y otros (2017)",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 4.966,
    "w": 6.172,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MARINE RESOURCE ECONOMICS",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 1.8
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 5.561,
    "w": 5.779,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Lleva ese enfoque al camarón en Estados Unidos, el mercado de referencia mundial del producto.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 13.222,
    "y": 4.139,
    "w": 5.611,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 13.222,
    "y": 4.405,
    "w": 6.172,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Guillen y Maynou (2014)",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 13.222,
    "y": 4.966,
    "w": 6.172,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SCIENTIA MARINA",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 1.8
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 13.222,
    "y": 5.561,
    "w": 5.779,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cómo se forma el precio en primera venta: qué pesa el volumen del día y qué pesa la temporada.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.548,
    "w": 5.611,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.815,
    "w": 6.172,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Asche y otros (2017)",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.376,
    "w": 6.172,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MARINE RESOURCE ECONOMICS",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 1.8
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.971,
    "w": 5.779,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Los camarones del mundo suelen moverse juntos. Acá se testeó y NO se cumple entre langostino y vannamei.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 7.194,
    "y": 7.548,
    "w": 5.611,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 7.815,
    "w": 6.172,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Huang (2015)",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 8.376,
    "w": 6.172,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MARINE RESOURCE ECONOMICS",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 1.8
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 8.971,
    "w": 5.779,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cangrejo azul de Chesapeake: un recurso, varias calidades. Casi ninguna responde al volumen, igual que acá.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 13.222,
    "y": 7.548,
    "w": 5.611,
    "h": 2.993,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 13.564,
    "y": 8.233,
    "w": 5.076,
    "h": 1.667,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se sumó el INIDEP para la biología de la especie: el langostino renueva casi toda su población entre temporadas, dato que condiciona el análisis.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   }
  ],
  "notas": "El punto de esta lámina: el método no se inventó para este trabajo, es el estándar de la disciplina, y uno de los supuestos de la literatura se testeó y se rechazó."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.033,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MÉTODO",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.998,
    "y": 0.708,
    "w": 0.919,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "04 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El modelo: demanda inversa",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 19.433,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se llama así porque da vuelta la pregunta habitual. Y esa vuelta es la que corresponde en una pesquería.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.659,
    "w": 8.542,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.917,
    "w": 9.396,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La demanda común pregunta",
        "sz": 30.0,
        "c": "5D5D60",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.521,
    "w": 8.798,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "«A cada precio, ¿cuánto se vende?» Sirve cuando el que produce decide cuánto sacar al mercado mirando el precio. Una fábrica, por ejemplo.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.292,
    "y": 3.659,
    "w": 8.542,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 10.292,
    "y": 3.926,
    "w": 9.396,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La demanda inversa pregunta",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.292,
    "y": 4.53,
    "w": 8.798,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "«Dada la cantidad que llegó, ¿a qué precio se vacía el mercado?» Sirve cuando la cantidad viene dada: la deciden el recurso, la flota y el calendario.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.212,
    "w": 16.094,
    "h": 0.917,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El número que se estima se llama ",
        "sz": 21.0,
        "c": "1D1F20",
        "f": "Barlow"
       },
       {
        "t": "flexibilidad-precio ",
        "sz": 21.0,
        "c": "1D1F20",
        "f": "Barlow",
        "b": true
       },
       {
        "t": ": cuánto se mueve el precio cuando la cantidad se mueve 1%. El umbral de decisión no es cero, es 1 — recortar oferta sube el ingreso sólo si el precio se mueve más que proporcionalmente.",
        "sz": 21.0,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.707,
    "w": 5.611,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.966,
    "w": 6.172,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,18",
        "sz": 78.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.086,
    "w": 6.172,
    "h": 0.406,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ecuación instrumental, precio transaccional",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1824
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 7.194,
    "y": 7.707,
    "w": 5.611,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 7.966,
    "w": 6.172,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,23",
        "sz": 78.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.194,
    "y": 9.086,
    "w": 6.172,
    "h": 0.406,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "registro oficial de aduana, sin marca de flota",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1824
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 13.222,
    "y": 7.707,
    "w": 5.611,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 13.222,
    "y": 7.966,
    "w": 6.172,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,27",
        "sz": 78.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 13.222,
    "y": 9.086,
    "w": 5.779,
    "h": 0.771,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "sistema de demanda inversa sobre importación europea",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1824
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.149,
    "w": 19.433,
    "h": 0.434,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Tres estimaciones con bases y métodos distintos. Ninguna se acerca al umbral de 1: el más alto está a un cuarto del camino.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1781
     }
    ]
   }
  ],
  "notas": "El marco es el de Barten y Bettendorf. Si preguntan por qué no una demanda común: daría el signo al revés, porque los años de buena captura coincidieron con años de demanda mundial fuerte."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.033,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MÉTODO",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.999,
    "y": 0.708,
    "w": 0.917,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "05 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La técnica: variable instrumental",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 19.433,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cruzar precio y captura no alcanza, y el motivo es concreto.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.659,
    "w": 8.542,
    "h": 3.112,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.592,
    "y": 4.084,
    "w": 8.461,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EL PROBLEMA",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 2.88
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.592,
    "y": 4.659,
    "w": 7.922,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Los años de buena captura fueron también años de demanda mundial fuerte. Precio y cantidad suben juntos por un tercer motivo, y la correlación cruda da el signo al revés.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.292,
    "y": 3.659,
    "w": 8.542,
    "h": 3.112,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.717,
    "y": 4.084,
    "w": 8.461,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "LA SOLUCIÓN",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 2.88
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.717,
    "y": 4.659,
    "w": 7.922,
    "h": 1.729,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Usar sólo la parte de la captura que se movió por un motivo ajeno al mercado. Ese motivo se llama instrumento, y acá es el conflicto gremial de 2025, que impidió que la flota zarpara a pescar.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.23,
    "w": 8.542,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.488,
    "w": 0.233,
    "h": 0.567,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "1",
        "sz": 42.0,
        "c": "5980A6",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.566,
    "y": 7.488,
    "w": 8.323,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Primera etapa",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.566,
    "y": 7.984,
    "w": 8.323,
    "h": 0.448,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se aísla cuánto cayó la captura por el conflicto y no por otra cosa.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.292,
    "y": 7.23,
    "w": 8.542,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.292,
    "y": 7.488,
    "w": 0.318,
    "h": 0.567,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2",
        "sz": 42.0,
        "c": "5980A6",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.776,
    "y": 7.488,
    "w": 8.863,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Segunda etapa",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.776,
    "y": 7.984,
    "w": 8.299,
    "h": 0.854,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se mide cómo se movió el precio ante esa parte, y sólo ante esa parte.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.236,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.453,
    "w": 4.515,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "138",
        "sz": 46.5,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6678
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.138,
    "w": 4.515,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "meses de serie",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.688,
    "y": 9.453,
    "w": 4.515,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2013-2026",
        "sz": 46.5,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6678
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.688,
    "y": 10.138,
    "w": 4.515,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "período estimado",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.208,
    "y": 9.453,
    "w": 4.515,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2 etapas",
        "sz": 46.5,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6678
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.208,
    "y": 10.138,
    "w": 4.515,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "mínimos cuadrados",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.729,
    "y": 9.453,
    "w": 4.515,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "robustos",
        "sz": 46.5,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6678
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.729,
    "y": 10.138,
    "w": 4.515,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "errores estándar",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   }
  ],
  "notas": "En la jerga: mínimos cuadrados en dos etapas, con la ventana del conflicto como instrumento de la cantidad y errores robustos a autocorrelación. No hace falta decirlo así salvo que lo pregunten."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 2.011,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "BASE EMPÍRICA",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.999,
    "y": 0.708,
    "w": 0.917,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "06 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Con qué datos",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 19.433,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Todo lo que entra al modelo es registro oficial o base comercial de despachos. Nada es estimación de escritorio.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.784,
    "w": 3.533,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 4.692,
    "y": 3.784,
    "w": 0.01,
    "h": 5.614,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.092,
    "w": 3.557,
    "h": 0.942,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "14",
        "sz": 72.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.159,
    "w": 3.557,
    "h": 0.425,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "fuentes primarias",
        "sz": 24.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.667,
    "w": 3.33,
    "h": 1.129,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "aduana, INDEC, SSPyA, Eurostat, EUMOFA, NOAA, FAO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 4.7,
    "y": 3.784,
    "w": 3.533,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 8.225,
    "y": 3.784,
    "w": 0.01,
    "h": 5.614,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 4.992,
    "y": 4.092,
    "w": 3.03,
    "h": 1.842,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2013-2026",
        "sz": 72.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 4.992,
    "y": 6.059,
    "w": 3.236,
    "h": 0.425,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "trece años y medio",
        "sz": 24.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 4.992,
    "y": 6.567,
    "w": 3.03,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "mes a mes, sin huecos en la serie principal",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 8.233,
    "y": 3.784,
    "w": 3.533,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 11.758,
    "y": 3.784,
    "w": 0.01,
    "h": 5.614,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 8.525,
    "y": 4.092,
    "w": 3.236,
    "h": 0.942,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "68.000",
        "sz": 72.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 8.525,
    "y": 5.159,
    "w": 3.236,
    "h": 0.425,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "despachos, uno por uno",
        "sz": 24.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 8.525,
    "y": 5.667,
    "w": 3.03,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "con precio, talla, destino y flota",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.767,
    "y": 3.784,
    "w": 3.533,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 15.292,
    "y": 3.784,
    "w": 0.01,
    "h": 5.614,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 12.058,
    "y": 4.092,
    "w": 3.236,
    "h": 0.942,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "547",
        "sz": 72.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 12.058,
    "y": 5.159,
    "w": 3.236,
    "h": 0.425,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "actas del CFP",
        "sz": 24.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 12.058,
    "y": 5.667,
    "w": 3.03,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "descargadas y leídas: 165 decisiones de oferta",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 15.3,
    "y": 3.784,
    "w": 3.533,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 15.592,
    "y": 4.092,
    "w": 3.566,
    "h": 0.942,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "5",
        "sz": 72.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 15.592,
    "y": 5.159,
    "w": 3.566,
    "h": 0.425,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "flotas identificadas",
        "sz": 24.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 15.592,
    "y": 5.667,
    "w": 3.339,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "la tangonera se separa del resto por el registro",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.398,
    "w": 16.146,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.698,
    "w": 16.63,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Un detalle que importa: el registro aduanero marca el congelado a bordo, así que se puede aislar el producto de la flota tangonera y no mezclarlo con el de la fresquera, que es otro negocio y otro precio.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": "Las fuentes están listadas una por una, con cobertura, unidad y limitaciones, en un documento aparte. Las actas del CFP se incorporaron en agosto de 2026 y todavía se están codificando."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.634,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EL RECURSO",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.01,
    "y": 0.708,
    "w": 0.906,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "07 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.667,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El recurso en catorce años",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.7,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Desembarque de langostino por flota. El total creció y después se amesetó; lo que cambió de fondo es quién lo pesca.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.627,
    "w": 0.271,
    "h": 0.146,
    "fill": "416180"
   },
   {
    "tipo": "txt",
    "x": 1.562,
    "y": 3.54,
    "w": 2.712,
    "h": 0.35,
    "anchor": "t",
    "m": 0.0,
    "p": [
     {
      "runs": [
       {
        "t": "Congeladora tangonera",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1782
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 4.566,
    "y": 3.627,
    "w": 0.271,
    "h": 0.146,
    "fill": "B5D9FD"
   },
   {
    "tipo": "txt",
    "x": 4.962,
    "y": 3.54,
    "w": 1.887,
    "h": 0.35,
    "anchor": "t",
    "m": 0.0,
    "p": [
     {
      "runs": [
       {
        "t": "Resto de la flota",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1782
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.049,
    "y": 3.498,
    "w": 3.246,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "toneladas desembarcadas",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.129,
    "w": 12.833,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.11,
    "w": 0.01,
    "h": 5.028,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 1.3,
    "y": 7.127,
    "w": 0.772,
    "h": 0.582,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 1.3,
    "y": 7.709,
    "w": 0.772,
    "h": 1.42,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 2.217,
    "y": 6.585,
    "w": 0.772,
    "h": 1.004,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 2.217,
    "y": 7.588,
    "w": 0.772,
    "h": 1.541,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 3.135,
    "y": 6.318,
    "w": 0.772,
    "h": 1.049,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 3.135,
    "y": 7.367,
    "w": 0.772,
    "h": 1.762,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 4.052,
    "y": 5.616,
    "w": 0.772,
    "h": 1.531,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 4.052,
    "y": 7.147,
    "w": 0.772,
    "h": 1.983,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 4.97,
    "y": 4.341,
    "w": 0.772,
    "h": 2.63,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 4.97,
    "y": 6.971,
    "w": 0.772,
    "h": 2.158,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 5.888,
    "y": 4.11,
    "w": 0.772,
    "h": 2.66,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 5.888,
    "y": 6.77,
    "w": 0.772,
    "h": 2.359,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 6.805,
    "y": 4.883,
    "w": 0.772,
    "h": 2.274,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 6.805,
    "y": 7.157,
    "w": 0.772,
    "h": 1.973,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 7.723,
    "y": 5.51,
    "w": 0.772,
    "h": 2.53,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 7.723,
    "y": 8.04,
    "w": 0.772,
    "h": 1.089,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 8.64,
    "y": 4.727,
    "w": 0.772,
    "h": 2.69,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 8.64,
    "y": 7.418,
    "w": 0.772,
    "h": 1.711,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 9.558,
    "y": 4.998,
    "w": 0.772,
    "h": 2.349,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 9.558,
    "y": 7.347,
    "w": 0.772,
    "h": 1.782,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 10.476,
    "y": 5.184,
    "w": 0.772,
    "h": 2.354,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 10.476,
    "y": 7.538,
    "w": 0.772,
    "h": 1.591,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 11.393,
    "y": 4.758,
    "w": 0.772,
    "h": 2.6,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 11.393,
    "y": 7.357,
    "w": 0.772,
    "h": 1.772,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 12.311,
    "y": 5.45,
    "w": 0.772,
    "h": 2.73,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 12.311,
    "y": 8.181,
    "w": 0.772,
    "h": 0.949,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 13.228,
    "y": 6.293,
    "w": 0.772,
    "h": 1.656,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 13.228,
    "y": 7.95,
    "w": 0.772,
    "h": 1.179,
    "fill": "416180"
   },
   {
    "tipo": "txt",
    "x": 1.25,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2013",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.168,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2014",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 3.086,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2015",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 4.004,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2016",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 4.923,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2017",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.841,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2018",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 6.759,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2019",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.677,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2020",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 8.595,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2021",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 9.513,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2022",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.432,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2023",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.35,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2024",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 12.268,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2025",
        "sz": 18.0,
        "c": "1D2D3D",
        "f": "Barlow",
        "b": true
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 13.186,
    "y": 9.283,
    "w": 0.856,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2026*",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.667,
    "y": 3.881,
    "w": 4.167,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 14.667,
    "y": 4.106,
    "w": 4.583,
    "h": 0.792,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "254.926 t",
        "sz": 60.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.667,
    "y": 4.96,
    "w": 4.583,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "el pico, en 2018",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.667,
    "y": 5.739,
    "w": 4.167,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 14.667,
    "y": 5.964,
    "w": 4.583,
    "h": 0.792,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "187.030 t",
        "sz": 60.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.667,
    "y": 6.818,
    "w": 4.583,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2025: el 73% de ese pico",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.667,
    "y": 7.596,
    "w": 4.167,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 14.667,
    "y": 7.821,
    "w": 4.583,
    "h": 0.675,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "70,9% → 25,8%",
        "sz": 48.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.7125
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.667,
    "y": 8.559,
    "w": 4.292,
    "h": 0.771,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "la participación tangonera, de 2013 a 2025",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1824
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.963,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.179,
    "w": 18.197,
    "h": 0.404,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SSPyA, planillas por puerto, flota, especie y mes. Auditado contra la columna Total de cada hoja: diferencia máxima 0,0 t. (*) 2026 llega hasta agosto.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "El dato de fondo: la tangonera pesca hoy la misma cantidad que en 2015 pero pesa la mitad dentro del total, porque la fresquera se multiplicó. Son dos negocios distintos y conviene no leerlos juntos."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 3.54,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EL EXPERIMENTO NATURAL",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.996,
    "y": 0.708,
    "w": 0.92,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "08 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.667,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El experimento que nadie quiso hacer",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.7,
    "w": 16.094,
    "h": 0.887,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "En 2025 el conflicto gremial dejó la flota parada cuatro meses. Es la prueba que el dato no suele regalar: una caída de oferta que no la causó el mercado.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.05,
    "w": 0.271,
    "h": 0.146,
    "fill": "B5D9FD"
   },
   {
    "tipo": "txt",
    "x": 1.562,
    "y": 3.962,
    "w": 0.653,
    "h": 0.35,
    "anchor": "t",
    "m": 0.0,
    "p": [
     {
      "runs": [
       {
        "t": "2024",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1782
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 2.507,
    "y": 4.05,
    "w": 0.271,
    "h": 0.146,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 2.903,
    "y": 3.962,
    "w": 0.643,
    "h": 0.35,
    "anchor": "t",
    "m": 0.0,
    "p": [
     {
      "runs": [
       {
        "t": "2025",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1782
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 8.029,
    "y": 3.921,
    "w": 3.246,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "toneladas desembarcadas",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.171,
    "w": 9.814,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.512,
    "w": 0.01,
    "h": 4.667,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 3.479,
    "y": 4.512,
    "w": 3.481,
    "h": 4.659,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 3.479,
    "y": 4.512,
    "w": 0.01,
    "h": 4.659,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 6.952,
    "y": 4.512,
    "w": 0.01,
    "h": 4.659,
    "fill": "416180"
   },
   {
    "tipo": "rect",
    "x": 3.767,
    "y": 7.95,
    "w": 0.297,
    "h": 1.221,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 4.105,
    "y": 9.143,
    "w": 0.297,
    "h": 0.028,
    "fill": "2C455D"
   },
   {
    "tipo": "rect",
    "x": 4.589,
    "y": 8.514,
    "w": 0.296,
    "h": 0.657,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 4.927,
    "y": 9.138,
    "w": 0.297,
    "h": 0.033,
    "fill": "2C455D"
   },
   {
    "tipo": "rect",
    "x": 5.412,
    "y": 4.712,
    "w": 0.297,
    "h": 4.458,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 5.75,
    "y": 9.143,
    "w": 0.297,
    "h": 0.028,
    "fill": "2C455D"
   },
   {
    "tipo": "rect",
    "x": 6.234,
    "y": 4.512,
    "w": 0.296,
    "h": 4.659,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 6.572,
    "y": 9.134,
    "w": 0.297,
    "h": 0.037,
    "fill": "2C455D"
   },
   {
    "tipo": "rect",
    "x": 7.056,
    "y": 4.754,
    "w": 0.297,
    "h": 4.417,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 7.395,
    "y": 5.015,
    "w": 0.297,
    "h": 4.156,
    "fill": "2C455D"
   },
   {
    "tipo": "rect",
    "x": 7.879,
    "y": 6.66,
    "w": 0.296,
    "h": 2.511,
    "fill": "B5D9FD"
   },
   {
    "tipo": "rect",
    "x": 8.217,
    "y": 4.95,
    "w": 0.297,
    "h": 4.221,
    "fill": "2C455D"
   },
   {
    "tipo": "rect",
    "x": 9.039,
    "y": 8.043,
    "w": 0.297,
    "h": 1.127,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 1.25,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Ene",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.073,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Feb",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.896,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Mar",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 3.719,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Abr",
        "sz": 18.0,
        "c": "1D2D3D",
        "f": "Barlow",
        "b": true
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 4.542,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "May",
        "sz": 18.0,
        "c": "1D2D3D",
        "f": "Barlow",
        "b": true
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.365,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Jun",
        "sz": 18.0,
        "c": "1D2D3D",
        "f": "Barlow",
        "b": true
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 6.188,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Jul",
        "sz": 18.0,
        "c": "1D2D3D",
        "f": "Barlow",
        "b": true
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.011,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Ago",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.834,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Sep",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 8.657,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Oct",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 9.48,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Nov",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.303,
    "y": 9.325,
    "w": 0.719,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Dic",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.564,
    "y": 3.921,
    "w": 7.27,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 11.564,
    "y": 4.146,
    "w": 7.996,
    "h": 0.715,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Abril a julio de 2025",
        "sz": 51.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.7125
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.564,
    "y": 5.152,
    "w": 7.996,
    "h": 0.667,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "106 · 150 · 103 · 157",
        "sz": 45.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "spc": 0.9
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.564,
    "y": 5.923,
    "w": 7.488,
    "h": 0.854,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "toneladas por mes, contra miles en cualquier año normal. La flota no pescó menos: no salió.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.564,
    "y": 7.671,
    "w": 7.27,
    "h": 2.042,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.963,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.179,
    "w": 18.197,
    "h": 0.404,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Desembarques de la flota congeladora tangonera. Fuente: Subsecretaría de Pesca y Acuicultura.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "La clave metodológica: el parate no lo causó el precio, así que sirve para aislar el efecto de la cantidad sobre el precio."
 },
 {
  "fondo": "1D2D3D",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.926,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EL RESULTADO",
        "sz": 18.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.001,
    "y": 0.708,
    "w": 0.916,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "09 / 28",
        "sz": 18.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.75,
    "w": 19.433,
    "h": 0.952,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué pasó con el precio",
        "sz": 63.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.94
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.847,
    "w": 19.433,
    "h": 0.495,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La respuesta, en dos números que se leen sin econometría.",
        "sz": 22.5,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1821
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.678,
    "w": 8.417,
    "h": 0.017,
    "fill": "B5D9FD"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.987,
    "w": 9.258,
    "h": 2.013,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−46%",
        "sz": 138.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "spc": -3.3
       }
      ],
      "algn": "l",
      "lns": 0.7167
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.166,
    "w": 9.258,
    "h": 0.569,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "la captura tangonera",
        "sz": 33.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.818,
    "w": 9.258,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "de 90.095 a 48.284 toneladas entre 2024 y 2025",
        "sz": 20.25,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.417,
    "y": 3.678,
    "w": 8.417,
    "h": 0.017,
    "fill": "B5D9FD"
   },
   {
    "tipo": "txt",
    "x": 10.417,
    "y": 3.987,
    "w": 9.258,
    "h": 2.013,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+3,1%",
        "sz": 130.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "spc": -3.3
       }
      ],
      "algn": "l",
      "lns": 0.7167
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.417,
    "y": 6.166,
    "w": 9.258,
    "h": 0.569,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "el precio del langostino",
        "sz": 33.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.417,
    "y": 6.818,
    "w": 8.669,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "medido contra el camarón de cultivo, para descontar lo que hizo el mercado mundial",
        "sz": 20.25,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.04,
    "w": 16.63,
    "h": 0.948,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se partió la oferta al medio y el precio se movió tres puntos. Ese contraste no depende de ningún modelo: son los dos datos, uno al lado del otro.",
        "sz": 22.5,
        "c": "F2F2F3",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1821
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.238,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.454,
    "w": 18.197,
    "h": 1.129,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cómo se calcula: es el precio del langostino argentino dividido por el precio del camarón de cultivo, 2025 contra 2024. Ese cociente subió 3,1%. Al mirar el cociente y no el precio en dólares por kilo, queda descontado lo que hizo el mercado mundial del camarón y sólo queda el movimiento propio del langostino. Es dato observado, no salida de un modelo.",
        "sz": 18.0,
        "c": "B5D9FD",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "Este es el corazón del trabajo. Todo lo demás confirma o matiza esta comparación."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.457,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "LA CUENTA",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.038,
    "y": 0.708,
    "w": 0.879,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "10 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "¿Cuánto debería haber subido para que convenga?",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 16.094,
    "h": 0.918,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Para que recortar oferta deje MÁS plata, el precio tiene que compensar todo el volumen que se resigna. La cuenta es de almacenero.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 9.992,
    "y": 4.383,
    "w": 0.01,
    "h": 3.384,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.383,
    "w": 8.974,
    "h": 2.102,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "86,6%",
        "sz": 172.5,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6431
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.694,
    "w": 8.974,
    "h": 0.569,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "lo que tendría que haber subido el precio",
        "sz": 33.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.346,
    "w": 8.974,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "sólo para que la facturación quedara igual que antes del parate",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.667,
    "y": 4.383,
    "w": 8.983,
    "h": 2.102,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "3,1%",
        "sz": 172.5,
        "c": "597EA3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6431
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.667,
    "y": 6.694,
    "w": 8.983,
    "h": 0.569,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "lo que efectivamente subió",
        "sz": 33.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8625
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.667,
    "y": 7.346,
    "w": 8.983,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "veintiocho veces menos de lo necesario",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.512,
    "w": 17.167,
    "h": 0.887,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "No es que el precio no reaccione. Reacciona, y en la dirección esperada. Pero reacciona muchísimo menos de lo que haría falta para que pescar menos sea negocio.",
        "sz": 21.75,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1802
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.588,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.783,
    "w": 18.197,
    "h": 0.8,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El 3,1% es el cambio observado del precio del langostino medido contra el camarón de cultivo, 2025 contra 2024. El 86,6% es aritmética pura: con la captura en 48.284 t contra 90.095 t, el precio debería multiplicarse por 90.095 ÷ 48.284 para que la facturación quedara igual.",
        "sz": 19.5,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1375
     }
    ]
   }
  ],
  "notas": "Si alguien pide el número técnico: la flexibilidad-precio da alrededor de −0,18, y el umbral para que convenga recortar es −1."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.616,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SIMULACIÓN",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.09,
    "y": 0.708,
    "w": 0.827,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "11 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué pasaría con un paquete de medidas concreto",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 19.433,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Zafra de Rawson acortada a cuatro meses y cierre de la zafra nacional a mediados de septiembre.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.28,
    "w": 4.417,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 5.575,
    "y": 4.28,
    "w": 0.01,
    "h": 3.043,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.588,
    "w": 4.482,
    "h": 1.148,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−15.520 t",
        "sz": 88.5,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6712
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.882,
    "w": 4.482,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "de desembarque",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.567,
    "w": 4.482,
    "h": 0.419,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "el 7,4% del total",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2247
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 5.583,
    "y": 4.28,
    "w": 4.417,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 9.992,
    "y": 4.28,
    "w": 0.01,
    "h": 3.043,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 5.917,
    "y": 4.588,
    "w": 4.116,
    "h": 1.148,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+1,4%",
        "sz": 88.5,
        "c": "597EA3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6712
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.917,
    "y": 5.882,
    "w": 4.116,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "el precio",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.917,
    "y": 6.567,
    "w": 3.854,
    "h": 0.797,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "proyectado, y relativo al camarón de cultivo",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2247
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.0,
    "y": 4.28,
    "w": 4.417,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 14.408,
    "y": 4.28,
    "w": 0.01,
    "h": 3.043,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.333,
    "y": 4.588,
    "w": 4.116,
    "h": 1.148,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−6,0%",
        "sz": 88.5,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6712
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.333,
    "y": 5.882,
    "w": 4.116,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "la facturación",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.333,
    "y": 6.567,
    "w": 4.116,
    "h": 0.419,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "lo que se pierde en total",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2247
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.417,
    "y": 4.28,
    "w": 4.417,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 14.75,
    "y": 4.588,
    "w": 4.492,
    "h": 1.148,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−52",
        "sz": 88.5,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6712
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.75,
    "y": 5.882,
    "w": 4.492,
    "h": 0.623,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "millones de dólares",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.75,
    "y": 6.567,
    "w": 4.492,
    "h": 0.419,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "por año, para el sector",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2247
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.402,
    "w": 17.167,
    "h": 0.948,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El precio sube, sí. Pero sube 1,4% mientras el volumen cae 7,4%: la cuenta da negativa por unos 52 millones de dólares al año.",
        "sz": 22.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1821
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.6,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.817,
    "w": 18.197,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El precio proyectado es relativo al camarón de cultivo: mide cuánto se despega el langostino argentino del referente mundial, no el precio en dólares por kilo. Surge de aplicar la flexibilidad estimada (−0,184) al recorte de volumen, no de una observación: el signo y el orden de magnitud son firmes, la cifra exacta no.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "El paquete es hipotético, construido sobre el desembarque medio 2022-2024. Sirve para dar orden de magnitud, no para pronosticar una medida puntual."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 1.09,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SOLIDEZ",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.048,
    "y": 0.708,
    "w": 0.869,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "12 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué tan firme es esto",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.763,
    "w": 19.433,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Conviene decirlo antes de que lo diga otro.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.413,
    "w": 8.458,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.742,
    "w": 9.304,
    "h": 0.546,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Lo que está sólido",
        "sz": 33.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.701,
    "w": 8.712,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El parate de 2025 fue un shock de oferta genuino, no un efecto del precio: se verificó contra todas las ventanas alternativas posibles de la serie.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 6.216,
    "w": 8.458,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.474,
    "w": 8.712,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Las dos magnitudes del episodio —46% menos de captura, 3,1% más de precio— son observación directa. No dependen de ningún modelo.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.568,
    "w": 8.458,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.827,
    "w": 8.712,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Tres estimaciones distintas, con bases y métodos distintos, dan lo mismo: entre −0,18 y −0,27, todas lejísimos del umbral de −1.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.375,
    "y": 4.413,
    "w": 8.458,
    "h": 0.017,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 3.742,
    "w": 9.304,
    "h": 0.546,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Lo que no conviene afirmar",
        "sz": 33.0,
        "c": "5D5D60",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 4.701,
    "w": 8.712,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El valor exacto del parámetro. La estimación se apoya en un solo episodio, y una prueba de robustez muestra que con un único shock no se puede defender el número con decimales ni su intervalo.",
        "sz": 20.25,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.375,
    "y": 6.216,
    "w": 8.458,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 6.474,
    "w": 8.712,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Lo que se sostiene es el orden de magnitud y la conclusión de política, no la precisión.",
        "sz": 20.25,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.375,
    "y": 7.568,
    "w": 8.458,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 7.827,
    "w": 8.712,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Para cerrarlo haría falta otro shock ajeno al mercado. El calendario del CFP se probó y no sirve: sus decisiones siguen al recurso.",
        "sz": 20.25,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": "Esta lámina es deliberada. Si el estudio se discute con un tercero, la objeción del único episodio va a aparecer; es mejor haberla puesto nosotros y haberla acotado."
 },
 {
  "fondo": "1D2D3D",
  "formas": [
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.123,
    "w": 19.433,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SEGUNDA PARTE · AGENDA COMERCIAL",
        "sz": 18.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.885,
    "w": 16.042,
    "h": 1.375,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Entonces, ¿dónde está el valor?",
        "sz": 96.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -1.92
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.552,
    "w": 12.875,
    "h": 1.033,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Si la palanca del volumen no rinde, el mismo trabajo muestra tres que sí. Ninguna cuesta toneladas.",
        "sz": 25.5,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1442
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.044,
    "w": 0.275,
    "h": 0.792,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "1",
        "sz": 54.0,
        "c": "94BCE3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.942,
    "y": 6.044,
    "w": 0.385,
    "h": 0.792,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2",
        "sz": 54.0,
        "c": "94BCE3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.827,
    "y": 6.044,
    "w": 0.389,
    "h": 0.792,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "3",
        "sz": 54.0,
        "c": "94BCE3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   }
  ],
  "notas": "Bisagra de la presentación. De acá en adelante es agenda comercial."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 2.983,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "PALANCA 1 · EL CANAL",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.045,
    "y": 0.708,
    "w": 0.872,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "14 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 0.403,
    "h": 1.104,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "1",
        "sz": 90.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6375
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.862,
    "y": 1.708,
    "w": 16.042,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El canal manda más que la cantidad",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.862,
    "y": 2.742,
    "w": 15.021,
    "h": 0.918,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El langostino entero se come afuera de casa: restaurante, hotel, catering. Cuando ese canal se mueve, el precio se mueve más que con la oferta.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.076,
    "w": 9.953,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Efecto sobre el precio, en %",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 6.807,
    "w": 9.048,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "rect",
    "x": 2.094,
    "y": 6.807,
    "w": 2.628,
    "h": 0.934,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 2.991,
    "y": 7.907,
    "w": 0.918,
    "h": 0.625,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−2,5",
        "sz": 42.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.195,
    "y": 8.594,
    "w": 2.427,
    "h": 0.393,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Si HORECA cae 10%",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.595,
    "y": 5.073,
    "w": 0.84,
    "h": 0.625,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+1,8",
        "sz": 42.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.75
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 6.66,
    "y": 5.823,
    "w": 2.628,
    "h": 0.984,
    "fill": "94BCE3"
   },
   {
    "tipo": "txt",
    "x": 6.752,
    "y": 6.973,
    "w": 2.443,
    "h": 2.014,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Si la captura cae 10%",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "ctr",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.965,
    "y": 4.913,
    "w": 7.868,
    "h": 3.196,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 11.39,
    "y": 5.338,
    "w": 7.72,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "QUÉ HACER CON ESTO",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 2.88
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.39,
    "y": 5.934,
    "w": 7.229,
    "h": 1.792,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Seguir la actividad HORECA de España, Italia, China y Japón es más útil para anticipar el precio que seguir el propio desembarque. Y no requiere resignar un solo kilo.",
        "sz": 21.0,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.238,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.454,
    "w": 18.197,
    "h": 1.129,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Las dos barras no están medidas contra la misma referencia: el efecto de la captura es sobre el precio relativo al camarón de cultivo y el del canal sobre el precio en euros. Sobre el precio relativo el canal pesa menos, porque cuando cerró el canal HORECA también cayó el precio del cultivo. Índice construido con estadística oficial de los cuatro destinos: INE, ISTAT, Oficina Nacional de Estadística de China y METI.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "Dato duro: en abril de 2020 el índice cayó 83% contra 2019. Ninguna variable de oferta explica lo que pasó con el precio ese año."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.042,
    "y": 1.2,
    "w": 17.917,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.042,
    "y": 0.625,
    "w": 2.983,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "PALANCA 1 · EL CANAL",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.171,
    "y": 0.625,
    "w": 0.87,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "15 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.042,
    "y": 1.438,
    "w": 19.708,
    "h": 0.67,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "No todos los canales volvieron igual",
        "sz": 43.5,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.65
       }
      ],
      "algn": "l",
      "lns": 0.7711
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.042,
    "y": 2.17,
    "w": 17.76,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Actividad HORECA en los cuatro destinos del L1, base 2019 = 100. El canal ya está por encima de la prepandemia. En uno, no.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.042,
    "y": 2.987,
    "w": 0.292,
    "h": 0.031,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 1.458,
    "y": 2.843,
    "w": 2.081,
    "h": 0.35,
    "anchor": "t",
    "m": 0.0,
    "p": [
     {
      "runs": [
       {
        "t": "Índice combinado",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1782
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 3.831,
    "y": 2.987,
    "w": 0.292,
    "h": 0.031,
    "fill": "94BCE3"
   },
   {
    "tipo": "txt",
    "x": 4.248,
    "y": 2.843,
    "w": 0.789,
    "h": 0.35,
    "anchor": "t",
    "m": 0.0,
    "p": [
     {
      "runs": [
       {
        "t": "Japón",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1782
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.042,
    "y": 8.537,
    "w": 9.91,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "rect",
    "x": 1.042,
    "y": 3.309,
    "w": 0.01,
    "h": 5.237,
    "fill": null
   },
   {
    "tipo": "img",
    "x": 1.042,
    "y": 3.309,
    "w": 9.91,
    "h": 5.237,
    "src": "image2.png"
   },
   {
    "tipo": "rect",
    "x": 1.104,
    "y": 4.23,
    "w": 1.248,
    "h": 0.388,
    "fill": "F2F2F3"
   },
   {
    "tipo": "txt",
    "x": 1.188,
    "y": 4.23,
    "w": 1.206,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2019 = 100",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.042,
    "y": 8.692,
    "w": 0.333,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'13",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.638,
    "y": 8.692,
    "w": 0.332,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'15",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 4.234,
    "y": 8.692,
    "w": 0.322,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'17",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.819,
    "y": 8.692,
    "w": 0.334,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'19",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 7.417,
    "y": 8.692,
    "w": 0.334,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'21",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 9.015,
    "y": 8.692,
    "w": 0.378,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'23",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.656,
    "y": 8.692,
    "w": 0.379,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "'25",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 2.801,
    "w": 8.075,
    "h": 0.431,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Dónde está cada mercado",
        "sz": 25.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8091
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 3.253,
    "w": 7.561,
    "h": 0.717,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "promedio de los últimos doce meses, y cuánto pesa en el volumen del L1",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.125
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.618,
    "y": 4.074,
    "w": 7.34,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 4.307,
    "w": 0.79,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Italia",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 16.968,
    "y": 4.207,
    "w": 0.865,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "127,4",
        "sz": 36.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.958,
    "y": 4.491,
    "w": 1.0,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "21,1%",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "r",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.618,
    "y": 5.076,
    "w": 7.34,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 5.278,
    "w": 0.881,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "China",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 16.926,
    "y": 5.178,
    "w": 0.907,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "125,9",
        "sz": 36.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.958,
    "y": 5.462,
    "w": 1.0,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "13,6%",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "r",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.618,
    "y": 6.047,
    "w": 7.34,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 6.249,
    "w": 1.114,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "España",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 16.908,
    "y": 6.149,
    "w": 0.925,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "120,9",
        "sz": 36.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.958,
    "y": 6.432,
    "w": 1.0,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "43,5%",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "r",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.618,
    "y": 7.018,
    "w": 7.34,
    "h": 1.083,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 11.618,
    "y": 8.093,
    "w": 7.34,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 11.618,
    "y": 7.018,
    "w": 7.34,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 7.272,
    "w": 0.96,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Japón",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.035,
    "y": 7.172,
    "w": 0.798,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "88,0",
        "sz": 36.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 17.958,
    "y": 7.455,
    "w": 1.0,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "11,5%",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "r",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.618,
    "y": 8.226,
    "w": 7.561,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Japón sigue 12% abajo de 2019 y no se recupera. Es uno de cada nueve kilos de L1.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.042,
    "y": 9.225,
    "w": 17.917,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.042,
    "y": 9.358,
    "w": 18.454,
    "h": 1.392,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "En abril de 2020 el índice combinado tocó 16,9, un 83,1% por debajo de 2019, y no volvió al nivel de 2019 hasta mayo de 2022. Por eso el modelo usa el índice observado y no una marca de pandemia. Fuente: elaboración propia sobre INE (España, CNAE 56), ISTAT (Italia, Ateco 56; mensual desde 2021, trimestral antes), NBS (China, ingresos HORECA) y METI (Japón, actividad terciaria, HORECA). Base 2019 = 100, series sin ajuste estacional. El combinado pondera por la participación de cada mercado en el volumen del L1 tangonero.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.125
     }
    ]
   }
  ],
  "notas": "La placa no dice «dejemos Japón»: dice que el canal explica el precio y que hay un mercado donde el canal no volvió. Sirve para leer la demanda de los próximos meses sin esperar el dato propio, que llega más tarde."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 3.322,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "PALANCA 2 · EL DESTINO",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.046,
    "y": 0.708,
    "w": 0.87,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "16 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 0.586,
    "h": 1.104,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2",
        "sz": 90.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6375
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.044,
    "y": 1.708,
    "w": 16.615,
    "h": 0.865,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El mismo producto vale distinto según a dónde va",
        "sz": 57.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.85
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.044,
    "y": 2.698,
    "w": 15.557,
    "h": 0.918,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Diferencia de precio del entero L1 contra España, a igual mes y producto. España ancla el volumen al precio más bajo.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.45,
    "w": 10.338,
    "h": 0.445,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Diferencia contra España, en %",
        "sz": 18.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.3091
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.168,
    "w": 1.719,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "China",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 5.199,
    "w": 5.981,
    "h": 0.583,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 5.199,
    "w": 5.718,
    "h": 0.583,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 9.211,
    "y": 5.104,
    "w": 1.49,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+8,6",
        "sz": 36.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.172,
    "w": 1.719,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Italia",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 6.204,
    "w": 5.981,
    "h": 0.583,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 6.204,
    "w": 3.989,
    "h": 0.583,
    "fill": "416180"
   },
   {
    "tipo": "txt",
    "x": 9.211,
    "y": 6.108,
    "w": 1.49,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+6,0",
        "sz": 36.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.176,
    "w": 1.719,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Japón",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 7.208,
    "w": 5.981,
    "h": 0.583,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 7.208,
    "w": 2.327,
    "h": 0.583,
    "fill": "749DC4"
   },
   {
    "tipo": "txt",
    "x": 9.211,
    "y": 7.112,
    "w": 1.49,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+3,5",
        "sz": 36.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.181,
    "w": 1.719,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "España",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 8.212,
    "w": 5.981,
    "h": 0.583,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 2.979,
    "y": 8.212,
    "w": 0.025,
    "h": 0.583,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 9.211,
    "y": 8.116,
    "w": 1.49,
    "h": 0.817,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "0",
        "sz": 36.0,
        "c": "5D5D60",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.315,
    "y": 4.721,
    "w": 7.519,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 11.315,
    "y": 4.988,
    "w": 8.27,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Nueve puntos",
        "sz": 78.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.315,
    "y": 6.13,
    "w": 7.744,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "separan el destino más caro del más barato, sobre el mismo producto físico y el mismo mes.",
        "sz": 20.25,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.315,
    "y": 7.307,
    "w": 7.744,
    "h": 1.354,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "España se lleva el volumen: es el comprador grande y paga el precio más bajo de la tabla. Ahí hay una decisión comercial, no un dato de la naturaleza.",
        "sz": 21.0,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.6,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.817,
    "w": 18.197,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Fuente: registro aduanero de exportación, entero L1 congelado a bordo y procesado en tierra, 2013-2026. Premium contra España a igual mes, ponderado por kilos. Destinos con 5% o más del valor exportado en 2021-2025.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "Ojo con leerlo como 'hay que dejar España': son mercados de distinto tamaño y la capacidad de absorción no es la misma. El punto es que la diferencia es medible y hoy no se está cobrando. El premium sale de una regresión ponderada por kilos sobre 19.160 despachos de 2013-2026 (R² 0.502), con efecto fijo de mes."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 3.753,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "PALANCA 3 · FLOTA Y TALLA",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.057,
    "y": 0.708,
    "w": 0.859,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "17 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.708,
    "w": 0.593,
    "h": 1.104,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "3",
        "sz": 90.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6375
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.052,
    "y": 1.708,
    "w": 15.603,
    "h": 0.865,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La flota y la talla ya son una ventaja: falta cobrarla",
        "sz": 57.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.85
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.052,
    "y": 2.698,
    "w": 15.603,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El producto tangonero es otro negocio, y el entero grande es el activo diferencial frente al camarón de cultivo.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.096,
    "w": 4.639,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 5.797,
    "y": 4.096,
    "w": 0.01,
    "h": 3.819,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.384,
    "w": 4.727,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "+25%",
        "sz": 78.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.526,
    "w": 4.426,
    "h": 0.856,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "vale el entero L1 tangonero sobre el mismo talle fresquero",
        "sz": 25.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.9399
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.465,
    "w": 4.426,
    "h": 1.492,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "7,23 contra 5,80 dólares por kilo en 2025. Es congelado a bordo contra procesado en tierra: distinto producto, distinto cliente.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 5.805,
    "y": 4.096,
    "w": 4.639,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 10.436,
    "y": 4.096,
    "w": 0.01,
    "h": 3.819,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 6.139,
    "y": 4.384,
    "w": 4.36,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "3,4 veces",
        "sz": 78.0,
        "c": "416180",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 6.139,
    "y": 5.526,
    "w": 4.083,
    "h": 0.856,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "más grande que el camarón ecuatoriano que llega a España",
        "sz": 25.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.9399
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 6.139,
    "y": 6.465,
    "w": 4.083,
    "h": 1.492,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El langostino entero L1 es un producto que el cultivo no replica. Ese tamaño tiene un precio y hoy no se está cobrando entero.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.444,
    "y": 4.096,
    "w": 4.639,
    "h": 0.017,
    "fill": "5980A6"
   },
   {
    "tipo": "rect",
    "x": 15.075,
    "y": 4.096,
    "w": 0.01,
    "h": 4.181,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 10.778,
    "y": 4.384,
    "w": 4.36,
    "h": 1.017,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−21%",
        "sz": 78.0,
        "c": "2C455D",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.778,
    "y": 5.526,
    "w": 4.083,
    "h": 0.856,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "el descuento con que se vende ajustado por talla",
        "sz": 25.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.9399
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.778,
    "y": 6.465,
    "w": 4.083,
    "h": 1.854,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Contra camarón ecuatoriano equivalente en el mismo mercado. Es la brecha que el trabajo mide por primera vez, y merece verificación propia.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 15.417,
    "y": 4.096,
    "w": 3.417,
    "h": 4.167,
    "fill": null
   },
   {
    "tipo": "img",
    "x": 14.922,
    "y": 4.865,
    "w": 4.469,
    "h": 2.976,
    "src": "image3.png"
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.238,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.454,
    "w": 18.197,
    "h": 1.129,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El descuento sale de 6,48 ÷ (6,01 × 1,36): entero L1 congelado a bordo contra camarón ecuatoriano al mismo mercado y mes, ajustado por talla con la elasticidad precio–piezas por kilo de −0,254 aplicada a 52 contra 15,5 piezas por kilo. La unidad del conteo está inferida y el ajuste extrapola fuera de muestra: según cómo se lea, el descuento va de 6% a 23%. Indicativo, no establecido.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "La tangonera pasó del 71% del desembarque total en 2013 al 26% en 2025. La participación cae, pero el valor por tonelada es el doble."
 },
 {
  "fondo": "F2F2F3",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 2.385,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "AGENDA DE DATOS",
        "sz": 18.0,
        "c": "416180",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.043,
    "y": 0.708,
    "w": 0.873,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "18 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.542,
    "w": 19.433,
    "h": 0.908,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué falta para afinar el número",
        "sz": 60.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.9
       }
      ],
      "algn": "l",
      "lns": 0.78
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.533,
    "w": 19.433,
    "h": 0.48,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El primero se probó y no resuelve el problema. Los otros dos dependen del sector.",
        "sz": 21.75,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2224
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.693,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.889,
    "w": 1.0,
    "h": 0.642,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "1",
        "sz": 48.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.417,
    "y": 3.889,
    "w": 15.171,
    "h": 0.545,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Calendario oficial de aperturas y cierres — PROBADO, NO ALCANZA",
        "sz": 31.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.849
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.417,
    "y": 4.517,
    "w": 14.205,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Las 547 actas del CFP están leídas: 165 decisiones, 55 fechadas. Como instrumento no identifican: el Consejo cierra cuando cae el rendimiento y abre de a poco en años flojos, así que sus decisiones siguen al recurso en vez de moverlo.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 17.422,
    "y": 3.889,
    "w": 1.412,
    "h": 0.571,
    "fill": "5980A6"
   },
   {
    "tipo": "txt",
    "x": 17.617,
    "y": 3.981,
    "w": 1.103,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "PROBADO",
        "sz": 18.0,
        "c": "2C455D",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 5.971,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.166,
    "w": 1.0,
    "h": 0.642,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2",
        "sz": 48.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.417,
    "y": 6.166,
    "w": 15.171,
    "h": 0.545,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Existencias mensuales de congelado",
        "sz": 31.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.849
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.417,
    "y": 6.795,
    "w": 14.205,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cuánto producto hay en cámara, por presentación y talla. Hoy medimos la respuesta del precio al desembarque, no a lo que efectivamente llega al mercado.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 17.286,
    "y": 6.166,
    "w": 1.547,
    "h": 0.575,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 17.484,
    "y": 6.26,
    "w": 1.235,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EMPRESAS",
        "sz": 18.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.681,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.826,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.022,
    "w": 1.0,
    "h": 0.642,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "3",
        "sz": 48.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.675
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.417,
    "y": 8.022,
    "w": 15.171,
    "h": 0.545,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Precio del competidor por calibre",
        "sz": 31.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.849
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.417,
    "y": 8.65,
    "w": 14.205,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Precio europeo de importación abierto por rango de talla, con la unidad del conteo declarada. Cierra la comparación con el vannamei.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 17.123,
    "y": 8.022,
    "w": 1.711,
    "h": 0.575,
    "fill": "2C455D"
   },
   {
    "tipo": "txt",
    "x": 17.321,
    "y": 8.115,
    "w": 1.398,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "PROVEEDOR",
        "sz": 18.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.12,
    "w": 19.433,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El paro de 2025 sigue siendo el único shock ajeno al recurso y al mercado. Lo que se sostiene son sus magnitudes, no un parámetro preciso.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": "El primero es el más importante y el más barato: son documentos públicos que hay que sistematizar."
 },
 {
  "fondo": "1D2D3D",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.283,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.708,
    "w": 0.955,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "CIERRE",
        "sz": 18.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed",
        "spc": 3.24
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.048,
    "y": 0.708,
    "w": 0.869,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "19 / 28",
        "sz": 18.0,
        "c": "B5D9FD",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.75,
    "w": 19.433,
    "h": 1.062,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Tres conclusiones",
        "sz": 72.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -1.44
       }
      ],
      "algn": "l",
      "lns": 0.765
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.129,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.513,
    "w": 1.333,
    "h": 0.821,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "1",
        "sz": 66.0,
        "c": "94BCE3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6375
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.833,
    "y": 3.513,
    "w": 17.6,
    "h": 0.637,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Recortar oferta no mejora el ingreso.",
        "sz": 39.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.833,
    "y": 4.233,
    "w": 16.042,
    "h": 0.479,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se partió la captura al medio y el precio subió 3,1%. Para que la cuenta cerrara tendría que haber subido 86,6%.",
        "sz": 21.0,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 5.046,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.429,
    "w": 1.333,
    "h": 0.821,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2",
        "sz": 66.0,
        "c": "94BCE3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6375
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.833,
    "y": 5.429,
    "w": 17.6,
    "h": 0.637,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El precio lo pone el mercado mundial, no la flota.",
        "sz": 39.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.833,
    "y": 6.15,
    "w": 15.021,
    "h": 0.917,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El langostino argentino es tomador de precio dentro del mercado global del camarón. La palanca del volumen es corta por definición.",
        "sz": 21.0,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.754,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.4,
    "w": 17.667,
    "h": 0.01,
    "fill": null
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.783,
    "w": 1.333,
    "h": 0.821,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "3",
        "sz": 66.0,
        "c": "94BCE3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.6375
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.833,
    "y": 7.783,
    "w": 17.6,
    "h": 0.637,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El valor está en el canal, el destino y la talla.",
        "sz": 39.0,
        "c": "F2F2F3",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 2.833,
    "y": 8.504,
    "w": 15.021,
    "h": 0.917,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La actividad HORECA mueve el precio más que la propia captura, y hay nueve puntos de diferencia entre destinos por el mismo producto.",
        "sz": 21.0,
        "c": "D6EBFF",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.122,
    "w": 19.433,
    "h": 0.461,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "LIC. FABIÁN PETTIGREW · SEPTIEMBRE DE 2026",
        "sz": 19.5,
        "c": "B5D9FD",
        "f": "Barlow Condensed",
        "spc": 2.34
       }
      ],
      "algn": "l",
      "lns": 1.2594
     }
    ]
   }
  ],
  "notas": "Cierre: la recomendación no es hacer nada, es mover las palancas que efectivamente pagan."
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.133,
    "w": 17.667,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.516,
    "w": 19.433,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MATERIAL DE RESPALDO · LÁMINAS 20 A 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 4.32
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.237,
    "w": 19.433,
    "h": 1.147,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Anexo metodológico",
        "sz": 78.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -1.56
       }
      ],
      "algn": "l",
      "lns": 0.765
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.634,
    "w": 14.896,
    "h": 0.525,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cómo está construido el número, con qué datos, y qué dice la literatura que lo respalda.",
        "sz": 24.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   }
  ],
  "notas": "De acá en adelante es material de respaldo: no se pasa en la presentación, se usa para contestar preguntas."
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.057,
    "y": 0.833,
    "w": 0.86,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "21 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué se estima, y contra qué umbral",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Un solo parámetro ordena toda la discusión.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.15,
    "w": 8.417,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.546,
    "w": 9.258,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La flexibilidad-precio",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.409,
    "w": 8.669,
    "h": 1.349,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Mide en cuánto por ciento se mueve el precio cuando la cantidad ofrecida se mueve un uno por ciento. Es negativa por definición: más mercadería, menos precio.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2759
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.925,
    "w": 8.669,
    "h": 0.914,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se estima sobre el precio del langostino relativo al camarón de cultivo, para que el ciclo mundial no se cuele en el resultado.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2759
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.417,
    "y": 4.15,
    "w": 8.417,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 10.417,
    "y": 3.546,
    "w": 9.258,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El umbral no es cero, es 1",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.417,
    "y": 4.409,
    "w": 8.669,
    "h": 1.349,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Como la facturación es precio por cantidad, recortar oferta la aumenta sólo si el precio sube MÁS de lo que cae el volumen. En términos del parámetro: sólo si es menor que −1.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2759
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.417,
    "y": 5.925,
    "w": 8.669,
    "h": 0.914,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Con −0,2, sacar el 10% de las toneladas sube el precio 2% y baja la facturación 8%.",
        "sz": 20.25,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2759
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.721,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.979,
    "w": 18.197,
    "h": 0.479,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "No alcanza con que el parámetro sea negativo y estadísticamente significativo: tiene que ser mayor que uno en valor absoluto.",
        "sz": 21.0,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.25
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.012,
    "y": 0.833,
    "w": 0.905,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "22 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Qué entra al modelo",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Series mensuales de enero de 2013 a julio de 2026. Todo es registro oficial o base comercial de despachos.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Precio",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.342,
    "w": 4.163,
    "h": 2.385,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Valor unitario FOB del entero L1 congelado a bordo, despacho por despacho. La flota se identifica por la marca de congelado a bordo: lo que la lleva es tangonera, lo que no la lleva es fresquera.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 5.708,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 5.708,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cantidad",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.708,
    "y": 4.342,
    "w": 4.163,
    "h": 1.604,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Desembarque oficial por puerto, flota y mes. Es la variable que la política mueve, y es exógena: no la decide el que vende.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.25,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 10.25,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Competidor",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.25,
    "y": 4.342,
    "w": 4.163,
    "h": 2.385,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Precio del camarón de cultivo importado por la Unión Europea, y exportación ecuatoriana por subpartida y país de destino, para comparar contra el mismo mercado y el mismo mes.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.792,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 14.792,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Demanda",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.792,
    "y": 4.342,
    "w": 4.163,
    "h": 1.995,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Índice mensual de actividad del canal HORECA en España, Italia, China y Japón, construido con estadística oficial de los cuatro países.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.315,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.573,
    "w": 18.197,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El desembarque de la flota tangonera es producto final que va directo a exportación, sin reproceso: por eso su composición por talla se observa en el despacho.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.01,
    "y": 0.833,
    "w": 0.906,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "23 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Por qué hace falta un experimento",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Precio y cantidad se determinan juntos. Cruzarlos sin más no mide la demanda: mide una mezcla.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.546,
    "w": 8.5,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.784,
    "w": 9.35,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2020 · un shock de DEMANDA",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.365,
    "w": 8.755,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Con el canal HORECA cerrado, precio y cantidad cayeron juntos. Leído sin distinguir, ese año «demuestra» que menos oferta baja el precio. Es exactamente el sesgo que hay que sacar.",
        "sz": 19.5,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.333,
    "y": 3.546,
    "w": 8.5,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 10.333,
    "y": 3.784,
    "w": 9.35,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "2025 · un shock de OFERTA",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.333,
    "y": 4.365,
    "w": 8.755,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La flota parada cuatro meses por un conflicto gremial, con la captura de del año 46% abajo. La cantidad se movió por un motivo ajeno al mercado: eso es lo que traza la curva de demanda.",
        "sz": 19.5,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 8.27,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.57,
    "w": 19.433,
    "h": 0.477,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Cómo se usa",
        "sz": 28.5,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.8108
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.151,
    "w": 16.094,
    "h": 1.307,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El conflicto entra como instrumento: se usa sólo la parte de la captura que se movió por el parate de la flota. La primera etapa da F = 61, muy por encima del umbral de 10 que se exige para que el instrumento sea fuerte. El cierre del canal entra como control, con índice observado y no supuesto.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.008,
    "y": 0.833,
    "w": 0.908,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "24 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.667,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Siete caminos, un número",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.519,
    "w": 17.167,
    "h": 0.887,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se estimó por vías deliberadamente distintas —otras bases, otras unidades de observación, otros métodos— para ver si el resultado dependía de la construcción.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.782,
    "w": 9.868,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.084,
    "w": 6.354,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Instrumental mensual, precio transaccional del L1",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.136,
    "y": 3.884,
    "w": 0.982,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,184",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 4.623,
    "w": 9.868,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.925,
    "w": 7.334,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Instrumental mensual, agregado de las dos tallas grandes",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.164,
    "y": 4.725,
    "w": 0.954,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,219",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 5.465,
    "w": 9.868,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 5.767,
    "w": 3.843,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Nivel campaña, con tendencia",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.146,
    "y": 5.567,
    "w": 0.972,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,196",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 6.307,
    "w": 9.868,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 6.609,
    "w": 8.116,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Las dos tallas grandes, con la participación del L2 como control",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.063,
    "y": 6.409,
    "w": 1.055,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,208",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.148,
    "w": 9.868,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 7.45,
    "w": 4.618,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Sistema de dos flotas, recompuesto",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.164,
    "y": 7.25,
    "w": 0.954,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,212",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 7.99,
    "w": 9.868,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 8.292,
    "w": 6.635,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Ecuación incondicional con desembarques por flota",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.086,
    "y": 8.092,
    "w": 1.032,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,239",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.673,
    "w": 9.868,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 8.832,
    "w": 9.868,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.134,
    "w": 7.881,
    "h": 0.407,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Sistema de demanda inversa por origen, importación europea",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.0969
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.101,
    "y": 8.934,
    "w": 1.017,
    "h": 0.688,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "−0,267",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.785,
    "y": 3.782,
    "w": 7.049,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 11.785,
    "y": 4.019,
    "w": 7.26,
    "h": 1.232,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Todas rechazan el umbral de −1 con holgura.",
        "sz": 42.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.765
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.785,
    "y": 5.639,
    "w": 7.26,
    "h": 1.26,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El rango va de −0,18 a −0,27: el precio se mueve entre un quinto y algo más de un cuarto de lo que se mueve la cantidad.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 11.785,
    "y": 7.181,
    "w": 7.26,
    "h": 0.854,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Ninguna construcción se acerca al valor que haría conveniente recortar.",
        "sz": 19.5,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 11.785,
    "y": 8.278,
    "w": 7.049,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 11.785,
    "y": 8.5,
    "w": 7.26,
    "h": 0.767,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Al sistema por origen se le impuso además la simetría teórica: da −0,282 en vez de −0,267.",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.773,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 10.01,
    "w": 18.197,
    "h": 0.448,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Siete construcciones distintas dan el mismo número: el resultado no depende del método elegido.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2188
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.01,
    "y": 0.833,
    "w": 0.907,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "25 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Lo que el trabajo no puede afirmar",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Conviene tenerlo a mano antes de que lo pregunte otro.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Glaseo",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.342,
    "w": 4.163,
    "h": 2.776,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "No está considerado y no puede estarlo con dato de aduana: sobre los 67.844 despachos de la base, siete mencionan glaseo y ninguno de ellos es entero L1, y el nomenclador oficial no tiene código para declararlo.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 5.708,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 5.708,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Existencias",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.708,
    "y": 4.342,
    "w": 4.163,
    "h": 1.995,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "No se miden. Lo que llega al mercado difiere de lo que se pescó entre −19% y +24% según la campaña, y esa brecha es error de medición en la cantidad.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.25,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 10.25,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El valor exacto",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.25,
    "y": 4.342,
    "w": 4.163,
    "h": 1.604,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La identificación se apoya en un solo episodio. El signo y el orden de magnitud son firmes; los decimales y el intervalo, no.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.792,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 14.792,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La tendencia",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.792,
    "y": 4.342,
    "w": 4.163,
    "h": 2.776,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Contra el mismo mercado, el precio relativo sube 1,1% por año. Comparar España contra España explicó la mitad de la tendencia; esta otra mitad todavía no. Los candidatos son certificación y góndola.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.736,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.995,
    "w": 18.197,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Ninguna de estas limitaciones cambia el signo del resultado: cambian su precisión.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.01,
    "y": 0.833,
    "w": 0.907,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "26 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La objeción del FOB contra el CIF",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El precio que enfrenta el comprador europeo no es el que cobra el barco argentino. Qué cambia si se mide sobre el otro.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El precio correcto",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.342,
    "w": 4.163,
    "h": 2.776,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Para esta pregunta el FOB es el precio correcto, y no un segundo mejor: el umbral de −1 sale de derivar el ingreso del productor, y ese ingreso es lo que cobra el barco. El flete no lo cobra la flota.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 5.708,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 5.708,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El flete, medido",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 5.708,
    "y": 4.342,
    "w": 4.163,
    "h": 1.995,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El mismo embarque se observa dos veces: como FOB de despacho del lado argentino y como CIF de importación del lado europeo. La diferencia es 0,73 EUR/kg, el 13,1% del FOB, con un pico de 1,10 en 2022 por la crisis mundial de fletes.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.25,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 10.25,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El signo del sesgo",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.25,
    "y": 4.342,
    "w": 4.163,
    "h": 1.604,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El flete no responde a cuánto langostino embarca la Argentina, así que medir sobre el FOB exagera la flexibilidad. Corregida a CIF, la estimación pasa de −0,184 a −0,164: se aleja del umbral en vez de acercarse.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 14.792,
    "y": 3.546,
    "w": 4.042,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 14.792,
    "y": 3.784,
    "w": 4.446,
    "h": 0.454,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Reestimado",
        "sz": 27.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 14.792,
    "y": 4.342,
    "w": 4.163,
    "h": 2.776,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "No se corrigió sólo multiplicando: se rehízo la estimación con un CIF equivalente para el entero L1. Da −0,171 si el flete es exógeno y −0,085 si responde como marca el dato. Las dos, más lejos de −1.",
        "sz": 18.75,
        "c": "424244",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.1402
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.736,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.995,
    "w": 18.197,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "La objeción es correcta en el mecanismo y, atendida, refuerza la conclusión en lugar de debilitarla.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.01,
    "y": 0.833,
    "w": 0.907,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "27 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Los estudios que fijan el método",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Los dos primeros de la placa 3, en detalle.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.546,
    "w": 8.458,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.784,
    "w": 9.304,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Barten y Bettendorf (1989)",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.325,
    "w": 9.304,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "EUROPEAN ECONOMIC REVIEW",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.16
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.9,
    "w": 8.712,
    "h": 2.56,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "El trabajo fundacional de la demanda inversa aplicada a pescado. Muestra que en productos pesqueros hay que dar vuelta el análisis: la captura llega al mercado ya decidida por el recurso y el calendario, y es el precio el que se acomoda para vaciarlo. De ahí sale el sistema de ecuaciones que se usa acá para estimar varias especies o flotas a la vez respetando que el gasto total tiene que cerrar.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2594
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.375,
    "y": 3.546,
    "w": 8.458,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 3.784,
    "w": 9.304,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Tabarestani, Keithly y Marzoughi-Ardakani (2017)",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 4.325,
    "w": 9.304,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MARINE RESOURCE ECONOMICS",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.16
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 4.9,
    "w": 8.712,
    "h": 2.98,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Lleva ese enfoque al mercado del camarón en Estados Unidos, que es el mercado de referencia mundial. Trata el desembarque salvaje del Golfo de México como cantidad ya dada y el precio del camarón de cultivo importado como dato externo. El resultado es el antecedente más directo de este trabajo: un cambio de 1% en el precio del importado mueve 0,98% el precio doméstico. El salvaje casi no tiene autonomía de precio frente al cultivo.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2594
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.736,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.995,
    "w": 18.197,
    "h": 0.464,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Es el enfoque que corresponde cuando la cantidad no la decide el que vende.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": ""
 },
 {
  "fondo": "E9E9EA",
  "formas": [
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 1.387,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 0.833,
    "w": 3.067,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "ANEXO METODOLÓGICO",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 3.6
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 18.021,
    "y": 0.833,
    "w": 0.896,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "28 / 28",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.52
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 1.771,
    "w": 19.433,
    "h": 0.748,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Los estudios que acotan la expectativa",
        "sz": 48.0,
        "c": "1D1F20",
        "f": "Barlow Condensed",
        "b": true,
        "spc": -0.72
       }
      ],
      "algn": "l",
      "lns": 0.795
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 2.623,
    "w": 19.433,
    "h": 0.465,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Los dos últimos de la placa 3, más el aporte del INIDEP.",
        "sz": 21.0,
        "c": "5D5D60",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2083
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 3.546,
    "w": 8.458,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 3.784,
    "w": 9.304,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Guillen y Maynou (2014)",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.325,
    "w": 9.304,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "SCIENTIA MARINA",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.16
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 4.9,
    "w": 8.712,
    "h": 2.98,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Estudia cómo se forma el precio en primera venta en pesquerías mediterráneas, con la gamba roja catalana. Separa qué pesa el volumen del día y qué pesa la temporada, y encuentra que el precio de primera venta es 14% menor los martes y miércoles. La recomendación es de calendario, no de recorte: concentrar la reducción de esfuerzo en los días de precio bajo. Es el antecedente de la palanca del canal en este trabajo.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2594
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 10.375,
    "y": 3.546,
    "w": 8.458,
    "h": 0.01,
    "fill": "1D1F20"
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 3.784,
    "w": 9.304,
    "h": 0.5,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Asche y otros (2017)",
        "sz": 30.0,
        "c": "1D1F20",
        "f": "Barlow Condensed"
       }
      ],
      "algn": "l",
      "lns": 0.825
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 4.325,
    "w": 9.304,
    "h": 0.429,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "MARINE RESOURCE ECONOMICS",
        "sz": 18.0,
        "c": "5D5D60",
        "f": "Barlow Condensed",
        "spc": 2.16
       }
      ],
      "algn": "l",
      "lns": 1.2917
     }
    ]
   },
   {
    "tipo": "txt",
    "x": 10.375,
    "y": 4.9,
    "w": 8.712,
    "h": 2.56,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Documenta que los distintos camarones del mundo suelen moverse como un solo mercado. Ese supuesto se testeó acá y NO se cumple entre el langostino argentino y el vannamei de cultivo: son productos diferenciados, no sustitutos perfectos. Es lo que deja lugar a la palanca de talla y diferenciación, y lo que impide tratar al langostino como una commodity más dentro del agregado camarón.",
        "sz": 19.5,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2594
     }
    ]
   },
   {
    "tipo": "rect",
    "x": 1.167,
    "y": 9.315,
    "w": 17.667,
    "h": 0.01,
    "fill": "B7B7BA"
   },
   {
    "tipo": "txt",
    "x": 1.167,
    "y": 9.573,
    "w": 18.197,
    "h": 0.885,
    "anchor": "t",
    "m": 2.0,
    "p": [
     {
      "runs": [
       {
        "t": "Se sumó el INIDEP para la biología de la especie: el langostino renueva casi toda su población entre temporadas, y por eso la captura de un año no sirve para predecir la del siguiente — un instrumento que se probó y se descartó.",
        "sz": 20.25,
        "c": "1D1F20",
        "f": "Barlow"
       }
      ],
      "algn": "l",
      "lns": 1.2348
     }
    ]
   }
  ],
  "notas": ""
 }
];

const pptx = new pptxgen();
pptx.defineLayout({ name: "DECK", width: 20, height: 11.25 });
pptx.layout = "DECK";
pptx.author = "Lic. Fabián Pettigrew";
pptx.company = "AXIA";
pptx.title = "Estudio econométrico · testeo de reducción de captura";

const ALIN = { l: "left", ctr: "center", r: "right", just: "justify" };

PLACAS.forEach(function (pl, i) {
  const s = pptx.addSlide();
  if (pl.fondo) s.background = { color: pl.fondo };
  if (pl.notas) s.addNotes(pl.notas);
  pl.formas.forEach(function (f) {
    const caja = { x: f.x, y: f.y, w: f.w, h: f.h };
    if (f.tipo === "rect") {
      s.addShape(pptx.ShapeType.rect, Object.assign({}, caja, {
        fill: f.fill ? { color: f.fill } : { type: "none" }, line: { width: 0 },
      }));
      return;
    }
    if (f.tipo === "img") {
      s.addImage(Object.assign({}, caja, { path: path.join(MEDIA, f.src) }));
      return;
    }
    // texto: un run de pptxgenjs por cada run del original, para conservar los
    // cambios de cuerpo y color dentro de un mismo párrafo
    const runs = [];
    f.p.forEach(function (par, k) {
      par.runs.forEach(function (r, j) {
        runs.push({
          text: r.t,
          options: {
            fontFace: r.f || "Barlow", fontSize: r.sz || 12,
            color: r.c || "1D1F20", bold: !!r.b, italic: !!r.i,
            charSpacing: r.spc, align: ALIN[par.algn] || "left",
            lineSpacingMultiple: par.lns,
            breakLine: j === par.runs.length - 1 && k < f.p.length - 1,
          },
        });
      });
    });
    s.addText(runs, Object.assign({}, caja, {
      isTextBox: true, margin: f.m || 0, valign: f.anchor === "ctr" ? "middle"
        : f.anchor === "b" ? "bottom" : "top",
      wrap: true,
    }));
  });
});

const salida = process.argv[2]
  || path.join(__dirname, "salidas", "deck_regenerado.pptx");
pptx.writeFile({ fileName: salida })
  .then(function () { console.log("escrito:", salida, "·", PLACAS.length, "placas"); });
