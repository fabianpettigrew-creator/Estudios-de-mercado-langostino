# -*- coding: utf-8 -*-
"""IV con las actas del CFP como instrumento de la cantidad.

Qué cambia respecto de T5. Hasta acá el único instrumento era la ventana del
conflicto de 2025 —un episodio— y el test de permutación mostró que con un
solo shock el f queda en la mediana de su distribución de placebos. Las 547
actas del CFP dan 165 decisiones de oferta, 55 con fecha de vigencia, en los
catorce años. Con eso se construye un instrumento que varía todos los años.

Construcción. El modelo usa como cantidad `tan12`, la captura acumulada de
doce meses. Un cierre que rige en el mes t deprime la captura de t y de los
meses siguientes, así que la construcción que calza es la suma móvil de doce
meses de decisiones de cierre. Se prueban tres variantes —cierres, aperturas,
neto— y se reporta la primera etapa de cada una. Se elige por fuerza de
primera etapa, que es legítimo; elegir por el f de la segunda no lo sería.

Las fechas «hasta» de un cierre («podrán operar hasta las 18:00 del 31 de
octubre») marcan el último día de pesca: el cierre empieza al día siguiente.

Permutación. Para el instrumento del CFP el placebo natural es reasignar al
azar los meses de los 55 eventos, conservando su número, y reestimar. B = 500.
Si el f real cae en la cola de esa distribución, el instrumento identifica; si
cae en el medio, no.

Robustez: los eventos cuya fecha salió del contexto (20 de 55) pueden
pertenecer a otra decisión. Se corre además sólo con los 35 de fecha propia.

Uso:  python iv_cfp.py
Salida: consola + salidas/iv_cfp.xlsx
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
import demanda_inversa_tangonera as T   # noqa: E402

B = 500
SEMILLA = 20260830
REAL = (pd.Period("2025-04", "M"), pd.Period("2026-03", "M"))


# ------------------------------------------------------------------ datos
def panel():
    df, _ = T.panel()
    d = df.dropna(subset=["p_eur", "tan12", "van_eur_kg", "horeca_ue"]).copy()
    for c, n in [("p_eur", "lp"), ("van_eur_kg", "lvan"), ("tan12", "lq"),
                 ("rel", "lrel")]:
        d[n] = np.log(d[c])
    d["trend"] = np.arange(len(d)) / 12.0
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d.index
    d["iv_conf"] = ((d.index >= REAL[0]) & (d.index <= REAL[1])).astype(float)
    return d, M


def eventos(solo_propio: bool = False) -> pd.DataFrame:
    e = pd.read_excel(os.path.join(RAIZ, "salidas", "cfp_langostino_decisiones.xlsx"),
                      sheet_name="eventos_oferta")
    e = e.dropna(subset=["fecha_vigencia"]).copy()
    if solo_propio:
        e = e[e.origen_fecha == "propio"]
    f = pd.to_datetime(e.fecha_vigencia, errors="coerce")
    # «hasta» = último día de pesca: el cierre rige desde el día siguiente
    f = f.where(e.clase_fecha != "hasta", f + pd.Timedelta(days=1))
    e["per"] = f.dt.to_period("M")
    e = e.dropna(subset=["per"])
    e["cierre"] = e.accion.isin(["cierre", "suspensión"]).astype(int)
    e["apertura"] = e.accion.isin(["apertura", "prospección", "prórroga"]).astype(int)
    return e[["per", "accion", "cierre", "apertura", "origen_fecha"]]


def instrumentos(e: pd.DataFrame, idx: pd.PeriodIndex) -> pd.DataFrame:
    """Series mensuales de decisiones y sus sumas móviles de doce meses."""
    todo = pd.period_range(min(idx.min(), e.per.min()), idx.max(), freq="M")
    g = e.groupby("per")[["cierre", "apertura"]].sum().reindex(todo, fill_value=0)
    z = pd.DataFrame(index=todo)
    z["cierres_12"] = g.cierre.rolling(12, min_periods=1).sum()
    z["aperturas_12"] = g.apertura.rolling(12, min_periods=1).sum()
    z["neto_12"] = z.cierres_12 - z.aperturas_12
    z["cierre_mes"] = (g.cierre > 0).astype(float)
    return z.reindex(idx)


# ------------------------------------------------------------------ modelo
def primera_etapa(d, M, z: pd.Series) -> dict:
    dd = pd.concat([d[["lq", "horeca", "trend"]], M], axis=1).copy()
    dd["z"] = z.reindex(dd.index)
    dd = dd.dropna()
    X = sm.add_constant(dd.drop(columns=["lq"]))
    m = sm.OLS(dd.lq, X).fit(cov_type="HAC", cov_kwds={"maxlags": T.HAC})
    return {"coef": float(m.params["z"]), "t": float(m.tvalues["z"]),
            "F": float(m.tvalues["z"] ** 2), "n": int(m.nobs)}


def iv(d, M, Z: pd.DataFrame) -> dict:
    dd = pd.concat([d[["lrel", "lq", "horeca", "trend"]], M, Z], axis=1).dropna()
    ex = sm.add_constant(dd[["horeca", "trend"] + list(M.columns)])
    r = IV2SLS(dd.lrel, ex, dd[["lq"]], dd[list(Z.columns)]).fit(
        cov_type="kernel", kernel="bartlett")
    out = {"f": float(r.params["lq"]), "se": float(r.std_errors["lq"]),
           "n": int(r.nobs),
           "F1": float(r.first_stage.diagnostics["f.stat"].iloc[0])}
    if len(Z.columns) > 1:
        try:
            j = r.sargan
            out["J"] = float(j.stat)
            out["J_p"] = float(j.pval)
        except Exception:
            pass
    return out


def permutar(d, M, e: pd.DataFrame, col: str, f_real: float, rng) -> dict:
    """Reasigna al azar los meses de los eventos y reestima. Devuelve la
    distribución de f y el p-valor de diseño (una cola, f <= f_real)."""
    idx = d.index
    meses = list(idx)
    fs, F1s = [], []
    for _ in range(B):
        ep = e.copy()
        ep["per"] = rng.choice(meses, size=len(ep), replace=True)
        Z = instrumentos(ep, idx)[[col]]
        try:
            r = iv(d, M, Z)
            fs.append(r["f"]); F1s.append(r["F1"])
        except Exception:
            continue
    fs, F1s = np.array(fs), np.array(F1s)
    return {"n_placebos": len(fs),
            "p_f": float(((fs <= f_real).sum() + 1) / (len(fs) + 1)),
            "mediana": float(np.median(fs)),
            "p5": float(np.percentile(fs, 5)), "p95": float(np.percentile(fs, 95)),
            "F1_mediana": float(np.median(F1s)), "F1_p95": float(np.percentile(F1s, 95))}


# ------------------------------------------------------------------ corrida
def main() -> None:
    rng = np.random.default_rng(SEMILLA)
    d, M = panel()
    print(f"Panel: {d.index.min()}..{d.index.max()} · N = {len(d)}")

    filas, res = [], {}
    for etiqueta, solo in [("todos los fechados", False), ("sólo fecha propia", True)]:
        e = eventos(solo)
        Z = instrumentos(e, d.index)
        print("\n" + "=" * 78)
        print(f"EVENTOS: {etiqueta} · {len(e)} eventos · "
              f"{int(e.cierre.sum())} cierres/suspensiones · "
              f"{int(e.apertura.sum())} aperturas/prospecciones")
        print(f"  meses con algún cierre en la ventana: {int(Z.cierre_mes.sum())} de {len(Z)}")

        print("\n  Primera etapa (lq sobre z + controles), por variante:")
        pe = {}
        for col in ["cierres_12", "aperturas_12", "neto_12", "cierre_mes"]:
            pe[col] = primera_etapa(d, M, Z[col])
            print(f"    {col:14s} coef {pe[col]['coef']:+.4f}  t {pe[col]['t']:+.2f}  "
                  f"F {pe[col]['F']:6.1f}")
        # se elige por fuerza de primera etapa, con el signo esperado (cierres
        # deprimen la cantidad; aperturas la suben; neto la deprime)
        cand = {c: pe[c]["F"] for c in ["cierres_12", "neto_12"] if pe[c]["coef"] < 0}
        cand.update({c: pe[c]["F"] for c in ["aperturas_12"] if pe[c]["coef"] > 0})
        if not cand:
            print("  NINGUNA variante tiene el signo esperado en primera etapa.")
            mejor = "cierres_12"
        else:
            mejor = max(cand, key=cand.get)
        print(f"  → instrumento elegido: {mejor} (F = {pe[mejor]['F']:.1f})")

        r_cfp = iv(d, M, Z[[mejor]])
        r_conf = iv(d, M, d[["iv_conf"]])
        r_ambos = iv(d, M, pd.concat([Z[[mejor]], d[["iv_conf"]]], axis=1))
        print("\n  IV 2SLS sobre el precio relativo:")
        for nom, r in [("sólo ventana del conflicto (T5)", r_conf),
                       (f"sólo CFP ({mejor})", r_cfp),
                       ("CFP + conflicto", r_ambos)]:
            extra = f"  J = {r['J']:.2f} (p {r['J_p']:.3f})" if "J" in r else ""
            print(f"    {nom:34s} f {r['f']:+.3f}  se {r['se']:.3f}  "
                  f"F1 {r['F1']:6.1f}{extra}")

        print(f"\n  Permutación ({B} reasignaciones al azar de los meses de los eventos):")
        pm = permutar(d, M, e, mejor, r_cfp["f"], rng)
        print(f"    f real {r_cfp['f']:+.3f} · placebos mediana {pm['mediana']:+.3f}, "
              f"p5 {pm['p5']:+.3f}, p95 {pm['p95']:+.3f}  → p = {pm['p_f']:.3f}")
        print(f"    F1 real {r_cfp['F1']:.1f} · placebos mediana {pm['F1_mediana']:.1f}, "
              f"p95 {pm['F1_p95']:.1f}")

        for nom, r in [("T5 conflicto", r_conf), ("CFP", r_cfp), ("CFP+conflicto", r_ambos)]:
            filas.append({"muestra": etiqueta, "instrumento": nom, **r})
        res[etiqueta] = {"pe": pe, "mejor": mejor, "perm": pm}

    R = pd.DataFrame(filas)
    out = os.path.join(RAIZ, "salidas", "iv_cfp.xlsx")
    try:
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            R.to_excel(w, sheet_name="iv", index=False)
            pd.DataFrame([{"muestra": k, **v["perm"], "instrumento": v["mejor"]}
                          for k, v in res.items()]).to_excel(w, sheet_name="permutacion",
                                                             index=False)
            pd.DataFrame([{"muestra": k, "variante": c, **pe}
                          for k, v in res.items() for c, pe in v["pe"].items()]
                         ).to_excel(w, sheet_name="primera_etapa", index=False)
        print(f"\nGuardado: {out}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {out}")


if __name__ == "__main__":
    main()
