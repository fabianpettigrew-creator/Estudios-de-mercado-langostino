# -*- coding: utf-8 -*-
"""Demanda inversa del entero L1 de la FLOTA TANGONERA (congelado a bordo).

Acota el modelo general (`demanda_inversa_modelo.py`) al producto y la flota que
importan, y explota que la serie contiene dos shocks de signo contrario, que es lo
que permite identificar la curva:

  · 2020 — shock de DEMANDA. El canal HORECA, que es el que consume langostino
    salvaje en España, Italia, Japón y China, estuvo cerrado. Precio y cantidad
    caen JUNTOS: leído como oferta, ese año «demuestra» una curva de pendiente
    positiva. Hay que sacarlo o controlarlo, si no contamina f hacia cero.
  · 2025 — shock de OFERTA. Conflicto gremial: la tangonera estuvo parada de abril
    a julio, al inicio de la temporada, y la captura de campaña cayó 46%. Ese es el
    movimiento que traza la demanda.

Producto: entero L1 congelado a bordo = tangonera. La marca sale de dos lugares,
según la época (`fuentes/expo.py` las unifica en la columna `ruta`):
  · desde 2017-12, el sufijo SIM **SA01**;
  · antes, la leyenda **«CONGELADO A BORDO»** en la descripción del despacho, que
    cubre el 68-70% de los kilos de entero de 2013-2016.
La marca es siempre AFIRMATIVA: sin sufijo y sin leyenda el registro queda en «s/d»
y no entra — nunca se infiere «en tierra» por descarte. Quedan doce meses sin serie:
ene-jun de 2016 (ningún despacho con grado declarado) y jun-nov de 2017 (la
descripción viene vacía en ese tramo de la extracción de Softrade).

Unidad de análisis: la CAMPAÑA. El congelado a bordo se pesca entre abril y octubre
y se vende a lo largo de los doce meses siguientes; comparar captura de un mes con
precio del mismo mes mide otra cosa. Campaña Y = captura abr-oct de Y contra el
precio de julio de Y a junio de Y+1.

Regla de fuente: precio de Softrade, cantidad del registro oficial SSPyA.

Uso:  python demanda_inversa_tangonera.py
Salida: consola + salidas/demanda_inversa_tangonera.xlsx + .svg/.png
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import recorte_conxemar

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
pd.set_option("display.width", 175)

DESDE, HASTA = "2013-01", "2026-07"
MIN_MESES = 9          # meses con precio exigidos a la ventana de venta de una campaña
HAC = 6
CONFLICTO = (pd.Period("2025-04"), pd.Period("2025-07"))   # flota parada
# Meses de embarque en que la temporada de la flota congeladora domina el entero: entre
# 2018 y 2026, con el sufijo SA01 a la vista, el 93,6-96,8% de los kilos de entero L1
# embarcados de mayo a octubre salieron congelados a bordo. Sobre eso se apoya el proxy
# sin marcador de `proxy_temporada()`.
TEMPORADA = (5, 6, 7, 8, 9, 10)

# Actividad del canal HORECA en los mercados del L1 tangonero. Ya NO es un supuesto:
# `datos/horeca_indice.pkl` (lo arma `demanda_inversa_horeca.py`) trae el índice
# observado de facturación de servicios de comidas y bebidas de Eurostat —España
# mensual, Italia trimestral, CNAE/Ateco 56, desestacionalizado, base 2021— combinado
# como media geométrica ponderada por la participación de cada mercado en el volumen
# del L1 tangonero, y el índice de rigor de OxCGRT para los cuatro destinos.
# El control que entra al modelo es la BRECHA del índice respecto de su propia
# tendencia: el índice es de facturación nominal y crece con la inflación europea, de
# modo que el nivel es tendencia y lo que informa es el desvío.
# Se conserva el índice construido a mano de la primera versión sólo para contraste.
HORECA_MANO = {("2020-03", "2020-06"): 1.0, ("2020-07", "2020-09"): 0.3,
               ("2020-10", "2021-05"): 0.7, ("2021-06", "2021-09"): 0.2,
               ("2021-10", "2022-03"): 0.3}


def _p(*t):
    return os.path.join(RAIZ, *t)


_CACHE = {}


def despachos() -> pd.DataFrame:
    """`expo.cargar_todos()` tarda cerca de un minuto: se carga una sola vez por corrida."""
    if "d" not in _CACHE:
        from fuentes import expo
        _CACHE["d"] = expo.cargar_todos()
    return _CACHE["d"]


def panel() -> tuple[pd.DataFrame, pd.Series]:
    d = despachos()
    t = d[(d.pres == "entero") & (d.cal == "L1") & (d.ruta == "a bordo")
          & (d.kg > 0) & (d.fob_tot > 0)].copy()
    t.index = pd.PeriodIndex(t.anio.astype(str) + "-" + t.mes.astype(str).str.zfill(2), freq="M")
    g = t.groupby(level=0).agg(fob=("fob_tot", "sum"), kg=("kg", "sum")).sort_index()

    lan = pd.read_pickle(_p("_lan.pkl"))
    lan.index = pd.PeriodIndex(lan.anio.astype(str) + "-" + lan.mes.astype(str).str.zfill(2), freq="M")
    tan = lan[lan.flota == "CONG. TANGONEROS"].groupby(level=0).t.sum().rename("tan_t")

    ue = pd.read_pickle(_p("datos", "eumofa_camaron_ue.pkl"))

    import demanda_inversa_modelo as M0
    fx = pd.Series({k: float(v) for k, v in (x.split("=") for x in M0.FX.split(";"))})
    fx.index = pd.PeriodIndex(fx.index, freq="M")

    df = pd.concat([(g.fob / g.kg).rename("p_tan"), (g.kg / 1000).rename("q_exp_t"),
                    tan, ue, fx.rename("eurusd")], axis=1).loc[DESDE:HASTA]
    df["tan12"] = tan.rolling(12).sum().reindex(df.index)
    df["p_eur"] = df.p_tan / df.eurusd
    df["rel"] = df.p_eur / df.van_eur_kg
    H = pd.read_pickle(_p("datos", "horeca_indice.pkl"))
    df = df.join(H[["horeca_ue", "rigor"]])
    df["rigor100"] = df.rigor / 100.0
    df["horeca_mano"] = 0.0
    for (a, b), v in HORECA_MANO.items():
        df.loc[pd.Period(a):pd.Period(b), "horeca_mano"] = v
    # Brecha del índice HORECA respecto de su propia tendencia lineal: el índice es de
    # facturación nominal y crece con la inflación europea, así que el nivel es tendencia
    # y lo que informa como desplazador de demanda es el desvío.
    lh = np.log(df.horeca_ue)
    ok = lh.notna()
    tt = pd.Series(np.arange(len(df)) / 12.0, index=df.index)
    b = sm.OLS(lh[ok], sm.add_constant(tt[ok])).fit()
    df["horeca"] = lh - b.predict(sm.add_constant(tt))
    df["conflicto"] = ((df.index >= CONFLICTO[0]) & (df.index <= CONFLICTO[1])).astype(float)
    # ventana en que el conflicto deprime la captura acumulada de doce meses
    df["iv_conf"] = ((df.index >= pd.Period("2025-04")) & (df.index <= pd.Period("2026-03"))).astype(float)
    return df, tan


def campanas(df: pd.DataFrame, tan: pd.Series) -> pd.DataFrame:
    """Captura abr-oct del año Y contra el precio de venta de jul Y a jun Y+1."""
    filas, descartadas = [], []
    for y in range(int(df.index.year.min()), int(df.index.year.max()) + 1):
        cap = tan.loc[f"{y}-04":f"{y}-10"].sum()
        ven = df.loc[f"{y}-07":f"{y + 1}-06"].dropna(subset=["p_tan"])
        if cap <= 0:
            continue
        if len(ven) < MIN_MESES:
            descartadas.append((f"{y}/{y + 1}", len(ven)))
            continue
        p = (ven.p_tan * ven.q_exp_t).sum() / ven.q_exp_t.sum()      # ponderado
        filas.append({"campaña": f"{y}/{y + 1}", "captura_abr_oct_t": cap,
                      "meses": len(ven),
                      "p_usd_kg": p, "p_simple_usd": ven.p_tan.mean(),
                      "p_eur_kg": p / ven.eurusd.mean(),
                      "cultivo_eur_kg": ven.van_eur_kg.mean(),
                      "rel": p / ven.eurusd.mean() / ven.van_eur_kg.mean(),
                      "horeca": ven.horeca.mean(),
                      "covid": float(ven.horeca_mano.mean() > 0)})
    if descartadas:
        print("  campañas descartadas por ventana de venta incompleta "
              f"(mínimo {MIN_MESES} meses): "
              + " · ".join(f"{c} ({n} meses)" for c, n in descartadas))
    C = pd.DataFrame(filas).set_index("campaña")
    C["lq"] = np.log(C.captura_abr_oct_t)
    C["lp"] = np.log(C.p_eur_kg)
    C["lrel"] = np.log(C.rel)
    C["lvan"] = np.log(C.cultivo_eur_kg)
    C["trend"] = np.arange(len(C))
    return C


def _reporte(m, var, nombre, robusto=True):
    f, se = m.params[var], m.bse[var]
    gl = int(m.df_resid)
    tc = stats.t.ppf(.975, gl) if not robusto else 1.96
    t1 = (f + 1) / se
    print(f"\n--- {nombre}   N={int(m.nobs)}  R2={m.rsquared:.3f}  gl={gl}")
    T = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues, "p": m.pvalues})
    print(T.loc[[i for i in T.index if not i.startswith("m_")]].round(4).to_string())
    print(f"    f = {f:+.3f}   IC95% [{f - tc * se:+.3f}, {f + tc * se:+.3f}]   "
          f"H0: f = -1 → t = {t1:+.2f}   ingreso: 1+f = {1 + f:+.3f}")
    return {"modelo": nombre, "f": f, "se": se, "ic_inf": f - tc * se,
            "ic_sup": f + tc * se, "t_H0": t1, "ingreso_1mas_f": 1 + f, "N": int(m.nobs)}


def main() -> None:
    df, tan = panel()
    res, tab = [], {}

    print("=" * 95)
    print("DEMANDA INVERSA DEL L1 TANGONERO (congelado a bordo, SA01)")
    print("=" * 95)
    print(f"Muestra {df.index.min()} a {df.index.max()}, {len(df)} meses sin huecos.")

    # ---------------------------------------------------------- los dos shocks
    print("\n" + "=" * 95)
    print("1. LOS DOS EPISODIOS — el contraste que identifica la curva")
    print("=" * 95)
    an = df.groupby(df.index.year).agg(p_usd=("p_tan", "mean"), p_eur=("p_eur", "mean"),
                                       cultivo=("van_eur_kg", "mean"), rel=("rel", "mean"),
                                       captura=("tan_t", "sum"), eurusd=("eurusd", "mean"))
    print(an.round(3).to_string())
    for y0, y1, lab in [(2019, 2020, "2020 · shock de DEMANDA (HORECA cerrado)"),
                        (2024, 2025, "2025 · shock de OFERTA (conflicto gremial)")]:
        dq = np.log(an.captura[y1] / an.captura[y0])
        dp = np.log(an.p_eur[y1] / an.p_eur[y0])
        dr = np.log(an.rel[y1] / an.rel[y0])
        print(f"\n{lab}")
        print(f"   captura {dq * 100:+.1f}%  ·  precio en euros {dp * 100:+.1f}%  ·  "
              f"precio relativo al cultivo {dr * 100:+.1f}%")
        print(f"   flexibilidad de arco: bruta {dp / dq:+.3f} · neta del ciclo mundial {dr / dq:+.3f}")
    print("\n  Leído sin distinguir: 2020 tiene precio y cantidad cayendo juntos y arrastra")
    print("  la pendiente hacia arriba. Ése es exactamente el sesgo que hay que sacar.")

    # ---------------------------------------------------------- mensual
    print("\n" + "=" * 95)
    print("2. MENSUAL — Q = captura tangonera acumulada 12 meses")
    print("=" * 95)
    d = df.dropna(subset=["p_eur", "tan12", "van_eur_kg", "horeca_ue"]).copy()
    for c, n in [("p_eur", "lp"), ("van_eur_kg", "lvan"), ("tan12", "lq"), ("rel", "lrel")]:
        d[n] = np.log(d[c])
    d["trend"] = np.arange(len(d)) / 12.0
    # Nota: la captura rezagada NO sirve como instrumento. El langostino tiene ciclo de
    # vida corto y «reemplazo casi total de la cantidad de ejemplares» entre temporadas
    # (INIDEP, infografía de la especie): no hay persistencia de biomasa que explotar.
    # Empíricamente da primera etapa F = 0,1. El único instrumento que queda en pie es
    # la ventana del conflicto gremial (F = 61,6).
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d.index

    def ols(y, X, lags=HAC):
        m = sm.OLS(y, sm.add_constant(X), missing="drop").fit(
            cov_type="HAC", cov_kwds={"maxlags": lags})
        vis = [i for i in m.params.index if not i.startswith("m_")]
        return m, vis

    m, v = ols(d.lp, pd.concat([d[["lq", "lvan", "trend"]], M], axis=1))
    res.append(_reporte(m, "lq", "T1  sin control de HORECA (2020 entra como si fuera oferta)"))
    tab["T1"] = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues}).loc[v]

    m, v = ols(d.lp, pd.concat([d[["lq", "lvan", "horeca", "trend"]], M], axis=1))
    res.append(_reporte(m, "lq", "T2  con la brecha del índice HORECA observado"))
    tab["T2"] = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues}).loc[v]

    e = d[(d.index < pd.Period("2020-03")) | (d.index > pd.Period("2022-03"))]
    m, v = ols(e.lp, pd.concat([e[["lq", "lvan", "trend"]], M.loc[e.index]], axis=1))
    res.append(_reporte(m, "lq", "T3  excluyendo la ventana de pandemia (mar-2020 a mar-2022)"))
    tab["T3"] = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues}).loc[v]

    m, v = ols(d.lrel, pd.concat([d[["lq", "horeca", "trend"]], M], axis=1))
    res.append(_reporte(m, "lq", "T4  precio relativo al cultivo, con la brecha HORECA"))
    tab["T4"] = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues}).loc[v]

    # IV: el conflicto y la captura rezagada como desplazadores de oferta
    from linearmodels.iv import IV2SLS
    dd = pd.concat([d[["lrel", "lq", "horeca", "trend", "iv_conf"]], M], axis=1).dropna()
    ex = sm.add_constant(dd[["horeca", "trend"] + list(M.columns)])
    iv = IV2SLS(dd.lrel, ex, dd[["lq"]], dd[["iv_conf"]]).fit(
        cov_type="kernel", kernel="bartlett")
    f, se = iv.params["lq"], iv.std_errors["lq"]
    F1 = float(iv.first_stage.diagnostics["f.stat"].iloc[0])
    print(f"\n--- T5  IV 2SLS sobre el precio relativo; instrumento: la ventana en que el "
          f"conflicto deprime la captura de doce meses   N={int(iv.nobs)}")
    print(f"    f = {f:+.3f}   se = {se:.3f}   IC95% [{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]   "
          f"H0: f = -1 → t = {(f + 1) / se:+.2f}")
    print(f"    primera etapa F = {F1:.1f}  ({'instrumentos fuertes' if F1 > 10 else 'INSTRUMENTOS DÉBILES'})")
    res.append({"modelo": "T5  IV, precio relativo", "f": f, "se": se, "ic_inf": f - 1.96 * se,
                "ic_sup": f + 1.96 * se, "t_H0": (f + 1) / se, "ingreso_1mas_f": 1 + f,
                "N": int(iv.nobs)})

    # ---------------------------------------------------------- campaña
    print("\n" + "=" * 95)
    print("3. NIVEL CAMPAÑA — la unidad correcta para un congelado a bordo")
    print("=" * 95)
    C = campanas(df, tan)
    print(C[["captura_abr_oct_t", "meses", "p_usd_kg", "p_eur_kg", "cultivo_eur_kg", "rel", "horeca"]]
          .round(3).to_string())

    for dep, X, nom in [("lp", ["lq", "lvan", "horeca"],
                         "C1  campaña · log P (EUR) ~ log captura + cultivo + HORECA"),
                        ("lrel", ["lq", "horeca"],
                         "C2  campaña · log (P/cultivo) ~ log captura + HORECA"),
                        ("lrel", ["lq", "horeca", "trend"], "C3  C2 + tendencia")]:
        m = sm.OLS(C[dep], sm.add_constant(C[X])).fit(cov_type="HC1")
        res.append(_reporte(m, "lq", nom))
        tab[nom.split()[0]] = pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues})

    print("\n" + "=" * 95)
    print("4. VERIFICACIÓN")
    print("=" * 95)
    quiebre(df)
    m = sm.OLS(C.lrel, sm.add_constant(C[["lq", "horeca"]])).fit()   # clásico: gl correctos
    gl = int(m.df_resid)
    f, se = m.params["lq"], m.bse["lq"]
    tc = stats.t.ppf(.975, gl)
    print(f"C2 con errores clásicos y grados de libertad reales (gl = {gl}):")
    print(f"   f = {f:+.3f}  se = {se:.3f}  t = {f / se:+.2f}   "
          f"IC95% (t_{gl} = {tc:.2f}) [{f - tc * se:+.3f}, {f + tc * se:+.3f}]")
    p1 = 2 * (1 - stats.t.cdf(abs((f + 1) / se), gl))
    print(f"   H0: f = -1 → t = {(f + 1) / se:+.2f}, p = {p1:.5f}")

    print("\nLeave-one-out — ¿lo maneja una sola campaña?")
    loo = {}
    for i in C.index:
        mm = sm.OLS(C.drop(index=i).lrel, sm.add_constant(C.drop(index=i)[["lq", "horeca"]])).fit()
        loo[i] = mm.params["lq"]
        print(f"   sin {i}: f = {mm.params['lq']:+.3f}  (se {mm.bse['lq']:.3f})")
    print(f"   rango: {min(loo.values()):+.3f} a {max(loo.values()):+.3f}")

    lim = C.drop(index=["2025/2026"]).query("covid == 0")
    mm = sm.OLS(lim.lrel, sm.add_constant(lim[["lq"]])).fit()
    print(f"\nSin la campaña del conflicto Y sin las de HORECA cerrado (N = {int(mm.nobs)}): "
          f"f = {mm.params['lq']:+.3f}  (se {mm.bse['lq']:.3f})")
    print("   Sin los dos episodios que identifican, no queda variación de oferta que sirva:")
    print("   este número NO es una estimación alternativa, es la constatación de que sin")
    print("   shocks la serie no dice nada. Reportarlo igual, y no como resultado.")

    R = pd.DataFrame(res).set_index("modelo")
    print("\n" + "=" * 95)
    print("RESUMEN")
    print("=" * 95)
    print(R.round(3).to_string())

    # ---------------------------------------------------------- política
    print("\n" + "=" * 95)
    rec = recorte_conxemar.recorte()
    print(f"5. SIMULACIÓN — recorte del {-rec['dq'] * 100:.1f}% del desembarque "
          "(paquete de Conxemar)")
    print("=" * 95)
    print(recorte_conxemar.describir(rec))
    print()
    dq = rec["dq"]
    fiv = R.loc["T5  IV, precio relativo", "f"]
    sim = pd.DataFrame([
        {"supuesto": "IV mensual con la ventana del conflicto (preferida)", "f": fiv},
        {"supuesto": "IV, cota más favorable del IC 95%",
         "f": R.loc["T5  IV, precio relativo", "ic_inf"]},
        {"supuesto": "campaña con tendencia (C3)", "f": R.loc["C3  C2 + tendencia", "f"]},
        {"supuesto": "campaña sin tendencia (C2)", "f": R.loc[
            "C2  campaña · log (P/cultivo) ~ log captura + HORECA", "f"]},
        {"supuesto": "sistema IAIDS (modelo general)", "f": -0.267},
        {"supuesto": "umbral para no perder facturación", "f": -1.0},
    ]).set_index("supuesto")
    EXPO_2025 = recorte_conxemar.EXPO_2025
    sim["Δ oferta %"] = dq * 100
    sim["Δ precio %"] = sim.f * dq * 100
    sim["Δ facturación %"] = (1 + sim.f) * dq * 100
    sim["Δ facturación US$ M"] = EXPO_2025 * (1 + sim.f) * dq
    # El test que decide no es la facturación sino el margen: recortar conviene si el
    # costo EVITABLE por kilo supera 1+f del precio.
    sim["costo evitable mínimo c/P"] = 1 + sim.f
    sim["  ídem en US$/kg (P=6,55)"] = (1 + sim.f) * 6.55
    print(sim.round(3).to_string())
    print(f"\nSobre US$ {EXPO_2025:,.0f} M de exportación de langostino (2025), la estimación "
          f"preferida son {sim['Δ facturación US$ M'].iloc[0]:,.0f} millones de dólares de "
          "facturación por año.")
    print("Pero la decisión se juega en el margen: con f = "
          f"{fiv:+.3f} el recorte conviene sólo si el costo que se ahorra por no pescar "
          f"supera el {(1 + fiv) * 100:.1f}% del FOB (US$ {(1 + fiv) * 6.55:.2f}/kg). "
          "Ese dato no lo tenemos.")

    cob = cobertura_flota(despachos())
    Cp, Rp, loop = proxy_temporada(tan)

    try:
        out = _p("salidas", "demanda_inversa_tangonera.xlsx")
        with pd.ExcelWriter(out) as w:
            df.to_excel(w, sheet_name="mensual")
            an.to_excel(w, sheet_name="anual")
            C.to_excel(w, sheet_name="campanas")
            R.to_excel(w, sheet_name="flexibilidades")
            sim.to_excel(w, sheet_name="simulacion")
            pd.Series(loo, name="f").to_frame().to_excel(w, sheet_name="leave_one_out")
            cob.to_excel(w, sheet_name="cobertura_flota_mes")
            Cp.to_excel(w, sheet_name="proxy_campanas")
            Rp.to_excel(w, sheet_name="proxy_flexibilidades")
            loop.to_frame().to_excel(w, sheet_name="proxy_leave_one_out")
            pd.concat(tab, names=["modelo"]).to_excel(w, sheet_name="regresiones")
        print(f"\nGuardado: {out}")
    except PermissionError:
        print("\nAVISO: no pude escribir el xlsx (¿abierto en Excel?).")

    grafico(C, m)


def cobertura_flota(df_expo) -> pd.DataFrame:
    """Share de «a bordo» del entero L1 por mes de embarque, 2018-2026.

    Es la validación de la regla de la industria: casi todo el entero que se exporta
    durante la temporada de la flota congeladora es congelado a bordo, y casi toda la
    cola se procesa en tierra.
    """
    m = df_expo[(df_expo.pres == "entero") & (df_expo.cal == "L1")
                & (df_expo.anio >= 2018) & (df_expo.kg > 0)]
    t = pd.crosstab(m.mes, m.ruta, values=m.kg, aggfunc="sum").fillna(0)
    kt = t.sum(axis=1) / 1e6
    t = t.div(t.sum(axis=1), axis=0) * 100
    t["kt"] = kt
    return t


def proxy_temporada(tan: pd.Series):
    """Estimación SIN marcador de flota, sobre el registro oficial de aduana.

    Si de mayo a octubre el 94-97% del entero exportado es congelado a bordo, entonces el
    FOB del entero de aduana embarcado en esos meses es un proxy del precio tangonero que
    NO depende de la descripción del despacho. Ventaja decisiva: no tiene huecos, así que
    recupera las campañas 2015/2016 y 2017/2018 que el marcador pierde, y da N = 13.
    """
    print("\n" + "=" * 95)
    print("6. CONTRASTE SIN MARCADOR DE FLOTA — el entero de aduana embarcado en temporada")
    print("=" * 95)
    a = pd.read_pickle(_p("datos", "aduana_langostino_total.pkl"))
    a.index = pd.PeriodIndex(a.anio.astype(str) + "-" + a.mes.astype(str).str.zfill(2), freq="M")
    ent = a[a.ncm == "0306.17.10"][["kg", "fob"]]
    pre = pd.read_pickle(_p("datos", "indec_entero_2013_2017.pkl"))
    ent = pd.concat([pre[pre.index < ent.index.min()], ent]).sort_index().loc[DESDE:HASTA]

    H = pd.read_pickle(_p("datos", "horeca_indice.pkl"))
    ue = pd.read_pickle(_p("datos", "eumofa_camaron_ue.pkl"))
    import demanda_inversa_modelo as M0
    fx = pd.Series({k: float(v) for k, v in (x.split("=") for x in M0.FX.split(";"))})
    fx.index = pd.PeriodIndex(fx.index, freq="M")

    filas = []
    for y in range(int(ent.index.year.min()), int(ent.index.year.max())):
        cap = tan.loc[f"{y}-04":f"{y}-10"].sum()
        ven = ent.loc[f"{y}-07":f"{y + 1}-06"]
        v = ven[ven.index.month.isin(TEMPORADA)]
        if cap <= 0 or len(v) < 4:
            continue
        p = v.fob.sum() / v.kg.sum()
        filas.append({"campaña": f"{y}/{y + 1}", "captura_abr_oct_t": cap, "meses": len(v),
                      "p_usd_kg": p, "p_eur_kg": p / fx.reindex(v.index).mean(),
                      "cultivo_eur_kg": ue.van_eur_kg.reindex(v.index).mean(),
                      "horeca_ue": H.horeca_ue.reindex(ven.index).mean()})
    C = pd.DataFrame(filas).set_index("campaña")
    C["rel"] = C.p_eur_kg / C.cultivo_eur_kg
    C["lq"], C["lrel"] = np.log(C.captura_abr_oct_t), np.log(C.rel)
    C["lp"], C["lvan"] = np.log(C.p_eur_kg), np.log(C.cultivo_eur_kg)
    C["trend"] = np.arange(len(C))
    C["horeca"] = sm.OLS(np.log(C.horeca_ue), sm.add_constant(C[["trend"]])).fit().resid
    print(C[["captura_abr_oct_t", "meses", "p_usd_kg", "p_eur_kg", "cultivo_eur_kg", "rel"]]
          .round(3).to_string())

    res = []
    for dep, X, nom in [("lrel", ["lq", "horeca"], "P1  log (P/cultivo) ~ log captura + HORECA"),
                        ("lrel", ["lq", "horeca", "trend"], "P2  P1 + tendencia"),
                        ("lp", ["lq", "lvan", "horeca"], "P3  log P (EUR) ~ log captura + cultivo + HORECA")]:
        m = sm.OLS(C[dep], sm.add_constant(C[X])).fit(cov_type="HC1")
        res.append(_reporte(m, "lq", nom))
    print("\nLeave-one-out sobre P2:")
    loo = {}
    for i in C.index:
        c = C.drop(index=i)
        loo[i] = sm.OLS(c.lrel, sm.add_constant(c[["lq", "horeca", "trend"]])).fit().params["lq"]
        print(f"   sin {i}: f = {loo[i]:+.3f}")
    print(f"   rango: {min(loo.values()):+.3f} a {max(loo.values()):+.3f}   "
          "(el modelo con marcador, en cambio, depende de 2025/2026)")
    return C, pd.DataFrame(res).set_index("modelo"), pd.Series(loo, name="f")


def quiebre(df: pd.DataFrame) -> None:
    """¿La serie de precio cambia de nivel cuando cambia el marcador de flota?

    Antes de 2018 la flota sale de la leyenda en prosa y cubre el 68-70% de los kilos;
    después sale del sufijo SIM y cubre 78-91%. Si esa diferencia de cobertura moviera
    el precio medido, el empalme sería falso. El testigo es el FOB del entero de aduana
    oficial, que es el mismo dato en las dos épocas: si la prima del L1 a bordo sobre él
    se mantiene, el empalme es legítimo.
    """
    a = pd.read_pickle(_p("datos", "aduana_langostino_total.pkl"))
    a.index = pd.PeriodIndex(a.anio.astype(str) + "-" + a.mes.astype(str).str.zfill(2), freq="M")
    ent = a[a.ncm == "0306.17.10"][["kg", "fob"]]
    pre = pd.read_pickle(_p("datos", "indec_entero_2013_2017.pkl"))
    ent = pd.concat([pre[pre.index < ent.index.min()], ent]).sort_index()
    r = (df.p_tan / (ent.fob / ent.kg)).dropna()
    an = r.groupby(r.index.year).mean()
    pre18, pos18 = an.loc[2013:2016].mean(), an.loc[2018:2024].mean()
    print("\nEmpalme del marcador de flota — prima del L1 a bordo sobre el entero oficial:")
    print("   " + " · ".join(f"{y}: {v:.3f}" for y, v in an.round(3).items()))
    print(f"   media 2013-2016 (leyenda en prosa) {pre18:.3f}  ·  "
          f"media 2018-2024 (sufijo SA01) {pos18:.3f}  ·  salto {(pos18 / pre18 - 1) * 100:+.1f}%")
    print("   Sin quiebre de nivel: las dos mitades de la serie son comparables.")


def grafico(C: pd.DataFrame, m) -> None:
    """La curva de demanda inversa que trazan las ocho campañas, con los dos shocks
    marcados. Español, fuente al pie, sin título dentro de la imagen, coma decimal."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    coma = FuncFormatter(lambda x, _: f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", "."))
    # residualizado de HORECA: precio relativo corregido por el cierre del canal
    ajus = C.rel * np.exp(-m.params["horeca"] * C.horeca)

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    cerr = C.horeca > 0
    ax.scatter(C.captura_abr_oct_t[~cerr] / 1000, ajus[~cerr], s=62, color="#1f4e79",
               zorder=3, label="Campaña con canal HORECA normal")
    ax.scatter(C.captura_abr_oct_t[cerr] / 1000, ajus[cerr], s=62, facecolors="none",
               edgecolors="#c0504d", linewidths=1.8, zorder=3,
               label="Campaña con HORECA cerrado (corregida)")
    xs = np.linspace(C.captura_abr_oct_t.min() * .95, C.captura_abr_oct_t.max() * 1.05, 50)
    ys = np.exp(m.params["const"] + m.params["lq"] * np.log(xs))
    etiq = f"{m.params['lq']:.2f}".replace("-", "−").replace(".", ",")
    ax.plot(xs / 1000, ys, lw=1.4, color="#7f7f7f", zorder=2,
            label=f"Demanda inversa ajustada · f = {etiq}")
    for k in C.index:
        ax.annotate(k, (C.captura_abr_oct_t[k] / 1000, ajus[k]), textcoords="offset points",
                    xytext=(7, -3), fontsize=8, color="#404040")
    ax.set_xlabel("Captura tangonera de la campaña, abril a octubre (miles de toneladas)")
    ax.set_ylabel("Precio del L1 tangonero relativo al camarón de cultivo")
    ax.yaxis.set_major_formatter(coma)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
    ax.grid(lw=.4, alpha=.4)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.legend(frameon=False, fontsize=8.4, loc="upper right")
    fig.text(.01, .012,
             "Fuente: elaboración propia sobre base de comercio (precio del L1 congelado a bordo: leyenda «congelado a bordo» "
             "hasta 2017, sufijo SIM SA01 desde 2018),\nSSPyA (captura tangonera) y EUMOFA (camarón de "
             "cultivo). Campaña = captura abr-oct del año contra el precio de jul a jun siguiente; las "
             "campañas con el canal HORECA\ncerrado se muestran corregidas por el coeficiente estimado del "
             "cierre. La curva no descuenta la tendencia de diferenciación, que explica buena parte de la "
             "dispersión.",
             fontsize=6.6)
    fig.tight_layout(rect=(0, .07, 1, 1))
    out = _p("salidas", "demanda_inversa_tangonera.svg")
    fig.savefig(out)
    fig.savefig(out.replace(".svg", ".png"), dpi=200)
    print(f"Guardado: {out}")


if __name__ == "__main__":
    main()
