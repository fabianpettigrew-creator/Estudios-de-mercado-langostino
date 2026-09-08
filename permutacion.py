# -*- coding: utf-8 -*-
"""Inferencia de diseño para f: test de permutación sobre la ventana del conflicto.

El problema. La estimación preferida del modelo de demanda inversa (T5 de
`demanda_inversa_tangonera.py`) es un IV cuyo único instrumento es una variable
indicadora de la ventana abr-2025 a mar-2026, en la que el conflicto gremial
deprimió la captura acumulada de doce meses. El F de primera etapa es 61, pero
eso mide la fuerza del ajuste, no cuántos shocks independientes hay: hay UNO. El
error estándar de 0,081 y el intervalo [−0,342, −0,026] tratan los 138 meses
como observaciones independientes, y con un solo episodio esa asintótica no
aplica. El síntoma ya está en el estudio: sacar la campaña 2025/2026 lleva f de
−0,247 a −0,024 en el modelo de campaña.

El test. Se reasigna la ventana del instrumento a todas las fechas alternativas
posibles de la muestra, se reestima el mismo IV con cada ventana falsa, y se
ubica la estimación real dentro de la distribución de placebos. El p-valor sale
del diseño —de cuán rara es la ventana verdadera entre todas las ventanas
posibles— y no de un supuesto distribucional. Es la inferencia que corresponde a
un diseño de un solo shock (Fisher; Conley y Taber, 2011, para pocas unidades
tratadas).

Tres estadísticos, porque cada uno responde una pregunta distinta:

  primera etapa   ¿la ventana real deprime la cantidad más que una ventana
                  cualquiera? Si no, el instrumento no tiene nada de especial.
  forma reducida  ¿el precio relativo sube en la ventana real más que en una
                  ventana cualquiera? Es el efecto que el IV después divide.
  f (2SLS)        el cociente de los dos. Es el número que se cita, pero con
                  primera etapa débil se vuelve inestable, así que se reporta
                  también la distribución condicionada a F ≥ 10.

Dos universos de placebos:

  todos        cualquier mes de inicio. Máximo número de placebos, pero las
               ventanas quedan desalineadas del calendario de zafra.
  abril        sólo ventanas que arrancan en abril, igual que la real. Son
               pocas —una por año— pero perfectamente comparables: mismo
               alineamiento estacional, misma relación con la temporada.

Las ventanas que se solapan con la real se excluyen del nulo: contienen el shock
verdadero y no son placebos.

Uso:  python permutacion.py
Salida: consola + salidas/permutacion_f.xlsx
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

LARGO = 12                                    # meses de la ventana, igual que la real
REAL = (pd.Period("2025-04", "M"), pd.Period("2026-03", "M"))


def base():
    """Reproduce exactamente el panel mensual sobre el que corre T5."""
    df, _ = T.panel()
    d = df.dropna(subset=["p_eur", "tan12", "van_eur_kg", "horeca_ue"]).copy()
    for c, n in [("p_eur", "lp"), ("van_eur_kg", "lvan"),
                 ("tan12", "lq"), ("rel", "lrel")]:
        d[n] = np.log(d[c])
    d["trend"] = np.arange(len(d)) / 12.0
    M = pd.get_dummies(d.index.month, prefix="m", drop_first=True).astype(float)
    M.index = d.index
    return d, M


def estimar(d, M, z):
    """IV2SLS idéntico al T5, con `z` como instrumento. Devuelve f, F, y las dos
    mitades del cociente: primera etapa y forma reducida."""
    dd = pd.concat([d[["lrel", "lq", "horeca", "trend"]], M], axis=1).copy()
    dd["z"] = pd.Series(z).reindex(dd.index).astype(float)
    dd = dd.dropna()
    if dd.z.nunique() < 2:
        return None
    ex = sm.add_constant(dd[["horeca", "trend"] + list(M.columns)])
    try:
        iv = IV2SLS(dd.lrel, ex, dd[["lq"]], dd[["z"]]).fit(
            cov_type="kernel", kernel="bartlett")
        f = float(iv.params["lq"])
        F1 = float(iv.first_stage.diagnostics["f.stat"].iloc[0])
    except Exception:
        return None
    # primera etapa y forma reducida por MCO, para leer el cociente por separado
    Xz = sm.add_constant(pd.concat([dd[["z", "horeca", "trend"]], dd[list(M.columns)]],
                                   axis=1))
    pe = sm.OLS(dd.lq, Xz).fit(cov_type="HAC", cov_kwds={"maxlags": T.HAC})
    fr = sm.OLS(dd.lrel, Xz).fit(cov_type="HAC", cov_kwds={"maxlags": T.HAC})
    return {"f": f, "F1": F1, "primera_etapa": float(pe.params["z"]),
            "forma_reducida": float(fr.params["z"]), "n": int(iv.nobs)}


def main() -> None:
    d, M = base()
    idx = d.index
    print(f"Panel mensual: {idx.min()}..{idx.max()} · N = {len(d)}")

    z_real = pd.Series(((idx >= REAL[0]) & (idx <= REAL[1])).astype(float), index=idx)
    real = estimar(d, M, z_real)
    print(f"\nVentana real {REAL[0]}..{REAL[1]} (replicación de T5):")
    print(f"  f = {real['f']:+.3f} · primera etapa F = {real['F1']:.1f} · "
          f"coef 1ª etapa = {real['primera_etapa']:+.3f} · "
          f"forma reducida = {real['forma_reducida']:+.3f} · N = {real['n']}")

    filas = []
    for i in range(len(idx) - LARGO + 1):
        a, b = idx[i], idx[i + LARGO - 1]
        if not (b < REAL[0] or a > REAL[1]):     # se solapa con la real: no es placebo
            continue
        z = pd.Series(((idx >= a) & (idx <= b)).astype(float), index=idx)
        r = estimar(d, M, z)
        if r is None:
            continue
        r.update({"inicio": str(a), "fin": str(b), "mes_inicio": a.month})
        filas.append(r)
    P = pd.DataFrame(filas)
    print(f"\nPlacebos evaluados: {len(P)} ventanas de {LARGO} meses "
          "(excluidas las que se solapan con la real)")

    def _pv(sub, campo, valor, cola="menor"):
        v = sub[campo].to_numpy()
        k = (v <= valor).sum() if cola == "menor" else (v >= valor).sum()
        return (k + 1) / (len(v) + 1)

    for nombre, sub in [("TODOS los meses de inicio", P),
                        ("sólo ventanas que arrancan en ABRIL", P[P.mes_inicio == 4]),
                        ("todos, condicionado a F ≥ 10", P[P.F1 >= 10])]:
        if not len(sub):
            continue
        print("\n" + "-" * 78)
        print(f"{nombre}   (n = {len(sub)})")
        pf = _pv(sub, "f", real["f"], "menor")
        ppe = _pv(sub, "primera_etapa", real["primera_etapa"], "menor")
        pfr = _pv(sub, "forma_reducida", real["forma_reducida"],
                  "mayor" if real["forma_reducida"] > 0 else "menor")
        print(f"  f:               real {real['f']:+.3f} · placebos mediana "
              f"{sub.f.median():+.3f}, p5 {sub.f.quantile(.05):+.3f}, "
              f"p95 {sub.f.quantile(.95):+.3f}  → p = {pf:.3f}")
        print(f"  primera etapa:   real {real['primera_etapa']:+.3f} · placebos mediana "
              f"{sub.primera_etapa.median():+.3f}, p5 "
              f"{sub.primera_etapa.quantile(.05):+.3f}  → p = {ppe:.3f}")
        print(f"  forma reducida:  real {real['forma_reducida']:+.3f} · placebos mediana "
              f"{sub.forma_reducida.median():+.3f}, p95 "
              f"{sub.forma_reducida.quantile(.95):+.3f}  → p = {pfr:.3f}")
        print(f"  F de 1ª etapa:   real {real['F1']:.1f} · placebos mediana "
              f"{sub.F1.median():.1f}, máx {sub.F1.max():.1f}, "
              f"con F≥10: {(sub.F1 >= 10).sum()}/{len(sub)}")

    print("\n" + "-" * 78)
    print("Los diez placebos con f más negativo (¿hay ventanas falsas tan «buenas»?):")
    print(P.nsmallest(10, "f")[["inicio", "fin", "f", "F1", "primera_etapa",
                                "forma_reducida"]].round(3).to_string(index=False))

    out = os.path.join(RAIZ, "salidas", "permutacion_f.xlsx")
    try:
        with pd.ExcelWriter(out) as w:
            pd.DataFrame([real]).to_excel(w, sheet_name="real", index=False)
            P.to_excel(w, sheet_name="placebos", index=False)
        print(f"\nGuardado: {out}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {out} (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
