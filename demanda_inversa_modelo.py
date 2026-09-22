# -*- coding: utf-8 -*-
"""Demanda inversa del langostino argentino entero L1.

Estima la flexibilidad-precio  f = dlogP/dlogQ  y contrasta H0: f = -1, que es el
umbral en el que regular la oferta deja de destruir ingreso:

    ingreso = P(Q)·Q   →   d(P·Q)/dQ = P·(1+f)
    |f| > 1  → recortar oferta SUBE el ingreso
    |f| < 1  → recortar oferta LO BAJA

Regla de fuente de la casa: el PRECIO sale del dato transaccional (Softrade, entero L1)
y la CANTIDAD del registro oficial (desembarques SSPyA). Nunca al revés.

Control imprescindible: el precio del camarón de cultivo en la UE (EUMOFA, warmwater
congelado extra-UE). Sin él, el shock de oferta de 2025 no se distingue del ciclo
mundial ni de la depreciación del dólar.

Insumos:
  datos/aduana_langostino_total.pkl     FOB y kg del entero y la cola (aduana oficial)
  datos/indec_entero_2013_2017.pkl      empalme INDEC 2013-01..2017-01
  datos/eumofa_camaron_ue.pkl           serie UE (la regenera demanda_inversa_eumofa.py)
  _lan.pkl                              desembarques SSPyA por puerto/flota/mes
  planillas Softrade vía fuentes/expo.py

Uso:  python demanda_inversa_modelo.py
Salida: consola + salidas/demanda_inversa_L1.xlsx + salidas/demanda_inversa_L1.svg
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

import flexibilidades_iaids as fx
import recorte_conxemar
from statsmodels.tsa.stattools import adfuller, kpss

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
pd.set_option("display.width", 170)

HAC = 6                       # rezagos de Newey-West, serie mensual
DESDE, HASTA = "2013-01", "2026-07"
PARO = (pd.Period("2025-04"), pd.Period("2025-11"))   # conflicto gremial y rebote

# EUR/USD promedio mensual (Wolfram FinancialData). Congelado: el modelo tiene que
# reproducirse igual el año que viene.
FX = (
    "2013-01=1.3569;2013-02=1.3136;2013-03=1.2817;2013-04=1.3095;2013-05=1.3042;2013-06=1.3013;"
    "2013-07=1.3267;2013-08=1.3215;2013-09=1.3495;2013-10=1.3723;2013-11=1.3590;2013-12=1.3806;"
    "2014-01=1.3557;2014-02=1.3707;2014-03=1.3753;2014-04=1.3813;2014-05=1.3636;2014-06=1.3643;"
    "2014-07=1.3395;2014-08=1.3128;2014-09=1.2690;2014-10=1.2609;2014-11=1.2444;2014-12=1.2162;"
    "2015-01=1.1288;2015-02=1.1194;2015-03=1.0828;2015-04=1.1112;2015-05=1.0985;2015-06=1.1219;"
    "2015-07=1.0941;2015-08=1.1211;2015-09=1.1254;2015-10=1.1005;2015-11=1.0583;2015-12=1.0935;"
    "2016-01=1.0831;2016-02=1.0924;2016-03=1.1333;2016-04=1.1451;2016-05=1.1148;2016-06=1.1122;"
    "2016-07=1.1174;2016-08=1.1150;2016-09=1.1219;2016-10=1.0982;2016-11=1.0647;2016-12=1.0517;"
    "2017-01=1.0708;2017-02=1.0586;2017-03=1.0688;2017-04=1.0896;2017-05=1.1173;2017-06=1.1439;"
    "2017-07=1.1747;2017-08=1.1891;2017-09=1.1815;2017-10=1.1651;2017-11=1.1852;2017-12=1.2003;"
    "2018-01=1.2411;2018-02=1.2226;2018-03=1.2323;2018-04=1.2123;2018-05=1.1665;2018-06=1.1682;"
    "2018-07=1.1708;2018-08=1.1666;2018-09=1.1604;2018-10=1.1346;2018-11=1.1393;2018-12=1.1439;"
    "2019-01=1.1486;2019-02=1.1380;2019-03=1.1218;2019-04=1.1185;2019-05=1.1130;2019-06=1.1389;"
    "2019-07=1.1157;2019-08=1.1062;2019-09=1.0943;2019-10=1.1154;2019-11=1.1012;2019-12=1.1202;"
    "2020-01=1.1029;2020-02=1.0997;2020-03=1.1030;2020-04=1.0877;2020-05=1.1079;2020-06=1.1247;"
    "2020-07=1.1872;2020-08=1.1918;2020-09=1.1742;2020-10=1.1679;2020-11=1.1971;2020-12=1.2300;"
    "2021-01=1.2120;2021-02=1.2160;2021-03=1.1724;2021-04=1.2127;2021-05=1.2190;2021-06=1.1902;"
    "2021-07=1.1893;2021-08=1.1797;2021-09=1.1602;2021-10=1.1684;2021-11=1.1293;2021-12=1.1325;"
    "2022-01=1.1152;2022-02=1.1181;2022-03=1.1101;2022-04=1.0540;2022-05=1.0713;2022-06=1.0387;"
    "2022-07=1.0198;2022-08=1.0000;2022-09=0.9748;2022-10=0.9914;2022-11=1.0376;2022-12=1.0666;"
    "2023-01=1.0833;2023-02=1.0619;2023-03=1.0875;2023-04=1.0981;2023-05=1.0683;2023-06=1.0866;"
    "2023-07=1.1023;2023-08=1.0868;2023-09=1.0594;2023-10=1.0619;2023-11=1.0931;2023-12=1.1050;"
    "2024-01=1.0837;2024-02=1.0826;2024-03=1.0811;2024-04=1.0718;2024-05=1.0852;2024-06=1.0705;"
    "2024-07=1.0828;2024-08=1.1087;2024-09=1.1196;2024-10=1.0882;2024-11=1.0562;2024-12=1.0389;"
    "2025-01=1.0393;2025-02=1.0411;2025-03=1.0815;2025-04=1.1373;2025-05=1.1339;2025-06=1.1720;"
    "2025-07=1.1446;2025-08=1.1658;2025-09=1.1741;2025-10=1.1554;2025-11=1.1566;2025-12=1.1750;"
    "2026-01=1.1919;2026-02=1.1805;2026-03=1.1498;2026-04=1.1702;2026-05=1.1644;2026-06=1.1394;"
    "2026-07=1.1485;2026-08=1.1699"
)


# ------------------------------------------------------------------ panel
def _p(*t):
    return os.path.join(RAIZ, *t)


def panel() -> pd.DataFrame:
    a = pd.read_pickle(_p("datos", "aduana_langostino_total.pkl"))
    a.index = pd.PeriodIndex(a.anio.astype(str) + "-" + a.mes.astype(str).str.zfill(2), freq="M")
    ent = a[a.ncm == "0306.17.10"][["kg", "fob"]]
    pre = pd.read_pickle(_p("datos", "indec_entero_2013_2017.pkl"))
    ent = pd.concat([pre[pre.index < ent.index.min()], ent]).sort_index()

    lan = pd.read_pickle(_p("_lan.pkl"))
    lan.index = pd.PeriodIndex(lan.anio.astype(str) + "-" + lan.mes.astype(str).str.zfill(2), freq="M")

    ue = pd.read_pickle(_p("datos", "eumofa_camaron_ue.pkl"))

    fx = pd.Series({k: float(v) for k, v in (x.split("=") for x in FX.split(";"))})
    fx.index = pd.PeriodIndex(fx.index, freq="M")

    # --- precio del L1: dato transaccional Softrade -----------------------
    from fuentes import expo
    d = expo.cargar_todos()
    l1 = d[(d.pres == "entero") & (d.cal == "L1") & (d.kg > 0) & (d.fob_tot > 0)].copy()
    l1.index = pd.PeriodIndex(l1.anio.astype(str) + "-" + l1.mes.astype(str).str.zfill(2), freq="M")
    g = l1.groupby(level=0).agg(fob=("fob_tot", "sum"), kg=("kg", "sum")).sort_index()
    p_l1 = (g.fob / g.kg).rename("p_l1")
    # 10 meses sin ninguna fila con grado declarado (ene-jun 2016, jun-sep 2017):
    # se interpolan en log para no romper los rezagos y se EXCLUYEN de la estimación.
    comp = pd.period_range(p_l1.index.min(), p_l1.index.max(), freq="M")
    interp = comp.difference(p_l1.index)
    p_l1 = np.exp(np.log(p_l1.reindex(comp)).interpolate())

    df = pd.concat([
        p_l1,
        (ent.fob / ent.kg).rename("p_ent_usd"),
        (ent.kg / 1000).rename("q_exp_t"),
        lan.groupby(level=0).t.sum().rename("desem_t"),
        lan[lan.flota == "CONG. TANGONEROS"].groupby(level=0).t.sum().rename("tan_t"),
        ue, fx.rename("eurusd"),
    ], axis=1).sort_index().loc[DESDE:HASTA]

    df["interp"] = df.index.isin(interp)
    df["desem3"] = df.desem_t.rolling(3).sum()
    df["desem12"] = df.desem_t.rolling(12).sum()
    # Los ceros de la tangonera durante el paro son reales, pero log(0) no existe:
    # mismo piso de 500 t que usa pronostico.py, para que las dos rutinas hablen igual.
    df["tan3"] = df.tan_t.rolling(3).sum().clip(lower=500.0)
    df["p_l1_eur"] = df.p_l1 / df.eurusd
    df["rel"] = df.p_l1_eur / df.van_eur_kg          # precio relativo al cultivo
    df["paro"] = ((df.index >= PARO[0]) & (df.index <= PARO[1])).astype(float)
    return df


# ------------------------------------------------------------------ utilería
def ols(y, X, nombre, mostrar, lags=HAC):
    m = sm.OLS(y, sm.add_constant(X), missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    t = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues, "p": m.pvalues})
    print(f"\n--- {nombre}   N={int(m.nobs)}  R2={m.rsquared:.3f}")
    print(t.loc[mostrar].round(4).to_string())
    return m, t


def flexibilidad(m, var, etiqueta=""):
    f, se = m.params[var], m.bse[var]
    lo, hi = f - 1.96 * se, f + 1.96 * se
    t1 = (f + 1) / se
    print(f"    f = {f:+.3f}   IC95% [{lo:+.3f}, {hi:+.3f}]   "
          f"H0: f = -1 → t = {t1:+.1f} ({'no se rechaza' if abs(t1) < 1.96 else 'SE RECHAZA'})   "
          f"elasticidad de ingreso 1+f = {1 + f:+.3f}")
    return {"modelo": etiqueta or var, "f": f, "se": se, "ic_inf": lo, "ic_sup": hi,
            "t_H0_f_igual_-1": t1, "ingreso_1mas_f": 1 + f}


# ------------------------------------------------------------------ main
def main() -> None:
    df = panel()
    d = df.dropna(subset=["p_l1", "van_eur_kg", "desem3"]).copy()
    for c, n in [("p_l1", "lp_usd"), ("p_l1_eur", "lp"), ("van_eur_kg", "lvan"),
                 ("van_ec_eur_kg", "lvan_ec"), ("desem3", "ldes3"), ("desem12", "ldes12"),
                 ("tan3", "ltan3"), ("eurusd", "lfx"), ("rel", "lrel"),
                 ("ar_kt", "lque"), ("q_exp_t", "lqexp")]:
        d[n] = np.log(d[c].clip(lower=1e-6))
    d["trend"] = np.arange(len(d)) / 12.0
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d.index
    s = d[~d.interp.astype(bool)]          # los meses reconstruidos no son evidencia
    Ms = M.loc[s.index]

    print("=" * 92)
    print("DEMANDA INVERSA DEL ENTERO L1 — precio Softrade, cantidad SSPyA, control EUMOFA")
    print("=" * 92)
    print(f"Muestra: {s.index.min()} a {s.index.max()}, N = {len(s)} "
          f"({int(d.interp.sum())} meses interpolados, excluidos)")

    print("\n--- Raíces unitarias (ADF: H0 = raíz unitaria · KPSS: H0 = estacionariedad)")
    ru = []
    for n in ["lp_usd", "lp", "lvan", "lrel", "ldes3"]:
        x = d[n].dropna()
        ad = adfuller(x, regression="c", autolag="AIC")
        kp = kpss(x, regression="c", nlags="auto")
        ver = "I(0)" if ad[1] < .05 and kp[1] > .05 else ("I(1)" if ad[1] >= .05 and kp[1] <= .05 else "ambiguo")
        ru.append({"serie": n, "ADF_p": ad[1], "KPSS_p": kp[1], "veredicto": ver})
    ru = pd.DataFrame(ru)
    print(ru.round(3).to_string(index=False))

    res, tablas = [], {}

    print("\n" + "=" * 92)
    print("1. ESPECIFICACIONES PRINCIPALES")
    print("=" * 92)
    m, tablas["M1"] = ols(s.lp_usd, pd.concat([s[["ldes3", "trend"]], Ms], axis=1),
                          "M1  log P_L1 (US$) ~ log desem3 + mes + tendencia   [sin control mundial]",
                          ["ldes3", "trend"])
    res.append(flexibilidad(m, "ldes3", "M1 sin control mundial"))

    m, tablas["M2"] = ols(s.lp_usd, pd.concat([s[["ldes3", "lvan", "lfx", "trend"]], Ms], axis=1),
                          "M2  + precio del cultivo en la UE + tipo de cambio",
                          ["ldes3", "lvan", "lfx", "trend"])
    res.append(flexibilidad(m, "ldes3", "M2 con control mundial y TC"))

    m, tablas["M3"] = ols(s.lp, pd.concat([s[["ldes3", "lvan", "trend"]], Ms], axis=1),
                          "M3  log P_L1 (EUR) ~ log desem3 + log cultivo + mes + tendencia",
                          ["ldes3", "lvan", "trend"])
    res.append(flexibilidad(m, "ldes3", "M3 en euros"))

    m, tablas["M4"] = ols(s.lrel, pd.concat([s[["ldes3", "trend"]], Ms], axis=1),
                          "M4  log (P_L1 / cultivo) ~ log desem3 + mes + tendencia   [demanda residual]",
                          ["ldes3", "trend"])
    res.append(flexibilidad(m, "ldes3", "M4 demanda residual"))

    print("\n" + "=" * 92)
    print("2. ROBUSTEZ")
    print("=" * 92)
    m, tablas["R1"] = ols(s.lp, pd.concat([s[["ldes12", "lvan", "trend"]], Ms], axis=1),
                          "R1  Q = desembarque acumulado 12 meses (neutraliza el stock de congelado)",
                          ["ldes12", "lvan", "trend"])
    res.append(flexibilidad(m, "ldes12", "R1 oferta 12 meses"))

    m, tablas["R2"] = ols(s.lp, pd.concat([s[["ltan3", "lvan", "trend"]], Ms], axis=1),
                          "R2  Q = captura tangonera 3 meses (la flota que hace el L1)",
                          ["ltan3", "lvan", "trend"])
    res.append(flexibilidad(m, "ltan3", "R2 sólo tangonera"))

    for L in (1, 2, 3, 6):
        s = s.assign(**{f"ld_l{L}": d.ldes3.shift(L).reindex(s.index)})
    cols = ["ldes3", "ld_l1", "ld_l2", "ld_l3", "ld_l6"]
    m, tablas["R3"] = ols(s.lp, pd.concat([s[cols + ["lvan", "trend"]], Ms], axis=1),
                          "R3  rezagos distribuidos del desembarque (0,1,2,3,6 meses)",
                          cols + ["lvan"])
    lp = m.params[cols].sum()
    print(f"    efecto de largo plazo (suma de coeficientes) = {lp:+.3f}")
    res.append({"modelo": "R3 largo plazo (suma de rezagos)", "f": lp, "se": np.nan,
                "ic_inf": np.nan, "ic_sup": np.nan, "t_H0_f_igual_-1": np.nan, "ingreso_1mas_f": 1 + lp})

    q25 = s.desem3.quantile(.25)
    s = s.assign(bajo=(s.desem3 < q25).astype(float))
    s = s.assign(ldes3_bajo=s.ldes3 * s.bajo)
    m, tablas["R4"] = ols(s.lp, pd.concat([s[["ldes3", "ldes3_bajo", "bajo", "lvan", "trend"]], Ms], axis=1),
                          "R4  ¿el efecto aparece sólo con recortes grandes? (cuartil inferior de oferta)",
                          ["ldes3", "ldes3_bajo", "bajo", "lvan"])
    print(f"    f en régimen de oferta baja = {m.params['ldes3'] + m.params['ldes3_bajo']:+.3f}")

    m, tablas["R5"] = ols(s.lp, pd.concat([s[["paro", "lvan", "trend"]], Ms], axis=1),
                          "R5  dummy del conflicto gremial (abr-nov 2025) en lugar de la cantidad",
                          ["paro", "lvan", "trend"])
    print("    el coeficiente de 'paro' es el efecto del mayor shock de oferta de la serie, "
          "una vez descontado el ciclo mundial.")

    dd = pd.DataFrame({"dlp": s.lp.diff(), "dldes3": s.ldes3.diff(), "dlvan": s.lvan.diff()}).dropna()
    m, tablas["R6"] = ols(dd.dlp, pd.concat([dd[["dldes3", "dlvan"]], M.reindex(dd.index)], axis=1),
                          "R6  en primeras diferencias", ["dldes3", "dlvan"])
    res.append(flexibilidad(m, "dldes3", "R6 primeras diferencias"))

    print("\n" + "=" * 92)
    print("3. ANUAL (2013-2025; 2026 incompleto queda afuera)")
    print("=" * 92)
    an = d.groupby(d.index.year).agg(p_l1=("p_l1", "mean"), p_eur=("p_l1_eur", "mean"),
                                     van=("van_eur_kg", "mean"), des=("desem_t", "sum"),
                                     qexp=("q_exp_t", "sum"), que=("ar_kt", "sum")).loc[2013:2025]
    an["lp"], an["lvan"], an["ldes"] = np.log(an.p_eur), np.log(an.van), np.log(an.des)
    an["trend"] = an.index - 2013
    print(an[["p_l1", "p_eur", "van", "des", "que"]].round(2).to_string())

    m, tablas["A1"] = ols(an.lp, an[["ldes", "lvan", "trend"]],
                          "A1  ANUAL  log P_L1 (EUR) ~ log desembarque + cultivo + tendencia",
                          ["ldes", "lvan", "trend"], lags=2)
    res.append(flexibilidad(m, "ldes", "A1 anual"))
    m, tablas["A2"] = ols(np.log(an.p_eur / an.van), an[["ldes", "trend"]],
                          "A2  ANUAL  log (P_L1 / cultivo) ~ log desembarque + tendencia",
                          ["ldes", "trend"], lags=2)
    res.append(flexibilidad(m, "ldes", "A2 anual, demanda residual"))

    R = pd.DataFrame(res).set_index("modelo")
    print("\n" + "=" * 92)
    print("RESUMEN DE FLEXIBILIDADES")
    print("=" * 92)
    print(R.round(3).to_string())
    peor = R.ic_inf.min()
    print(f"\nCota inferior más favorable de todo el conjunto (IC 95%): f = {peor:.3f}")
    print(f"→ un recorte de oferta del 10% subiría el precio, como MÁXIMO, {abs(peor) * 10:.1f}% "
          f"y bajaría el ingreso al menos {(1 + peor) * 10:.1f}%.")

    # ------------------------------------------------------ sistema de demanda inversa
    F, esc, w, se_ar = sistema()
    f_sis = F.loc["AR", "AR"]

    # ------------------------------------------------------ simulación de política
    print("\n" + "=" * 92)
    print("5. SIMULACIÓN: las medidas propuestas en Conxemar 2025")
    print("=" * 92)
    rec = recorte_conxemar.recorte()
    base = recorte_conxemar.base_exportadora()
    print(recorte_conxemar.describir(rec))
    print()
    print(recorte_conxemar.describir_base(base))
    print()
    # El ÁMBITO de cada f no es decorativo: dice sobre qué parte del valor exportado
    # rige. Las de la ecuación única salen del FOB argentino a todos los destinos; las
    # del sistema por origen, del precio de importación europeo, que no gobierna lo que
    # Argentina le vende a Estados Unidos ni a Asia.
    u_tot = recorte_conxemar.umbral(rec, base, "total")
    u_ue = recorte_conxemar.umbral(rec, base, "ue")
    sim = recorte_conxemar.tabla([
        ("ecuación única, anual (A2)", R.loc["A2 anual, demanda residual", "f"], "total"),
        ("sistema de demanda inversa (central)", f_sis, "ue"),
        ("sistema, cota más favorable del IC 95%", f_sis - 1.96 * se_ar, "ue"),
        ("si TODOS los orígenes recortaran a la vez (escala)", esc["AR"], "ue"),
        ("el f que haría falta para no perder plata — ámbito total", u_tot, "total"),
        ("el f que haría falta para no perder plata — ámbito UE", u_ue, "ue"),
    ], rec, base)
    print(sim.round(2).to_string())
    print(f"\nSobre US$ {base['v_total']:,.0f} M de exportación de langostino "
          f"({base['anio']}), el escenario del sistema implica "
          f"{sim.loc['sistema de demanda inversa (central)', 'Δ ingreso US$ M']:,.0f} "
          "millones de dólares de facturación.")
    print(f"El umbral de facturación es {u_tot:+.2f} para una f de alcance argentino, pero "
          f"{u_ue:+.2f} para una f europea:")
    print("el precio sube sólo donde rige la f y el resto del embarque pierde volumen sin")
    print("compensación, así que «alcanza con |f| > 1» es una vara demasiado baja para el")
    print("sistema por origen, no demasiado alta.")

    # ------------------------------------------------------ salidas
    try:
        out = _p("salidas", "demanda_inversa_L1.xlsx")
        with pd.ExcelWriter(out) as w:
            df.to_excel(w, sheet_name="panel_mensual")
            an.to_excel(w, sheet_name="anual")
            ru.to_excel(w, sheet_name="raices_unitarias", index=False)
            R.to_excel(w, sheet_name="flexibilidades")
            F.to_excel(w, sheet_name="sistema_flexibilidades")
            esc.to_frame().to_excel(w, sheet_name="sistema_escala")
            sim.to_excel(w, sheet_name="simulacion")
            pd.concat(tablas, names=["modelo"]).to_excel(w, sheet_name="regresiones")
        print(f"\nGuardado: {out}")
    except PermissionError:
        print("\nAVISO: no pude escribir el xlsx (¿abierto en Excel?).")

    grafico(d)


ORIGENES = ["AR", "EC", "IN", "VN", "RE"]


def sistema():
    """Sistema de demanda inversa (LA/IAIDS) sobre la importación extra-UE de camarón
    tropical congelado, por origen, mensual.

        w_i = a_i + Σ_j g_ij·log q_j + b_i·log Q,   log Q = Σ_k w̄_k·log q_k (Stone)

    Homogeneidad impuesta por normalización (se usa log q_j − log q_RE) y adición por
    construcción (la ecuación de «resto» sale por diferencia). La simetría NO se impone:
    con cinco orígenes y errores HAC, imponerla exige SUR iterado y no cambia el signo
    ni el orden de magnitud de la flexibilidad propia argentina. Se informa el sistema
    sin restringir y se deja constancia.

    El índice de Stone va con participaciones MEDIAS, no corrientes: con las corrientes
    el regresor lleva adentro la variable dependiente (la regla del anexo A.11, que el
    sistema de flotas ya respetaba y éste no).

    Las flexibilidades salen de `flexibilidades_iaids`, que es la única definición del
    proyecto:  f_ij = g_ij/w_i + b_i·w_j/w_i − δ_ij  y  f_i^escala = b_i/w_i − 1.
    """
    print("\n" + "=" * 92)
    print("4. SISTEMA DE DEMANDA INVERSA (LA/IAIDS) — importación extra-UE por origen")
    print("=" * 92)
    O = pd.read_pickle(_p("datos", "eumofa_camaron_origen.pkl"))
    V = O.eur.unstack().fillna(0)[ORIGENES]
    Q = (O.kg.unstack().fillna(0) / 1e6)[ORIGENES]          # miles de toneladas
    W = V.div(V.sum(axis=1), axis=0)
    X = np.log(Q.clip(lower=1e-3))
    lnQ = X @ W.mean()                                      # Stone con w MEDIAS (A.11)

    print("participación media en el valor importado (%):")
    print((W.mean() * 100).round(1).to_string())
    print("precio medio de importación (EUR/kg):")
    print((V.sum() / (Q.sum() * 1e6)).round(2).to_string())

    Z = pd.DataFrame({f"x_{c}": X[c] - X["RE"] for c in ORIGENES[:-1]})
    Z["lnQ"] = lnQ
    Z["trend"] = np.arange(len(Z)) / 12.0
    Mm = pd.get_dummies(Z.index.month, prefix="m", drop_first=True).astype(float)
    Mm.index = Z.index
    REG = pd.concat([Z, Mm], axis=1).dropna()

    par, se = {}, {}
    for i in ORIGENES[:-1]:
        m = sm.OLS(W[i].reindex(REG.index), sm.add_constant(REG), missing="drop").fit(
            cov_type="HAC", cov_kwds={"maxlags": HAC})
        par[i], se[i] = m.params, m.bse
    par, se = pd.DataFrame(par), pd.DataFrame(se)
    par["RE"] = -par[ORIGENES[:-1]].sum(axis=1)             # adición
    par.loc["const", "RE"] = 1 - par.loc["const", ORIGENES[:-1]].sum()

    w = W.mean()
    G = pd.DataFrame(0.0, index=ORIGENES, columns=ORIGENES)
    for i in ORIGENES:
        for j in ORIGENES[:-1]:
            G.loc[i, j] = par.loc[f"x_{j}", i]
        G.loc[i, "RE"] = -G.loc[i, ORIGENES[:-1]].sum()     # homogeneidad
    b = par.loc["lnQ", ORIGENES]
    F, esc = fx.matriz(G, b, w)
    fx.verificar(F, esc, w)

    print("\nFlexibilidades de cantidad, no compensadas (fila = precio de i, col = cantidad de j):")
    print(F.round(3).to_string())
    print("\nFlexibilidad de escala (todas las cantidades suben 1% a la vez):")
    print(esc.round(3).to_string())
    print("  (cada fila de la matriz suma su flexibilidad de escala; es la identidad"
          " que verifica flexibilidades_iaids.verificar)")
    fx.informar_negatividad(G, w)
    se_ar = se.loc["x_AR", "AR"] / w["AR"]
    f = F.loc["AR", "AR"]
    print(f"\nArgentina — flexibilidad propia f = {f:+.3f}  (SE {se_ar:.3f})  "
          f"IC95% [{f - 1.96 * se_ar:+.3f}, {f + 1.96 * se_ar:+.3f}]")
    print(f"  H0: f = -1 → t = {(f + 1) / se_ar:+.1f}  "
          f"({'no se rechaza' if abs((f + 1) / se_ar) < 1.96 else 'SE RECHAZA'})")
    print(f"  cruzada con Ecuador: {F.loc['AR', 'EC']:+.3f} · con India: {F.loc['AR', 'IN']:+.3f}")
    print(f"  escala: si TODO el mercado recortara 1%, el precio argentino subiría "
          f"{-esc['AR']:.2f}% — tampoco alcanza el umbral de 1.")
    return F, esc, w, se_ar


def grafico(d: pd.DataFrame) -> None:
    """Precio del L1 y del cultivo contra el desembarque. Español, fuente al pie,
    sin título dentro de la imagen, coma decimal."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    def _coma(dec):
        return FuncFormatter(lambda x, _: f"{x:,.{dec}f}".replace(",", "@").replace(".", ",").replace("@", "."))

    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    x = d.index.to_timestamp()
    ax.plot(x, d.p_l1_eur, lw=1.6, color="#1f4e79", label="Entero L1 argentino (EUR/kg)")
    ax.plot(x, d.van_eur_kg, lw=1.6, color="#c0504d", label="Camarón de cultivo, importación UE (EUR/kg)")
    ax.set_ylabel("EUR por kilo")
    ax.yaxis.set_major_formatter(_coma(1))
    ax.set_ylim(3.9, 9.6)
    ax2 = ax.twinx()
    ax2.fill_between(x, d.desem3 / 1000, color="#9bbb59", alpha=.30, lw=0,
                     label="Desembarque acumulado 3 meses (miles de t)")
    ax2.set_ylabel("Miles de toneladas")
    ax2.yaxis.set_major_formatter(_coma(0))
    ax2.set_ylim(0, 320)
    ax2.set_yticks([0, 40, 80, 120])
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(.5, 1.14),
              ncol=3, frameon=False, fontsize=8.2)
    ax.grid(axis="y", lw=.4, alpha=.4)
    for s_ in ("top",):
        ax.spines[s_].set_visible(False); ax2.spines[s_].set_visible(False)
    fig.text(.01, .01, "Fuente: elaboración propia sobre base de comercio (precio del L1), SSPyA (desembarques) y "
                       "EUMOFA (importación extra-UE de camarón de cultivo congelado). "
                       "Precios convertidos a euros al promedio mensual EUR/USD.", fontsize=6.6)
    fig.tight_layout(rect=(0, .035, 1, 1))
    out = _p("salidas", "demanda_inversa_L1.svg")
    fig.savefig(out); fig.savefig(out.replace(".svg", ".png"), dpi=200)
    print(f"Guardado: {out}")


if __name__ == "__main__":
    main()
