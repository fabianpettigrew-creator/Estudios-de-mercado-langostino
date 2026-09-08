# -*- coding: utf-8 -*-
"""La serie que hay detrás del +3,1% de la placa 9.

Pone una al lado de la otra las dos series de precio que el estudio compara:

  · el FOB del langostino entero L1 congelado a bordo de la flota tangonera, que sale
    de la base de comercio (despachos con kilos y FOB positivos), pasado a euros con
    el tipo de cambio mensual;
  · el precio de importación extra-UE de camarón de cultivo congelado —EUMOFA,
    «Shrimp, warmwater», Ecuador, India, Vietnam, Bangladesh, Indonesia y Tailandia—,
    que es el valor unitario de la importación, en euros por kilo. Se agrega también
    la variante sólo Ecuador, que es la más cercana a vannamei puro.

El cociente entre las dos es el precio relativo. El +3,1% de la placa es la variación
de ese cociente entre 2024 y 2025, en promedio anual de la serie mensual y medida en
diferencia de logaritmos, que es como está en `demanda_inversa_tangonera.main()`.

Uso:  python serie_precios_comparada.py
Salida: consola + salidas/serie_precios_comparada.xlsx
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

COLS = ["p_tan", "eurusd", "p_eur", "van_eur_kg", "van_ec_eur_kg", "rel", "rel_ec",
        "tan_t", "q_exp_t"]


def serie() -> pd.DataFrame:
    df, _ = T.panel()
    d = df.copy()
    d["rel_ec"] = d.p_eur / d.van_ec_eur_kg
    return d[COLS]


def grafico(d: pd.DataFrame, an: pd.DataFrame) -> None:
    """Dos paneles: los precios en euros por kilo arriba y el cociente abajo, con
    2024 y 2025 sombreados, que son los dos años que compara la placa."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    coma = FuncFormatter(lambda x, _: f"{x:,.2f}".replace(".", ","))
    x = d.index.to_timestamp()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.2, 6.4), sharex=True,
                                 gridspec_kw={"height_ratios": [1.35, 1]})

    for ax in (a1, a2):
        for y0, col in [(2024, "#dce6f1"), (2025, "#f4dcda")]:
            ax.axvspan(pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y0 + 1}-01-01"),
                       color=col, zorder=0)
        ax.grid(lw=.4, alpha=.4)
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)

    a1.plot(x, d.p_eur, lw=1.7, color="#1f4e79",
            label="Langostino entero L1 tangonero, FOB (EUR/kg)")
    a1.plot(x, d.van_eur_kg, lw=1.6, color="#c0504d",
            label="Camarón de cultivo, importación extra-UE (EUR/kg)")
    a1.plot(x, d.van_ec_eur_kg, lw=1.2, color="#e0a58f", ls="--",
            label="Ídem, sólo Ecuador (EUR/kg)")
    a1.set_ylabel("Euros por kilo")
    a1.yaxis.set_major_formatter(coma)
    a1.legend(frameon=False, fontsize=8.4, loc="upper left")

    a2.plot(x, d.rel, lw=1.7, color="#1f4e79")
    a2.axhline(1, lw=.8, color="#7f7f7f")
    for y0, yt in ((2024, 0.70), (2025, 0.64)):
        a2.plot([pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y0 + 1}-01-01")],
                [an.rel[y0]] * 2, lw=2.4, color="#404040", zorder=4)
        a2.annotate(f"promedio {y0}: {an.rel[y0]:.3f}".replace(".", ","),
                    (pd.Timestamp(f"{y0}-07-01"), an.rel[y0]),
                    xytext=(pd.Timestamp(f"{y0}-07-01"), yt), fontsize=8.4,
                    color="#404040", ha="center", va="top", zorder=5,
                    arrowprops={"arrowstyle": "-", "lw": .7, "color": "#8a8a8a",
                                "shrinkA": 2, "shrinkB": 2})
    d24, d25 = an.rel[2024], an.rel[2025]
    a2.set_ylabel("Cociente L1 / cultivo")
    a2.yaxis.set_major_formatter(coma)
    a2.annotate("promedios anuales de la línea azul: "
                f"{np.log(d25 / d24) * 100:+.1f}%".replace(".", ","),
                (pd.Timestamp("2022-01-01"), 1.20), fontsize=9, color="#c0504d")

    fig.text(.01, .012,
             "Fuente: elaboración propia sobre base de comercio (FOB del entero L1 "
             "congelado a bordo: leyenda «congelado a bordo» hasta 2017, sufijo SIM SA01 "
             "desde 2018), BCE (tipo de\ncambio) y EUMOFA (importación extra-UE de camarón "
             "warmwater congelado desde Ecuador, India, Vietnam, Bangladesh, Indonesia y "
             "Tailandia; valor unitario). El cociente\ndel panel inferior es el precio "
             "relativo que usa el modelo: mide el langostino descontando lo que hizo el "
             "mercado mundial del camarón.",
             fontsize=6.6)
    fig.tight_layout(rect=(0, .075, 1, 1))
    out = os.path.join(RAIZ, "salidas", "serie_precios_comparada.svg")
    fig.savefig(out)
    fig.savefig(out.replace(".svg", ".png"), dpi=200)
    print(f"\nGráfico: {out} (+ .png)")


def main() -> None:
    d = serie()
    print("=" * 100)
    print("SERIE COMPARADA DE PRECIOS · LANGOSTINO L1 TANGONERO vs CAMARÓN DE CULTIVO")
    print("=" * 100)
    print(f"Mensual, {d.index.min()} a {d.index.max()} · {len(d)} meses")
    print("p_tan   FOB del entero L1 a bordo, US$/kg (base de comercio)")
    print("p_eur   el mismo precio en EUR/kg")
    print("van     camarón de cultivo importado por la UE, EUR/kg (EUMOFA warmwater)")
    print("van_ec  ídem, sólo Ecuador (el más cercano a vannamei puro)")
    print("rel     p_eur / van   ·   rel_ec  p_eur / van_ec")

    # ------------------------------------------------------------------ anual
    an = d.groupby(d.index.year).agg(
        p_usd=("p_tan", "mean"), eurusd=("eurusd", "mean"), p_eur=("p_eur", "mean"),
        van=("van_eur_kg", "mean"), van_ec=("van_ec_eur_kg", "mean"),
        rel=("rel", "mean"), rel_ec=("rel_ec", "mean"),
        captura_t=("tan_t", "sum"), meses=("p_tan", "size"))
    print("\n" + "-" * 100)
    print("PROMEDIOS ANUALES")
    print("-" * 100)
    print(an.round(3).to_string())

    # ------------------------------------------------- de dónde sale el 3,1%
    print("\n" + "-" * 100)
    print("EL +3,1% DE LA PLACA 9, PASO A PASO")
    print("-" * 100)
    a, b = 2024, 2025
    for nom, c in [("precio del L1 en euros", "p_eur"),
                   ("camarón de cultivo", "van"),
                   ("precio relativo (el cociente)", "rel")]:
        v0, v1 = an[c][a], an[c][b]
        dl = np.log(v1 / v0) * 100
        print(f"   {nom:<32s} {v0:6.3f} → {v1:6.3f}   {dl:+5.1f}%   "
              f"(variación simple {100 * (v1 / v0 - 1):+.1f}%)")
    dq = np.log(an.captura_t[b] / an.captura_t[a]) * 100
    print(f"   {'captura tangonera (t)':<32s} {an.captura_t[a]:6.0f} → "
          f"{an.captura_t[b]:6.0f}   {dq:+5.1f}%")
    dr = np.log(an.rel[b] / an.rel[a]) * 100
    print(f"\n   Flexibilidad de arco = {dr:.1f} / {dq:.1f} = {dr / dq:+.3f}")
    print("   Con el cociente sólo contra Ecuador el mismo cálculo da "
          f"{np.log(an.rel_ec[b] / an.rel_ec[a]) * 100:+.1f}%.")
    print("\n   El +3,1% es la VARIACIÓN del cociente, no la brecha de nivel entre los")
    n_ag = an.rel[[a, b]].mean()
    n_ec = an.rel_ec[[a, b]].mean()
    print(f"   dos precios. La brecha de nivel, promedio {a}-{b}, es otra cosa: el L1")
    print(f"   cotiza {abs(n_ag - 1) * 100:.1f}% por "
          f"{'debajo' if n_ag < 1 else 'encima'} del agregado de cultivo "
          f"(cociente {n_ag:.3f}) y")
    print(f"   {abs(n_ec - 1) * 100:.1f}% por {'debajo' if n_ec < 1 else 'encima'} "
          f"del ecuatoriano (cociente {n_ec:.3f}).")

    grafico(d, an)

    # ---------------------------------------------------------------- salida
    sal = os.path.join(RAIZ, "salidas", "serie_precios_comparada.xlsx")
    try:
        with pd.ExcelWriter(sal, engine="openpyxl") as w:
            m = d.copy()
            m.index = m.index.astype(str)
            m.round(4).to_excel(w, sheet_name="mensual")
            an.round(4).to_excel(w, sheet_name="anual")
        print(f"\nGuardado: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal} (¿abierto en Excel?)")


if __name__ == "__main__":
    main()
