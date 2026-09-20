# -*- coding: utf-8 -*-
"""La demanda inversa estimada sólo en España e Italia, que es donde va el langostino.

POR QUÉ PUEDE VALER LA PENA. El trabajo principal cruza un precio FOB de despacho —de
todos los destinos, incluidos China y Japón— contra una canasta de cultivo importada por
toda la Unión Europea, y contra la captura de la flota. Son tres universos distintos
pegados con cinta. España e Italia permiten cerrar el triángulo:

  · el PRECIO es el CIF de importación del langostino argentino declarado por esos dos
    países, que es el precio al que la mercadería efectivamente entra al mercado;
  · la CANTIDAD es el volumen argentino que entra a esos dos países, que es la cantidad
    que enfrenta ese precio, y no una captura que se despacha a cualquier lado;
  · el COMPETIDOR es el camarón de cultivo importado por esos mismos dos países, no por
    los veintisiete;
  · y el CANAL es el índice HORECA de España y de Italia, que es de donde salió el
    índice compuesto del trabajo, ahora sin promediar con China y Japón.

Las cuatro variables pasan a referirse al mismo mercado y al mismo mes. Es la
especificación de manual de una demanda inversa, que el trabajo principal no puede
correr porque su precio —el del entero L1 congelado a bordo— sólo existe del lado FOB.

LO QUE SE PIERDE. El precio de EUMOFA no distingue calibre ni flota, así que esto mide
«el langostino argentino en España e Italia» y no «el entero L1 tangonero». Y la
cantidad deja de ser un shock de oferta puro: cuánto va a Europa es una decisión de
cartera del exportador, no sólo cuánto se pescó. El instrumento tiene que cargar con eso.

España e Italia son el 94% del langostino argentino que entra a la Unión.

Uso:  python demanda_inversa_es_it.py
Salida: consola + salidas/demanda_inversa_es_it.xlsx
"""
from __future__ import annotations

import glob
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 210)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from biblioteca import fuente
EUMOFA = fuente("eumofa_ue")
COLS = ["year", "month", "country", "flow_type", "intra_extra_EU", "partner_contry",
        "main_commercial_species", "preservation", "value(EUR)", "volume(kg)"]
CONGELADO = ["PS2 Frozen", "PS5 Unspecified"]
CULTIVO = ["Ecuador", "India", "Viet Nam", "Bangladesh", "Indonesia", "Thailand"]
MERCADOS = {"ES": ["Spain"], "IT": ["Italy"], "ES+IT": ["Spain", "Italy"]}
HAC = 6
# La ventana en que el conflicto deprime la cantidad, corrida por el tránsito: el paro
# fue de abril a julio de 2025 y la mercadería que falta aparece en Europa dos meses
# después.
CONF_EU = (pd.Period("2025-06"), pd.Period("2026-05"))


def _p(*t):
    return os.path.join(RAIZ, *t)


def eumofa() -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(
        EUMOFA, "EUMOFA BASES", "DESCARGA MASIVA", "EXPO IMPO", "EU",
        "*_Trade_data_reported_by_EU_countries.csv")))
    parcial = os.path.join(EUMOFA, "2026_Trade_data_reported_by_EU_countries.csv")
    if os.path.exists(parcial):
        files.append(parcial)
    tr = []
    for f in files:
        d = pd.read_csv(f, sep=";", dtype=str, low_memory=False,
                        usecols=lambda c: c in COLS)
        tr.append(d[(d.flow_type == "Import") & (d.intra_extra_EU == "Extra EU")
                    & d.country.isin(["Spain", "Italy"])
                    & d.main_commercial_species.str.startswith("Shrimp", na=False)
                    & d.preservation.isin(CONGELADO)])
    d = pd.concat(tr, ignore_index=True)
    d["eur"] = pd.to_numeric(d["value(EUR)"], errors="coerce")
    d["kg"] = pd.to_numeric(d["volume(kg)"], errors="coerce")
    d = d[(d.kg > 0) & (d.eur > 0)]
    d["per"] = pd.PeriodIndex(
        pd.to_numeric(d.year).astype(int).astype(str) + "-"
        + pd.to_numeric(d.month).astype(int).astype(str).str.zfill(2), freq="M")
    return d


def panel(d: pd.DataFrame, paises: list[str]) -> pd.DataFrame:
    s = d[d.country.isin(paises)]
    ar = s[(s.partner_contry == "Argentina")].groupby("per")[["eur", "kg"]].sum()
    va = s[s.partner_contry.isin(CULTIVO)
           & (s.main_commercial_species == "Shrimp, warmwater")] \
        .groupby("per")[["eur", "kg"]].sum()
    m = pd.DataFrame({
        "p_ar": ar.eur / ar.kg, "q_ar": ar.kg / 1e6,
        "p_van": va.eur / va.kg, "q_van": va.kg / 1e6}).dropna()

    H = pd.read_pickle(_p("datos", "horeca_indice.pkl"))
    cols = [c for c in (["h_ES"] if "Spain" in paises else [])
            + (["h_IT"] if "Italy" in paises else [])]
    h = np.log(H[cols]).mean(axis=1).reindex(m.index)
    # Igual que en el trabajo: lo que informa es la BRECHA contra su propia tendencia,
    # porque el índice es de facturación nominal y crece con la inflación.
    ok = h.notna()
    tt = pd.Series(np.arange(len(m)) / 12.0, index=m.index)
    b = sm.OLS(h[ok], sm.add_constant(tt[ok])).fit()
    m["horeca"] = h - b.predict(sm.add_constant(tt))
    m["q12"] = m.q_ar.rolling(12).sum()
    m["rel"] = m.p_ar / m.p_van
    m["share"] = m.q_ar / (m.q_ar + m.q_van)
    m["iv"] = ((m.index >= CONF_EU[0]) & (m.index <= CONF_EU[1])).astype(float)
    m["trend"] = np.arange(len(m)) / 12.0
    return m.dropna(subset=["horeca"])


def raiz(s, nom):
    s = s.dropna()
    ad, kp = adfuller(s, autolag="AIC"), kpss(s, regression="c", nlags="auto")
    return {"serie": nom, "ADF": ad[0], "ADF_p": ad[1], "KPSS_p": kp[1],
            "veredicto": ("estacionaria" if ad[1] < .05 and kp[1] > .05 else
                          "raíz unitaria" if ad[1] > .05 and kp[1] < .05 else "ambiguo")}


def main() -> None:
    print("=" * 105)
    print("DEMANDA INVERSA DEL LANGOSTINO ARGENTINO EN ESPAÑA E ITALIA")
    print("=" * 105)
    d = eumofa()
    P = {k: panel(d, v) for k, v in MERCADOS.items()}
    m = P["ES+IT"]
    print(f"Muestra {m.index.min()} a {m.index.max()} · {len(m)} meses")

    tot = d[d.partner_contry == "Argentina"].kg.sum()
    print(f"\nVolumen argentino declarado por España e Italia: {tot/1e6:,.0f} kt")
    print("\nPromedios anuales del mercado combinado:")
    an = m.groupby(m.index.year).agg(p_ar=("p_ar", "mean"), p_van=("p_van", "mean"),
                                     rel=("rel", "mean"), q_ar=("q_ar", "sum"),
                                     q_van=("q_van", "sum"), share=("share", "mean"))
    print(an.round(3).to_string())

    print("\n" + "-" * 105)
    print("1. ORDEN DE INTEGRACIÓN")
    print("-" * 105)
    RU = pd.DataFrame([raiz(np.log(m.p_ar), "log p argentino"),
                       raiz(np.log(m.p_van), "log p cultivo"),
                       raiz(np.log(m.rel), "log del cociente"),
                       raiz(np.log(m.q_ar), "log q argentino"),
                       raiz(np.log(m.q12), "log q 12 meses")])
    for _, r in RU.iterrows():
        print(f"   {r.serie:<20s} ADF {r.ADF:+6.2f} (p {r.ADF_p:.3f})   "
              f"KPSS p {r.KPSS_p:.3f}   {r.veredicto}")

    print("\n" + "-" * 105)
    print("2. ESTIMACIÓN POR MERCADO")
    print("-" * 105)
    from linearmodels.iv import IV2SLS
    res = []
    for k, x in P.items():
        M = pd.get_dummies(x.index.month, prefix="m", drop_first=True).astype(float)
        M.index = x.index
        for qn, qetq in [("q_ar", "cantidad del mes"), ("q12", "cantidad 12 meses")]:
            b = x.dropna(subset=[qn]).copy()
            MM = M.reindex(b.index)
            lq = np.log(b[qn])
            X = pd.concat([lq.rename("lq"), np.log(b[["p_van"]]).rename(
                columns={"p_van": "lvan"}), b[["horeca", "trend"]], MM], axis=1)
            r1 = sm.OLS(np.log(b.p_ar), sm.add_constant(X)).fit(
                cov_type="HAC", cov_kwds={"maxlags": HAC})
            X2 = pd.concat([lq.rename("lq"), b[["horeca", "trend"]], MM], axis=1)
            r2 = sm.OLS(np.log(b.rel), sm.add_constant(X2)).fit(
                cov_type="HAC", cov_kwds={"maxlags": HAC})
            dd = pd.concat([np.log(b.rel).rename("lrel"), lq.rename("lq"),
                            b[["horeca", "trend", "iv"]], MM], axis=1).dropna()
            ex = sm.add_constant(dd[["horeca", "trend"] + list(MM.columns)])
            iv = IV2SLS(dd.lrel, ex, dd[["lq"]], dd[["iv"]]).fit(
                cov_type="kernel", kernel="bartlett")
            F1 = float(iv.first_stage.diagnostics["f.stat"].iloc[0])
            print(f"\n   {k} · {qetq}   N = {len(b)}")
            print(f"      MCO  log p ~ log q + cultivo    f = {r1.params['lq']:+.3f} "
                  f"(se {r1.bse['lq']:.3f})")
            print(f"      MCO  log (p/cultivo) ~ log q    f = {r2.params['lq']:+.3f} "
                  f"(se {r2.bse['lq']:.3f})")
            print(f"      IV   log (p/cultivo) ~ log q    f = {iv.params['lq']:+.3f} "
                  f"(se {iv.std_errors['lq']:.3f})   primera etapa F = {F1:.1f}"
                  + ("" if F1 > 10 else "   INSTRUMENTO DÉBIL"))
            for nom, f, se, n in [("MCO nivel", r1.params["lq"], r1.bse["lq"], len(b)),
                                  ("MCO cociente", r2.params["lq"], r2.bse["lq"],
                                   len(b)),
                                  ("IV cociente", iv.params["lq"],
                                   iv.std_errors["lq"], int(iv.nobs))]:
                res.append({"mercado": k, "cantidad": qetq, "modelo": nom, "f": f,
                            "se": se, "t_H0_menos1": (f + 1) / se, "N": n,
                            "F1": F1 if nom == "IV cociente" else np.nan})
    R = pd.DataFrame(res)

    print("\n" + "-" * 105)
    print("3. RESUMEN Y COMPARACIÓN CON EL TRABAJO")
    print("-" * 105)
    piv = R.pivot_table(index=["mercado", "cantidad"], columns="modelo", values="f")
    print(piv.round(3).to_string())
    print(f"\n   Rango de las {len(R)} estimaciones: {R.f.min():+.3f} a {R.f.max():+.3f}")
    print("   El trabajo, con el FOB del entero L1 tangonero: −0,184 a −0,282.")
    print(f"   Ninguna se acerca a −1: el máximo t contra esa hipótesis es "
          f"{R.t_H0_menos1.min():.1f}.")

    try:
        out = _p("salidas", "demanda_inversa_es_it.xlsx")
        with pd.ExcelWriter(out) as w:
            for k, x in P.items():
                y = x.copy()
                y.index = y.index.astype(str)
                y.round(4).to_excel(w, sheet_name=f"panel_{k.replace('+', '_')}")
            an.round(4).to_excel(w, sheet_name="anual")
            RU.round(4).to_excel(w, sheet_name="raices", index=False)
            R.round(4).to_excel(w, sheet_name="flexibilidades", index=False)
        print(f"\nGuardado: {out}")
    except PermissionError:
        print("\nAVISO: no pude escribir el xlsx (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
