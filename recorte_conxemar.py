# -*- coding: utf-8 -*-
"""El recorte de desembarque del paquete de medidas discutido en Conxemar 2025.

Una sola definición del recorte, para que `demanda_inversa_modelo.py` y
`demanda_inversa_tangonera.py` simulen exactamente el mismo escenario. Antes cada uno
lo tenía por su lado: el modelo lo derivaba de los desembarques y la tangonera lo
llevaba escrito como −0,0736. Coincidían a tres decimales, pero eran dos fuentes.

El paquete son dos medidas:
  * **Zafra de Rawson acortada a cuatro meses.** Su zafra efectiva es noviembre-marzo,
    así que la que sale es la punta más chica, marzo.
  * **Cierre de la zafra nacional a mediados de septiembre.** Se pierde la mitad de
    septiembre y todo octubre de la flota congeladora tangonera.

La base es el promedio 2013-2026 acotado a **2022-2024**: tres años, para no anclar el
escenario ni en el pico de 2018 ni en el paro de 2025. El porcentaje se mide contra el
desembarque de langostino de TODAS las flotas, que es el universo sobre el que se
discute la medida.

Fuente: `_lan.pkl`, planillas de la Subsecretaría de Pesca y Acuicultura por puerto,
flota, especie y mes.
"""
from __future__ import annotations

import os

import pandas as pd

RAIZ = os.path.dirname(os.path.abspath(__file__))
PKL = os.path.join(RAIZ, "_lan.pkl")
ANIOS_BASE = (2022, 2024)
FLOTA_TANGONERA = "CONG. TANGONEROS"

# Exportación total de langostino de 2025, en millones de dólares. Es lo que convierte
# el porcentaje de facturación del escenario en la cifra que va a la presentación, y
# vive acá por el mismo motivo que el recorte: los tres scripts de simulación la usaban
# escrita por separado.
EXPO_2025 = 867.0


def recorte(pkl: str = PKL) -> dict:
    """Toneladas que deja de desembarcar el paquete, y qué fracción del total son."""
    lan = pd.read_pickle(pkl)
    base = lan[lan.anio.between(*ANIOS_BASE)]
    n = ANIOS_BASE[1] - ANIOS_BASE[0] + 1

    total = base.t.sum() / n
    rawson_mes = (base[base.puerto.str.contains("Rawson", case=False, na=False)]
                  .groupby("mes").t.sum() / n)
    tangonera_mes = (base[base.flota == FLOTA_TANGONERA].groupby("mes").t.sum() / n)

    corte_rawson = rawson_mes.loc[3]                                  # marzo
    corte_nacional = tangonera_mes.loc[9] / 2 + tangonera_mes.loc[10]  # ½ sep + oct
    corte = corte_rawson + corte_nacional

    return {"total_t": total,
            "rawson_t": corte_rawson,
            "nacional_t": corte_nacional,
            "corte_t": corte,
            "dq": -corte / total}


def describir(r: dict | None = None) -> str:
    """Las tres líneas que los dos scripts imprimen antes de la simulación."""
    r = r or recorte()
    return (f"Desembarque base (media {ANIOS_BASE[0]}-{ANIOS_BASE[1]}): "
            f"{r['total_t']:,.0f} t\n"
            f"  Rawson a cuatro meses (sale marzo):            -{r['rawson_t']:,.0f} t\n"
            f"  cierre nacional a mediados de septiembre:      -{r['nacional_t']:,.0f} t\n"
            f"  RECORTE TOTAL: {r['corte_t']:,.0f} t = "
            f"{-r['dq'] * 100:.1f}% del desembarque")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    r = recorte()
    print(describir(r))
    print(f"\ndq = {r['dq']:.6f}")
