# -*- coding: utf-8 -*-
"""Índice hedónico de precio del langostino entero L1 (FOB origen, USD/kg).

Problema que resuelve. La serie que hoy alimenta `pronostico.py --l1` es el
ratio Σfob/Σkg del mes. Ese ratio se mueve por COMPOSICIÓN DE DESTINO aunque
ningún precio haya cambiado: un mes con más China y menos España baja el
promedio sin que nadie haya bajado un centavo. Ese movimiento espurio es ruido
en la variable dependiente, y ruido en la dependiente infla el RMSE del modelo
y empuja el U de Theil hacia 1 — que es justamente el veredicto que hoy tiene
el L1 en tiempos normales (U 0,96/0,91/0,90 pre-paro).

Especificación (índice de dummies temporales, ponderado por kilos):

    log p_i = α + Σ_t δ_t D_t + γ' destino_i + ε_i        peso = kg_i

Los δ_t son el índice a mezcla de destino constante. Se estima por WLS con
pesos = kilos (es un índice de precio de exportación: lo que importa es el
precio al que se movió el volumen, no el promedio de las facturas) y errores
HC1. El nivel se normaliza para que el promedio ponderado del índice coincida
con el del ratio ingenuo, así ambas series son directamente comparables y el
índice queda en USD/kg de verdad, no en números índice.

Decisiones de depuración, todas reportadas en pantalla con su costo en filas
y en kilos:

  envase   — 100% nulo en el entero L1 (el sufijo SIM que lo codifica sólo
             existe en 0306.17.90, que es cola). No entra.
  ruta     — s/d en el 100% de 2013-2016 y el 85% de 2017. Meterla con "s/d"
             como categoría la vuelve casi colineal con ese período y
             contamina los δ_t de esos años. No entra en la principal; se
             estima aparte sobre 2018+ como robustez (--robustez).
  outliers — se excluye fob fuera de [3, 15] USD/kg y embarques de menos de
             500 kg. Son muestras, ajustes y errores de tipeo: juntos no
             llegan al 0,1% del volumen. El recorte se reporta y hay
             sensibilidad sin recorte en --robustez.
  destino  — se agrupan en "Otros" los destinos con menos de 0,5% de los
             kilos o menos de 50 filas. Un efecto fijo estimado sobre tres
             despachos es ruido con nombre propio.

Limitación conocida: γ (el premium de cada destino) se supone constante en
trece años. La robustez lo deja variar entre pre y post 2020.

Uso:  python hedonico.py [--robustez] [--backtest]
      --robustez  corre las especificaciones alternativas y las compara
      --backtest  pasa el índice por el MISMO backtest de pronostico.py y
                  muestra el U de Theil de las dos series una al lado de la otra

Salida: consola + salidas/indice_hedonico_l1.xlsx + salidas/indice_hedonico_l1.md
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.abspath(__file__))

FOB_MIN, FOB_MAX = 3.0, 15.0     # USD/kg; fuera de esto no es entero L1
KG_MIN = 500.0                   # embarques menores son muestras, no comercio
DEST_MIN_SHARE = 0.005           # 0,5% de los kilos
DEST_MIN_N = 50                  # filas


# ------------------------------------------------------------------ datos
def cargar_micro(pres: str = "entero", cal: str = "L1",
                 recortar: bool = True, verbose: bool = True,
                 ruta: str | None = None, desde: int | None = None) -> pd.DataFrame:
    """Micro-datos transaccionales de Softrade, filtrados y con el destino
    agrupado. Reporta el costo de cada filtro en filas y en kilos.

    ruta='a bordo' aísla el producto de la flota congeladora tangonera, que se
    elabora y congela a bordo y se desembarca listo para exportar. El SA00
    ('en tierra') es otro producto: entero de flota fresquera, procesado en
    planta. Los dos son contra-estacionales (el de a bordo sigue al desembarque
    tangonero, que pica jun-oct; el de tierra sigue al fresquero, que pica
    dic-ene) y el precio difiere ~12%, así que mezclarlos mete en la serie una
    variación que ningún regresor de oferta tangonera puede explicar.
    La bandera SA sólo existe desde 2018: con ruta se fuerza desde=2018.
    """
    from fuentes import expo

    d = expo.cargar_todos()
    d = d[(d.pres == pres) & (d.cal == cal)].copy()
    if ruta is not None:
        desde = max(desde or 0, 2018)   # antes de 2018 la bandera SA es s/d
    if desde is not None:
        d = d[d.anio >= desde]
    n0, kg0 = len(d), d.kg.sum()
    if ruta is not None:
        pre = len(d)
        d = d[d.ruta == ruta].copy()
        if verbose:
            print(f"Corte de ruta '{ruta}' desde {desde}: quedan {len(d):,} "
                  f"de {pre:,} filas")

    pasos = []

    def _paso(nombre, mask):
        nonlocal d
        n, kg = len(d), d.kg.sum()
        d = d[mask(d)].copy()
        pasos.append({"filtro": nombre, "filas_fuera": n - len(d),
                      "kg_fuera": kg - d.kg.sum(),
                      "%_kg_fuera": (kg - d.kg.sum()) / kg0 * 100})

    _paso("kg y fob positivos", lambda x: (x.kg > 0) & (x.fob > 0))
    if recortar:
        _paso(f"fob fuera de [{FOB_MIN:.0f}, {FOB_MAX:.0f}] USD/kg",
              lambda x: x.fob.between(FOB_MIN, FOB_MAX))
        _paso(f"embarque < {KG_MIN:.0f} kg", lambda x: x.kg >= KG_MIN)

    d["per"] = pd.PeriodIndex(
        d.anio.astype(str) + "-" + d.mes.astype(str).str.zfill(2), freq="M")

    # Agrupación de destinos: los chicos van a "Otros".
    por_dest = d.groupby("destino").agg(kg=("kg", "sum"), n=("kg", "size"))
    grandes = por_dest[(por_dest.kg / por_dest.kg.sum() >= DEST_MIN_SHARE)
                       & (por_dest.n >= DEST_MIN_N)].index
    d["dest_g"] = d.destino.where(d.destino.isin(grandes), "Otros")

    if verbose:
        print(f"Micro-datos {pres} {cal}: {n0:,} filas / {kg0/1e6:,.1f} kt iniciales")
        print(pd.DataFrame(pasos).round(3).to_string(index=False))
        print(f"  quedan {len(d):,} filas / {d.kg.sum()/1e6:,.1f} kt "
              f"({d.kg.sum()/kg0*100:.2f}% del volumen)")
        print(f"  destinos con efecto fijo propio ({len(grandes)}): "
              f"{', '.join(sorted(grandes))}")
        print(f"  a 'Otros': {d.destino.nunique() - len(grandes)} destinos, "
              f"{d[d.dest_g=='Otros'].kg.sum()/d.kg.sum()*100:.1f}% de los kilos\n")
    return d


# ------------------------------------------------------------------ modelo
def estimar(d: pd.DataFrame, con_ruta: bool = False,
            dest_por_era: bool = False, ponderar: str = "kg") -> dict:
    """WLS de log(precio unitario) sobre dummies de mes y de destino.

    Devuelve dict con la serie del índice (USD/kg), el error estándar de cada
    δ_t (en log), y los estadísticos de la regresión.
    """
    y = np.log(d.fob.to_numpy())
    w = {"kg": d.kg.to_numpy(),
         "sqrt_kg": np.sqrt(d.kg.to_numpy()),
         "ninguno": np.ones(len(d))}[ponderar]

    meses = pd.PeriodIndex(sorted(d.per.unique()), freq="M")
    base_mes = meses[0]                       # δ del primer mes = 0
    base_dest = (d.groupby("dest_g").kg.sum().idxmax())   # España, el más grande

    X = pd.get_dummies(d.per.astype(str), prefix="m", dtype=float).drop(
        columns=[f"m_{base_mes}"])
    cols_mes = list(X.columns)

    if dest_por_era:
        era = np.where(d.anio >= 2020, "post", "pre")
        dg = pd.Series(d.dest_g.to_numpy() + "_" + era, index=d.index)
        D = pd.get_dummies(dg, prefix="d", dtype=float)
        D = D.drop(columns=[c for c in D.columns if c.startswith(f"d_{base_dest}_")])
    else:
        D = pd.get_dummies(d.dest_g, prefix="d", dtype=float).drop(
            columns=[f"d_{base_dest}"])
    X = pd.concat([X.reset_index(drop=True), D.reset_index(drop=True)], axis=1)

    if con_ruta:
        R = pd.get_dummies(d.ruta, prefix="r", dtype=float).drop(columns=["r_a bordo"])
        X = pd.concat([X, R.reset_index(drop=True)], axis=1)

    X = sm.add_constant(X, has_constant="add")
    res = sm.WLS(y, X.to_numpy(dtype=float), weights=w).fit(cov_type="HC1")
    nom = list(X.columns)

    # δ_t en log y su SE. El mes base tiene δ=0 por construcción.
    delta = pd.Series(0.0, index=meses, dtype=float)
    se = pd.Series(np.nan, index=meses, dtype=float)
    for c in cols_mes:
        p = pd.Period(c[2:], freq="M")
        j = nom.index(c)
        delta[p], se[p] = res.params[j], res.bse[j]

    # Nivel: el índice sale en logs con base arbitraria. Se reescala para que el
    # promedio ponderado por kilos coincida con el del ratio ingenuo, así queda
    # en USD/kg y es comparable renglón a renglón con la serie que usa hoy
    # pronostico.py. (Esto absorbe también el sesgo de retransformación de la
    # exponencial, que es un factor multiplicativo constante.)
    g = d.groupby("per").agg(fob_tot=("fob_tot", "sum"), kg=("kg", "sum"),
                             n=("kg", "size"), dest=("dest_g", "nunique"))
    naive = (g.fob_tot / g.kg).rename("pu_naive")
    bruto = np.exp(delta)
    k = (naive * g.kg).sum() / (bruto * g.kg).sum()
    idx = (bruto * k).rename("idx_hedonico")

    return {"idx": idx, "naive": naive, "se_log": se, "n": g.n, "kg": g.kg,
            "dest": g.dest, "res": res, "nom": nom, "base_dest": base_dest,
            "base_mes": base_mes}


def premios_destino(out: dict) -> pd.DataFrame:
    """Premium de cada destino contra la base, en % sobre el precio."""
    res, nom = out["res"], out["nom"]
    filas = []
    for j, c in enumerate(nom):
        if not c.startswith("d_"):
            continue
        filas.append({"destino": c[2:], "premium_%": (np.exp(res.params[j]) - 1) * 100,
                      "se_%": res.bse[j] * 100, "t": res.tvalues[j]})
    return pd.DataFrame(filas).sort_values("premium_%", ascending=False)


# ------------------------------------------------------------------ comparación
def comparar(out: dict) -> pd.DataFrame:
    """Cuánto del movimiento del ratio ingenuo era composición de destino."""
    idx, naive = out["idx"], out["naive"]
    comp = np.log(naive) - np.log(idx)          # el residuo de composición
    dl_n, dl_i, dl_c = np.log(naive).diff(), np.log(idx).diff(), comp.diff()
    return pd.DataFrame([
        {"serie": "ratio ingenuo Σfob/Σkg", "media_usd_kg": naive.mean(),
         "sd_nivel": naive.std(), "sd_Δlog": dl_n.std(),
         "autocorr_Δlog_1": dl_n.autocorr(1)},
        {"serie": "índice hedónico", "media_usd_kg": idx.mean(),
         "sd_nivel": idx.std(), "sd_Δlog": dl_i.std(),
         "autocorr_Δlog_1": dl_i.autocorr(1)},
        {"serie": "componente de composición", "media_usd_kg": np.nan,
         "sd_nivel": np.nan, "sd_Δlog": dl_c.std(),
         "autocorr_Δlog_1": dl_c.autocorr(1)},
    ]).set_index("serie")


# ------------------------------------------------------------------ backtest
def backtest_comparado(out: dict, out2: dict | None = None,
                       etiquetas: tuple[str, str] = ("ratio ingenuo", "hedónico")
                       ) -> pd.DataFrame:
    """Pasa dos series por el MISMO backtest de pronostico.py.

    Es la única prueba que importa: si el índice hedónico no baja el U de
    Theil, sacó ruido que no molestaba y no hay que cambiar nada.

    Por defecto compara el ratio ingenuo contra el hedónico de `out`. Con
    `out2` compara el índice de `out` contra el de `out2` (se usa para el
    corte por flota).
    """
    import pronostico as pr

    def _prep(s: pd.Series) -> tuple[pd.Series, pd.Series, pd.PeriodIndex]:
        # mismos huecos y mismo tratamiento que cargar_series('l1'): se
        # interpolan en log para no romper los rezagos y NO se puntúan.
        completo = pd.period_range(s.index.min(), s.index.max(), freq="M")
        interp = completo.difference(s.index)
        s = np.exp(np.log(s.reindex(completo)).interpolate())
        _, tan3 = pr.cargar_series("l1")
        comun = s.index.intersection(tan3.index)
        return s[comun], tan3[comun], interp

    pares = ((etiquetas[0], out["naive"] if out2 is None else out["idx"]),
             (etiquetas[1], out["idx"] if out2 is None else out2["idx"]))
    filas = []
    for nombre, serie in pares:
        s, tan3, interp = _prep(serie)
        bt = pr.backtest(np.log(s), np.log(tan3), interp)
        for h in bt.index:
            filas.append({"serie": nombre, "h": h, "n": bt.loc[h, "n"],
                          "U_thiel": bt.loc[h, "U_thiel"],
                          "U_preparo": bt.loc[h, "U_preparo"],
                          "U_paro": bt.loc[h, "U_paro"],
                          "rmse_modelo": bt.loc[h, "rmse_modelo"]})
        filas[-3]["direccional_h1"] = bt.attrs["acierto_direccional_h1"]
    return pd.DataFrame(filas).set_index(["serie", "h"])


# ------------------------------------------------------------------ salida
def _md(df: pd.DataFrame, indice: bool = True) -> str:
    """Markdown a mano: `to_markdown` de pandas exige tabulate, que no está
    instalado y no vale una dependencia nueva por una tabla."""
    d = df.reset_index() if indice else df
    cols = [str(c) for c in d.columns]
    filas = [[("" if pd.isna(v) else str(v)) for v in r] for r in d.to_numpy()]
    an = ["|" + "|".join(cols) + "|", "|" + "|".join("---" for _ in cols) + "|"]
    an += ["|" + "|".join(r) + "|" for r in filas]
    return "\n".join(an)


def main() -> None:
    flags = sys.argv[1:]
    d = cargar_micro()
    out = estimar(d)
    res = out["res"]

    print(f"WLS ponderado por kilos · N = {int(res.nobs):,} · "
          f"R² = {res.rsquared:.3f} · errores HC1")
    print(f"Base: mes {out['base_mes']}, destino {out['base_dest']}\n")

    print("Premium por destino (contra "
          f"{out['base_dest']}, a mezcla temporal constante):")
    print(premios_destino(out).round(1).to_string(index=False))
    print()

    print("Índice hedónico vs ratio ingenuo:")
    print(comparar(out).round(4).to_string())
    print()

    tabla = pd.DataFrame({"pu_naive": out["naive"], "idx_hedonico": out["idx"],
                          "se_log": out["se_log"], "n_filas": out["n"],
                          "kg": out["kg"], "destinos": out["dest"]})
    tabla["dif_%"] = (tabla.idx_hedonico / tabla.pu_naive - 1) * 100
    print("Últimos 12 meses:")
    print(tabla.tail(12).round(3).to_string())
    print()
    flacos = tabla[tabla.n_filas < 25]
    if len(flacos):
        print(f"AVISO: {len(flacos)} meses con menos de 25 despachos — el δ_t "
              "de esos meses tiene error estándar grande y no debería leerse "
              "como dato duro:")
        print("  " + ", ".join(str(p) for p in flacos.index))
        print()

    if "--robustez" in flags:
        print("=" * 70)
        print("ROBUSTEZ (correlación del Δlog contra la principal)\n")
        alts = {
            "sin recorte de outliers": (cargar_micro(recortar=False, verbose=False), {}),
            "ponderado por sqrt(kg)": (d, {"ponderar": "sqrt_kg"}),
            "sin ponderar": (d, {"ponderar": "ninguno"}),
            "destino × era (pre/post 2020)": (d, {"dest_por_era": True}),
            "con ruta, 2018+": (d[d.anio >= 2018], {"con_ruta": True}),
        }
        base_dl = np.log(out["idx"]).diff()
        filas = []
        for nombre, (dd, kw) in alts.items():
            o = estimar(dd, **kw)
            dl = np.log(o["idx"]).diff()
            com = base_dl.index.intersection(dl.index)
            filas.append({"especificación": nombre, "N": int(o["res"].nobs),
                          "R²": o["res"].rsquared,
                          "corr_Δlog_vs_principal": base_dl[com].corr(dl[com]),
                          "sd_Δlog": dl.std()})
        print(pd.DataFrame(filas).round(4).to_string(index=False))
        print()

    if "--abordo" in flags:
        print("=" * 70)
        print("CORTE POR FLOTA — L1 a bordo (tangonero) vs mezcla, misma ventana\n")
        # Misma ventana 2018+ en las tres series: si no, el corte por flota se
        # confunde con el cambio de período muestral.
        d18 = cargar_micro(desde=2018, verbose=False)
        o_mix = estimar(d18)
        o_ab = estimar(cargar_micro(ruta="a bordo", verbose=False))
        cmp_ = pd.DataFrame({
            "mezcla 2018+": [len(d18), o_mix["res"].rsquared,
                             np.log(o_mix["idx"]).diff().std()],
            "sólo a bordo": [int(o_ab["res"].nobs), o_ab["res"].rsquared,
                             np.log(o_ab["idx"]).diff().std()]},
            index=["N", "R²", "sd_Δlog"])
        print(cmp_.round(4).to_string())
        print()
        print("Backtest sobre la misma ventana:")
        print(backtest_comparado(o_mix, o_ab,
                                 ("hedónico mezcla", "hedónico a bordo")
                                 ).round(3).to_string())
        print()

    bt = None
    if "--backtest" in flags:
        print("=" * 70)
        print("BACKTEST — mismo modelo de pronostico.py, las dos series\n")
        bt = backtest_comparado(out)
        print(bt.round(3).to_string())
        print()

    # ---- exportación
    sal = os.path.join(RAIZ, "salidas")
    xlsx = os.path.join(sal, "indice_hedonico_l1.xlsx")
    try:
        with pd.ExcelWriter(xlsx) as w:
            tabla.to_excel(w, sheet_name="indice")
            premios_destino(out).to_excel(w, sheet_name="premium_destino", index=False)
            comparar(out).to_excel(w, sheet_name="comparacion")
            if bt is not None:
                bt.to_excel(w, sheet_name="backtest")
        print(f"Guardado: {xlsx}")
    except PermissionError:
        print(f"AVISO: no pude escribir {xlsx} (¿abierto en Excel?).")

    md = os.path.join(sal, "indice_hedonico_l1.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("# Índice hedónico de precio — langostino entero L1 (FOB, USD/kg)\n\n")
        f.write(f"WLS ponderado por kilos, N = {int(res.nobs):,}, "
                f"R² = {res.rsquared:.3f}, errores HC1. "
                f"Base: mes {out['base_mes']}, destino {out['base_dest']}.\n\n")
        f.write("## Premium por destino\n\n")
        f.write(_md(premios_destino(out).round(1), indice=False) + "\n\n")
        f.write("## Índice vs ratio ingenuo\n\n")
        f.write(_md(comparar(out).round(4)) + "\n\n")
        if bt is not None:
            f.write("## Backtest\n\n" + _md(bt.round(3)) + "\n\n")
        f.write("## Serie mensual\n\n")
        f.write(_md(tabla.round(3)) + "\n")
    print(f"Guardado: {md}")


if __name__ == "__main__":
    main()
