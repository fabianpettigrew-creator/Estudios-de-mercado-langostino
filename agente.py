"""
El agente: un bucle sobre la API de Anthropic con las herramientas de consulta.

No hay framework. Son unas cuarenta líneas de bucle, y esa es la idea: podés
leerlo entero y saber exactamente qué pasa en cada iteración.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import anthropic

from almacen import guardar_informe
from config import DB_PATH, INFORMES_DIR, MAX_ITERACIONES, MAX_TOKENS, MODELO
from herramientas import ESQUEMAS, ejecutar

log = logging.getLogger(__name__)

INSTRUCCIONES = """Sos un analista de mercado especializado en langostino y camarón, \
y escribís para una cámara de armadores pesqueros argentinos.

Reglas que no se negocian:

1. Toda cifra que escribas tiene que venir de una herramienta. Si querés un \
número que ninguna herramienta devuelve, decí que no está disponible. Nunca \
estimes, nunca completes de memoria, nunca redondees hacia una cifra "más linda".

2. El langostino argentino (Pleoticus muelleri) es salvaje y premium. El grueso \
del mercado mundial es vannamei de cultivo (Ecuador, India, Vietnam). No son el \
mismo producto, pero compiten por el presupuesto del importador. Analizá esa \
sustitución de forma explícita: si el vannamei baja de precio, el langostino \
argentino pierde espacio aunque su propio precio no se mueva.

3. Consultá siempre el informe anterior antes de redactar. El informe de este \
mes tiene que decir qué cambió respecto del anterior y qué se confirmó. Un \
informe que repite las mismas generalidades doce veces por año no sirve.

4. Distinguí lo que los datos muestran de lo que interpretás. Las hipótesis van \
marcadas como tales.

5. Si una serie tiene pocos meses o hay huecos, decilo. Un dato flojo señalado \
es útil; un dato flojo presentado como firme es un problema.

Estructura del informe:
- Síntesis (5 líneas, lo que un directivo lee si no lee nada más)
- Estados Unidos: volúmenes, precios, posición argentina
- Unión Europea: ídem, abriendo por mercado nacional si hay datos
- Precio relativo langostino argentino vs. vannamei
- Qué cambió respecto del mes anterior
- Señales a seguir

Escribí en español rioplatense, sobrio y directo. Sin adjetivos de más."""


def _bloque_texto(mensaje) -> str:
    return "\n".join(b.text for b in mensaje.content if b.type == "text")


def ejecutar_agente(anio: int, mes: int, ruta_db: Path | str = DB_PATH,
                    guardar: bool = True) -> str:
    """
    Corre el agente para un período y devuelve el informe.

    El bucle: el modelo pide herramientas, se las ejecutamos, le devolvemos
    los resultados, y así hasta que responde sin pedir nada más.
    """
    cliente = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    mensajes = [{
        "role": "user",
        "content": (
            f"Preparás el informe mensual de mercado correspondiente a "
            f"{mes:02d}/{anio}. Empezá por el resumen del período y el informe "
            f"anterior, después profundizá donde encuentres algo que explicar. "
            f"Cuando tengas todo, escribí el informe completo."
        ),
    }]

    for iteracion in range(MAX_ITERACIONES):
        respuesta = cliente.messages.create(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=INSTRUCCIONES,
            tools=ESQUEMAS,
            messages=mensajes,
        )

        mensajes.append({"role": "assistant", "content": respuesta.content})

        if respuesta.stop_reason != "tool_use":
            informe = _bloque_texto(respuesta)
            log.info("Informe listo en %d iteraciones", iteracion + 1)
            if guardar:
                guardar_informe(anio, mes, informe, ruta_db)
                INFORMES_DIR.mkdir(parents=True, exist_ok=True)
                destino = INFORMES_DIR / f"informe_{anio}_{mes:02d}.md"
                destino.write_text(informe, encoding="utf-8")
                log.info("Guardado en %s", destino)
            return informe

        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue
            log.info("→ %s(%s)", bloque.name,
                     ", ".join(f"{k}={v}" for k, v in bloque.input.items()))
            salida = ejecutar(bloque.name, bloque.input, ruta_db)
            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,
                "content": json.dumps(salida, ensure_ascii=False, default=str),
            })

        mensajes.append({"role": "user", "content": resultados})

    raise RuntimeError(
        f"El agente no terminó en {MAX_ITERACIONES} iteraciones. "
        f"Revisá si alguna herramienta está devolviendo error en loop."
    )


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="Genera el informe mensual")
    p.add_argument("anio", type=int)
    p.add_argument("mes", type=int)
    args = p.parse_args()

    print(ejecutar_agente(args.anio, args.mes))
