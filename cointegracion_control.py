# -*- coding: utf-8 -*-
"""¿Está bien construido el control del competidor? Cointegración y causalidad entre
el precio del L1 tangonero y el del camarón de cultivo importado por la UE.

Por qué importa. Todo el estudio usa como variable dependiente el precio RELATIVO,
p_L1 / p_cultivo. Dividir una serie por otra sólo tiene sentido si las dos comparten
una relación de largo plazo: si no están cointegradas, el cociente no es un control
sino una serie nueva con vida propia, y el coeficiente de cantidad estaría midiendo
también el desacople entre las dos.

La literatura no da una respuesta única. Béné, Cadren y Lantz (2000) encuentran que el
camarón salvaje de Guayana Francesa y el black tiger de cultivo tailandés SÍ están
cointegrados en Rungis, con el cultivado liderando. Fernández-Polanco y otros
encuentran lo contrario para dorada salvaje y de cultivo en España: mercados separados.
O sea que es una pregunta abierta y hay que testearla, no suponerla.

Qué se corre:
    1. ADF y KPSS sobre cada serie en nivel y en primera diferencia
    2. Engle-Granger sobre el residuo de la relación de largo plazo
    3. Johansen con rezagos elegidos por criterio de información
    4. Granger en las dos direcciones, que es la pregunta de quién lidera
    5. El mismo juego sobre el precio del L1 puesto en España, que es donde la
       literatura discrepa

Uso:  python cointegracion_control.py
Salida: consola + salidas/cointegracion_control.xlsx
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint, grangercausalitytests, kpss
from statsmodels.tsa.vector_ar.vecm import coint_johansen, select_order

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402

MAXLAG = 12


def _md(x, d=3):
    return f"{x:+.{d}f}".replace(".", ",")


def series():
    """Precio del L1 tangonero en euros y precio del cultivo importado por la UE."""
    df, _ = T.panel()
    d = df.dropna(subset=["p_eur", "van_eur_kg"]).copy()
    out = pd.DataFrame({"l_l1": np.log(d.p_eur), "l_cult": np.log(d.van_eur_kg)})
    return out.dropna()


def raiz(s: pd.Series, nom: str) -> dict:
    ad = adfuller(s.dropna(), autolag="AIC")
    kp = kpss(s.dropna(), regression="c", nlags="auto")
    return {"serie": nom, "ADF": ad[0], "ADF_p": ad[1], "KPSS": kp[0], "KPSS_p": kp[1],
            "veredicto": ("estacionaria" if ad[1] < 0.05 and kp[1] > 0.05 else
                          "raíz unitaria" if ad[1] > 0.05 and kp[1] < 0.05 else
                          "ambiguo")}


def main() -> None:
    d = series()
    print("=" * 92)
    print("¿ESTÁN COINTEGRADOS EL L1 TANGONERO Y EL CAMARÓN DE CULTIVO?")
    print("=" * 92)
    print(f"Muestra {d.index.min()} a {d.index.max()} · N = {len(d)} meses")

    print("\n" + "-" * 92)
    print("1. Orden de integración")
    print("-" * 92)
    filas = []
    for nom, s in [("log p_L1", d.l_l1), ("log p_cultivo", d.l_cult),
                   ("Δ log p_L1", d.l_l1.diff()), ("Δ log p_cultivo", d.l_cult.diff()),
                   ("log del cociente", d.l_l1 - d.l_cult)]:
        r = raiz(s, nom)
        filas.append(r)
        print(f"   {nom:<18s} ADF {r['ADF']:+6.2f} (p {r['ADF_p']:.3f})   "
              f"KPSS {r['KPSS']:5.2f} (p {r['KPSS_p']:.3f})   {r['veredicto']}")
    RU = pd.DataFrame(filas)

    print("\n" + "-" * 92)
    print("2. Engle-Granger sobre la relación de largo plazo")
    print("-" * 92)
    t, p, cv = coint(d.l_l1, d.l_cult, trend="c", autolag="AIC")
    m = sm.OLS(d.l_l1, sm.add_constant(d.l_cult)).fit()
    print(f"   relación estimada: log p_L1 = {m.params['const']:+.3f} "
          f"{m.params['l_cult']:+.3f}·log p_cultivo   (R² {m.rsquared:.3f})")
    print(f"   estadístico {t:+.3f}   p = {p:.4f}   críticos 1/5/10%: "
          f"{cv[0]:+.2f} / {cv[1]:+.2f} / {cv[2]:+.2f}")
    print("   " + ("SE RECHAZA la no cointegración: hay relación de largo plazo."
                   if p < 0.05 else
                   "NO se rechaza la no cointegración: no hay evidencia de relación "
                   "de largo plazo."))

    print("\n" + "-" * 92)
    print("3. Johansen")
    print("-" * 92)
    k = select_order(d[["l_l1", "l_cult"]], maxlags=MAXLAG, deterministic="ci").aic
    j = coint_johansen(d[["l_l1", "l_cult"]], det_order=0, k_ar_diff=max(1, int(k)))
    print(f"   rezagos por AIC: {k}")
    for i, nom in enumerate(["r = 0", "r ≤ 1"]):
        print(f"   traza {nom}: {j.lr1[i]:7.3f}   críticos 90/95/99%: "
              f"{j.cvt[i][0]:.2f} / {j.cvt[i][1]:.2f} / {j.cvt[i][2]:.2f}"
              + ("   RECHAZA al 95%" if j.lr1[i] > j.cvt[i][1] else "   no rechaza"))

    print("\n" + "-" * 92)
    print("4. Causalidad de Granger, en las dos direcciones")
    print("-" * 92)
    D = d.diff().dropna()
    res = {}
    for etq, cols in [("cultivo → L1", ["l_l1", "l_cult"]),
                      ("L1 → cultivo", ["l_cult", "l_l1"])]:
        g = grangercausalitytests(D[cols], maxlag=6, verbose=False)
        ps = {L: g[L][0]["ssr_ftest"][1] for L in range(1, 7)}
        mejor = min(ps, key=ps.get)
        res[etq] = ps
        print(f"   {etq:<14s} p mínimo {ps[mejor]:.4f} en el rezago {mejor}   "
              + ("hay precedencia" if ps[mejor] < 0.05 else "no hay precedencia"))
    G = pd.DataFrame(res)

    print("\n" + "=" * 92)
    print("5. Qué significa para el estudio")
    print("=" * 92)
    coint_ok = p < 0.05
    print("   El control por cociente supone una relación de largo plazo entre las dos")
    print("   series. " + ("El dato la respalda." if coint_ok else
                           "El dato NO la respalda: hay que declararlo."))
    print("   La causalidad de Granger es precedencia temporal, no identificación: el")
    print("   parámetro causal del estudio sale del shock de oferta de 2025, no de acá.")

    sal = os.path.join(RAIZ, "salidas", "cointegracion_control.xlsx")
    try:
        with pd.ExcelWriter(sal, engine="openpyxl") as w:
            RU.to_excel(w, sheet_name="raices", index=False)
            pd.DataFrame([{"test": "Engle-Granger", "estadistico": t, "p": p,
                           "cv_5%": cv[1], "beta": m.params["l_cult"],
                           "R2": m.rsquared}]).to_excel(w, sheet_name="engle_granger",
                                                        index=False)
            pd.DataFrame({"traza": j.lr1, "cv_95": [c[1] for c in j.cvt]}).to_excel(
                w, sheet_name="johansen")
            G.to_excel(w, sheet_name="granger")
        print(f"\nGuardado: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal}")


if __name__ == "__main__":
    main()
