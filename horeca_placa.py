# -*- coding: utf-8 -*-
"""Prepara los datos de la placa del canal HORECA para el deck.

El deck no escribe ninguna de estas cifras a mano: las lee de
«salidas/horeca_placa.json», que genera este guion desde el índice mensual.
Si cambia el dato, correr esto y regenerar el deck.

Sale, además de las series:
  · el promedio de los últimos doce meses de cada mercado, en base 2019 = 100
  · el pozo de abril de 2020, que es el argumento para usar índice observado
    y no una variable binaria de pandemia
  · el mes en que el combinado recuperó el nivel de 2019

Uso:  python horeca_placa.py
Salida: salidas/horeca_placa.json
"""
from __future__ import annotations

import json
import os
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))

# Participación de cada mercado en el volumen del L1 tangonero, de la cabecera de
# demanda_inversa_horeca.py. Suman 89,7%.
PESO = {"h_ES": 43.5, "h_IT": 21.1, "h_CN": 13.6, "h_JP": 11.5}
NOMBRE = {"h_ES": "España", "h_IT": "Italia", "h_CN": "China", "h_JP": "Japón"}
SERIES = ["h_ES", "h_IT", "h_CN", "h_JP"]


def main() -> None:
    d = pd.read_pickle(os.path.join(RAIZ, "datos", "horeca_indice.pkl"))
    d = d[SERIES + ["horeca_ue"]]

    # Etiquetas: el año sólo en enero, para que el eje no se amontone.
    # Año de dos dígitos y cada dos años: con 163 categorías, una etiqueta de
    # cuatro caracteres no entra en el ancho de una y PowerPoint la parte.
    labels = ["'" + str(p.year)[2:] if (p.month == 1 and p.year % 2 == 1) else ""
              for p in d.index]

    # Promedio de los últimos doce meses con dato en cada serie: las fuentes no
    # cierran todas el mismo mes (China publica antes que Italia).
    ult = {c: float(d[c].dropna().tail(12).mean()) for c in SERIES + ["horeca_ue"]}

    c = d.horeca_ue.dropna()
    pozo_val, pozo_per = float(c.min()), c.idxmin()
    vuelta = c[(c.index > pozo_per) & (c >= 100)].index.min()

    MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    out = {
        "labels": labels,
        "series": [{"name": NOMBRE[c], "values": [None if pd.isna(v) else round(float(v), 1)
                                                  for v in d[c]]} for c in SERIES],
        "combinado": {"name": "Índice combinado",
                      "values": [None if pd.isna(v) else round(float(v), 1)
                                 for v in d.horeca_ue]},
        "tarjetas": [{"mercado": NOMBRE[c], "nivel": round(ult[c], 1),
                      "brecha_pct": round(ult[c] - 100, 1), "peso_pct": PESO[c]}
                     for c in sorted(SERIES, key=lambda k: -ult[k])],
        "combinado_ult12": round(ult["horeca_ue"], 1),
        "pozo": {"nivel": round(pozo_val, 1),
                 "caida_pct": round(100 - pozo_val, 1),
                 "mes": f"{MES[pozo_per.month - 1]} de {pozo_per.year}"},
        "vuelta_a_100": f"{MES[vuelta.month - 1]} de {vuelta.year}",
        "desde": str(d.index.min()), "hasta": str(d.index.max()),
        "pie": ("Fuente: elaboración propia sobre INE (España, CNAE 56), ISTAT "
                "(Italia, Ateco 56; "
                "mensual desde 2021, trimestral antes), NBS (China, ingresos "
                "HORECA) y METI (Japón, actividad terciaria, HORECA). "
                "Base 2019 = 100, series sin ajuste estacional. El combinado pondera "
                "por la participación de cada mercado en el volumen del L1 tangonero."),
    }

    sal = os.path.join(RAIZ, "salidas", "horeca_placa.json")
    with open(sal, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"{d.index.min()} a {d.index.max()} · {len(d)} meses")
    print(f"pozo: {out['pozo']['nivel']} en {out['pozo']['mes']} "
          f"(−{out['pozo']['caida_pct']}%)   ·   vuelve a 100 en {out['vuelta_a_100']}")
    print(f"últimos doce meses, combinado {out['combinado_ult12']}")
    for t in out["tarjetas"]:
        print(f"   {t['mercado']:<8s} {t['nivel']:6.1f}  ({t['brecha_pct']:+.1f} contra 2019)"
              f"   peso {t['peso_pct']}%")
    print(f"\nGuardado: {sal}")


if __name__ == "__main__":
    main()
