# -*- coding: utf-8 -*-
"""¿Sirve el calendario del CFP como instrumento de oferta?

El modelo identifica la flexibilidad con un solo episodio (el conflicto de 2025) y el test de
permutación del §9.5 muestra lo que cuesta. La salida propuesta era el calendario oficial de
aperturas y cierres del Consejo Federal Pesquero: variación administrativa de la oferta en
todos los años, decidida por criterios biológicos (juveniles, relación M/L, by-catch de merluza)
y no por el precio. Este guion lo pone a prueba.

CALENDARIO. Codificado a mano desde los párrafos de las 547 actas 2013-2026 (libro
`cfp_calendario_codificado.xlsx`, con la cita literal de cada fecha). Para el tangonero lo que
manda es la temporada DENTRO del Área de Veda Permanente de Juveniles de Merluza (AVPJM), que es
donde pesca de mayo a octubre: fecha de la primera apertura comercial y fecha de la suspensión
del despacho. Fuera del AVPJM la pesca estuvo abierta todo el año hasta la suspensión provisoria
de noviembre de 2019; desde 2020 el CFP decide cada año la apertura de marzo-abril.

TRES INSTRUMENTOS CANDIDATOS, todos en ventana móvil de doce meses para emparejar con `tan12`:
  Z1  días con el AVPJM abierto (temporada nacional)
  Z2  días con alguna agua nacional abierta (AVPJM + fuera del AVPJM)
  Z3  saldo de decisiones: aperturas de subárea menos cierres, por mes de vigencia

PRUEBAS.
  1. Primera etapa: coeficiente y signo, no el F (§9.5).
  2. Permutación: se reasignan los calendarios anuales entre años (todas las permutaciones
     posibles son demasiadas; se toman 1.000 al azar) y se ubica el coeficiente real.
  3. IV con cada Z, con y sin 2025, y junto al conflicto (sobreidentificación).
  4. Exclusión: ¿la fecha de apertura o el largo de la temporada responden al precio de la
     campaña anterior? Si sí, el instrumento está contaminado.

Uso:  python demanda_inversa_cfp.py
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
pd.set_option("display.width", 200)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
HAC = 6
rng = np.random.default_rng(20260901)

# ----------------------------------------------------------------------------- calendario
# Fuente: actas del CFP. «aprox» = la fecha no está en el texto del acta y sale de una nota de
# la Autoridad de Aplicación citada en un acta posterior, o de la fecha de habilitación de los
# buques. «imputada» = no consta en ninguna acta; se usa el punto medio de los años vecinos.
CAL = pd.DataFrame([
    # año  apert.fuera  apert.AVPJM   fin AVPJM     calidad  fuente
    (2013, None,        "2013-05-29", "2013-11-08", "media", "Acta 17/13 (apertura sin fecha; buques habilitados desde 29/05 s/ Acta 46/13) · Acta 37/13 susp. despacho norte 45°S 08/11"),
    (2014, None,        "2014-05-29", "2014-10-31", "alta",  "Acta 19/14 ratifica apertura DNCP 29/05 · Acta 43/14 despacho hasta 18:00 del 31/10"),
    (2015, None,        "2015-06-12", "2015-11-02", "baja",  "Acta 22/15 ratifica apertura SA I-II sin fecha (aprox) · Acta 42/15 nota DNCP 996 del 02/11 (aprox; temporada terminó 19/11 s/ Acta 12/16)"),
    (2016, None,        "2016-05-31", "2016-10-27", "baja",  "Acta 14/16 ratifica nota DNCP 411/16 del 31/05 · fin IMPUTADO: ninguna acta lo registra (delegado a la AA en Acta 23/16)"),
    (2017, None,        "2017-05-19", "2017-10-21", "alta",  "Acta 12/17 apertura 19/05 · Acta 29/17 susp. despacho 0:00 del 21/10"),
    (2018, None,        "2018-05-24", "2018-10-31", "media", "Acta 11/18 prospección; apertura 45°-46°20' aprox 24/05 (título IAyT 69) · Acta 30/18 susp. despacho 20:00 del 31/10"),
    (2019, None,        "2019-06-13", "2019-10-15", "alta",  "Acta 15/19 apertura SA 1.3, 2.5, 2.4 el 13/06 · Acta 29/19 cierre del AVPJM 20:00 del 15/10"),
    (2020, "2020-04-18", "2020-06-18", "2020-10-10", "alta",  "Acta 8/20 levanta suspensión fuera AVPJM 18/04 · Acta 15/20 apertura SA 5-6 18/06 · Acta 26/20 susp. despacho AVPJM 10/10"),
    (2021, "2021-04-17", "2021-06-05", "2021-09-23", "media", "Acta 9/21 fuera AVPJM 17/04 · apertura SA 13-14 nota DNCyFP 04/06, datos desde 05/06 (aprox) · Acta 23/21 susp. despacho AVPJM 23:59 del 23/09"),
    (2022, "2022-04-01", "2022-06-08", "2022-09-21", "alta",  "Acta 6/22 fuera AVPJM 01/04 · Acta 16/22 apertura SA 13-16 nota 08/06 · Acta 27/22 susp. despacho 23:59 del 21/09"),
    (2023, "2023-04-15", "2023-06-02", "2023-09-25", "alta",  "Acta 8/23 fuera AVPJM 07:00 del 15/04 · Acta 16/23 apertura SA 13-15-16 02/06 · Acta 29/23 susp. despacho 23:59 del 25/09"),
    (2024, "2024-03-27", "2024-05-29", "2024-09-19", "alta",  "Acta 1/24 ratifica AA 27/03 · Acta 4/24 apertura 29/05 · cierre SA 15 y prohibición en todo el AVPJM 19/09; prohibición total 28/09 (Acta 17/24)"),
    (2025, "2025-03-17", "2025-07-09", "2025-10-04", "alta",  "Acta 7/25 fuera AVPJM 07:00 del 17/03 · Acta 21/25 SA 12 desde 09/07 · Acta 28/25 susp. despacho 0:00 del 04/10"),
    (2026, "2026-04-15", "2026-05-29", None,         "alta",  "Acta 10/26 fuera AVPJM 15/04 · Acta 15/26 apertura SA 4-5-15-16 29/05 · temporada en curso (última acta 23/26 del 20/08)"),
], columns=["anio", "ap_fuera", "ap_avpjm", "fin_avpjm", "calidad", "fuente"])
for c in ["ap_fuera", "ap_avpjm", "fin_avpjm"]:
    CAL[c] = pd.to_datetime(CAL[c])
# Fuera del AVPJM: abierto todo el año hasta la suspensión provisoria del 08/11/2019.
SUSP_PROV = pd.Timestamp("2019-11-08")
HOY = pd.Timestamp("2026-08-20")     # última acta disponible
# El panel del modelo tiene huecos de precio (ene-jun 2016, jun-nov 2017): el calendario se
# construye sobre el índice mensual COMPLETO y recién después se alinea al panel, si no la
# ventana móvil de doce filas abarca más de doce meses.
IDX = pd.period_range("2013-01", "2026-07", freq="M")


def _dias_mes(idx: pd.PeriodIndex, tramos) -> pd.Series:
    """Días de cada mes cubiertos por al menos un tramo [a, b]."""
    d0 = idx[0].start_time.normalize(); d1 = idx[-1].end_time.normalize()
    dias = pd.date_range(d0, d1, freq="D")
    cub = np.zeros(len(dias), dtype=bool)
    for a, b in tramos:
        if pd.isna(a) or pd.isna(b):
            continue
        cub |= (dias >= a) & (dias <= b)
    s = pd.Series(cub.astype(float), index=dias)
    return s.groupby(dias.to_period("M")).sum().reindex(idx).fillna(0.0)


def calendario_mensual(cal: pd.DataFrame, idx: pd.PeriodIndex) -> pd.DataFrame:
    tr_avpjm = [(r.ap_avpjm, r.fin_avpjm if pd.notna(r.fin_avpjm) else HOY) for r in cal.itertuples()]
    tr_fuera = [(pd.Timestamp("2013-01-01"), SUSP_PROV)]
    for r in cal.itertuples():
        if pd.notna(r.ap_fuera):
            # fuera del AVPJM cierra con la suspensión total; se aproxima con el fin del AVPJM + 7 días
            fin = (r.fin_avpjm + pd.Timedelta(days=7)) if pd.notna(r.fin_avpjm) else HOY
            tr_fuera.append((r.ap_fuera, fin))
    M = pd.DataFrame(index=idx)
    M["d_avpjm"] = _dias_mes(idx, tr_avpjm)
    M["d_nac"] = _dias_mes(idx, tr_avpjm + tr_fuera)
    M["z1"] = M.d_avpjm.rolling(12).sum()
    M["z2"] = M.d_nac.rolling(12).sum()
    return M


def saldo_decisiones(idx: pd.PeriodIndex) -> pd.Series:
    """Z3: aperturas de subárea menos cierres, por mes de vigencia (o de acta si no hay)."""
    c = pd.read_pickle(os.path.join(RAIZ, "..", "cfp", "cod_all.pkl")) if os.path.exists(
        os.path.join(RAIZ, "..", "cfp", "cod_all.pkl")) else pd.read_pickle("/tmp/lango/cfp/cod_all.pkl")
    c = c[c.accion.isin(["apertura_subarea", "cierre_subarea"])].copy()
    f = pd.to_datetime(c.fecha_efectiva.replace("", np.nan), errors="coerce")
    f = f.fillna(pd.to_datetime(c.fecha_acta, errors="coerce"))
    c["per"] = f.dt.to_period("M")
    c["s"] = np.where(c.accion == "apertura_subarea", 1, -1)
    s = c.groupby("per").s.sum().reindex(idx).fillna(0.0)
    return s.rolling(12).sum().rename("z3")


# ----------------------------------------------------------------------------- estimación
def regs(df: pd.DataFrame, Z: list[str], nom: str, iv_extra=None):
    from linearmodels.iv import IV2SLS
    d = df.dropna(subset=["rel", "tan12", "horeca"] + Z).copy()
    d["lq"] = np.log(d.tan12)
    d["lrel"] = np.log(d.rel)
    d["trend"] = np.arange(len(d)) / 12.0
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d.index
    ex = sm.add_constant(pd.concat([d[["horeca", "trend"]], M], axis=1))
    # primera etapa
    fs = sm.OLS(d.lq, pd.concat([ex, d[Z]], axis=1)).fit(cov_type="HAC", cov_kwds={"maxlags": HAC})
    s = " · ".join(f"{z} {fs.params[z]:+.3f} (t {fs.tvalues[z]:+.2f})" for z in Z)
    print(f"   {nom:<38s} N={int(fs.nobs):3d}  1ª etapa: {s}  R²parcial={fs.rsquared:.3f}")
    r = IV2SLS(d.lrel, ex, d[["lq"]], d[Z]).fit(cov_type="kernel", kernel="bartlett")
    f, se = r.params["lq"], r.std_errors["lq"]
    extra = ""
    if len(Z) > 1:
        j = r.sargan
        extra = f"  Sargan p={j.pval:.3f}"
    print(f"   {'':<38s}         IV: f = {f:+.3f}  se {se:.3f}  IC95% [{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]{extra}")
    return fs, r


def regs_nt(df, Z, nom):
    from linearmodels.iv import IV2SLS
    d = df.dropna(subset=["rel", "tan12", "horeca"] + Z).copy()
    d["lq"] = np.log(d.tan12); d["lrel"] = np.log(d.rel)
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float); M.index = d.index
    ex = sm.add_constant(pd.concat([d[["horeca"]], M], axis=1))
    fs = sm.OLS(d.lq, pd.concat([ex, d[Z]], axis=1)).fit(cov_type="HAC", cov_kwds={"maxlags": HAC})
    r = IV2SLS(d.lrel, ex, d[["lq"]], d[Z]).fit(cov_type="kernel", kernel="bartlett")
    f, se = r.params["lq"], r.std_errors["lq"]
    print(f"   {nom:<38s} N={int(fs.nobs):3d}  1ª etapa: {Z[0]} {fs.params[Z[0]]:+.3f} (t {fs.tvalues[Z[0]]:+.2f})")
    print(f"   {'':<38s}         IV: f = {f:+.3f}  se {se:.3f}")


def permutacion(df: pd.DataFrame, n: int = 1000):
    """Reasigna los calendarios anuales (apertura, fin) entre años y reestima la primera etapa y la
    forma reducida. Si la primera etapa real es extrema y la forma reducida no, el calendario mueve
    la cantidad pero no el precio."""
    base = CAL.copy()
    anios = base.anio.tolist()
    d0 = df.dropna(subset=["rel", "tan12", "horeca"]).copy()
    d0["lq"] = np.log(d0.tan12)
    d0["lrel"] = np.log(d0.rel)
    d0["trend"] = np.arange(len(d0)) / 12.0
    M = pd.get_dummies(d0.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d0.index
    ex = sm.add_constant(pd.concat([d0[["horeca", "trend"]], M], axis=1))

    def coef(cal):
        Mc = calendario_mensual(cal, IDX)
        z = np.log(Mc.z1.replace(0, np.nan)).reindex(d0.index)
        ok = z.notna() & np.isfinite(z)
        X = pd.concat([ex[ok], z[ok].rename("z")], axis=1)
        m1 = sm.OLS(d0.lq[ok], X).fit()
        m2 = sm.OLS(d0.lrel[ok], X).fit()
        return m1.params["z"], m2.params["z"]

    fs_real, rf_real = coef(base)
    FS, RF = [], []
    for _ in range(n):
        perm = rng.permutation(len(anios))
        cal = base.copy()
        ap = (base.ap_avpjm - pd.to_datetime(base.anio.astype(str) + "-01-01")).dt.days.values
        fi = (base.fin_avpjm - pd.to_datetime(base.anio.astype(str) + "-01-01")).dt.days.values
        ap, fi = ap[perm], fi[perm]
        cal["ap_avpjm"] = pd.to_datetime(cal.anio.astype(str) + "-01-01") + pd.to_timedelta(ap, unit="D")
        cal["fin_avpjm"] = pd.to_datetime(cal.anio.astype(str) + "-01-01") + pd.to_timedelta(fi, unit="D")
        cal.loc[cal.anio == 2026, "fin_avpjm"] = pd.NaT
        try:
            a, b = coef(cal); FS.append(a); RF.append(b)
        except Exception:
            pass
    FS, RF = np.array(FS), np.array(RF)
    p_fs = (np.abs(FS) >= abs(fs_real)).mean()
    p_rf = (np.abs(RF) >= abs(rf_real)).mean()
    print(f"   primera etapa:  real {fs_real:+.3f} · placebos mediana {np.median(FS):+.3f} "
          f"[p5 {np.percentile(FS, 5):+.3f}, p95 {np.percentile(FS, 95):+.3f}] · p bilateral {p_fs:.3f}")
    print(f"   forma reducida: real {rf_real:+.3f} · placebos mediana {np.median(RF):+.3f} "
          f"[p5 {np.percentile(RF, 5):+.3f}, p95 {np.percentile(RF, 95):+.3f}] · p bilateral {p_rf:.3f}")
    print(f"   ({len(FS)} permutaciones)")
    return fs_real, rf_real, FS, RF


def exclusion(df: pd.DataFrame):
    """¿El calendario responde al precio de la campaña anterior?"""
    tan = pd.read_pickle("/tmp/lango/cfp/tan_mensual.pkl")
    print("\n   Regresión anual: fecha de apertura del AVPJM (día del año) y largo de temporada sobre el")
    print("   precio relativo medio de la campaña ANTERIOR (jul-jun) y sobre la captura del año anterior.")
    an = []
    for r in CAL.itertuples():
        y = r.anio
        if pd.isna(r.fin_avpjm):
            continue
        prev = df.loc[f"{y - 1}-07":f"{y}-06"]
        an.append({"anio": y,
                   "apertura_doy": (r.ap_avpjm - pd.Timestamp(f"{y}-01-01")).days,
                   "largo": (r.fin_avpjm - r.ap_avpjm).days,
                   "lrel_prev": np.log(prev.rel.mean()),
                   "lq_prev": np.log(tan.loc[f"{y - 1}-01":f"{y - 1}-12"].sum())})
    A = pd.DataFrame(an).set_index("anio").replace([np.inf, -np.inf], np.nan).dropna()
    print(A.round(3).to_string())
    for yv in ["apertura_doy", "largo"]:
        m = sm.OLS(A[yv], sm.add_constant(A[["lrel_prev", "lq_prev"]])).fit(cov_type="HC1")
        print(f"   {yv:<13s}: precio prev {m.params.lrel_prev:+.1f} días por unidad de log (t {m.tvalues.lrel_prev:+.2f}) · "
              f"captura prev {m.params.lq_prev:+.1f} (t {m.tvalues.lq_prev:+.2f}) · R² {m.rsquared:.2f} · N={int(m.nobs)}")
        m2 = sm.OLS(A[yv], sm.add_constant(A[["lrel_prev"]])).fit(cov_type="HC1")
        print(f"   {'':<13s}  sólo precio: {m2.params.lrel_prev:+.1f} (t {m2.tvalues.lrel_prev:+.2f}) · corr {A[yv].corr(A.lrel_prev):+.2f}")
    return A


def iv_campana(df: pd.DataFrame):
    """Modelo de campaña (como 6.2 del informe) con la fecha de apertura del AVPJM como instrumento
    de la captura. N = campañas con calendario y precio."""
    from linearmodels.iv import IV2SLS
    tan = pd.read_pickle("/tmp/lango/cfp/tan_mensual.pkl")
    filas = []
    for r in CAL.itertuples():
        y = r.anio
        if pd.isna(r.fin_avpjm):
            continue
        cap = tan.loc[f"{y}-04":f"{y}-10"].sum()
        ven = df.loc[f"{y}-07":f"{y + 1}-06"].dropna(subset=["p_tan"])
        if cap <= 0 or len(ven) < 9:
            continue
        p = (ven.p_tan * ven.q_exp_t).sum() / ven.q_exp_t.sum()
        filas.append({"anio": y, "lq": np.log(cap),
                      "lrel": np.log(p / ven.eurusd.mean() / ven.van_eur_kg.mean()),
                      "horeca": ven.horeca.mean(),
                      "ap_doy": (r.ap_avpjm - pd.Timestamp(f"{y}-01-01")).days,
                      "largo": (r.fin_avpjm - r.ap_avpjm).days,
                      "conflicto": float(y == 2025)})
    C = pd.DataFrame(filas).set_index("anio")
    C["trend"] = np.arange(len(C))
    print(f"   campañas disponibles: {len(C)} ({C.index.min()}-{C.index.max()})")
    for Z, nom in [(["ap_doy"], "apertura (día del año)"), (["largo"], "largo de temporada"),
                   (["ap_doy"], "apertura, sin 2025")]:
        D = C if "sin" not in nom else C[C.index != 2025]
        ex = sm.add_constant(D[["horeca", "trend"]])
        fs = sm.OLS(D.lq, pd.concat([ex, D[Z]], axis=1)).fit(cov_type="HC1")
        r = IV2SLS(D.lrel, ex, D[["lq"]], D[Z]).fit(cov_type="robust")
        f, se = r.params["lq"], r.std_errors["lq"]
        print(f"   {nom:<28s} N={len(D):2d}  1ª etapa {Z[0]} {fs.params[Z[0]]:+.4f} (t {fs.tvalues[Z[0]]:+.2f})  "
              f"→ IV f = {f:+.3f}  se {se:.3f}")
    ols = sm.OLS(C.lrel, sm.add_constant(C[["lq", "horeca", "trend"]])).fit(cov_type="HC1")
    print(f"   {'MCO de campaña (referencia)':<28s} N={len(C):2d}  f = {ols.params.lq:+.3f}  se {ols.bse.lq:.3f}")
    return C


def main():
    df = pd.read_pickle("/tmp/lango/cfp/df_modelo.pkl")
    Mc = calendario_mensual(CAL, IDX)
    z3 = saldo_decisiones(IDX)
    df = df.join(Mc.reindex(df.index)).join(z3.reindex(df.index))
    df["lz1"] = np.log(df.z1.replace(0, np.nan))
    df["lz2"] = np.log(df.z2.replace(0, np.nan))

    print("=" * 100)
    print("EL CALENDARIO DEL CFP COMO INSTRUMENTO")
    print("=" * 100)
    T = CAL.copy()
    T["largo_avpjm"] = (T.fin_avpjm - T.ap_avpjm).dt.days
    T["apertura_doy"] = (T.ap_avpjm - pd.to_datetime(T.anio.astype(str) + "-01-01")).dt.days
    tan = pd.read_pickle("/tmp/lango/cfp/tan_mensual.pkl")
    cap = tan.groupby(tan.index.year).sum()
    T["captura_tan_t"] = T.anio.map(cap).round(0)
    print("\nTemporada dentro del AVPJM, por año:")
    print(T[["anio", "ap_fuera", "ap_avpjm", "fin_avpjm", "largo_avpjm", "captura_tan_t", "calidad"]]
          .to_string(index=False))
    s = T.dropna(subset=["largo_avpjm"])
    print(f"\n   largo de temporada: media {s.largo_avpjm.mean():.0f} días · desvío {s.largo_avpjm.std():.0f} · "
          f"rango {s.largo_avpjm.min():.0f}-{s.largo_avpjm.max():.0f}")
    print(f"   correlación anual largo × captura tangonera: {s.largo_avpjm.corr(s.captura_tan_t):+.2f}  ·  "
          f"sin 2025: {s[s.anio != 2025].largo_avpjm.corr(s[s.anio != 2025].captura_tan_t):+.2f}")
    print(f"   correlación anual apertura (día del año) × captura: {s.apertura_doy.corr(s.captura_tan_t):+.2f}  ·  "
          f"sin 2025: {s[s.anio != 2025].apertura_doy.corr(s[s.anio != 2025].captura_tan_t):+.2f}")

    print("\n" + "=" * 100)
    print("1. PRIMERA ETAPA E IV — log(tan12) sobre cada instrumento, con los controles del modelo")
    print("=" * 100)
    regs(df, ["iv_conf"], "referencia: ventana del conflicto")
    regs(df, ["lz1"], "Z1 log días AVPJM abierto (12m)")
    regs(df, ["lz2"], "Z2 log días aguas nacionales (12m)")
    regs(df, ["z3"], "Z3 saldo aperturas−cierres SA (12m)")
    print("\n   Z1 sin tendencia lineal (¿la tendencia se come la variación del calendario?):")
    df_nt = df.copy()
    regs_nt(df_nt, ["lz1"], "Z1 sin trend")
    print("\n   Sin 2025 ni 2026 (la variación que NO es el conflicto):")
    d24 = df[df.index < pd.Period("2025-04")]
    regs(d24, ["lz1"], "Z1 hasta mar-2025")
    regs(d24, ["lz2"], "Z2 hasta mar-2025")
    regs(d24, ["z3"], "Z3 hasta mar-2025")
    print("\n   Conflicto + calendario (sobreidentificado):")
    regs(df, ["iv_conf", "lz1"], "conflicto + Z1")
    regs(df, ["iv_conf", "z3"], "conflicto + Z3")

    print("\n" + "=" * 100)
    print("2. PERMUTACIÓN DEL CALENDARIO — se barajan (apertura, fin) entre años, 1.000 veces")
    print("=" * 100)
    permutacion(df)
    print("   Sin 2025 ni 2026:")
    permutacion(d24)

    print("\n" + "=" * 100)
    print("2b. MODELO DE CAMPAÑA con la fecha de apertura como instrumento")
    print("=" * 100)
    iv_campana(df)

    print("\n" + "=" * 100)
    print("3. EXCLUSIÓN — ¿el CFP responde al precio?")
    print("=" * 100)
    exclusion(df)

    df[["tan_t", "tan12", "rel", "horeca", "iv_conf", "d_avpjm", "d_nac", "z1", "z2", "z3"]].to_pickle(
        "/tmp/lango/cfp/panel_cfp.pkl")
    return df, T


if __name__ == "__main__":
    main()
