# -*- coding: utf-8 -*-
"""El análisis completo de demanda inversa, rehecho con el precio argentino de EUMOFA.

POR QUÉ CORRERLO APARTE. El estudio mide el langostino con el FOB de despacho del
entero L1 congelado a bordo, que sale de la base de comercio. Esa serie tiene dos
propiedades que conviene poner a prueba desde afuera: es de fuente privada y es FOB de
origen, mientras que el control del competidor es CIF en frontera de la UE. EUMOFA
—Eurostat-Comext— permite rehacer todo con una fuente pública y con las dos puntas del
mismo lado de la aduana.

QUÉ CAMBIA RESPECTO DEL ESTUDIO. Tres cosas, y hay que tenerlas juntas para leer el
resultado:

  1. El producto. «Shrimp, miscellaneous» congelado de origen Argentina es TODO el
     langostino que entra a la UE: entero y cola, todos los calibres, las dos flotas.
     No es el entero L1 tangonero. Es una canasta más ancha y su valor unitario se
     mueve también con la mezcla.
  2. El mercado. EUMOFA ve la importación de la UE. El FOB de despacho ve todo el
     destino, incluidos China, Japón y Estados Unidos. Son dos universos distintos.
  3. La valuación. EUMOFA es CIF, con flete y seguro adentro; el despacho es FOB.

QUÉ SE MANTIENE IGUAL. El diseño: la cantidad entra en logaritmo, el canal HORECA entra
como brecha del índice observado respecto de su tendencia, hay estacionalidad mensual,
tendencia y la ventana del conflicto gremial de 2025 como instrumento de oferta.

TRES CANTIDADES. Como el precio ya no es el del producto de una sola flota, la cantidad
correcta deja de ser obvia y se corren las tres candidatas:
     Q_tan  captura tangonera acumulada 12 meses, que es la del estudio;
     Q_tot  desembarque total de langostino, las dos flotas, acumulado 12 meses;
     Q_ue   volumen argentino efectivamente importado por la UE, acumulado 12 meses,
            que es la cantidad que enfrenta ese precio en ese mercado.

Uso:  python demanda_inversa_eumofa_argentina.py
Salida: consola + salidas/demanda_inversa_eumofa_argentina.xlsx
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 205)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402

HAC = 6
MIN_MESES = 9
CANTIDADES = {"Q_tan": "captura tangonera 12 meses",
              "Q_tot": "desembarque total de langostino 12 meses",
              "Q_ue": "volumen argentino importado por la UE 12 meses"}


def _p(*t):
    return os.path.join(RAIZ, *t)


# --------------------------------------------------------------------- panel
def panel() -> pd.DataFrame:
    """El panel del estudio, con el precio de EUMOFA y las tres cantidades."""
    df, tan = T.panel()
    d = df.copy()

    lan = pd.read_pickle(_p("_lan.pkl"))
    lan.index = pd.PeriodIndex(lan.anio.astype(str) + "-"
                               + lan.mes.astype(str).str.zfill(2), freq="M")
    tot = lan.groupby(level=0).t.sum().rename("tot_t")

    d["tot_t"] = tot.reindex(d.index)
    d["Q_tan"] = d.tan12
    d["Q_tot"] = tot.rolling(12).sum().reindex(d.index)
    d["Q_ue"] = d.ar_kt.rolling(12).sum()
    d["rel_eu"] = d.ar_eur_kg / d.van_eur_kg
    d["rel_eu_ec"] = d.ar_eur_kg / d.van_ec_eur_kg
    return d


def raiz(s: pd.Series, nom: str) -> dict:
    s = s.dropna()
    ad = adfuller(s, autolag="AIC")
    kp = kpss(s, regression="c", nlags="auto")
    ver = ("estacionaria" if ad[1] < .05 and kp[1] > .05 else
           "raíz unitaria" if ad[1] > .05 and kp[1] < .05 else "ambiguo")
    return {"serie": nom, "ADF": ad[0], "ADF_p": ad[1], "KPSS": kp[0],
            "KPSS_p": kp[1], "veredicto": ver}


def _rep(m, var, nombre, robusto=True):
    f, se = m.params[var], m.bse[var]
    gl = int(m.df_resid)
    tc = 1.96 if robusto else stats.t.ppf(.975, gl)
    print(f"\n--- {nombre}   N={int(m.nobs)}  R2={m.rsquared:.3f}")
    print(f"    f = {f:+.3f}  se = {se:.3f}  IC95% [{f - tc * se:+.3f}, "
          f"{f + tc * se:+.3f}]   H0: f = -1 → t = {(f + 1) / se:+.2f}   "
          f"1+f = {1 + f:+.3f}")
    return {"modelo": nombre, "f": f, "se": se, "ic_inf": f - tc * se,
            "ic_sup": f + tc * se, "t_H0": (f + 1) / se, "N": int(m.nobs)}


def campanas(d: pd.DataFrame, q: str) -> pd.DataFrame:
    """Captura abr-oct del año Y contra el precio de importación de jul Y a jun Y+1,
    ponderado por el volumen argentino que entró a la UE en cada mes."""
    filas = []
    base = d.tan_t if q == "Q_tan" else d.tot_t if q == "Q_tot" else d.ar_kt
    for y in range(int(d.index.year.min()), int(d.index.year.max()) + 1):
        cap = base.loc[f"{y}-04":f"{y}-10"].sum()
        ven = d.loc[f"{y}-07":f"{y + 1}-06"].dropna(subset=["ar_eur_kg", "ar_kt"])
        if cap <= 0 or len(ven) < MIN_MESES:
            continue
        p = (ven.ar_eur_kg * ven.ar_kt).sum() / ven.ar_kt.sum()
        filas.append({"campaña": f"{y}/{y + 1}", "cantidad_t": cap, "meses": len(ven),
                      "p_eur_kg": p, "cultivo_eur_kg": ven.van_eur_kg.mean(),
                      "rel": p / ven.van_eur_kg.mean(),
                      "horeca": ven.horeca.mean(),
                      "covid": float(ven.horeca_mano.mean() > 0)})
    C = pd.DataFrame(filas).set_index("campaña")
    C["lq"], C["lp"] = np.log(C.cantidad_t), np.log(C.p_eur_kg)
    C["lrel"], C["lvan"] = np.log(C.rel), np.log(C.cultivo_eur_kg)
    C["trend"] = np.arange(len(C))
    return C


def main() -> None:
    d = panel()
    res, tab = [], {}

    print("=" * 100)
    print("DEMANDA INVERSA DEL LANGOSTINO ARGENTINO CON EL PRECIO DE EUMOFA/COMEXT")
    print("=" * 100)
    print("Precio: «Shrimp, miscellaneous» congelado, origen Argentina, importación "
          "extra-UE,")
    print("valor unitario CIF en euros por kilo. Control: «Shrimp, warmwater» desde "
          "Ecuador,")
    print("India, Vietnam, Bangladesh, Indonesia y Tailandia, mismo tratamiento.")
    print(f"Muestra {d.index.min()} a {d.index.max()}.")

    an = d.groupby(d.index.year).agg(
        ar=("ar_eur_kg", "mean"), van=("van_eur_kg", "mean"),
        rel=("rel_eu", "mean"), ar_kt=("ar_kt", "sum"),
        tan_t=("tan_t", "sum"), tot_t=("tot_t", "sum"))
    print("\n" + "-" * 100)
    print("1. LOS DATOS, POR AÑO")
    print("-" * 100)
    print(an.round(3).to_string())
    for y0, y1, lab in [(2019, 2020, "2020 · shock de DEMANDA"),
                        (2024, 2025, "2025 · shock de OFERTA")]:
        dr = np.log(an.rel[y1] / an.rel[y0]) * 100
        for q, nom in [("tan_t", "captura tangonera"), ("tot_t", "desembarque total"),
                       ("ar_kt", "volumen a la UE")]:
            dq = np.log(an[q][y1] / an[q][y0]) * 100
            print(f"   {lab:<26s} {nom:<20s} {dq:+6.1f}%   precio relativo "
                  f"{dr:+5.1f}%   arco {dr / dq:+.3f}")

    # ------------------------------------------------------- 2. raíces
    print("\n" + "-" * 100)
    print("2. ORDEN DE INTEGRACIÓN (ADF y KPSS, antes de estimar)")
    print("-" * 100)
    RU = []
    for nom, s in [("log precio AR (EUMOFA)", np.log(d.ar_eur_kg)),
                   ("log precio cultivo", np.log(d.van_eur_kg)),
                   ("log del cociente", np.log(d.rel_eu)),
                   ("log Q_tan", np.log(d.Q_tan)),
                   ("log Q_tot", np.log(d.Q_tot)),
                   ("log Q_ue", np.log(d.Q_ue))]:
        r = raiz(s, nom)
        RU.append(r)
        print(f"   {nom:<24s} ADF {r['ADF']:+6.2f} (p {r['ADF_p']:.3f})   "
              f"KPSS {r['KPSS']:5.2f} (p {r['KPSS_p']:.3f})   {r['veredicto']}")
    RU = pd.DataFrame(RU)

    # ------------------------------------------------------- 3. mensual
    print("\n" + "-" * 100)
    print("3. MENSUAL — el mismo diseño del estudio, con las tres cantidades")
    print("-" * 100)
    b = d.dropna(subset=["ar_eur_kg", "van_eur_kg", "horeca", "Q_tan", "Q_tot",
                         "Q_ue"]).copy()
    b["lp"] = np.log(b.ar_eur_kg)
    b["lvan"] = np.log(b.van_eur_kg)
    b["lrel"] = np.log(b.rel_eu)
    for q in CANTIDADES:
        b["l" + q] = np.log(b[q])
    b["trend"] = np.arange(len(b)) / 12.0
    M = pd.get_dummies(b.index.month, prefix="m", drop_first=True).astype(float)
    M.index = b.index
    print(f"   N = {len(b)} meses, {b.index.min()} a {b.index.max()}")

    def ols(y, X):
        m = sm.OLS(y, sm.add_constant(X), missing="drop").fit(
            cov_type="HAC", cov_kwds={"maxlags": HAC})
        return m, [i for i in m.params.index if not i.startswith("m_")]

    for q, etq in CANTIDADES.items():
        lq = "l" + q
        m, v = ols(b.lp, pd.concat([b[[lq, "lvan", "trend"]], M], axis=1))
        r = _rep(m, lq, f"E1·{q}  log P (EUR) ~ log Q + cultivo + tendencia  [{etq}]")
        res.append(r)
        tab[f"E1_{q}"] = pd.DataFrame({"coef": m.params, "se": m.bse,
                                       "t": m.tvalues}).loc[v]

        m, v = ols(b.lp, pd.concat([b[[lq, "lvan", "horeca", "trend"]], M], axis=1))
        res.append(_rep(m, lq, f"E2·{q}  E1 + brecha HORECA"))
        tab[f"E2_{q}"] = pd.DataFrame({"coef": m.params, "se": m.bse,
                                       "t": m.tvalues}).loc[v]

        m, v = ols(b.lrel, pd.concat([b[[lq, "horeca", "trend"]], M], axis=1))
        res.append(_rep(m, lq, f"E3·{q}  precio relativo al cultivo + HORECA"))
        tab[f"E3_{q}"] = pd.DataFrame({"coef": m.params, "se": m.bse,
                                       "t": m.tvalues}).loc[v]

    # El cociente de EUMOFA tiene raíz unitaria (ver la sección 2), cosa que NO pasa con
    # el del entero L1. Con una dependiente I(1) la regresión en niveles puede ser
    # espuria, así que se repite todo en primeras diferencias, que es el chequeo que
    # corresponde: si el resultado sobrevive, no lo fabricó la tendencia común.
    print("\n   En primeras diferencias, porque el cociente de EUMOFA es I(1):")
    D = b.diff().dropna()
    MD = M.reindex(D.index)
    for q in CANTIDADES:
        lq = "l" + q
        m, v = ols(D.lrel, pd.concat([D[[lq, "horeca"]], MD], axis=1))
        res.append(_rep(m, lq, f"E6·{q}  Δ log (P/cultivo) ~ Δ log Q + Δ HORECA"))
        tab[f"E6_{q}"] = pd.DataFrame({"coef": m.params, "se": m.bse,
                                       "t": m.tvalues}).loc[v]

    e = b[(b.index < pd.Period("2020-03")) | (b.index > pd.Period("2022-03"))]
    m, v = ols(e.lp, pd.concat([e[["lQ_tan", "lvan", "trend"]], M.loc[e.index]], axis=1))
    res.append(_rep(m, "lQ_tan", "E4  sin la ventana de pandemia (mar-2020 a mar-2022)"))
    tab["E4"] = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues}).loc[v]

    # ------------------------------------------------------------ 4. IV
    print("\n" + "-" * 100)
    print("4. IV 2SLS — instrumento: la ventana en que el conflicto deprime la captura")
    print("-" * 100)
    from linearmodels.iv import IV2SLS
    for q in CANTIDADES:
        lq = "l" + q
        dd = pd.concat([b[["lrel", lq, "horeca", "trend", "iv_conf"]], M],
                       axis=1).dropna()
        ex = sm.add_constant(dd[["horeca", "trend"] + list(M.columns)])
        iv = IV2SLS(dd.lrel, ex, dd[[lq]], dd[["iv_conf"]]).fit(
            cov_type="kernel", kernel="bartlett")
        f, se = iv.params[lq], iv.std_errors[lq]
        F1 = float(iv.first_stage.diagnostics["f.stat"].iloc[0])
        fuerte = F1 > 10
        print(f"\n--- E5·{q}  IV sobre el precio relativo   N={int(iv.nobs)}")
        print(f"    f = {f:+.3f}  se = {se:.3f}  IC95% [{f - 1.96 * se:+.3f}, "
              f"{f + 1.96 * se:+.3f}]   H0: f = -1 → t = {(f + 1) / se:+.2f}")
        print(f"    primera etapa F = {F1:.1f}  "
              + ("(instrumento fuerte)" if fuerte else "(INSTRUMENTO DÉBIL — no usar)"))
        res.append({"modelo": f"E5·{q}  IV, precio relativo", "f": f, "se": se,
                    "ic_inf": f - 1.96 * se, "ic_sup": f + 1.96 * se,
                    "t_H0": (f + 1) / se, "N": int(iv.nobs), "F1": F1})

    # ------------------------------------------------------- 5. campaña
    print("\n" + "-" * 100)
    print("5. NIVEL CAMPAÑA")
    print("-" * 100)
    CC = {}
    for q in CANTIDADES:
        C = campanas(d, q)
        CC[q] = C
        if q == "Q_tan":
            print(C[["cantidad_t", "meses", "p_eur_kg", "cultivo_eur_kg",
                     "rel"]].round(3).to_string())
        for dep, X, nom in [("lp", ["lq", "lvan", "horeca"], f"C1·{q}  log P ~ log Q + cultivo + HORECA"),
                            ("lrel", ["lq", "horeca"], f"C2·{q}  log (P/cultivo) ~ log Q + HORECA"),
                            ("lrel", ["lq", "horeca", "trend"], f"C3·{q}  C2 + tendencia")]:
            m = sm.OLS(C[dep], sm.add_constant(C[X])).fit(cov_type="HC1")
            res.append(_rep(m, "lq", nom))
            tab[nom.split()[0]] = pd.DataFrame({"coef": m.params, "se": m.bse,
                                                "t": m.tvalues})

    print("\n   Leave-one-out sobre C2·Q_tan — ¿lo maneja una sola campaña?")
    C = CC["Q_tan"]
    loo = {}
    for i in C.index:
        mm = sm.OLS(C.drop(index=i).lrel,
                    sm.add_constant(C.drop(index=i)[["lq", "horeca"]])).fit()
        loo[i] = mm.params["lq"]
    print("   " + " · ".join(f"sin {k}: {v:+.3f}" for k, v in loo.items()))
    print(f"   rango: {min(loo.values()):+.3f} a {max(loo.values()):+.3f}")

    # -------------------------------------------------- 6. la comparación
    R = pd.DataFrame(res).set_index("modelo")
    print("\n" + "=" * 100)
    print("6. RESUMEN")
    print("=" * 100)
    print(R.round(3).to_string())

    print("\n" + "-" * 100)
    print("7. CONTRA EL ESTUDIO")
    print("-" * 100)
    ESTUDIO = {"IV mensual sobre el precio relativo": -0.184,
               "campaña C2": -0.212, "campaña C3 con tendencia": -0.239,
               "sistema IAIDS con simetría": -0.282}
    print("   El estudio, con el FOB del entero L1 tangonero:")
    for k, v in ESTUDIO.items():
        print(f"      {k:<44s} f = {v:+.3f}")
    iv_tan = R.loc["E5·Q_tan  IV, precio relativo", "f"]
    print("\n   Esta corrida, con el precio de EUMOFA:")
    for k in R.index:
        print(f"      {k:<44s} f = {R.f[k]:+.3f}   IC95% "
              f"[{R.ic_inf[k]:+.3f}, {R.ic_sup[k]:+.3f}]")
    print(f"\n   Todas las estimaciones están MUY por encima de −1: la mayor en valor "
          f"absoluto es {R.f.min():+.3f}.")
    print("   El umbral de decisión del estudio —recortar oferta sólo conviene si "
          "|f| > 1— no se")
    print("   toca con ninguna de las dos fuentes.")

    # ------------------------------------------------------------ salida
    try:
        out = _p("salidas", "demanda_inversa_eumofa_argentina.xlsx")
        with pd.ExcelWriter(out) as w:
            m_ = d[["ar_eur_kg", "van_eur_kg", "van_ec_eur_kg", "rel_eu", "rel_eu_ec",
                    "ar_kt", "tan_t", "tot_t", "Q_tan", "Q_tot", "Q_ue", "horeca",
                    "p_eur", "rel"]].copy()
            m_.index = m_.index.astype(str)
            m_.round(4).to_excel(w, sheet_name="mensual")
            an.round(3).to_excel(w, sheet_name="anual")
            RU.round(4).to_excel(w, sheet_name="raices", index=False)
            R.round(4).to_excel(w, sheet_name="flexibilidades")
            for q, C in CC.items():
                C.round(4).to_excel(w, sheet_name=f"campanas_{q}")
            pd.Series(loo, name="f").to_frame().round(4).to_excel(
                w, sheet_name="leave_one_out")
            pd.concat(tab, names=["modelo"]).round(4).to_excel(
                w, sheet_name="regresiones")
            pd.DataFrame([{"fuente": "estudio (FOB entero L1 tangonero)", "modelo": k,
                           "f": v} for k, v in ESTUDIO.items()]
                         + [{"fuente": "EUMOFA (langostino argentino CIF)",
                             "modelo": k, "f": R.f[k]} for k in R.index]).round(4) \
                .to_excel(w, sheet_name="comparacion", index=False)
        print(f"\nGuardado: {out}")
    except PermissionError:
        print("\nAVISO: no pude escribir el xlsx (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
