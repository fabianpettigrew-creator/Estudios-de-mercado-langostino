# -*- coding: utf-8 -*-
"""IAIDS por origen con SIMETRÍA IMPUESTA por SUR iterado — análisis independiente.

Qué se contesta. El sistema de demanda inversa por origen del §7 se estima hoy ecuación
por ecuación: la homogeneidad entra por normalización y la adición por construcción, pero
la simetría de Slutsky-Antonelli (γ_ij = γ_ji) se testea y no se impone. El A.9 del anexo
lo deja anotado como el refinamiento que corresponde si el trabajo va a arbitraje. Acá se
impone y se mide qué cambia.

El modelo (LA/IAIDS, Eales-Unnevehr; Barten-Bettendorf para el caso pesquero):

    w_i = a_i + Σ_j γ_ij·log q_j + b_i·log Q ,   log Q = Σ_k w̄_k·log q_k   (índice de Stone)

con w_i la participación del origen i en el valor importado extra-UE de camarón congelado
y q_i su volumen. Restricciones teóricas:

    adición       Σ_i a_i = 1 ,  Σ_i γ_ij = 0 ,  Σ_i b_i = 0
    homogeneidad  Σ_j γ_ij = 0
    simetría      γ_ij = γ_ji

La adición hace singular al sistema: se estiman N−1 = 4 ecuaciones y la quinta sale por
diferencia. La homogeneidad se impone escribiendo los regresores como log q_j − log q_RE.
La simetría son seis restricciones CRUZADAS entre ecuaciones —una por par de los cuatro
orígenes nombrados—, y las que involucran al resto se cumplen solas por adición.

Por qué SUR iterado y no MCO. Con restricciones cruzadas el sistema deja de estimarse
ecuación por ecuación. El SUR de un paso depende de qué ecuación se descarta; iterando la
matriz de covarianzas hasta converger se llega al máximo verosímil, que es invariante a
esa elección. Acá se verifica esa invariancia descartando dos ecuaciones distintas.

Aviso de lectura. Con los mismos regresores en las cinco ecuaciones y sin restringir, el
SUR es idéntico al MCO ecuación por ecuación. Eso es una ventaja para el contraste: lo
único que mueve el punto estimado entre la versión actual y ésta es la simetría.

Salidas:
    f propio de Argentina, con y sin simetría, y su contraste contra el umbral de −1
    test de Wald y test de razón de verosimilitud de las seis restricciones
    matriz completa de flexibilidades no compensadas y flexibilidad de escala

Uso:  python iaids_simetria.py
Salida: consola + salidas/iaids_simetria.xlsx
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

import flexibilidades_iaids as fx
from linearmodels.system import SUR
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))

HAC = 6                       # rezagos de Newey-West, igual que el resto del proyecto
ORIGENES = ["AR", "EC", "IN", "VN", "RE"]
NOMBRE = {"AR": "Argentina", "EC": "Ecuador", "IN": "India", "VN": "Vietnam",
          "RE": "resto"}


def _p(*t):
    return os.path.join(RAIZ, *t)


def _md(x: float, dec: int = 3) -> str:
    return f"{x:+.{dec}f}".replace(".", ",")


# ----------------------------------------------------------------------- datos
def panel():
    """Participaciones, cantidades y el índice de escala, tal como los arma el §7."""
    O = pd.read_pickle(_p("datos", "eumofa_camaron_origen.pkl"))
    V = O.eur.unstack().fillna(0)[ORIGENES]
    Q = (O.kg.unstack().fillna(0) / 1e6)[ORIGENES]          # miles de toneladas
    W = V.div(V.sum(axis=1), axis=0)
    X = np.log(Q.clip(lower=1e-3))
    lnQ = X @ W.mean()                                      # Stone con w MEDIAS (A.11)

    Z = pd.DataFrame({f"x_{c}": X[c] - X["RE"] for c in ORIGENES[:-1]})
    Z["lnQ"] = lnQ
    Z["trend"] = np.arange(len(Z)) / 12.0
    M = pd.get_dummies(Z.index.month, prefix="m", drop_first=True).astype(float)
    M.index = Z.index
    REG = sm.add_constant(pd.concat([Z, M], axis=1)).dropna()
    return W.reindex(REG.index), Q.reindex(REG.index), REG


# --------------------------------------------------------------- estacionariedad
def raices(W: pd.DataFrame, REG: pd.DataFrame) -> pd.DataFrame:
    """ADF y KPSS sobre lo que entra al sistema, antes de estimar nada."""
    filas = []
    series = {f"w_{c}": W[c] for c in ORIGENES}
    series.update({c: REG[c] for c in REG.columns if c.startswith("x_")})
    series["lnQ"] = REG["lnQ"]
    for nom, s in series.items():
        s = s.dropna()
        ad = adfuller(s, autolag="AIC")
        kp = kpss(s, regression="c", nlags="auto")
        filas.append({"serie": nom, "ADF": ad[0], "ADF_p": ad[1],
                      "KPSS": kp[0], "KPSS_p": kp[1],
                      "veredicto": ("estacionaria" if ad[1] < 0.05 and kp[1] > 0.05 else
                                    "raíz unitaria" if ad[1] > 0.05 and kp[1] < 0.05 else
                                    "ambiguo")})
    return pd.DataFrame(filas)


# ------------------------------------------------------------------- estimación
def ecuaciones(W: pd.DataFrame, REG: pd.DataFrame, fuera: str) -> dict:
    """Las cuatro ecuaciones que se estiman; la de «fuera» sale por adición."""
    dentro = [c for c in ORIGENES if c != fuera]
    return {c: {"dependent": W[c], "exog": REG} for c in dentro}


def _gamma_lineal(nombres: list[str], dentro: list[str], fuera: str) -> dict:
    """Cada γ_ij de la matriz 5×5 escrito como combinación lineal de los parámetros
    que efectivamente se estiman.

    Los que están en una ecuación estimada y en una columna nombrada son un parámetro
    directo. Los de la columna del resto salen por homogeneidad (Σ_j γ_ij = 0) y los de
    la fila descartada por adición (Σ_i γ_ij = 0); la esquina de los dos, por las dos.
    """
    v = {}
    for i in dentro:
        for j in ORIGENES[:-1]:
            u = pd.Series(0.0, index=nombres)
            u[f"{i}_x_{j}"] = 1.0
            v[(i, j)] = u
        v[(i, "RE")] = -sum(v[(i, k)] for k in ORIGENES[:-1])
    for j in ORIGENES[:-1]:
        v[(fuera, j)] = -sum(v[(k, j)] for k in dentro)
    v[(fuera, "RE")] = -sum(v[(fuera, k)] for k in ORIGENES[:-1])
    return v


def restricciones(mod: SUR, dentro: list[str], fuera: str) -> pd.DataFrame:
    """γ_ij = γ_ji sobre los diez pares, reducido a un subconjunto independiente.

    Con adición y homogeneidad ya impuestas, sólo (N−1)(N−2)/2 = 6 de las diez son
    independientes; las otras cuatro se cumplen solas. Cuál de las diez se puede
    escribir sobre parámetros estimados depende de qué ecuación se descartó, así que se
    arman las diez y se eligen por rango. Sin esto, descartar una ecuación distinta
    impone menos restricciones y el sistema deja de ser invariante.
    """
    nombres = list(mod.param_names)
    v = _gamma_lineal(nombres, dentro, fuera)
    filas, etq, M = [], [], np.zeros((0, len(nombres)))
    for k, i in enumerate(ORIGENES):
        for j in ORIGENES[k + 1:]:
            fila = (v[(i, j)] - v[(j, i)]).values
            if np.allclose(fila, 0):
                continue                       # se cumple por construcción
            M2 = np.vstack([M, fila])
            if np.linalg.matrix_rank(M2, tol=1e-9) > M.shape[0]:
                M, filas, etq = M2, filas + [fila], etq + [f"{i}={j}"]
    return pd.DataFrame(np.array(filas), index=etq, columns=nombres)


def estimar(W, REG, fuera="RE", simetria=True):
    mod = SUR(ecuaciones(W, REG, fuera))
    dentro = [c for c in ORIGENES if c != fuera]
    R = restricciones(mod, dentro, fuera) if simetria else None
    if simetria:
        mod.add_constraints(R)
    r = mod.fit(method="gls", iterate=True, cov_type="kernel", kernel="bartlett",
                bandwidth=HAC)
    return r, R, dentro


def matriz_gamma(res, dentro: list[str], fuera: str) -> pd.DataFrame:
    """γ completa 5×5: lo estimado, más la fila que falta por adición y la columna
    del resto por homogeneidad."""
    G = pd.DataFrame(np.nan, index=ORIGENES, columns=ORIGENES)
    p = res.params
    for i in dentro:
        for j in ORIGENES[:-1]:
            G.loc[i, j] = p[f"{i}_x_{j}"]
    for j in ORIGENES[:-1]:                      # adición: Σ_i γ_ij = 0
        G.loc[fuera, j] = -G.loc[dentro, j].sum()
    for i in ORIGENES:                           # homogeneidad: Σ_j γ_ij = 0
        G.loc[i, "RE"] = -G.loc[i, ORIGENES[:-1]].sum()
    return G


def flexibilidades(G: pd.DataFrame, res, dentro, fuera, w: pd.Series):
    """Delega en `flexibilidades_iaids`, que es la única definición del proyecto:
    f_ij = γ_ij/w_i + β_i·w_j/w_i − δ_ij. La ecuación que queda fuera del sistema
    recupera su β por adición (Σ_i β_i = 0)."""
    b = {i: res.params[f"{i}_lnQ"] for i in dentro}
    b[fuera] = -sum(b.values())
    b = pd.Series(b).reindex(ORIGENES)
    F, esc = fx.matriz(G, b, w)
    fx.verificar(F, esc, w)
    return F, esc


def se_propia(res, w: pd.Series, i: str = "AR") -> float:
    """Delta con w tomada como fija, igual que en el §7."""
    return float(res.std_errors[f"{i}_x_{i}"] / w[i])


# ------------------------------------------------------------------------ tests
def wald_simetria(res, R: pd.DataFrame) -> tuple[float, float, int]:
    b = res.params.reindex(R.columns).values
    V = res.cov.reindex(index=R.columns, columns=R.columns).values
    Rm = R.values
    d = Rm @ b
    W = float(d @ np.linalg.solve(Rm @ V @ Rm.T, d))
    g = Rm.shape[0]
    return W, float(stats.chi2.sf(W, g)), g


def lr_simetria(res_r, res_u, T: int, g: int) -> tuple[float, float]:
    """Con SUR iterado el estimador es de máxima verosimilitud, así que la razón de
    verosimilitud sobre los determinantes de Σ es el contraste que corresponde."""
    s_r = np.linalg.slogdet(np.asarray(res_r.sigma))[1]
    s_u = np.linalg.slogdet(np.asarray(res_u.sigma))[1]
    lr = T * (s_r - s_u)
    return float(lr), float(stats.chi2.sf(lr, g))


def en_diferencias(W: pd.DataFrame, REG: pd.DataFrame, w: pd.Series):
    """El mismo sistema con simetría, sobre primeras diferencias.

    El paso 1 encuentra raíz unitaria en varias participaciones y en varios log de
    cantidad. Con regresores I(1) el chi-cuadrado del test de simetría no tiene la
    distribución que se le supone, y el punto estimado se lee como relación de largo
    plazo. Estimar en diferencias saca esa objeción a costa de perder el nivel: si el f
    no se mueve, la conclusión no depende de cómo se trate la tendencia estocástica.
    """
    cols = [c for c in REG.columns if c.startswith("x_")] + ["lnQ"]
    D = REG[cols].diff()
    M = REG[[c for c in REG.columns if c.startswith("m_")]]
    Rd = sm.add_constant(pd.concat([D, M], axis=1)).dropna()
    Wd = W.diff().reindex(Rd.index)
    mod = SUR({c: {"dependent": Wd[c], "exog": Rd} for c in ORIGENES[:-1]})
    mod.add_constraints(restricciones(mod, ORIGENES[:-1], "RE"))
    r = mod.fit(method="gls", iterate=True, cov_type="kernel", kernel="bartlett",
                bandwidth=HAC)
    G = matriz_gamma(r, ORIGENES[:-1], "RE")
    F, esc = flexibilidades(G, r, ORIGENES[:-1], "RE", w)
    return r, F, esc, len(Rd)


# ---------------------------------------------------------------------- corrida
SEP = chr(10)


def main() -> None:
    W, Q, REG = panel()
    w = W.mean()
    T = len(REG)
    print("=" * 94)
    print("IAIDS POR ORIGEN CON SIMETRÍA IMPUESTA — SUR ITERADO")
    print("=" * 94)
    print(f"Muestra {REG.index.min()} a {REG.index.max()} · {T} meses · "
          f"{len(ORIGENES)} orígenes")
    print("\nParticipación media en el valor importado (%):")
    print("  " + " · ".join(f"{NOMBRE[c]} {w[c] * 100:.1f}" for c in ORIGENES))

    print("\n" + "-" * 94)
    print("1. Raíces unitarias, antes de estimar")
    print("-" * 94)
    RU = raices(W, REG)
    for _, f in RU.iterrows():
        print(f"   {f.serie:<8s} ADF {f.ADF:+7.2f} (p {f.ADF_p:.3f})   "
              f"KPSS {f.KPSS:5.2f} (p {f.KPSS_p:.3f})   {f.veredicto}")

    print("\n" + "-" * 94)
    print("2. Sin simetría — replica del §7 y punto de partida")
    print("-" * 94)
    res_u, _, dentro = estimar(W, REG, fuera="RE", simetria=False)
    G_u = matriz_gamma(res_u, dentro, "RE")
    F_u, esc_u = flexibilidades(G_u, res_u, dentro, "RE", w)
    se_u = se_propia(res_u, w)
    print(f"   f propio de Argentina  {_md(F_u.loc['AR', 'AR'])}  (SE {se_u:.3f})")
    print(f"   cruzadas con Ecuador {_md(F_u.loc['AR', 'EC'])} · India "
          f"{_md(F_u.loc['AR', 'IN'])} · Vietnam {_md(F_u.loc['AR', 'VN'])}")
    print(f"   escala {_md(esc_u['AR'])}")
    asim = pd.DataFrame({"γ_ij": [G_u.loc[i, j] for i in ORIGENES[:-1]
                                  for j in ORIGENES[:-1] if i < j],
                         "γ_ji": [G_u.loc[j, i] for i in ORIGENES[:-1]
                                  for j in ORIGENES[:-1] if i < j]},
                        index=[f"{i}·{j}" for i in ORIGENES[:-1]
                               for j in ORIGENES[:-1] if i < j])
    asim["brecha"] = asim["γ_ij"] - asim["γ_ji"]
    print("\n   Qué tan lejos está de ser simétrica ya:")
    for k, f in asim.iterrows():
        print(f"     {k}   γ_ij {_md(f['γ_ij'], 4)}   γ_ji {_md(f['γ_ji'], 4)}   "
              f"brecha {_md(f['brecha'], 4)}")

    print("\n" + "-" * 94)
    print("3. Con simetría impuesta — SUR iterado")
    print("-" * 94)
    res_r, R, dentro_r = estimar(W, REG, fuera="RE", simetria=True)
    G_r = matriz_gamma(res_r, dentro_r, "RE")
    F_r, esc_r = flexibilidades(G_r, res_r, dentro_r, "RE", w)
    se_r = se_propia(res_r, w)
    f_r = F_r.loc["AR", "AR"]
    print(f"   iteraciones hasta converger: {getattr(res_r, 'iterations', 'n/d')}")
    print(f"   f propio de Argentina  {_md(f_r)}  (SE {se_r:.3f})  "
          f"IC95% [{_md(f_r - 1.96 * se_r)}, {_md(f_r + 1.96 * se_r)}]")
    t1 = (f_r + 1) / se_r
    print(f"   H0: f = −1  →  t = {t1:+.1f}  "
          f"({'SE RECHAZA' if abs(t1) > 1.96 else 'no se rechaza'})")
    print(f"   cruzadas con Ecuador {_md(F_r.loc['AR', 'EC'])} · India "
          f"{_md(F_r.loc['AR', 'IN'])} · Vietnam {_md(F_r.loc['AR', 'VN'])}")
    print(f"   escala {_md(esc_r['AR'])}")

    print("\n   Matriz de flexibilidades no compensadas (fila: precio de i, col: cantidad de j):")
    print(F_r.round(3).to_string())

    print("\n" + "-" * 94)
    print("4. ¿Aguanta la simetría?")
    print("-" * 94)
    R_w = restricciones(SUR(ecuaciones(W, REG, "RE")), dentro, "RE")
    Wd, pw, g = wald_simetria(res_u, R_w)
    lr, plr = lr_simetria(res_r, res_u, T, g)
    print(f"   Wald sobre las {g} restricciones   χ² = {Wd:6.2f}   p = {pw:.4f}")
    print(f"   Razón de verosimilitud             χ² = {lr:6.2f}   p = {plr:.4f}")
    print("   " + ("Los datos RECHAZAN la simetría: imponerla es una decisión teórica, "
                   "no un hallazgo." if min(pw, plr) < 0.05 else
                   "Los datos NO rechazan la simetría: imponerla es gratis y gana "
                   "precisión."))

    print("\n" + "-" * 94)
    print("5. Invariancia: el SUR iterado no debe depender de qué ecuación se descarta")
    print("-" * 94)
    inv = []
    for fuera in ["RE", "AR", "EC"]:
        rr, _, dd = estimar(W, REG, fuera=fuera, simetria=True)
        GG = matriz_gamma(rr, dd, fuera)
        FF, ee = flexibilidades(GG, rr, dd, fuera, w)
        inv.append({"ecuación descartada": NOMBRE[fuera], "f_AR": FF.loc["AR", "AR"],
                    "escala_AR": ee["AR"], "iteraciones": getattr(rr, "iterations", np.nan)})
        print(f"   se descarta {NOMBRE[fuera]:<10s} f_AR {_md(FF.loc['AR', 'AR'])}   "
              f"escala {_md(ee['AR'])}")
    INV = pd.DataFrame(inv)
    disp = INV.f_AR.max() - INV.f_AR.min()
    print(f"   dispersión entre las tres: {disp:.4f}  "
          f"({'invariante' if disp < 5e-3 else 'NO invariante — revisar convergencia'})")

    print(SEP + "-" * 94)
    print("6. Robustez a las raíces unitarias: el mismo sistema en diferencias")
    print("-" * 94)
    res_d, F_d, esc_d, T_d = en_diferencias(W, REG, w)
    se_d = se_propia(res_d, w)
    print(f"   f propio de Argentina  {_md(F_d.loc['AR', 'AR'])}  (SE {se_d:.3f})  "
          f"sobre {T_d} diferencias")
    print(f"   escala {_md(esc_d['AR'])}")

    print(SEP + "=" * 94)
    print("7. El número que importa")
    print("=" * 94)
    print(f"   sin simetría (lo que dice hoy el §7)   f = {_md(F_u.loc['AR', 'AR'])}")
    print(f"   con simetría impuesta                  f = {_md(f_r)}")
    print(f"   diferencia                             {_md(f_r - F_u.loc['AR', 'AR'])}")
    print(f"   umbral de decisión                     f = −1,000")
    print("   La conclusión de política no cambia: el precio se mueve mucho menos que")
    print("   proporcionalmente y recortar oferta baja la facturación.")

    sal = _p("salidas", "iaids_simetria.xlsx")
    try:
        with pd.ExcelWriter(sal, engine="openpyxl") as x:
            RU.to_excel(x, sheet_name="estacionariedad", index=False)
            pd.DataFrame({"sin_simetria": res_u.params,
                          "se_sin": res_u.std_errors,
                          "con_simetria": res_r.params,
                          "se_con": res_r.std_errors}).to_excel(x, sheet_name="parametros")
            G_u.to_excel(x, sheet_name="gamma_sin_simetria")
            G_r.to_excel(x, sheet_name="gamma_con_simetria")
            F_u.to_excel(x, sheet_name="flex_sin_simetria")
            F_r.to_excel(x, sheet_name="flex_con_simetria")
            pd.DataFrame({"escala_sin": esc_u, "escala_con": esc_r}).to_excel(
                x, sheet_name="escala")
            asim.to_excel(x, sheet_name="brechas_de_simetria")
            pd.DataFrame([{"test": "Wald", "chi2": Wd, "gl": g, "p": pw},
                          {"test": "razón de verosimilitud", "chi2": lr, "gl": g,
                           "p": plr}]).to_excel(x, sheet_name="tests", index=False)
            INV.to_excel(x, sheet_name="invariancia", index=False)
            F_d.to_excel(x, sheet_name="flex_diferencias")
            pd.DataFrame([{"version": "sin simetría", "f_AR": F_u.loc["AR", "AR"],
                           "se": se_u, "escala_AR": esc_u["AR"]},
                          {"version": "con simetría", "f_AR": f_r, "se": se_r,
                           "escala_AR": esc_r["AR"]},
                          {"version": "con simetría, en diferencias",
                           "f_AR": F_d.loc["AR", "AR"], "se": se_d,
                           "escala_AR": esc_d["AR"]}]).to_excel(
                x, sheet_name="resumen", index=False)
        print(f"\nGuardado: {sal}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {sal} (¿abierto en Excel?)")


if __name__ == "__main__":
    main()
