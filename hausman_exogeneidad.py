# -*- coding: utf-8 -*-
"""Test de exogeneidad de Hausman sobre el sistema por origen — ¿inverso o mixto?

Qué se contesta. El sistema del §7 trata como predeterminadas las CANTIDADES de los
cinco orígenes. Para Argentina eso es defendible: es captura salvaje, la fija la biología
y el calendario. Para Ecuador, India y Vietnam es acuicultura, y Tabarestani, Keithly y
Marzoughi-Ardakani (2017) —el antecedente que el estudio cita como el más pertinente—
sostienen justamente lo contrario: en camarón, las cantidades importadas son endógenas y
los precios de importación exógenos. Su aporte es el sistema de demanda MIXTA, con la
producción salvaje en forma inversa y las importaciones de cultivo en forma directa.

Este test decide cuál de las dos formas admite el dato, origen por origen. Es el paso 7
de `salidas/Verificacion_consistencia_Barten_Tabarestani.md` y el único de esa lista que
puede cambiar el modelo y no sólo el número.

El procedimiento es el del Apéndice A de Tabarestani, que es una función de control
(Durbin-Wu-Hausman en su forma de regresión aumentada):

  1. Primera etapa. Cada variable candidata se regresa sobre sus rezagos de primer y
     segundo orden, dummies estacionales y una tendencia. Se guardan los residuos.
  2. Se agregan los residuos a TODAS las ecuaciones del sistema.
  3. Wald sobre los coeficientes de cada residuo por separado; LR sobre todos juntos.
     Se decide por el LR. El Wald de las veinte restricciones conjuntas rechaza el 82%
     de las veces bajo el nulo en una muestra del largo de ésta —está roto— y el de
     cuatro restricciones, el 14%. Medido en `validar_hausman.py`.
  4. Si los coeficientes del residuo son cero, la variable es exógena respecto del
     sistema y la forma que la trata como predeterminada está justificada.

Se corre dos veces, porque rechazar la exogeneidad de las cantidades sin mirar los
precios deja el diagnóstico a mitad de camino:

    sistema INVERSO   w_i sobre log q   → se testean las cinco CANTIDADES
    sistema DIRECTO   w_i sobre log p   → se testean los cinco PRECIOS

y el cruce de los dos veredictos dice en qué bloque va cada origen:

    cantidad exógena, precio endógeno  → forma inversa   (el caso del salvaje)
    cantidad endógena, precio exógeno  → forma directa   (el caso del cultivo)
    las dos exógenas                   → cualquiera de las dos sirve
    las dos endógenas                  → ninguna; hacen falta instrumentos de verdad

Grados de libertad. Con adición impuesta se estiman cuatro ecuaciones y la quinta sale
por diferencia, así que cada residuo aporta cuatro coeficientes: el Wald por variable va
contra chi-cuadrado de 4 y el LR conjunto de los cinco, contra chi-cuadrado de 20. En
Tabarestani el LR de las importaciones va contra chi-cuadrado de 7 porque ahí el residuo
propio entra sólo en su propia ecuación y el del resto del mundo no está identificado por
ser la base de la normalización.

Advertencia que conviene leer antes que el resultado. La validez de esta prueba descansa
en que los rezagos propios sean instrumentos legítimos, o sea que no correlacionen con el
error estructural. Si el error del sistema está autocorrelacionado —y Tabarestani encontró
correlación serial y la corrigió con un AR(1)— el rezago deja de ser válido y el test
pierde sentido. Por eso se informa la autocorrelación de los residuos del sistema junto
con el veredicto: si es alta, el test no concluye nada. Lo mismo vale para las raíces
unitarias que `iaids_simetria.py` encuentra en varias series: con regresores I(1) el
chi-cuadrado no tiene la distribución que se le supone, y por eso todo se repite en
primeras diferencias.

Uso:   python hausman_exogeneidad.py [--pkl RUTA]
       --pkl apunta a un panel alternativo, para validar el test contra un dato de
       ground truth conocido (ver validar_hausman.py).
Salida: consola + salidas/hausman_exogeneidad.xlsx
"""
from __future__ import annotations

import argparse
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.system import SUR
from scipy import stats

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
pd.set_option("display.width", 170)

ORIGENES = ["AR", "EC", "IN", "VN", "RE"]
FUERA = "RE"                  # la ecuación que sale por adición
HAC = 6                       # rezagos de Newey-West, igual que el resto del proyecto
NIVEL = 0.05
R2_MAX = 0.95               # arriba de esto el residuo es el propio regresor

# Valor crítico del LR conjunto al 5%, simulado bajo el nulo en `validar_hausman.py`.
# El chi-cuadrado de 20 vale 31,4, pero en una muestra de 160 meses el LR rechaza el
# 10-17% de las veces cuando no hay nada: el asintótico llega tarde. Se usa el simulado.
CRITICO_LR = 37.0


def _p(*t):
    return os.path.join(RAIZ, *t)


# ------------------------------------------------------------------------ panel
def panel(pkl: str | None = None):
    """Valor, cantidad, precio y participaciones por origen, mensual."""
    O = pd.read_pickle(pkl or _p("datos", "eumofa_camaron_origen.pkl"))
    V = O.eur.unstack().fillna(0)[ORIGENES]
    Q = (O.kg.unstack().fillna(0) / 1e6)[ORIGENES]          # millones de kg
    W = V.div(V.sum(axis=1), axis=0)
    P = V / (Q * 1e6)                                       # EUR/kg
    return V, Q, P, W


def _controles(Z: pd.DataFrame) -> pd.DataFrame:
    Z = Z.copy()
    Z["trend"] = np.arange(len(Z)) / 12.0
    M = pd.get_dummies(Z.index.month, prefix="m", drop_first=True).astype(float)
    M.index = Z.index
    return sm.add_constant(pd.concat([Z, M], axis=1))


def diferenciar(REG: pd.DataFrame) -> pd.DataFrame:
    """Primeras diferencias de una matriz de diseño.

    Se sacan antes la constante y la tendencia. Diferenciar la constante la deja en
    cero; diferenciar la tendencia la vuelve una constante, que es lo mismo que la
    constante que se repone después. Con cualquiera de las dos adentro el sistema
    queda sin rango completo y `linearmodels` corta.
    """
    return sm.add_constant(REG.drop(columns=["const", "trend"]).diff())


def reg_inversa(Q: pd.DataFrame, W: pd.DataFrame) -> pd.DataFrame:
    """LA/IAIDS: w_i sobre log q normalizado y el índice de Stone de cantidad."""
    X = np.log(Q.clip(lower=1e-3))
    Z = pd.DataFrame({f"x_{c}": X[c] - X[FUERA] for c in ORIGENES[:-1]})
    Z["esc"] = X @ W.mean()                                 # Stone con w MEDIAS
    return _controles(Z)


def reg_directa(P: pd.DataFrame, V: pd.DataFrame, W: pd.DataFrame) -> pd.DataFrame:
    """LA/AIDS: w_i sobre log p normalizado y el gasto real del grupo."""
    lp = np.log(P.clip(lower=1e-6))
    Z = pd.DataFrame({f"x_{c}": lp[c] - lp[FUERA] for c in ORIGENES[:-1]})
    Z["esc"] = np.log(V.sum(axis=1)) - (lp @ W.mean())      # gasto deflactado por Stone
    return _controles(Z)


# ---------------------------------------------------------------- primera etapa
def primera_etapa(S: pd.DataFrame):
    """Cada variable sobre sus rezagos 1 y 2, estacionalidad y tendencia (Tabarestani A).

    Devuelve los residuos y el diagnóstico. El F de los dos rezagos es lo que le da
    poder al test: si los rezagos no predicen, el residuo es casi la variable entera y
    el contraste no distingue nada.
    """
    D = pd.get_dummies(S.index.month, prefix="m", drop_first=True).astype(float)
    D.index = S.index
    D["trend"] = np.arange(len(S)) / 12.0
    res, diag = {}, []
    for c in S.columns:
        d = pd.concat([S[c].rename("y"), S[c].shift(1).rename("l1"),
                       S[c].shift(2).rename("l2"), D], axis=1).dropna()
        m = sm.OLS(d.y, sm.add_constant(d.drop(columns="y"))).fit()
        res[c] = m.resid
        f = m.f_test("l1 = 0, l2 = 0")
        diag.append({"variable": c, "N": int(m.nobs), "R2": m.rsquared,
                     "F_rezagos": float(np.squeeze(f.fvalue)), "p_F": float(f.pvalue)})
    return pd.DataFrame(res), pd.DataFrame(diag).set_index("variable")


# ------------------------------------------------------------------- estimación
def estimar(W: pd.DataFrame, REG: pd.DataFrame):
    """SUR iterado sobre las cuatro ecuaciones independientes. Iterado porque así el
    estimador es de máxima verosimilitud y el LR sobre los determinantes de Σ es el
    contraste que corresponde."""
    dentro = [c for c in ORIGENES if c != FUERA]
    idx = REG.dropna().index.intersection(W.dropna().index)
    eq = {c: {"dependent": W[c].loc[idx], "exog": REG.loc[idx]} for c in dentro}
    r = SUR(eq).fit(method="gls", iterate=True, cov_type="kernel",
                    kernel="bartlett", bandwidth=HAC)
    return r, dentro, idx


def wald(res, nombres: list[str]):
    """H0: los coeficientes nombrados son todos cero."""
    b = res.params.reindex(nombres).values
    V = res.cov.reindex(index=nombres, columns=nombres).values
    w = float(b @ np.linalg.solve(V, b))
    return w, float(stats.chi2.sf(w, len(nombres))), len(nombres)


def lr(res_r, res_u, T: int, g: int):
    s_r = np.linalg.slogdet(np.asarray(res_r.sigma))[1]
    s_u = np.linalg.slogdet(np.asarray(res_u.sigma))[1]
    v = T * (s_r - s_u)
    return float(v), float(stats.chi2.sf(v, g)), g


def colinealidad(RES: pd.DataFrame, REG: pd.DataFrame) -> pd.Series:
    """R² de cada residuo de primera etapa contra los regresores del propio sistema.

    Es el modo de falla silencioso del test. Si los rezagos no predicen a la variable,
    el residuo es la variable entera, y la variable ya está en el sistema: la regresión
    aumentada queda casi singular y el Wald no distingue nada. En una simulación donde
    la endogeneidad estaba puesta a mano, con R² de 0,99 el test la declaró exógena en
    los tres orígenes contaminados. Un R² cerca de uno no significa «exógena»: significa
    que el test no contesta.
    """
    out = {}
    for c in RES.columns:
        d = pd.concat([RES[c].rename("v"), REG], axis=1).dropna()
        out[c] = float(sm.OLS(d.v, d.drop(columns="v")).fit().rsquared)
    return pd.Series(out, name="R2_vs_sistema")


def autocorrelacion(res, dentro: list[str]) -> pd.Series:
    """ρ de primer orden de los residuos de cada ecuación. Si es alta, el rezago propio
    no es instrumento válido y todo el test queda en suspenso."""
    out = {}
    for k, i in enumerate(dentro):
        e = pd.Series(np.asarray(res.resids)[:, k])
        out[i] = float(e.corr(e.shift(1)))
    return pd.Series(out, name="rho_1")


# ------------------------------------------------------------------------ test
def nucleo(W: pd.DataFrame, REG: pd.DataFrame, RES: pd.DataFrame,
           individuales: bool = True):
    """El test, sin imprimir nada. Devuelve (individuales, conjunto, contexto).

    Separado de `hausman` para que `validar_hausman.py` pueda correrlo miles de veces
    sobre paneles simulados y medir tamaño y poder.
    """
    # Muestra común a todo el ejercicio. Los rezagos de la primera etapa se comen las
    # dos primeras observaciones, y un LR entre modelos estimados sobre muestras
    # distintas no significa nada.
    idx = (REG.dropna().index
           .intersection(W.dropna().index)
           .intersection(RES.dropna().index))
    REG, W, RES = REG.loc[idx], W.loc[idx], RES.loc[idx]

    r0, dentro, _ = estimar(W, REG)
    T = len(idx)
    rho = autocorrelacion(r0, dentro)
    col = colinealidad(RES, REG)
    filas = []
    for c in (ORIGENES if individuales else []):     # una variable por vez
        aug = pd.concat([REG, RES[[c]].rename(columns={c: f"v_{c}"})], axis=1)
        r1, dentro1, _ = estimar(W, aug)
        nombres = [f"{i}_v_{c}" for i in dentro1]
        w, pw, g = wald(r1, nombres)
        l, pl, _ = lr(r0, r1, T, g)
        degenerado = col[c] > R2_MAX
        filas.append({"variable": c, "Wald": w, "gl": g, "p_Wald": pw,
                      "LR": l, "p_LR": pl, "R2_col": col[c],
                      "veredicto": ("indeterminado" if degenerado else
                                    "exógena" if pl > NIVEL else "ENDÓGENA")})
    ind = (pd.DataFrame(filas).set_index("variable") if filas
           else pd.DataFrame(columns=["Wald", "gl", "p_Wald", "LR", "p_LR",
                                      "R2_col", "veredicto"]))

    aug = pd.concat([REG, RES.rename(columns={c: f"v_{c}" for c in RES.columns})], axis=1)
    rj, dentroj, _ = estimar(W, aug)
    nombres = [f"{i}_v_{c}" for i in dentroj for c in ORIGENES]
    wj, pwj, gj = wald(rj, nombres)
    lj, plj, _ = lr(r0, rj, T, gj)
    conj = {"Wald": wj, "p_Wald": pwj, "LR": lj, "p_LR": plj, "gl": gj,
            "rho_max": float(rho.abs().max())}
    return ind, conj, {"T": T, "dentro": dentro, "rho": rho, "k": len(REG.columns)}


def hausman(W: pd.DataFrame, REG: pd.DataFrame, RES: pd.DataFrame, etiqueta: str):
    """`nucleo` más el informe por consola."""
    print("\n" + "=" * 92)
    print(f"{etiqueta}")
    print("=" * 92)
    ind, conj, ctx = nucleo(W, REG, RES)
    wj, pwj, lj, plj, gj = (conj["Wald"], conj["p_Wald"], conj["LR"],
                            conj["p_LR"], conj["gl"])
    print(f"sistema base: {len(ctx['dentro'])} ecuaciones, T = {ctx['T']}, "
          f"{ctx['k']} regresores por ecuación")
    print("autocorrelación de primer orden de los residuos: "
          + " · ".join(f"{i} {v:+.2f}" for i, v in ctx["rho"].items()))
    if ctx["rho"].abs().max() > 0.3:
        print("  AVISO: con |ρ| > 0,30 el rezago propio no es un instrumento limpio.")

    print("\nUna variable por vez (Wald sobre sus cuatro coeficientes):")
    print(ind.round(3).to_string())
    if (ind.veredicto == "indeterminado").any():
        malas = list(ind.index[ind.veredicto == "indeterminado"])
        print(f"  AVISO: {', '.join(malas)} tienen el residuo casi colineal con el propio")
        print(f"  sistema (R2 > {R2_MAX}). Para esas variables el test no contesta: no son")
        print("  'exógenas', son indeterminadas. Hace falta un instrumento de verdad.")
    print(f"\nTODAS JUNTAS (el contraste que manda): Wald = {wj:.2f} "
          f"(gl {gj}, p = {pwj:.4f}) · LR = {lj:.2f} (p = {plj:.4f})")
    print(f"  chi-cuadrado crítico al 5%: {stats.chi2.ppf(.95, gj):.1f} — "
          f"valor crítico SIMULADO al 5%: {CRITICO_LR:.1f} (validar_hausman.py)")
    print(f"  contra el simulado: {'no se rechaza' if lj < CRITICO_LR else 'SE RECHAZA'}")
    print(f"  → {'no se rechaza la exogeneidad conjunta' if plj > NIVEL else 'SE RECHAZA la exogeneidad conjunta'}")
    print("  Se decide por el LR, no por el Wald. En la simulación de validar_hausman.py")
    print("  el Wald de las veinte restricciones rechaza el 82% de las veces cuando NO hay")
    print("  nada que rechazar: con esa cantidad de restricciones y una matriz HAC estimada,")
    print("  el Wald está roto en una muestra de 160 meses. El LR queda en 0,10 contra un")
    print("  nominal de 0,05, que es leíble con cuidado. Tabarestani también enuncia sus")
    print("  conclusiones sobre el LR.")
    print("  Y el conjunto es el que decide: la tabla de arriba es indicativa, porque cuando")
    print("  varios orígenes comparten el mismo shock el test localiza mal en cuál está.")
    return ind, conj


def veredicto(q: pd.DataFrame, p: pd.DataFrame) -> pd.DataFrame:
    """Cruza los dos test y dice en qué bloque va cada origen."""
    filas = []
    for c in ORIGENES:
        vq, vp = q.loc[c, "veredicto"], p.loc[c, "veredicto"]
        qe, pe = vq == "exógena", vp == "exógena"
        if "indeterminado" in (vq, vp):
            forma = "sin veredicto: el test es degenerado de al menos un lado"
        else:
            forma = ("inversa (cantidad dada, el precio ajusta)" if qe and not pe else
                     "directa (precio dado, la cantidad ajusta)" if pe and not qe else
                     "cualquiera: las dos exógenas" if qe and pe else
                     "NINGUNA: las dos endógenas, hacen falta instrumentos")
        filas.append({"origen": c, "cantidad": q.loc[c, "veredicto"],
                      "precio": p.loc[c, "veredicto"], "forma que admite el dato": forma})
    return pd.DataFrame(filas).set_index("origen")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl", default=None, help="panel alternativo (validación)")
    a = ap.parse_args()

    V, Q, P, W = panel(a.pkl)
    print("=" * 92)
    print("TEST DE EXOGENEIDAD DE HAUSMAN — ¿demanda inversa o demanda mixta?")
    print("=" * 92)
    print(f"Muestra {Q.index.min()} a {Q.index.max()}, {len(Q)} meses.")
    print("participación media en el valor importado (%): "
          + " · ".join(f"{c} {W[c].mean()*100:.1f}" for c in ORIGENES))

    lq, lp = np.log(Q.clip(lower=1e-3)), np.log(P.clip(lower=1e-6))
    RQ, dq = primera_etapa(lq)
    RP, dp = primera_etapa(lp)
    print("\nPrimera etapa — cada variable sobre sus rezagos 1 y 2, estacionalidad y tendencia")
    print("cantidades:")
    print(dq.round(3).to_string())
    print("precios:")
    print(dp.round(3).to_string())
    if (dq.p_F > .05).any() or (dp.p_F > .05).any():
        print("  AVISO: hay primeras etapas donde los rezagos no predicen (p_F > 0,05);")
        print("  para esas variables el test tiene poco poder y el 'exógena' no dice mucho.")

    q_ind, q_j = hausman(W, reg_inversa(Q, W), RQ,
                         "SISTEMA INVERSO (el del §7) — se testean las CANTIDADES")
    p_ind, p_j = hausman(W, reg_directa(P, V, W), RP,
                         "SISTEMA DIRECTO (la alternativa) — se testean los PRECIOS")

    ver = veredicto(q_ind, p_ind)
    print("\n" + "=" * 92)
    print("VEREDICTO POR ORIGEN")
    print("=" * 92)
    print(ver.to_string())

    inv = [c for c in ORIGENES if ver.loc[c, "forma que admite el dato"].startswith("inversa")]
    dir_ = [c for c in ORIGENES if ver.loc[c, "forma que admite el dato"].startswith("directa")]
    print()
    if inv and dir_:
        print(f"El dato pide un sistema MIXTO: {', '.join(inv)} en forma inversa y "
              f"{', '.join(dir_)} en forma directa.")
        print("Es exactamente la estructura de Tabarestani, Keithly y Marzoughi-Ardakani")
        print("(2017): salvaje predeterminado, cultivo con precio predeterminado.")
    elif not dir_:
        print("Ningún origen exige la forma directa: el sistema inverso del §7 queda en pie.")
    else:
        print("Ningún origen admite la forma inversa: el sistema del §7 está mal planteado.")

    # ------------------------------------------------- todo otra vez en diferencias
    print("\n" + "=" * 92)
    print("REPETICIÓN EN PRIMERAS DIFERENCIAS")
    print("=" * 92)
    print("Varias series tienen raíz unitaria (ver iaids_simetria.py, paso 1). Con")
    print("regresores I(1) el chi-cuadrado no tiene la distribución que se le supone.")
    dW = W.diff()
    q_d, _ = hausman(dW, diferenciar(reg_inversa(Q, W)), RQ.diff(),
                     "INVERSO en diferencias — CANTIDADES")
    p_d, _ = hausman(dW, diferenciar(reg_directa(P, V, W)), RP.diff(),
                     "DIRECTO en diferencias — PRECIOS")
    print("\nVeredicto en diferencias:")
    print(veredicto(q_d, p_d).to_string())

    sal = _p("salidas", "hausman_exogeneidad.xlsx")
    try:
        with pd.ExcelWriter(sal) as x:
            dq.to_excel(x, sheet_name="primera_etapa_q")
            dp.to_excel(x, sheet_name="primera_etapa_p")
            q_ind.to_excel(x, sheet_name="hausman_cantidades")
            p_ind.to_excel(x, sheet_name="hausman_precios")
            pd.DataFrame([dict(bloque="cantidades", **q_j),
                          dict(bloque="precios", **p_j)]).to_excel(
                x, sheet_name="conjuntos", index=False)
            ver.to_excel(x, sheet_name="veredicto")
            veredicto(q_d, p_d).to_excel(x, sheet_name="veredicto_diferencias")
        print(f"\nEscrito: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal} (¿abierto en Excel?)")


if __name__ == "__main__":
    main()
