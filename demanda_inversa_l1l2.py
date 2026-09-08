# -*- coding: utf-8 -*-
"""Demanda inversa del entero congelado a bordo, L1 y L2 juntos.

Por qué L1+L2 y no sólo L1. El congelado a bordo es PRODUCTO FINAL: lo que la flota
tangonera desembarca es exactamente lo que exporta, sin reproceso en tierra. Eso tiene dos
consecuencias que el modelo de L1 solo no aprovechaba:

  1. La composición por talla del desembarque es OBSERVABLE en el despacho de exportación.
     No hace falta pedirla a nadie.
  2. Tomando L1 y L2 juntos se cubre la casi totalidad del producto —el resto es marginal—,
     de modo que la variación de mezcla entre las dos tallas deja de ser error de medición
     de Q y pasa a ser una variable medida, que se controla.

Se estima todo por duplicado —L1 solo y L1+L2— para que la comparación quede a la vista.
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 190)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402

DESDE, HASTA = "2013-01", "2026-07"
CAL = ["L1", "L2"]


def _p(*t):
    return os.path.join(RAIZ, *t)


# ---------------------------------------------------------------- panel por talla
def panel_talla():
    d = T.despachos()
    e = d[(d.pres == "entero") & (d.ruta == "a bordo") & (d.kg > 0) & (d.fob_tot > 0)].copy()
    e.index = pd.PeriodIndex(e.anio.astype(str) + "-" + e.mes.astype(str).str.zfill(2), freq="M")
    e = e.sort_index()

    kg = e.pivot_table(index=e.index, columns="cal", values="kg", aggfunc="sum")
    fob = e.pivot_table(index=e.index, columns="fob_tot", values="fob_tot", aggfunc="sum") \
        if False else e.pivot_table(index=e.index, columns="cal", values="fob_tot", aggfunc="sum")
    return e, kg.fillna(0.0), fob.fillna(0.0)


def main():
    df, tan = T.panel()          # trae precio del L1, captura, cultivo, fx, HORECA
    e, kg, fob = panel_talla()

    print("=" * 100)
    print("DEMANDA INVERSA DEL ENTERO CONGELADO A BORDO — L1 Y L2 JUNTOS")
    print("=" * 100)

    # ------------------------------------------------ 1. cuánto es L1+L2
    tot = kg.sum().sort_values(ascending=False)
    print("\n1. COBERTURA — kilos de entero congelado a bordo por talla, 2013-2026 (kt)")
    print((tot / 1e6).round(1).to_string())
    cob = kg[CAL].sum().sum() / kg.sum().sum() * 100
    print(f"\n   L1 + L2 = {cob:.1f}% de todo el entero de la flota congeladora.")
    print(f"   L1 solo = {kg['L1'].sum() / kg.sum().sum() * 100:.1f}%   ·   "
          f"L2 solo = {kg['L2'].sum() / kg.sum().sum() * 100:.1f}%")

    # ------------------------------------------------ 2. el share, por campaña
    print("\n2. LA MEZCLA — participación de cada talla dentro del entero a bordo, por campaña")
    filas = []
    for y in range(2013, 2026):
        v = kg.loc[f"{y}-07":f"{y + 1}-06"]
        v = v[v.index.month.isin(T.TEMPORADA)]
        if v.sum().sum() <= 0:
            continue
        s = v.sum()
        filas.append({"campaña": f"{y}/{y + 1}", "kt": s.sum() / 1e6,
                      "L1_%": s.get("L1", 0) / s.sum() * 100,
                      "L2_%": s.get("L2", 0) / s.sum() * 100,
                      "L1+L2_%": (s.get("L1", 0) + s.get("L2", 0)) / s.sum() * 100})
    S = pd.DataFrame(filas).set_index("campaña")
    print(S.round(1).to_string())
    print(f"\n   L1 solo: desvío {S['L1_%'].std():.1f} puntos, rango {S['L1_%'].min():.1f}-{S['L1_%'].max():.1f}")
    print(f"   L1+L2  : desvío {S['L1+L2_%'].std():.1f} puntos, rango "
          f"{S['L1+L2_%'].min():.1f}-{S['L1+L2_%'].max():.1f}")
    print("   → tomando las dos tallas juntas, la mezcla deja de moverse: el agregado ES la flota.")

    # ------------------------------------------------ 3. precio agregado
    # (a) valor unitario del agregado — mezcla incluida
    # (b) índice de peso fijo — purga la mezcla usando participaciones medias de todo el período
    k = kg[CAL]
    f_ = fob[CAL]
    p_tal = (f_ / k.replace(0, np.nan))                      # precio por talla y mes
    w_fijo = (k.sum() / k.sum().sum())                       # ponderación fija
    p_uv = f_.sum(axis=1) / k.sum(axis=1)                    # valor unitario agregado
    p_fijo = (p_tal * w_fijo).sum(axis=1) / w_fijo.sum()     # índice de peso fijo
    q_l1l2 = k.sum(axis=1)                                   # kilos exportados L1+L2

    A = pd.DataFrame({"p_uv": p_uv, "p_fijo": p_fijo, "q_expo_kg": q_l1l2,
                      "sL2": k["L2"] / k.sum(axis=1),
                      "p_L1": p_tal["L1"], "p_L2": p_tal["L2"]}).loc[DESDE:HASTA]
    A = A.join(df[["tan_t", "tan12", "van_eur_kg", "eurusd", "horeca", "horeca_ue"]])
    A["p_uv_eur"] = A.p_uv / A.eurusd
    A["p_fijo_eur"] = A.p_fijo / A.eurusd
    A["rel_uv"] = A.p_uv_eur / A.van_eur_kg
    A["rel_fijo"] = A.p_fijo_eur / A.van_eur_kg

    print("\n3. PRECIO — L2 contra L1 y cuánto pesa la mezcla")
    d2 = A.dropna(subset=["p_L1", "p_L2"])
    print(f"   descuento medio del L2 respecto del L1: {(1 - (d2.p_L2 / d2.p_L1).mean()) * 100:.1f}%  "
          f"(desvío {(d2.p_L2 / d2.p_L1).std() * 100:.1f} puntos)")
    print(f"   correlación mensual de los dos precios en logs: "
          f"{np.corrcoef(np.log(d2.p_L1), np.log(d2.p_L2))[0, 1]:.3f}")
    b = sm.OLS(np.log(d2.p_L2), sm.add_constant(np.log(d2.p_L1))).fit(
        cov_type="HAC", cov_kwds={"maxlags": 6})
    print(f"   elasticidad del precio del L2 al del L1: {b.params['p_L1']:+.3f} "
          f"(se {b.bse['p_L1']:.3f}) — se mueven como un solo producto")
    dd = A.dropna(subset=["p_uv_eur", "p_fijo_eur"])
    print(f"   valor unitario contra índice de peso fijo: correlación en logs "
          f"{np.corrcoef(np.log(dd.p_uv_eur), np.log(dd.p_fijo_eur))[0, 1]:.4f}, "
          f"brecha media {((dd.p_uv_eur / dd.p_fijo_eur - 1).mean() * 100):+.2f}%")

    # ------------------------------------------------ 4. mensual: L1 vs L1+L2
    print("\n" + "=" * 100)
    print("4. MENSUAL — la misma especificación, con L1 solo y con L1+L2")
    print("=" * 100)
    from linearmodels.iv import IV2SLS

    B = A.join(df[["p_eur", "rel", "iv_conf"]]).dropna(
        subset=["rel", "rel_uv", "rel_fijo", "tan12", "horeca"])
    B["lq"] = np.log(B.tan12)
    B["trend"] = np.arange(len(B)) / 12.0
    M = pd.get_dummies(B.index.month, prefix="m", drop_first=True).astype(float)
    M.index = B.index

    def corre(dep, nom, iv=False):
        y = np.log(B[dep])
        if not iv:
            X = pd.concat([B[["lq", "horeca", "trend"]], M], axis=1)
            m = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
            f, se, extra = m.params["lq"], m.bse["lq"], ""
            N = int(m.nobs)
        else:
            ex = sm.add_constant(pd.concat([B[["horeca", "trend"]], M], axis=1))
            r = IV2SLS(y, ex, B[["lq"]], B[["iv_conf"]]).fit(cov_type="kernel", kernel="bartlett")
            f, se = r.params["lq"], r.std_errors["lq"]
            F1 = float(r.first_stage.diagnostics["f.stat"].iloc[0])
            extra, N = f"  ·  primera etapa F = {F1:.1f}", int(r.nobs)
        print(f"   {nom:<52s} f = {f:+.3f}  se {se:.3f}  "
              f"IC95% [{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]  N={N}{extra}")
        return {"modelo": nom, "f": f, "se": se, "ic_inf": f - 1.96 * se,
                "ic_sup": f + 1.96 * se, "N": N}

    print("\n   MCO sobre el precio relativo al cultivo (equivale a T4):")
    r = [corre("rel", "L1 solo"),
         corre("rel_uv", "L1+L2, valor unitario"),
         corre("rel_fijo", "L1+L2, índice de peso fijo")]
    print("\n   IV, instrumento = ventana del conflicto (equivale a T5):")
    r += [corre("rel", "L1 solo", iv=True),
          corre("rel_uv", "L1+L2, valor unitario", iv=True),
          corre("rel_fijo", "L1+L2, índice de peso fijo", iv=True)]

    # ------------------------------------------------ 5. campaña
    print("\n" + "=" * 100)
    print("5. CAMPAÑA — captura abr-oct contra precio de venta jul-jun, ponderado por volumen")
    print("=" * 100)
    H = A.horeca_ue
    filas = []
    for y in range(2013, 2026):
        cap = tan.loc[f"{y}-04":f"{y}-10"].sum()
        ven = A.loc[f"{y}-07":f"{y + 1}-06"].dropna(subset=["p_uv"])
        if cap <= 0 or len(ven) < 9:
            continue
        w = ven.q_expo_kg
        filas.append({
            "campaña": f"{y}/{y + 1}", "captura_t": cap, "meses": len(ven),
            "p_uv_eur": (ven.p_uv_eur * w).sum() / w.sum(),
            "p_fijo_eur": (ven.p_fijo_eur * w).sum() / w.sum(),
            "p_L1_eur": (ven.p_L1 / ven.eurusd * ven.q_expo_kg).sum() / w.sum(),
            "cultivo_eur": ven.van_eur_kg.mean(),
            "sL2": (ven.sL2 * w).sum() / w.sum(),
            "expo_kt": w.sum() / 1e6,
            "horeca_ue": H.reindex(ven.index).mean()})
    C = pd.DataFrame(filas).set_index("campaña")
    C["rel_uv"] = C.p_uv_eur / C.cultivo_eur
    C["rel_fijo"] = C.p_fijo_eur / C.cultivo_eur
    C["rel_L1"] = C.p_L1_eur / C.cultivo_eur
    C["lq"] = np.log(C.captura_t)
    C["trend"] = np.arange(len(C))
    C["horeca"] = sm.OLS(np.log(C.horeca_ue), sm.add_constant(C[["trend"]])).fit().resid
    print(C[["captura_t", "meses", "expo_kt", "sL2", "p_L1_eur", "p_uv_eur", "p_fijo_eur",
             "cultivo_eur", "rel_uv"]].round(3).to_string())

    print("\n   log (P/cultivo) ~ log captura + HORECA + tendencia, HC1:")
    rc = []
    for dep, nom in [("rel_L1", "L1 solo"), ("rel_uv", "L1+L2, valor unitario"),
                     ("rel_fijo", "L1+L2, índice de peso fijo")]:
        m = sm.OLS(np.log(C[dep]), sm.add_constant(C[["lq", "horeca", "trend"]])).fit(cov_type="HC1")
        f, se = m.params["lq"], m.bse["lq"]
        print(f"   {nom:<32s} f = {f:+.3f}  se {se:.3f}  "
              f"IC95% [{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]  R2={m.rsquared:.3f}  N={int(m.nobs)}")
        rc.append({"modelo": nom, "f": f, "se": se, "R2": m.rsquared, "N": int(m.nobs)})

    print("\n   ¿La mezcla explica algo? Agregando el share de L2 como control:")
    for dep, nom in [("rel_uv", "L1+L2, valor unitario")]:
        m = sm.OLS(np.log(C[dep]),
                   sm.add_constant(C[["lq", "horeca", "trend", "sL2"]])).fit(cov_type="HC1")
        print(pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues}).round(4).to_string())

    print("\n   Leave-one-out del agregado L1+L2 (valor unitario):")
    loo = {}
    for i in C.index:
        c = C.drop(index=i)
        loo[i] = sm.OLS(np.log(c.rel_uv), sm.add_constant(c[["lq", "horeca", "trend"]])).fit().params["lq"]
    print("   " + " · ".join(f"sin {k}: {v:+.3f}" for k, v in loo.items()))
    print(f"   rango: {min(loo.values()):+.3f} a {max(loo.values()):+.3f}")

    # ------------------------------------------------ 6. Q observada
    print("\n" + "=" * 100)
    print("6. Q MEDIDA SOBRE EL PROPIO PRODUCTO FINAL")
    print("=" * 100)
    print("El congelado a bordo no se reprocesa: lo desembarcado es lo exportado. Desde 2020 el")
    print("volumen del despacho es confiable, así que la cantidad ofrecida se puede medir directo.")
    C2 = C[C.index >= "2020/2021"].copy()
    C2["lq_expo"] = np.log(C2.expo_kt)
    C2["trend"] = np.arange(len(C2))
    print(C2[["captura_t", "expo_kt", "p_uv_eur", "rel_uv"]].round(3).to_string())
    for q, nom in [("lq", "Q = captura tangonera"), ("lq_expo", "Q = kilos L1+L2 exportados")]:
        m = sm.OLS(np.log(C2.rel_uv), sm.add_constant(C2[[q, "horeca"]])).fit(cov_type="HC1")
        f, se = m.params[q], m.bse[q]
        print(f"   {nom:<32s} f = {f:+.3f}  se {se:.3f}  R2={m.rsquared:.3f}  N={int(m.nobs)}")
    print("   (seis campañas: es un contraste de orden de magnitud, no una estimación)")

    with pd.ExcelWriter(_p("salidas", "demanda_inversa_l1l2.xlsx")) as w:
        S.to_excel(w, sheet_name="mezcla_por_campana")
        A.to_excel(w, sheet_name="panel_mensual")
        C.to_excel(w, sheet_name="campanas")
        pd.DataFrame(r).to_excel(w, sheet_name="flex_mensual", index=False)
        pd.DataFrame(rc).to_excel(w, sheet_name="flex_campana", index=False)
    print("\nEscrito: salidas/demanda_inversa_l1l2.xlsx")
    return A, C, S


if __name__ == "__main__":
    main()
