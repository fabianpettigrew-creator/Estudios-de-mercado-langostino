# -*- coding: utf-8 -*-
"""Reespecificación del modelo de precio sobre la serie tangonera (SA01).

Motivo. El índice hedónico del L1 a bordo perdió contra el random walk
(U 1,06 / 1,13 / 1,21) al pasarlo por la especificación de `pronostico.py`,
que está armada para la serie MEZCLADA y le queda mal a la tangonera pura
en dos puntos medidos:

  · `_zafra()` marca nov-mar, que es el 5,3% del desembarque tangonero y el
    60,3% del fresquero. Para la serie tangonera apunta a la temporada de la
    otra flota. Acá se usa jul-oct, que es el 70,5% del desembarque tangonero.
  · `PISO_TAN` clipea Tan3 en 500 t en 26 de 103 meses (25%), 21 de ellos
    ene-mar. El clip le saca la mitad de la varianza al regresor: sd de
    log(Tan3) 3,46 → 1,84. Los ceros de dic-feb son reales (la flota no
    pesca) y quedan enmascarados como si fueran 500 t.

Se prueban tres variables de oferta contra la misma serie de precio:

  tan3   log(Tan3) con piso, tal cual hoy — línea de base
  tan1p  log(1 + Tan del mes), sin piso: admite los ceros reales
  stock  log(1 + stock implícito), la variable de estado del almacenamiento

Stock implícito. Que el desembarque congelador sea el producto final que se
exporta (no pasa por planta) hace que valga la identidad

    S(t) = S(t-1) + Desembarque_tan(t) − Exportación_tan(t)|materia prima

Las dos puntas tienen que estar en materia prima equivalente. El entero va
1:1 y la cola se divide por el rendimiento de cola, 0,55, que la industria fijó
igual para las dos flotas (24-ago-2026; antes era 0,65 para la tangonera). El nivel de exportación NO sale de Softrade: sus volúmenes
pre-2020 están inflados hasta 1,45× por doble conteo. Sale de la aduana
oficial por NCM, y Softrade aporta sólo el SHARE de SA01 dentro de cada NCM,
que es un cociente y por lo tanto inmune al doble conteo (misma lógica que
usa el v46 para atribuir flota).

S(0) no se conoce. Se fija de modo que el mínimo de la serie sea cero: es el
supuesto más conservador (en algún momento del período el stock tocó piso) y
sólo desplaza el nivel, no la dinámica.

Uso:  python respec.py
Salida: consola + salidas/respecificacion_tangonera.xlsx
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.abspath(__file__))
MIN_TRAIN = 36
HORIZONTES = (1, 2, 3)
REND_COLA_TAN = 0.55        # materia prima → cola. Igual en las dos flotas por
                            # indicación de la industria (24-ago-2026). Antes 0,65.
PISO_TAN = 500.0            # el piso de pronostico.py, para replicar la base

_CACHE: dict = {}


def micro():
    """expo.cargar_todos() es caro (relee ~30 xlsx) y acá se usa varias veces."""
    if "micro" not in _CACHE:
        from fuentes import expo
        _CACHE["micro"] = expo.cargar_todos()
    return _CACHE["micro"]


# ------------------------------------------------------------------ series
def _per(d: pd.DataFrame) -> pd.PeriodIndex:
    return pd.PeriodIndex(d.anio.astype(str) + "-" + d.mes.astype(str).str.zfill(2),
                          freq="M")


def serie_precio(desde: str = "2017-12") -> pd.Series:
    """Índice hedónico del entero L1 a bordo (tangonero), USD/kg."""
    import hedonico as hd
    d = hd.cargar_micro(ruta="a bordo", verbose=False)
    d = d[_per(d) >= pd.Period(desde, freq="M")].copy()
    return hd.estimar(d)["idx"]


def desembarque_tangonero() -> pd.Series:
    lan = pd.read_pickle(os.path.join(RAIZ, "_lan.pkl"))
    t = lan[lan.flota == "CONG. TANGONEROS"].groupby(["anio", "mes"]).t.sum()
    t.index = pd.PeriodIndex([f"{y}-{m:02d}" for y, m in t.index], freq="M")
    return t.sort_index()


def stock_implicito(verbose: bool = True) -> pd.Series:
    """Stock implícito de producto tangonero, en toneladas de materia prima."""
    d = micro()
    d = d[d.ruta == "a bordo"].copy()
    d["per"] = _per(d)
    d["fam"] = np.where(d.pres == "entero", "entero", "cola")
    d = d[d.pres != "otra especie"]

    # Share de SA01 dentro de cada familia, mes a mes (cociente: sin doble conteo).
    tot = micro().copy()
    tot["per"] = _per(tot)
    tot["fam"] = np.where(tot.pres == "entero", "entero", "cola")
    tot = tot[tot.pres != "otra especie"]
    num = d.groupby(["per", "fam"]).kg.sum().unstack(fill_value=0.0)
    den = tot.groupby(["per", "fam"]).kg.sum().unstack(fill_value=0.0)
    share = (num / den.replace(0, np.nan)).fillna(0.0)

    # Nivel oficial por NCM (0306.17.10 entero, 0306.17.90 cola).
    a = pd.read_pickle(os.path.join(RAIZ, "datos", "aduana_langostino_total.pkl"))
    a = a.copy()
    a.index = pd.PeriodIndex(a.anio.astype(str) + "-" + a.mes.astype(str).str.zfill(2),
                             freq="M")
    ofi = a.pivot_table(index=a.index, columns="ncm", values="kg", aggfunc="sum")
    ofi = ofi.rename(columns={"0306.17.10": "entero", "0306.17.90": "cola"})

    com = share.index.intersection(ofi.index)
    ent_t = (ofi.loc[com, "entero"] * share.loc[com, "entero"]) / 1000.0   # t
    col_t = (ofi.loc[com, "cola"] * share.loc[com, "cola"]) / 1000.0
    # a materia prima: el entero va 1:1, la cola se divide por el rendimiento
    expo_mp = (ent_t + col_t / REND_COLA_TAN).rename("expo_mp_t")

    des = desembarque_tangonero().reindex(expo_mp.index).fillna(0.0)
    flujo = des - expo_mp
    S = flujo.cumsum()
    S = (S - S.min()).rename("stock_t")      # S(0) tal que el mínimo sea cero

    if verbose:
        print("Stock implícito tangonero (t de materia prima)")
        print(f"  ventana {S.index.min()}..{S.index.max()} ({len(S)} meses)")
        print(f"  desembarque medio {des.mean():,.0f} t/mes · "
              f"exportación mp media {expo_mp.mean():,.0f} t/mes")
        print(f"  cierre anual (expo mp / desembarque):")
        anual = pd.DataFrame({"des": des, "expo": expo_mp})
        anual["a"] = anual.index.year
        r = anual.groupby("a").apply(lambda g: g.expo.sum() / g.des.sum() * 100
                                     if g.des.sum() else np.nan, include_groups=False)
        print("   " + "  ".join(f"{a}:{v:.0f}%" for a, v in r.items() if pd.notna(v)))
        print(f"  stock: media {S.mean():,.0f} t · máx {S.max():,.0f} t · "
              f"sd {S.std():,.0f} t")
        print(f"  meses de cobertura (S / expo mensual media): "
              f"{(S.mean()/expo_mp.mean()):.1f}\n")
    return S


# ------------------------------------------------------------------ modelo
def _dummy(per: pd.Period, meses: tuple) -> float:
    return 1.0 if per.month in meses else 0.0


def _X(idx: pd.PeriodIndex, lp: np.ndarray, z: np.ndarray,
       zafra: tuple, dic_ene: bool) -> np.ndarray:
    cols = [np.ones(len(idx)), lp, z, np.array([_dummy(p, zafra) for p in idx])]
    if dic_ene:
        cols.append(np.array([_dummy(p, (12, 1)) for p in idx]))
    return np.column_stack(cols)


def _ajustar(lf: pd.Series, lz: pd.Series, zafra: tuple, dic_ene: bool):
    d = pd.DataFrame({"dl": lf.diff(), "l1": lf.shift(1), "z1": lz.shift(1)}).dropna()
    X = _X(d.index, d.l1.to_numpy(), d.z1.to_numpy(), zafra, dic_ene)
    b, *_ = np.linalg.lstsq(X, d.dl.to_numpy(), rcond=None)
    return b


def _proyectar(lf, lz, h, zafra, dic_ene):
    b = _ajustar(lf, lz, zafra, dic_ene)
    ly, lzz, per = lf.iloc[-1], lz.iloc[-1], lf.index[-1]
    for _ in range(h):
        per = per + 1
        x = [1.0, ly, lzz, _dummy(per, zafra)]
        if dic_ene:
            x.append(_dummy(per, (12, 1)))
        ly = ly + float(np.dot(b, x))
    return ly


def backtest(lf: pd.Series, lz: pd.Series, zafra: tuple, dic_ene: bool,
             interpolados=None) -> dict:
    err = {h: {"m": [], "rw": []} for h in HORIZONTES}
    ac = []
    for i in range(MIN_TRAIN, len(lf)):
        tr_f, tr_z = lf.iloc[:i], lz.iloc[:i]
        for h in HORIZONTES:
            if i + h - 1 >= len(lf):
                continue
            if interpolados is not None and lf.index[i + h - 1] in interpolados:
                continue
            real = lf.iloc[i + h - 1]
            pron = _proyectar(tr_f, tr_z, h, zafra, dic_ene)
            err[h]["m"].append(pron - real)
            err[h]["rw"].append(tr_f.iloc[-1] - real)
            if h == 1:
                ac.append(np.sign(pron - tr_f.iloc[-1]) == np.sign(real - tr_f.iloc[-1]))
    out = {}
    for h in HORIZONTES:
        em, er = np.array(err[h]["m"]), np.array(err[h]["rw"])
        out[h] = {"n": len(em),
                  "U": float(np.sqrt((em ** 2).mean()) / np.sqrt((er ** 2).mean())),
                  "rmse": float(np.sqrt((em ** 2).mean()))}
    out["dir"] = float(np.mean(ac))
    return out


# ------------------------------------------------------------------ corrida
def main() -> None:
    print("Serie de precio: índice hedónico entero L1 a bordo (SA01)\n")
    p = serie_precio()
    # mismos huecos, mismo trato que en pronostico.py: interpolar en log, no puntuar
    completo = pd.period_range(p.index.min(), p.index.max(), freq="M")
    interp = completo.difference(p.index)
    p = np.exp(np.log(p.reindex(completo)).interpolate())
    print(f"  {p.index.min()}..{p.index.max()} · {len(p)} meses · "
          f"{len(interp)} interpolados (no se puntúan)")
    print(f"  media {p.mean():.2f} USD/kg · sd Δlog {np.log(p).diff().std():.4f}\n")

    tan = desembarque_tangonero()
    tan3 = tan.rolling(3).sum()
    S = stock_implicito()

    ofertas = {
        "log Tan3 con piso (base)": np.log(tan3.clip(lower=PISO_TAN)),
        "log(1+Tan) sin piso": np.log1p(tan),
        "log(1+Stock implícito)": np.log1p(S),
    }
    zafras = {"nov-mar (actual)": (11, 12, 1, 2, 3), "jul-oct (tangonera)": (7, 8, 9, 10)}

    filas = []
    for nom_z, z in zafras.items():
        for nom_o, serie_o in ofertas.items():
            com = p.index.intersection(serie_o.dropna().index)
            lf, lz = np.log(p[com]), serie_o[com]
            r = backtest(lf, lz, z, True, interp)
            filas.append({"zafra": nom_z, "oferta": nom_o, "n": r[1]["n"],
                          "U_h1": r[1]["U"], "U_h2": r[2]["U"], "U_h3": r[3]["U"],
                          "direccional": r["dir"]})
    # stock sin dummy estacional: el stock ya lleva la temporada adentro
    com = p.index.intersection(S.dropna().index)
    r = backtest(np.log(p[com]), np.log1p(S[com]), (), False, interp)
    filas.append({"zafra": "sin dummy", "oferta": "log(1+Stock implícito)",
                  "n": r[1]["n"], "U_h1": r[1]["U"], "U_h2": r[2]["U"],
                  "U_h3": r[3]["U"], "direccional": r["dir"]})

    # ---- barrido de rezagos del desembarque como proxy de la oferta que llega
    # al mercado. Si el pico está en un rezago corto (la correlación cruzada
    # dice t-1), entonces S(t) ≈ Tan(t) + c y el stock implícito no agrega
    # nada sobre el desembarque: son la misma variable con otro nombre.
    for k in range(0, 4):
        z = np.log1p(tan.shift(k))
        com = p.index.intersection(z.dropna().index)
        r = backtest(np.log(p[com]), z[com], (7, 8, 9, 10), True, interp)
        filas.append({"zafra": "jul-oct (tangonera)",
                      "oferta": f"log(1+Tan) rezago {k} (efectivo {k+1})",
                      "n": r[1]["n"], "U_h1": r[1]["U"], "U_h2": r[2]["U"],
                      "U_h3": r[3]["U"], "direccional": r["dir"]})

    t = pd.DataFrame(filas)
    # ¿Stock y desembarque son la misma variable? Si la correlación es alta, el
    # stock es redundante y hay que quedarse con el desembarque, que no necesita
    # ni el rendimiento de cola ni el share SA01.
    com = S.dropna().index.intersection(tan.dropna().index)
    print(f"Colinealidad stock vs desembarque: corr(log(1+S), log(1+Tan)) = "
          f"{np.log1p(S[com]).corr(np.log1p(tan[com])):.3f} · "
          f"en Δlog = {np.log1p(S[com]).diff().corr(np.log1p(tan[com]).diff()):.3f}\n")

    print("BACKTEST — serie tangonera, U de Theil (menor que 1 = le gana al naive)\n")
    print(t.round(3).to_string(index=False))
    print()
    mej = t.loc[t.U_h1.idxmin()]
    print(f"Mejor a h=1: {mej.oferta} + zafra {mej.zafra} → U {mej.U_h1:.3f}, "
          f"direccional {mej.direccional:.1%}")
    if mej.U_h1 >= 1:
        print("NINGUNA especificación le gana al random walk a 1 mes. La lectura (b) "
              "se sostiene: el precio del L1 tangonero no se pronostica mes a mes, y "
              "lo que el modelo sobre la serie mezclada anticipaba era la composición "
              "de flota, no el precio.")

    out = os.path.join(RAIZ, "salidas", "respecificacion_tangonera.xlsx")
    try:
        with pd.ExcelWriter(out) as w:
            t.to_excel(w, sheet_name="backtest", index=False)
            pd.DataFrame({"precio_hedonico": p, "tan_t": tan.reindex(p.index),
                          "tan3_t": tan3.reindex(p.index),
                          "stock_t": S.reindex(p.index)}).to_excel(w, sheet_name="series")
        print(f"\nGuardado: {out}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {out} (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
