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

## La base de la simulación: tres cantidades que no son la misma

Acá vive también `simular()`, y el motivo es un error que los tres scripts de simulación
cometían por separado. La identidad del ingreso

    d(P·Q)/dQ = P·(1 + f)      →      Δingreso% = (1 + f)·Δq%

sólo vale si las tres cantidades que intervienen son la misma. No lo eran:

    f          del sistema IAIDS europeo: es ∂log p / ∂log q del volumen argentino
               EMBARCADO A LA UE, y sólo describe el precio en ese mercado
    Δq         medido sobre el DESEMBARQUE de todas las flotas
    la base    US$ 867 M de EXPORTACIÓN TOTAL, todos los productos y destinos

Argentina también vende a Estados Unidos y a Asia. Si el precio sube sólo en la UE, la
facturación del resto cae con el volumen y sin compensación de precio. Separando ámbitos:

    Δingreso = V_ámbito·(1+f)·Δq  +  V_resto·Δq  =  Δq·(V_total + f·V_ámbito)
    Δingreso% = Δq·(1 + f·s)           con s = V_ámbito / V_total

La fórmula vieja es el caso particular s = 1, o sea suponer que la f europea gobierna el
precio de todo lo que Argentina exporta. Como f es negativa y s < 1, corregirlo empeora
el escenario: el recorte pierde MÁS plata, no menos.

El ámbito depende de qué f se use, y no todas son europeas:

    sistema IAIDS por origen        precio de importación en la UE      →  ámbito UE
    ecuación única, tangonera, IV   FOB argentino, todos los destinos   →  ámbito total

Para las segundas s = 1 y la fórmula vieja era correcta; el error estaba en aplicarle la
misma base a la primera.

Fuentes: `_lan.pkl` (desembarques SSPyA por puerto, flota, especie y mes) para el recorte;
`datos/aduana_langostino_total.pkl` para el valor exportado total; Softrade vía
`fuentes/expo.py` para la composición por destino y por flota, que es para lo que sirve
—la regla de la casa es nivel del registro oficial, composición del transaccional—.
"""
from __future__ import annotations

import os

import pandas as pd

RAIZ = os.path.dirname(os.path.abspath(__file__))
PKL = os.path.join(RAIZ, "_lan.pkl")
ANIOS_BASE = (2022, 2024)
FLOTA_TANGONERA = "CONG. TANGONEROS"

# Exportación total de langostino de 2025, en millones de dólares. Queda como CONTRASTE
# del valor que `base_exportadora()` calcula del registro oficial: si los dos difieren
# más de un 5% hay algo mal en el filtro de NCM o en el año, y conviene enterarse.
EXPO_2025 = 867.0
ANIO_BASE_EXPO = 2025

# Los 27 de la UE con las grafías de la base de comercio. Definición única del proyecto:
# `cif_vs_fob.py` la tenía por su lado.
UE = ["ESPAÑA", "ESPANA", "ITALIA", "FRANCIA", "PAISES BAJOS", "PAÍSES BAJOS",
      "HOLANDA", "BELGICA", "BÉLGICA", "ALEMANIA", "PORTUGAL", "GRECIA", "DINAMARCA",
      "LITUANIA", "POLONIA", "SUECIA", "IRLANDA", "RUMANIA", "RUMANÍA", "LETONIA",
      "ESTONIA", "FINLANDIA", "AUSTRIA", "REPUBLICA CHECA", "REPÚBLICA CHECA",
      "BULGARIA", "CROACIA", "ESLOVENIA", "HUNGRIA", "HUNGRÍA", "MALTA", "CHIPRE",
      "ESLOVAQUIA", "LUXEMBURGO"]


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

    # Composición del corte por flota. No es cosmética: la segunda medida es 100%
    # tangonera congeladora, que es la que hace el entero que va a España e Italia, y
    # la primera cae sobre Rawson, que es plaza fresquera. El corte NO es neutral en
    # destino, y eso cambia cuánto de él pega en el mercado donde se estimó la f.
    raw = base[base.puerto.str.contains("Rawson", case=False, na=False)]
    raw_mar = raw[raw.mes == 3]
    raw_tan = raw_mar[raw_mar.flota == FLOTA_TANGONERA].t.sum() / n
    corte_tan = raw_tan + corte_nacional
    tan_total = base[base.flota == FLOTA_TANGONERA].t.sum() / n

    return {"total_t": total,
            "rawson_t": corte_rawson,
            "nacional_t": corte_nacional,
            "corte_t": corte,
            "dq": -corte / total,
            "corte_tan_t": corte_tan,
            "corte_fre_t": corte - corte_tan,
            "tan_total_t": tan_total,
            "fre_total_t": total - tan_total}


def base_exportadora(anio: int = ANIO_BASE_EXPO) -> dict:
    """Valor exportado total y qué fracción de él va a la UE, por flota.

    Nivel del registro oficial (aduana), composición del transaccional (Softrade): es
    la regla de la casa y acá importa, porque Softrade no sirve para nivel de volumen
    —antes de 2020 tiene doble conteo que infla los kilos hasta 1,45x— pero sí para
    destino y para la marca de congelado a bordo, que es lo que separa las flotas.
    """
    a = pd.read_pickle(os.path.join(RAIZ, "datos", "aduana_langostino_total.pkl"))
    v_total = float(a[a.anio == anio].fob.sum()) / 1e6            # US$ M, todos los NCM

    if abs(v_total - EXPO_2025) / EXPO_2025 > 0.05 and anio == ANIO_BASE_EXPO:
        print(f"AVISO: la exportación {anio} calculada del registro oficial da "
              f"US$ {v_total:,.0f} M contra los US$ {EXPO_2025:,.0f} M de referencia. "
              "Revisar el filtro de NCM antes de usar el número.")

    from fuentes import expo
    e = expo.cargar_todos()
    e = e[(e.anio == anio) & (e.kg > 0) & (e.fob_tot > 0)].copy()
    e["ue"] = e.destino.str.upper().str.strip().isin(UE)
    e["tan"] = e.ruta.eq("a bordo")                # congelado a bordo = tangonera

    def _s(sub):
        return float(sub[sub.ue].fob_tot.sum() / sub.fob_tot.sum()) if len(sub) else float("nan")

    return {"anio": anio,
            "v_total": v_total,
            "s_ue": _s(e),
            "s_ue_tan": _s(e[e.tan]),
            "s_ue_fre": _s(e[~e.tan]),
            "v_ue": v_total * _s(e)}


def simular(f: float, rec: dict, base: dict, ambito: str = "total") -> dict:
    """Efecto del recorte sobre precio y facturación, con el ámbito explícito.

    `ambito` dice sobre qué mercado rige la f que se le pasa:
        "total"  f estimada sobre el FOB argentino, todos los destinos (ecuación
                 única, tangonera, IV). El precio se mueve en todo lo exportado.
        "ue"     f estimada sobre el precio de importación europeo (sistema IAIDS por
                 origen). El precio se mueve SÓLO en lo que se embarca a la UE; el
                 resto pierde volumen sin compensación.

    Δingreso% = Δq·(1 + f·s), con s la fracción del valor exportado que cae bajo la f.
    Con s = 1 se recupera la fórmula vieja, que es la correcta para el ámbito total.
    """
    if ambito not in ("total", "ue"):
        raise ValueError(f"ámbito desconocido: {ambito}")
    dq = rec["dq"]

    if ambito == "total":
        s, dq_amb = 1.0, dq
    else:
        # El corte no es neutral en destino: se traduce a volumen UE pasando cada
        # flota por SU propia participación europea, y se mide contra el volumen UE.
        s = base["s_ue"]
        corte_ue = (rec["corte_tan_t"] * base["s_ue_tan"]
                    + rec["corte_fre_t"] * base["s_ue_fre"])
        q_ue = (rec["tan_total_t"] * base["s_ue_tan"]
                + rec["fre_total_t"] * base["s_ue_fre"])
        dq_amb = -corte_ue / q_ue

    return {"f": f, "ambito": ambito, "s": s,
            "Δ oferta %": dq * 100,
            "Δ oferta en el ámbito %": dq_amb * 100,
            "Δ precio %": f * dq_amb * 100,
            "Δ ingreso %": (dq + f * s * dq_amb) * 100,
            "Δ ingreso US$ M": base["v_total"] * (dq + f * s * dq_amb)}


def umbral(rec: dict, base: dict, ambito: str = "total") -> float:
    """La f que deja la facturación igual. NO siempre es −1.

    De Δingreso = Δq·(1 + f·s·ρ) = 0 sale f* = −1/(s·ρ), con ρ = Δq_ámbito/Δq. Con
    ámbito total (s = 1, ρ = 1) da −1, que es el umbral que el estudio viene usando.
    Con una f europea y la mitad del valor exportado fuera de la UE, el umbral se va
    cerca de −2: el precio sube sólo donde rige la f, y la otra mitad pierde volumen
    sin compensación. O sea que para el sistema por origen, «alcanza con |f| > 1» es
    una vara demasiado baja, no demasiado alta.
    """
    if ambito == "total":
        return -1.0
    r = simular(0.0, rec, base, ambito)
    rho = r["Δ oferta en el ámbito %"] / r["Δ oferta %"]
    return -1.0 / (base["s_ue"] * rho)


def tabla(supuestos, rec: dict | None = None, base: dict | None = None):
    """`supuestos` es una lista de (nombre, f, ámbito). Devuelve el cuadro del §5."""
    rec = rec or recorte()
    base = base or base_exportadora()
    filas = [dict(supuesto=n, **simular(f, rec, base, amb)) for n, f, amb in supuestos]
    return pd.DataFrame(filas).set_index("supuesto")


def describir_base(base: dict) -> str:
    return (f"Base exportadora {base['anio']}: US$ {base['v_total']:,.0f} M en total, "
            f"{base['s_ue'] * 100:.0f}% a la UE (US$ {base['v_ue']:,.0f} M).\n"
            f"  participación europea por flota: tangonera {base['s_ue_tan'] * 100:.0f}% · "
            f"fresquera {base['s_ue_fre'] * 100:.0f}%")


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
    print(f"  del corte, {r['corte_tan_t']:,.0f} t son tangoneras y "
          f"{r['corte_fre_t']:,.0f} t fresqueras")
    b = base_exportadora()
    print("\n" + describir_base(b))
    print("\nEl mismo recorte, según el ámbito de la f (f = -0,241 del sistema europeo):")
    print(tabla([("f europea leída como si rigiera todo (lo que se hacía)", -0.241, "total"),
                 ("f europea con su ámbito correcto", -0.241, "ue")],
                r, b).round(2).to_string())
    print(f"\nUmbral de facturación: ámbito total {umbral(r, b, 'total'):+.2f} · "
          f"ámbito UE {umbral(r, b, 'ue'):+.2f}")
