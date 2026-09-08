# -*- coding: utf-8 -*-
"""Exploración previa al modelo de demanda inversa del langostino argentino L1.

NO estima el modelo: mide el orden de magnitud de la flexibilidad-precio con el dato
tal como está y deja a la vista el problema de identificación — a frecuencia mensual la
oferta y la demanda se mueven juntas, así que la regresión ingenua da pendiente POSITIVA.

Insumos (los que ya usa pronostico.py):
  datos/aduana_langostino_total.pkl   FOB y kg mensuales por NCM (aduana oficial)
  datos/indec_entero_2013_2017.pkl    empalme INDEC 2013-01..2017-01
  _lan.pkl                            desembarques SSPyA por puerto/flota/mes

Uso:   python demanda_inversa_explora.py
Salida: consola + salidas/demanda_inversa_diagnostico.xlsx
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
pd.set_option("display.width", 160)

HAC = 6          # rezagos de Newey-West en la serie mensual
DESDE, HASTA = "2013-01", "2026-07"


# ------------------------------------------------------------------ datos
def cargar() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Devuelve (mensual, entero_crudo, desembarques_crudos)."""
    a = pd.read_pickle(os.path.join(RAIZ, "datos", "aduana_langostino_total.pkl"))
    a.index = pd.PeriodIndex(
        a.anio.astype(str) + "-" + a.mes.astype(str).str.zfill(2), freq="M")
    ent = a[a.ncm == "0306.17.10"][["kg", "fob"]]
    col = a[a.ncm == "0306.17.90"][["kg", "fob"]]

    # Empalme histórico con INDEC (el pu coincide al 4º decimal en el solape de 2017).
    pre = pd.read_pickle(os.path.join(RAIZ, "datos", "indec_entero_2013_2017.pkl"))
    ent = pd.concat([pre[pre.index < ent.index.min()], ent]).sort_index()

    lan = pd.read_pickle(os.path.join(RAIZ, "_lan.pkl"))
    lan.index = pd.PeriodIndex(
        lan.anio.astype(str) + "-" + lan.mes.astype(str).str.zfill(2), freq="M")

    df = pd.concat([
        (ent.fob / ent.kg).rename("p_ent"),
        (ent.kg / 1000).rename("q_ent_t"),
        (col.fob / col.kg).rename("p_col"),
        (col.kg / 1000).rename("q_col_t"),
        lan.groupby(level=0).t.sum().rename("desem_t"),
        lan[lan.flota == "CONG. TANGONEROS"].groupby(level=0).t.sum().rename("tan_t"),
    ], axis=1).sort_index().loc[DESDE:HASTA]
    df["desem3"] = df.desem_t.rolling(3).sum()
    df["tan3"] = df.tan_t.rolling(3).sum()
    return df, ent, lan


# ------------------------------------------------------------------ OLS
def ols(y, X, nombre, lags=HAC):
    m = sm.OLS(y, sm.add_constant(X), missing="drop").fit(
        cov_type="HAC", cov_kwds={"maxlags": lags})
    out = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues, "p": m.pvalues})
    vis = out.loc[[i for i in out.index if not i.startswith("m_")]]
    print(f"--- {nombre}   N={int(m.nobs)}  R2={m.rsquared:.3f}")
    print(vis.round(4).to_string(), "\n")
    return m, out


def main() -> None:
    df, ent, lan = cargar()

    print("=== correlaciones simples, mensual ===")
    print(df[["p_ent", "q_ent_t", "desem_t", "desem3", "p_col"]].corr().round(3), "\n")

    # ---- 1. la regresión ingenua da el signo equivocado -----------------
    d = df.dropna(subset=["p_ent", "q_ent_t"]).copy()
    d["lp"] = np.log(d.p_ent)
    d["lq"] = np.log(d.q_ent_t)
    d["ld"] = np.log(d.desem3.clip(lower=100))
    d["lt3"] = np.log(d.tan3.clip(lower=100))
    d["trend"] = np.arange(len(d)) / 12.0
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d.index

    print("=== demanda inversa ingenua (mensual) — ojo con el signo ===")
    tablas = {}
    _, tablas["A1"] = ols(d.lp, d[["lq", "trend"]],
                          "A1  log P ~ log Q exportado + tendencia")
    _, tablas["A2"] = ols(d.lp, pd.concat([d[["lq", "trend"]], M], axis=1),
                          "A2  A1 + 11 dummies de mes")
    _, tablas["B1"] = ols(d.lp, pd.concat([d[["ld", "trend"]], M], axis=1),
                          "B1  log P ~ log desembarque 3m + mes + tendencia")
    _, tablas["B2"] = ols(d.lp, pd.concat([d[["lt3", "trend"]], M], axis=1),
                          "B2  log P ~ log captura tangonera 3m + mes + tendencia")

    # ---- 2. anual: signo correcto, sin potencia -------------------------
    an = pd.DataFrame({
        "q_exp_t": ent.kg.groupby(ent.index.year).sum() / 1000,
        "fob_musd": ent.fob.groupby(ent.index.year).sum() / 1e6,
        "desem_t": lan.t.groupby(lan.index.year).sum(),
    }).loc[2013:2025]                      # 2026 incompleto: no entra
    an["p_usd_kg"] = an.fob_musd * 1e6 / (an.q_exp_t * 1000)
    an["lp"], an["lq"], an["ld"] = np.log(an.p_usd_kg), np.log(an.q_exp_t), np.log(an.desem_t)
    an["trend"] = an.index - 2013
    # flexibilidad de arco año contra año
    an["flex_expo"] = an.lp.diff() / an.lq.diff()
    an["flex_desem"] = an.lp.diff() / an.ld.diff()

    print("=== serie anual 2013-2025 ===")
    print(an[["q_exp_t", "desem_t", "p_usd_kg", "fob_musd",
              "flex_expo", "flex_desem"]].round(2).to_string(), "\n")
    print(f"flexibilidad de arco, mediana: sobre exportación {an.flex_expo.median():.2f} · "
          f"sobre desembarque {an.flex_desem.median():.2f}   "
          "(positivas = sin sentido económico)\n")

    _, tablas["C1"] = ols(an.lp, an[["lq", "trend"]],
                          "C1  ANUAL  log P ~ log Q exportado + tendencia", lags=2)
    _, tablas["C2"] = ols(an.lp, an[["ld", "trend"]],
                          "C2  ANUAL  log P ~ log desembarques + tendencia", lags=2)
    _, tablas["C3"] = ols(an.lp, an[["ld"]],
                          "C3  ANUAL  log P ~ log desembarques", lags=2)

    # ---- 3. el conflicto gremial de 2025 como shock de oferta -----------
    print("=== 2025: el único episodio con variación de oferta plausiblemente exógena ===")
    ev = an.loc[2024:2025, ["desem_t", "q_exp_t", "p_usd_kg", "fob_musd"]]
    print(ev.round(1).to_string())
    print("variación %:", ((ev.loc[2025] / ev.loc[2024] - 1) * 100).round(1).to_dict())
    fx_e = (np.log(ev.p_usd_kg[2025] / ev.p_usd_kg[2024])
            / np.log(ev.q_exp_t[2025] / ev.q_exp_t[2024]))
    fx_d = (np.log(ev.p_usd_kg[2025] / ev.p_usd_kg[2024])
            / np.log(ev.desem_t[2025] / ev.desem_t[2024]))
    print(f"flexibilidad de arco 2024→2025:  sobre exportación {fx_e:.2f} · "
          f"sobre desembarque {fx_d:.2f}   (umbral de política: -1)")
    print("Ingreso FOB del entero: cayó US$ "
          f"{ev.fob_musd[2024] - ev.fob_musd[2025]:.0f} M pese al precio más alto.\n")
    print("ADVERTENCIA: en 2026 el precio siguió subiendo CON el volumen recuperándose, "
          "así que el episodio no separa el recorte argentino del ciclo mundial. "
          "Sin control de precio mundial (vannamei / NOAA import price) no es evidencia.\n")

    print(df.loc["2024-01":, ["p_ent", "q_ent_t", "desem_t"]].round(2).to_string())

    # ---- salida ---------------------------------------------------------
    out = os.path.join(RAIZ, "salidas", "demanda_inversa_diagnostico.xlsx")
    try:
        with pd.ExcelWriter(out) as w:
            df.to_excel(w, sheet_name="mensual")
            an.to_excel(w, sheet_name="anual")
            pd.concat(tablas, names=["modelo"]).to_excel(w, sheet_name="regresiones")
        print(f"\nGuardado: {out}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {out} (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
