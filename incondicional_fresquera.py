# -*- coding: utf-8 -*-
"""La flexibilidad incondicional de la flota FRESQUERA — el cruce que le falta.

Qué se contesta. El sistema de dos flotas da la matriz condicional dentro del grupo
argentino, con f_fre,fre = −0,315. Devolviéndole el efecto escala por la fórmula del
§A.5.4 —f_i = f_ii + s_i·(1 + f_G)— la fresquera daría −0,171. Ese número no está
validado: para la tangonera la recomposición se contrastó contra una ecuación
incondicional estimada aparte —−0,212 contra −0,239— y para la fresquera ese contraste
nunca se corrió. Acá se corre.

La ecuación es la misma que la de la tangonera, con las dos flotas cambiadas de lugar:

    log(p_fre / p_cultivo) = a + f·log(D_fre) + c·log(D_tan) + h·HORECA + τ·t + meses

con las cantidades medidas por DESEMBARQUE oficial acumulado a doce meses —la variable
exógena, no los kilos embarcados, que llevan adentro la decisión de cuándo vender.

El problema que se espera. El instrumento del proyecto es la ventana del conflicto de
2025, que fue un paro de la flota TANGONERA. Sobre el desembarque fresquero ese episodio
pega poco y de rebote: en el mismo sistema, la caída fresquera del período es −22,4% con
t = −1,44, o sea no distinguible de cero. Si la primera etapa sale débil, la versión
instrumental no es informativa y hay que decirlo, no maquillarla.

Uso:  python incondicional_fresquera.py
Salida: consola + salidas/incondicional_fresquera.xlsx
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_sistema_flotas as S   # noqa: E402

HAC = S.HAC


def _md(x, d=3):
    return f"{x:+.{d}f}".replace(".", ",")


def panel():
    """El mismo panel del sistema de dos flotas, más el precio relativo fresquero."""
    A, wt, wf = S.panel()
    A["rel_fre"] = (A.p_fresquera / A.eurusd) / A.van_eur_kg
    A = A[A.rel_fre > 0].copy()
    A["lrelf"] = np.log(A.rel_fre)
    A["ldt"], A["ldf"] = np.log(A.d_tan), np.log(A.d_fre)
    M = pd.get_dummies(A.index.month, prefix="m", drop_first=True).astype(float)
    M.index = A.index
    return A, M, wt, wf


def raices(A: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for nom in ["lrelf", "lrel", "ldf", "ldt"]:
        s = A[nom].dropna()
        ad, kp = adfuller(s, autolag="AIC"), kpss(s, regression="c", nlags="auto")
        filas.append({"serie": nom, "ADF": ad[0], "ADF_p": ad[1], "KPSS": kp[0],
                      "KPSS_p": kp[1],
                      "veredicto": ("estacionaria" if ad[1] < 0.05 and kp[1] > 0.05 else
                                    "raíz unitaria" if ad[1] > 0.05 and kp[1] < 0.05 else
                                    "ambiguo")})
    return pd.DataFrame(filas)


def mco(A, M, dep, propia, otra):
    X = pd.concat([A[[propia, otra, "horeca", "trend"]], M], axis=1)
    m = sm.OLS(A[dep], sm.add_constant(X)).fit(cov_type="HAC",
                                               cov_kwds={"maxlags": HAC})
    return {"f": m.params[propia], "se": m.bse[propia], "t": m.tvalues[propia],
            "cruzada": m.params[otra], "t_cruzada": m.tvalues[otra],
            "R2": m.rsquared, "n": int(m.nobs)}


def iv(A, M, dep, propia, otra):
    ex = sm.add_constant(pd.concat([A[[otra, "horeca", "trend"]], M], axis=1))
    r = IV2SLS(A[dep], ex, A[[propia]], A[["iv_conf"]]).fit(cov_type="kernel",
                                                            kernel="bartlett")
    return {"f": float(r.params[propia]), "se": float(r.std_errors[propia]),
            "cruzada": float(r.params[otra]), "n": int(r.nobs),
            "F1": float(r.first_stage.diagnostics["f.stat"].iloc[0])}


def primera_etapa(A, M, propia):
    """Qué tanto mueve el paro de 2025 al desembarque de esta flota."""
    X = pd.concat([A[["iv_conf", "horeca", "trend"]], M], axis=1)
    m = sm.OLS(A[propia], sm.add_constant(X)).fit(cov_type="HAC",
                                                  cov_kwds={"maxlags": HAC})
    return {"coef": m.params["iv_conf"], "t": m.tvalues["iv_conf"],
            "F": m.tvalues["iv_conf"] ** 2,
            "efecto_%": (np.exp(m.params["iv_conf"]) - 1) * 100}


def main() -> None:
    A, M, wt, wf = panel()
    print("=" * 96)
    print("FLEXIBILIDAD INCONDICIONAL DE LA FLOTA FRESQUERA")
    print("=" * 96)
    print(f"Muestra {A.index.min()} a {A.index.max()} · N = {len(A)} meses")
    print(f"Participación media en el valor exportado del entero: tangonera {wt:.1%} · "
          f"fresquera {wf:.1%}")

    print("\n" + "-" * 96)
    print("1. Raíces unitarias")
    print("-" * 96)
    RU = raices(A)
    for _, f in RU.iterrows():
        print(f"   {f.serie:<7s} ADF {f.ADF:+6.2f} (p {f.ADF_p:.3f})   "
              f"KPSS {f.KPSS:5.2f} (p {f.KPSS_p:.3f})   {f.veredicto}")

    print("\n" + "-" * 96)
    print("2. ¿Sirve el paro de 2025 como instrumento de la cantidad FRESQUERA?")
    print("-" * 96)
    PE = {}
    for et, col in [("tangonera", "ldt"), ("fresquera", "ldf")]:
        PE[et] = primera_etapa(A, M, col)
        print(f"   desembarque {et:<10s} {PE[et]['efecto_%']:+6.1f}%   t {PE[et]['t']:+5.2f}   "
              f"F {PE[et]['F']:6.1f}")
    debil = PE["fresquera"]["F"] < 10
    print("   " + ("La primera etapa fresquera NO llega al umbral de 10: el instrumento no "
                  "sirve para esta flota." if debil else
                  "La primera etapa fresquera pasa el umbral de 10."))

    print("\n" + "-" * 96)
    print("3. La ecuación incondicional, por MCO")
    print("-" * 96)
    o_fre = mco(A, M, "lrelf", "ldf", "ldt")
    o_tan = mco(A, M, "lrel", "ldt", "ldf")
    print(f"   FRESQUERA  f = {_md(o_fre['f'])}  se {o_fre['se']:.3f}  t {o_fre['t']:+.2f}   "
          f"cruzada con la tangonera {_md(o_fre['cruzada'])} (t {o_fre['t_cruzada']:+.2f})   "
          f"R² {o_fre['R2']:.3f}")
    print(f"   tangonera  f = {_md(o_tan['f'])}  se {o_tan['se']:.3f}  t {o_tan['t']:+.2f}   "
          f"(la de referencia, para leer la de arriba en escala)")

    print("\n" + "-" * 96)
    print("4. La misma ecuación instrumentada")
    print("-" * 96)
    i_fre = iv(A, M, "lrelf", "ldf", "ldt")
    i_tan = iv(A, M, "lrel", "ldt", "ldf")
    print(f"   FRESQUERA  f = {_md(i_fre['f'])}  se {i_fre['se']:.3f}   "
          f"primera etapa F = {i_fre['F1']:.1f}")
    print(f"   tangonera  f = {_md(i_tan['f'])}  se {i_tan['se']:.3f}   "
          f"primera etapa F = {i_tan['F1']:.1f}")
    if i_fre["F1"] < 10:
        print("   El IV fresquero se reporta para dejar constancia, no para usarlo: con la")
        print("   primera etapa por debajo de 10 el estimador está sesgado hacia el MCO y su")
        print("   error estándar no es interpretable.")

    print("\n" + "=" * 96)
    print("5. El cruce que se quería hacer")
    print("=" * 96)
    # la recomposición, con los números que devuelve el propio sistema
    res_g = S.etapa_grupo(A)
    _, Fc, _, _ = S.sistema_interno(A, wt, wf)
    fg = res_g["desembarque"][0]
    s_fre = (A.q_fresquera / A.Qg).mean()
    s_tan = (A.q_tangonera / A.Qg).mean()
    rec_fre = Fc.iloc[1, 1] + s_fre * (1 + fg)
    rec_tan = Fc.iloc[0, 0] + s_tan * (1 + fg)
    print(f"   recomposición del sistema de dos flotas   f = {_md(rec_fre)}   "
          f"({_md(Fc.iloc[1, 1])} + {s_fre:.3f}·(1 {_md(fg)}))")
    print(f"      control: la misma cuenta para la tangonera da {_md(rec_tan)}, que es el "
          f"número publicado")
    print(f"   ecuación incondicional, MCO               f = {_md(o_fre['f'])}")
    print(f"   ecuación incondicional, IV (no usable)    f = {_md(i_fre['f'])}")
    print("\n   Para la tangonera las dos vías coinciden (−0,212 recompuesto contra −0,239)")
    print("   porque hay un shock que mueve su cantidad. La fresquera no tiene ese shock.")

    sal = os.path.join(RAIZ, "salidas", "incondicional_fresquera.xlsx")
    try:
        with pd.ExcelWriter(sal, engine="openpyxl") as x:
            RU.to_excel(x, sheet_name="estacionariedad", index=False)
            pd.DataFrame(PE).T.to_excel(x, sheet_name="primera_etapa")
            pd.DataFrame([{"flota": "fresquera", "metodo": "recomposición",
                           "f": rec_fre}, {"flota": "tangonera",
                           "metodo": "recomposición", "f": rec_tan},
                          {"flota": "fresquera", "metodo": "MCO", **o_fre},
                          {"flota": "tangonera", "metodo": "MCO", **o_tan},
                          {"flota": "fresquera", "metodo": "IV", **i_fre},
                          {"flota": "tangonera", "metodo": "IV", **i_tan}]).to_excel(
                x, sheet_name="incondicional", index=False)
        print(f"\nGuardado: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal}")


if __name__ == "__main__":
    main()
