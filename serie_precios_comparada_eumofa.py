# -*- coding: utf-8 -*-
"""El mismo análisis de la placa 9, pero con el precio argentino que publica EUMOFA.

La versión original mide el langostino con el FOB de despacho del entero L1 congelado a
bordo, que sale de la base de comercio, y lo compara contra el precio de importación
del camarón de cultivo de EUMOFA. Esa comparación tiene una asimetría: el numerador es
FOB de origen y el denominador es CIF en frontera de la UE.

Acá se rehace todo del lado de EUMOFA, que es la comparación simétrica:

  numerador     «Shrimp, miscellaneous» congelado, origen Argentina, importación
                extra-UE, valor unitario CIF en euros por kilo;
  denominador   «Shrimp, warmwater» congelado desde Ecuador, India, Vietnam,
                Bangladesh, Indonesia y Tailandia, mismo tratamiento.

Las dos puntas son entonces CIF, misma fuente, misma convención y mismo mes.

LO QUE SE GANA Y LO QUE SE PIERDE. Se gana simetría: desaparece el desfase FOB/CIF y
las dos series pasan por el mismo filtro estadístico. Se pierde producto: el agregado
argentino de EUMOFA es TODO el langostino congelado que entra a la UE —entero y cola,
todos los calibres, las dos flotas—, mientras que el FOB de la base de comercio aísla
el entero L1 congelado a bordo, que es el producto del que trata el estudio. O sea que
esta versión mide bien el precio relativo de «el langostino argentino» y peor el
precio relativo del L1 tangonero.

Uso:  python serie_precios_comparada_eumofa.py
Salida: consola + salidas/serie_precios_comparada_eumofa.xlsx + .svg/.png
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402

A, B = 2024, 2025


def serie() -> pd.DataFrame:
    """Todo junto: las tres series de EUMOFA, el FOB del L1 para contraste y la
    captura tangonera."""
    df, _ = T.panel()
    d = pd.DataFrame(index=df.index)
    d["ar_eur_kg"] = df.ar_eur_kg              # Argentina CIF, EUMOFA
    d["van_eur_kg"] = df.van_eur_kg            # cultivo agregado CIF, EUMOFA
    d["van_ec_eur_kg"] = df.van_ec_eur_kg      # Ecuador CIF, EUMOFA
    d["p_eur"] = df.p_eur                      # FOB del L1 a bordo, en euros
    d["rel_eumofa"] = d.ar_eur_kg / d.van_eur_kg
    d["rel_eumofa_ec"] = d.ar_eur_kg / d.van_ec_eur_kg
    d["rel_fob"] = df.rel                      # la versión original
    d["tan_t"] = df.tan_t
    d["ar_kt"] = df.ar_kt
    return d


def variacion(an: pd.DataFrame, col: str) -> float:
    return float(np.log(an[col][B] / an[col][A]) * 100)


def grafico(d: pd.DataFrame, an: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    coma = FuncFormatter(lambda x, _: f"{x:,.2f}".replace(".", ","))
    x = d.index.to_timestamp()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.2, 6.4), sharex=True,
                                 gridspec_kw={"height_ratios": [1.35, 1]})
    for ax in (a1, a2):
        for y0, col in [(A, "#dce6f1"), (B, "#f4dcda")]:
            ax.axvspan(pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y0 + 1}-01-01"),
                       color=col, zorder=0)
        ax.grid(lw=.4, alpha=.4)
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)

    a1.plot(x, d.ar_eur_kg, lw=1.7, color="#1f4e79",
            label="Langostino argentino, importación extra-UE (EUR/kg CIF)")
    a1.plot(x, d.van_eur_kg, lw=1.6, color="#c0504d",
            label="Camarón de cultivo, importación extra-UE (EUR/kg CIF)")
    a1.plot(x, d.van_ec_eur_kg, lw=1.2, color="#e0a58f", ls="--",
            label="Ídem, sólo Ecuador (EUR/kg CIF)")
    a1.set_ylabel("Euros por kilo")
    a1.yaxis.set_major_formatter(coma)
    a1.legend(frameon=False, fontsize=8.4, loc="upper left")

    a2.plot(x, d.rel_eumofa, lw=1.7, color="#1f4e79",
            label="Cociente EUMOFA: langostino argentino / cultivo (las dos puntas CIF)")
    a2.plot(x, d.rel_fob, lw=1.0, color="#9aa7ad",
            label="Versión anterior: FOB del entero L1 a bordo / cultivo")
    a2.axhline(1, lw=.8, color="#7f7f7f")
    for y0, yt in ((A, 0.72), (B, 0.66)):
        a2.plot([pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y0 + 1}-01-01")],
                [an.rel_eumofa[y0]] * 2, lw=2.4, color="#404040", zorder=4)
        a2.annotate(f"promedio {y0}: {an.rel_eumofa[y0]:.3f}".replace(".", ","),
                    (pd.Timestamp(f"{y0}-07-01"), an.rel_eumofa[y0]),
                    xytext=(pd.Timestamp(f"{y0}-07-01"), yt), fontsize=8.4,
                    color="#404040", ha="center", va="top", zorder=5,
                    arrowprops={"arrowstyle": "-", "lw": .7, "color": "#8a8a8a",
                                "shrinkA": 2, "shrinkB": 2})
    a2.set_ylabel("Cociente Argentina / cultivo")
    a2.yaxis.set_major_formatter(coma)
    a2.legend(frameon=False, fontsize=8, loc="upper left")
    a2.annotate("promedios anuales de la línea azul: "
                f"{variacion(an, 'rel_eumofa'):+.1f}%".replace(".", ","),
                (pd.Timestamp("2015-06-01"), 0.635), fontsize=9, color="#c0504d")

    fig.text(.01, .012,
             "Fuente: elaboración propia sobre EUMOFA / Eurostat-Comext, importación "
             "extra-UE de camarón congelado: «Shrimp, miscellaneous» de origen Argentina "
             "en el numerador y «Shrimp,\nwarmwater» desde Ecuador, India, Vietnam, "
             "Bangladesh, Indonesia y Tailandia en el denominador; valores unitarios CIF "
             "en frontera. La línea gris del panel inferior es la versión anterior, con "
             "el\nFOB de despacho del entero L1 congelado a bordo. El agregado argentino "
             "de EUMOFA incluye entero y cola, todos los calibres y las dos flotas.",
             fontsize=6.6)
    fig.tight_layout(rect=(0, .085, 1, 1))
    out = os.path.join(RAIZ, "salidas", "serie_precios_comparada_eumofa.svg")
    fig.savefig(out)
    fig.savefig(out.replace(".svg", ".png"), dpi=200)
    print(f"\nGráfico: {out} (+ .png)")


def main() -> None:
    d = serie()
    print("=" * 100)
    print("EL MISMO ANÁLISIS, CON EL PRECIO ARGENTINO DE EUMOFA (las dos puntas CIF)")
    print("=" * 100)
    print(f"Mensual, {d.index.min()} a {d.index.max()}")

    an = d.groupby(d.index.year).agg(
        ar=("ar_eur_kg", "mean"), van=("van_eur_kg", "mean"),
        van_ec=("van_ec_eur_kg", "mean"), p_eur=("p_eur", "mean"),
        rel_eumofa=("rel_eumofa", "mean"), rel_eumofa_ec=("rel_eumofa_ec", "mean"),
        rel_fob=("rel_fob", "mean"), captura_t=("tan_t", "sum"),
        ar_kt=("ar_kt", "sum"))
    print("\n" + "-" * 100)
    print("PROMEDIOS ANUALES")
    print("-" * 100)
    print(an.round(3).to_string())

    print("\n" + "-" * 100)
    print(f"{A} → {B}, PASO A PASO")
    print("-" * 100)
    for nom, c in [("langostino argentino (EUMOFA, CIF)", "ar"),
                   ("camarón de cultivo (EUMOFA, CIF)", "van"),
                   ("cociente Argentina / cultivo", "rel_eumofa")]:
        v0, v1 = an[c][A], an[c][B]
        print(f"   {nom:<38s} {v0:6.3f} → {v1:6.3f}   {np.log(v1 / v0) * 100:+5.1f}%")
    dq = np.log(an.captura_t[B] / an.captura_t[A]) * 100
    dr = variacion(an, "rel_eumofa")
    print(f"   {'captura tangonera (t)':<38s} {an.captura_t[A]:6.0f} → "
          f"{an.captura_t[B]:6.0f}   {dq:+5.1f}%")
    print(f"\n   Flexibilidad de arco = {dr:.1f} / {dq:.1f} = {dr / dq:+.3f}")

    print("\n" + "-" * 100)
    print("LAS DOS VERSIONES, UNA AL LADO DE LA OTRA")
    print("-" * 100)
    filas = [("Precio argentino de EUMOFA contra cultivo agregado", "rel_eumofa"),
             ("Precio argentino de EUMOFA contra Ecuador", "rel_eumofa_ec"),
             ("FOB del entero L1 a bordo contra cultivo agregado (la placa 9)",
              "rel_fob")]
    for nom, c in filas:
        print(f"   {nom:<62s} {an[c][A]:.3f} → {an[c][B]:.3f}   "
              f"{variacion(an, c):+5.1f}%")
    print("\n   El número de la placa 9 es el de la última línea.")

    # ------------------------------------------------------------- salida
    sal = os.path.join(RAIZ, "salidas", "serie_precios_comparada_eumofa.xlsx")
    try:
        with pd.ExcelWriter(sal, engine="openpyxl") as w:
            m = d.copy()
            m.index = m.index.astype(str)
            m.round(4).to_excel(w, sheet_name="mensual")
            an.round(4).to_excel(w, sheet_name="anual")
            pd.DataFrame([{"version": n, str(A): an[c][A], str(B): an[c][B],
                           "var_%": variacion(an, c)} for n, c in filas]).round(3) \
                .to_excel(w, sheet_name="versiones", index=False)
        print(f"\nGuardado: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal}")

    grafico(d, an)


if __name__ == "__main__":
    main()
