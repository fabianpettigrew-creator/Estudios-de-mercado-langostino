# -*- coding: utf-8 -*-
"""Qué cambia en el modelo cuando la flota queda bien definida.

Regla de la industria (Fabián, 23-ago-2026): el entero congelado A BORDO es de la flota
TANGONERA; lo que no lleva esa marca es de la flota FRESQUERA, procesada en tierra. No hay
tercera categoría. Y el desembarque tangonero es PRODUCTO FINAL que va directo a exportación.

Tres pruebas:
  1. ¿Se cierra la identidad desembarque = exportación en la tangonera? Si cierra, la cantidad
     ofrecida se puede MEDIR en vez de aproximarla con la captura, y el desvío que quede ES la
     existencia.
  2. ¿Cuánto pesa la fresquera y mueve el precio del tangonero? Antes no entraba al modelo.
  3. ¿El corrimiento de la fresquera hacia el L2 explica la tendencia sin nombre?
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
pd.set_option("display.width", 210)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402

# Rendimiento a peso entero equivalente, para sumar presentaciones distintas.
# Cadena de rendimientos fijada por la industria (Fabián, 24-ago-2026), igual en las dos flotas:
#     entero → cola            0,55
#     cola   → pelado devenado 0,70   →  sobre entero: 0,55 × 0,70 = 0,385
# El easy peel es cola con el caparazón cortado, así que va con la cola. El pelado ahumado se
# trata como pelado: es marginal (2,2 kt en toda la serie) y no mueve ningún resultado.
REND = {"entero": 1.00, "cola": 0.55, "pelado": 0.385, "pelado devenado": 0.385,
        "easy peel": 0.55, "pelado ahumado": 0.385}
HAC = 6


def base():
    df, tan = T.panel()
    e = T.despachos()
    e = e[e.kg > 0].copy()
    # LA REGLA: a bordo = tangonera; todo lo demás = fresquera.
    e["flota"] = np.where(e.ruta == "a bordo", "tangonera", "fresquera")
    e.index = pd.PeriodIndex(e.anio.astype(str) + "-" + e.mes.astype(str).str.zfill(2), freq="M")
    e = e.sort_index()
    e["kg_ent"] = e.kg / e.pres.map(REND).fillna(1.0)
    return df, tan, e


def identidad(tan, e):
    print("\n" + "=" * 100)
    print("1. ¿SE CIERRA LA IDENTIDAD DESEMBARQUE = EXPORTACIÓN EN LA TANGONERA?")
    print("=" * 100)
    print("Captura SSPyA abr-oct del año Y contra exportación a bordo de jul Y a jun Y+1, en peso")
    print("entero equivalente. Sólo campañas con volumen de despacho confiable (2020 en adelante).")
    filas = []
    for y in range(2020, 2026):
        cap = tan.loc[f"{y}-04":f"{y}-10"].sum()
        v = e.loc[f"{y}-07":f"{y + 1}-06"]
        ab = v[v.flota == "tangonera"]
        filas.append({"campaña": f"{y}/{y + 1}", "captura_t": cap,
                      "expo_peso_entero_t": ab.kg_ent.sum() / 1000,
                      "expo_bruto_t": ab.kg.sum() / 1000})
    C = pd.DataFrame(filas).set_index("campaña")
    C["razón"] = C.expo_peso_entero_t / C.captura_t
    print(C.round(3).to_string())
    s = C.razón
    print(f"\n   razón: media {s.mean():.3f}  desvío {s.std():.3f}")
    sx = s.drop("2020/2021")
    print(f"   excluyendo 2020/2021 —el año de descarga del stock pospandemia—: "
          f"media {sx.mean():.3f}  desvío {sx.std():.3f}  rango {sx.min():.3f}-{sx.max():.3f}")
    print("   → la identidad cierra en promedio; lo que queda alrededor del 1 ES la existencia.")
    return C


def peso_fresquera(e):
    print("\n" + "=" * 100)
    print("2. CUÁNTO PESA LA FRESQUERA")
    print("=" * 100)
    filas = []
    for y in range(2020, 2026):
        v = e.loc[f"{y}-07":f"{y + 1}-06"]
        filas.append({"campaña": f"{y}/{y + 1}",
                      "tangonera_kt": v[v.flota == "tangonera"].kg_ent.sum() / 1e6,
                      "fresquera_kt": v[v.flota == "fresquera"].kg_ent.sum() / 1e6})
    G = pd.DataFrame(filas).set_index("campaña")
    G["fresquera_%"] = G.fresquera_kt / (G.tangonera_kt + G.fresquera_kt) * 100
    print(G.round(2).to_string())
    print("   → la fresquera es la mitad o más del volumen exportado, y no estaba en el modelo.")
    return G


def panel_flotas(df, e):
    idx = df.index
    CAL = ["L1", "L2", "L3", "L4", "L5"]
    ab = e[(e.flota == "tangonera") & (e.pres == "entero") & (e.cal.isin(["L1", "L2"]))]
    fr = e[(e.flota == "fresquera") & (e.pres == "entero") & (e.cal.isin(CAL))]
    A = pd.DataFrame({
        "p_ab": (ab.groupby(level=0).fob_tot.sum() / ab.groupby(level=0).kg.sum()).reindex(idx),
        "p_fr": (fr.groupby(level=0).fob_tot.sum() / fr.groupby(level=0).kg.sum()).reindex(idx),
        "q_frL1": (fr[fr.cal == "L1"].groupby(level=0).kg.sum() / 1e6).reindex(idx).fillna(0),
        "q_frC": (fr.groupby(level=0).kg.sum() / 1e6).reindex(idx).fillna(0)}, index=idx)
    A = A.join(df[["tan12", "van_eur_kg", "eurusd", "horeca", "iv_conf"]])
    A["rel"] = (A.p_ab / A.eurusd) / A.van_eur_kg
    A["prima"] = A.p_ab / A.p_fr
    A["q_frL1_12"] = A.q_frL1.rolling(12).sum()
    A["q_frC_12"] = A.q_frC.rolling(12).sum()
    A["shL1_fr"] = A.q_frL1_12 / A.q_frC_12
    B = A.dropna(subset=["rel", "tan12", "horeca", "q_frL1_12", "p_fr"]).copy()
    B = B[B.q_frL1_12 > 0]
    B["lq"] = np.log(B.tan12)
    B["lqfr"] = np.log(B.q_frC_12)
    B["lqfrL1"] = np.log(B.q_frL1_12)
    B["lpfr"] = np.log(B.p_fr)
    B["trend"] = np.arange(len(B)) / 12.0
    return A, B


def regresiones(B):
    M = pd.get_dummies(B.index.month, prefix="m", drop_first=True).astype(float)
    M.index = B.index

    def run(X, nom):
        m = sm.OLS(np.log(B.rel), sm.add_constant(pd.concat([B[X], M], axis=1))).fit(
            cov_type="HAC", cov_kwds={"maxlags": HAC})
        s = " · ".join(f"{v} {m.params[v]:+.3f} (t {m.tvalues[v]:+.2f})" for v in X)
        print(f"   {nom:<44s} N={int(m.nobs)} R2={m.rsquared:.3f}  {s}")

    print("\n   MCO sobre log del precio relativo al cultivo, Newey-West 6 rezagos:")
    run(["lq", "horeca", "trend"], "base (sólo captura tangonera)")
    run(["lq", "lqfr", "horeca", "trend"], "+ volumen fresquero exportado (12m)")
    run(["lq", "lpfr", "horeca", "trend"], "+ precio fresquero")
    run(["lq", "shL1_fr", "horeca", "trend"], "+ mezcla de tallas de la fresquera")

    from linearmodels.iv import IV2SLS
    print("\n   IV 2SLS, instrumento = ventana del conflicto:")
    for X, nom in [(["horeca", "trend"], "IV base"),
                   (["horeca", "trend", "lqfr"], "IV + volumen fresquero"),
                   (["horeca", "trend", "shL1_fr"], "IV + mezcla de la fresquera")]:
        ex = sm.add_constant(pd.concat([B[X], M], axis=1))
        r = IV2SLS(np.log(B.rel), ex, B[["lq"]], B[["iv_conf"]]).fit(
            cov_type="kernel", kernel="bartlett")
        F1 = float(r.first_stage.diagnostics["f.stat"].iloc[0])
        f, se = r.params["lq"], r.std_errors["lq"]
        print(f"   {nom:<44s} N={int(r.nobs)}  f = {f:+.3f}  se {se:.3f}  "
              f"IC95% [{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]  F1 = {F1:.1f}")


def tendencia(B):
    print("\n" + "=" * 100)
    print("3. ¿LA MEZCLA DE LA FRESQUERA EXPLICA LA TENDENCIA SIN NOMBRE?")
    print("=" * 100)
    M = pd.get_dummies(B.index.month, prefix="m", drop_first=True).astype(float)
    M.index = B.index
    print(f"   participación del L1 en el entero fresquero clasificado (12m): "
          f"{B.shL1_fr.iloc[0] * 100:.1f}% → {B.shL1_fr.iloc[-1] * 100:.1f}%  "
          f"(mín {B.shL1_fr.min() * 100:.1f}, máx {B.shL1_fr.max() * 100:.1f})")

    def run(X, nom):
        m = sm.OLS(np.log(B.rel), sm.add_constant(pd.concat([B[X], M], axis=1))).fit(
            cov_type="HAC", cov_kwds={"maxlags": HAC})
        s = " · ".join(f"{v} {m.params[v]:+.3f} (t {m.tvalues[v]:+.2f})" for v in X)
        print(f"   {nom:<44s} R2={m.rsquared:.3f}  {s}")

    run(["lq", "horeca", "trend"], "base, con tendencia")
    run(["lq", "horeca", "shL1_fr"], "mezcla EN LUGAR de la tendencia")
    run(["lq", "horeca", "lqfrL1"], "volumen L1 fresquero EN LUGAR de la tendencia")
    run(["lq", "horeca", "shL1_fr", "trend"], "las dos")
    print("   → la tendencia no se mueve: la fresquera no la explica.")


def main():
    df, tan, e = base()
    print("=" * 100)
    print("QUÉ CAMBIA CON LA FLOTA BIEN DEFINIDA — tangonera = a bordo · fresquera = el resto")
    print("=" * 100)
    print("\nComposición del despacho por flota y presentación, 2013-2026 (kt):")
    print((e.pivot_table(index="pres", columns="flota", values="kg", aggfunc="sum") / 1e6)
          .round(1).to_string())

    identidad(tan, e)
    peso_fresquera(e)
    A, B = panel_flotas(df, e)
    print("\n" + "=" * 100)
    print("2b. ¿LA FRESQUERA MUEVE EL PRECIO DEL TANGONERO?")
    print("=" * 100)
    print(f"   prima del entero tangonero sobre el fresquero: media {A.prima.mean():.3f}  ·  "
          f"2018-2026 {A.loc['2018-01':].prima.mean():.3f}")
    print(f"   correlación de log(prima) con log(volumen fresquero 12m): "
          f"{np.corrcoef(np.log(B.prima), B.lqfr)[0, 1]:+.3f}  "
          "→ productos diferenciados, no sustitutos perfectos")
    regresiones(B)
    tendencia(B)
    return A, B


if __name__ == "__main__":
    main()
