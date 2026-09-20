# -*- coding: utf-8 -*-
"""Pronóstico del FOB del langostino entero (0306.17.10) a 1-3 meses.

Modelo estructural elegido por backtest (2026-08):

    Δlog P(t) = a + b·log P(t-1) + c·log Tan3(t-1) + d·zafra(t) + e·dic_ene(t)

donde Tan3 es la captura tangonera acumulada 3 meses (SSPyA) y zafra es
nov-mar. La lógica es demanda inversa (Barten-Bettendorf): la oferta está
predeterminada por la biología y la flota, el precio ajusta. El vannamei
NO entra: en el FOB de origen no es significativo (la integración con el
cultivo, débil, opera en el CIF de destino).

Regla de la casa: ningún pronóstico se reporta sin su backtest. El U de
Theil (RMSE modelo / RMSE naive) se computa acá mismo, con el mismo código
que genera el pronóstico, y sale impreso al lado de cada número. U < 1 es
ganarle al random walk; con la serie oficial completa (INDEC mensual
2013-01..2017-01 empalmado con aduana 2017-02 en adelante, backtest de
127 meses 2016-01..2026-07 que incluye pandemia y paro) da 0,88 / 0,78 /
0,72 a 1/2/3 meses, robusto en los subperíodos pre y post paro 2025.

La reversión a la media sola NO aporta (U≈1): el filo viene de oferta +
estacionalidad. Esto revisa el veredicto de 2026-08-06, que se había
estimado sobre el precio promedio con mezcla de presentaciones; sobre el
entero solo, con driver de oferta, el random walk sí se puede batir.

Con --l1 corre además sobre el entero L1 solo (serie transaccional; ratios
válidos aunque el volumen transaccional no lo sea). La serie cubre 2013-01
a 2026-07, pero en dos dialectos: hasta 2017 el grado viaja en prosa ("DE
11 HASTA 20 PIEZAS POR kg") y desde 2017-10 como código AI(L1). El parser
de `fuentes/expo.py` recupera ambos con los mismos tramos oficiales del
NCM; quedan 10 meses sin ninguna fila con grado (ene-jun 2016, jun-sep
2017) que se interpolan para no romper los rezagos y NO se puntúan en el
backtest.

Historia del veredicto sobre el L1, en tres actos: con la serie 2020-2026
parecía random walk fuera del paro; con la serie que arrancaba en 2017-10
(mal descrita entonces como "desde 2013") el veredicto pareció refutado; y
con la serie realmente larga vuelve la lectura original, ahora sí sobre 117
meses de test: U pre-paro 0,96 / 0,91 / 0,90 — en tiempos normales el L1
apenas le gana al naive a 1 mes. El filo vive en el shock de oferta (U de
0,80 / 0,68 / 0,57 durante el paro). Usarlo como señal direccional (63%) y
alarma de oferta; el nivel, tomarlo del agregado.

Insumos:
  datos/aduana_langostino_total.pkl  (ingesta de fuentes/aduana.py)
  _lan.pkl                           (regenerar con fuentes/desembarques.py)
  planillas Softrade vía fuentes/expo.py (solo con --l1)

Con --es corre además el FOB del entero a España (INDEC mensual por
destino, país 410: 0% de secreto, sin huecos, 2013-2026). España resultó
MÁS predecible que el agregado (U 0,85/0,69/0,64 vs 0,88/0,78/0,72): la
zafra pesa más (t=-5,7) porque España es el gran comprador de temporada.
El gap España-agregado como corrección de error NO aporta (t=-1,4) y no
se incluye. Ojo: el INDEC publica con un mes más de rezago que la aduana.

Uso:  python pronostico.py [--l1] [--es]
Salida: consola + salidas/pronostico_fob_entero.xlsx
        (+ pronostico_fob_l1.xlsx con --l1, pronostico_fob_espana.xlsx con --es)
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.abspath(__file__))
MIN_TRAIN = 36          # meses mínimos de entrenamiento en el backtest
HORIZONTES = (1, 2, 3)
COSTO_ESPERA = 0.01     # costo financiero+frío de demorar la venta un mes
PISO_TAN = 500.0        # t; los ceros del paro 2025 son reales pero log(0) no


# ---------------------------------------------------------------- datos
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from biblioteca import fuente
DIR_INDEC_M = fuente("aduana_control")


def _serie_espana() -> pd.DataFrame:
    """FOB entero a España (INDEC mensual por destino, país AFIP 410).

    España es destino grande: 0 celdas bajo secreto estadístico en TODA la
    serie 2013-2026, sin huecos. Cache en datos/, reconstruido solo si aparece
    un zip de INDEC más nuevo que el pickle (los expomYY/exponmYY pesan 35 MB).
    """
    import glob as _glob
    import zipfile as _zip
    cache = os.path.join(RAIZ, "datos", "indec_es_entero.pkl")
    zips = sorted(_glob.glob(os.path.join(DIR_INDEC_M, "exports_*_M.zip")))
    if os.path.exists(cache) and os.path.getmtime(cache) >= max(
            os.path.getmtime(z) for z in zips):
        return pd.read_pickle(cache)
    filas = []
    for zp in zips:
        with _zip.ZipFile(zp) as z:
            for n in z.namelist():
                # expomYY (hasta 2017) / exponmYY (2018+): NCM×destino×mes.
                # La variante 'p' (expopmYY) es vintage provisorio: da menos.
                base = n.rsplit("/", 1)[-1]
                if not (base.startswith("expom") or base.startswith("exponm")):
                    continue
                with z.open(n) as f:
                    d = pd.read_csv(f, sep=";", encoding="latin-1", dtype=str)
                d.columns = ["anio", "mes", "ncm", "pdes", "kg", "fob"]
                d = d[(d.ncm.str.strip() == "03061710")
                      & (d.pdes.astype(str).str.strip() == "410")]
                filas.append(d)
    d = pd.concat(filas)
    for c in ("kg", "fob"):
        d[c] = pd.to_numeric(d[c].str.strip().str.replace(".", "", regex=False)
                             .str.replace(",", ".", regex=False), errors="coerce")
    d = d.dropna(subset=["kg", "fob"])
    d.index = pd.PeriodIndex(d.anio.str.strip() + "-"
                             + d.mes.str.strip().str.zfill(2), freq="M")
    g = d.groupby(level=0)[["kg", "fob"]].sum().sort_index()
    g.to_pickle(cache)
    return g


def cargar_series(objetivo: str = "entero") -> tuple[pd.Series, pd.Series]:
    """objetivo: 'entero' (aduana oficial, 0306.17.10), 'l1' (Softrade, solo L1)
    o 'es' (FOB entero a España, INDEC mensual por destino)."""
    if objetivo == "es":
        g = _serie_espana()
        fob = (g.fob / g.kg).rename("fob_espana")
    elif objetivo == "l1":
        from fuentes import expo
        d = expo.cargar_todos()
        l1 = d[(d.pres == "entero") & (d.cal == "L1") & (d.kg > 0) & (d.fob > 0)].copy()
        l1.index = pd.PeriodIndex(
            l1.anio.astype(str) + "-" + l1.mes.astype(str).str.zfill(2), freq="M")
        g = l1.groupby(level=0).agg(fob_tot=("fob_tot", "sum"), kg=("kg", "sum"))
        fob = (g.fob_tot / g.kg).sort_index().rename("fob_l1")
        # La serie tiene 10 huecos (ene-jun 2016 y jun-sep 2017: meses sin ninguna
        # fila con grado declarado). Sin reindexar, el diff() del modelo restaría
        # meses no consecutivos como si lo fueran. Se completa por interpolación
        # en logaritmo y se registra cuáles son: el backtest NO los puntúa.
        completo = pd.period_range(fob.index.min(), fob.index.max(), freq="M")
        interpolados = completo.difference(fob.index)
        fob = np.exp(np.log(fob.reindex(completo)).interpolate()).rename("fob_l1")
        fob.attrs["interpolados"] = interpolados
    else:
        a = pd.read_pickle(os.path.join(RAIZ, "datos", "aduana_langostino_total.pkl"))
        ent = a[a.ncm == "0306.17.10"].copy()
        ent.index = pd.PeriodIndex(
            ent.anio.astype(str) + "-" + ent.mes.astype(str).str.zfill(2), freq="M")
        serie = ent[["kg", "fob"]]
        # Empalme histórico: INDEC base usuaria mensual 2013-01..2017-01 (0% de
        # secreto estadístico en esos años; el pu coincide con la base de aduana
        # al 4º decimal en el solape de 2017). Dato congelado: pickle estático.
        pre = pd.read_pickle(os.path.join(RAIZ, "datos", "indec_entero_2013_2017.pkl"))
        serie = pd.concat([pre[pre.index < serie.index.min()], serie]).sort_index()
        fob = (serie.fob / serie.kg).rename("fob_entero")

    lan = pd.read_pickle(os.path.join(RAIZ, "_lan.pkl"))
    tan = lan[lan.flota == "CONG. TANGONEROS"].groupby(["anio", "mes"]).t.sum()
    tan.index = pd.PeriodIndex([f"{y}-{m:02d}" for y, m in tan.index], freq="M")
    tan3 = tan.sort_index().rolling(3).sum().clip(lower=PISO_TAN).rename("tan3")

    comun = fob.index.intersection(tan3.index)
    fob2, tan2 = fob[comun], tan3[comun]
    fob2.attrs["interpolados"] = fob.attrs.get("interpolados", pd.PeriodIndex([], freq="M"))
    return fob2, tan2


# ---------------------------------------------------------------- modelo
def _zafra(per: pd.Period) -> float:
    return 1.0 if (per.month >= 11 or per.month <= 3) else 0.0


def _dic_ene(per: pd.Period) -> float:
    """Resaca post-fiestas. La demanda europea pica para las fiestas de fin de
    año pero se EMBARCA en sep-nov; para dic-ene la compra ya está hecha y el
    precio afloja más de lo que la zafra sola explica (t=-3,1; los tres peores
    errores de sobreestimación del backtest eran diciembres-eneros). Probada
    contra la alternativa de demanda observada (importaciones españolas de
    camarón, EUMOFA): la dummy de calendario le gana — la proxy de demanda
    no es significativa (t=0,6) y empeora el U en todos los horizontes."""
    return 1.0 if per.month in (12, 1) else 0.0


def _ajustar(lf: pd.Series, lt: pd.Series) -> np.ndarray:
    """OLS de Δlog P sobre [1, logP(-1), logTan3(-1), zafra, dic_ene]."""
    d = pd.DataFrame({"dl": lf.diff(), "l1": lf.shift(1), "t1": lt.shift(1)}).dropna()
    z = np.array([_zafra(p) for p in d.index])
    dc = np.array([_dic_ene(p) for p in d.index])
    X = np.column_stack([np.ones(len(d)), d.l1, d.t1, z, dc])
    b, *_ = np.linalg.lstsq(X, d.dl.to_numpy(), rcond=None)
    return b


def _proyectar(lf: pd.Series, lt: pd.Series, h: int, naive: bool = False) -> float:
    """Pronóstico iterado h meses adelante desde el final de lf.

    La captura futura no se conoce: se congela en el último Tan3 observado.
    Los calendarios de zafra y dic-ene sí se conocen y se usan.
    """
    ly, ltan = lf.iloc[-1], lt.iloc[-1]
    if naive:
        return ly
    b = _ajustar(lf, lt)
    per = lf.index[-1]
    for _ in range(h):
        per = per + 1
        ly = ly + b[0] + b[1] * ly + b[2] * ltan + b[3] * _zafra(per) + b[4] * _dic_ene(per)
    return ly


# ---------------------------------------------------------------- backtest
CORTE_PARO = pd.Period("2025-03", freq="M")   # separa tiempos normales del paro+rebote


def backtest(lf: pd.Series, lt: pd.Series,
             interpolados: pd.PeriodIndex | None = None) -> pd.DataFrame:
    """Rolling one-step, reestimando en cada paso. Devuelve U y RMSE por horizonte,
    con el U desdoblado pre/post paro 2025 — si el filo vive solo en el shock,
    tiene que verse acá, no descubrirse después."""
    filas = []
    err = {h: {"m": [], "rw": [], "f": []} for h in HORIZONTES}
    aciertos = []
    for i in range(MIN_TRAIN, len(lf)):
        tr_f, tr_t = lf.iloc[:i], lt.iloc[:i]
        for h in HORIZONTES:
            if i + h - 1 >= len(lf):
                continue
            # un mes reconstruido no es evidencia: no se puntúa como objetivo
            if interpolados is not None and lf.index[i + h - 1] in interpolados:
                continue
            real = lf.iloc[i + h - 1]
            pron = _proyectar(tr_f, tr_t, h)
            err[h]["m"].append(pron - real)
            err[h]["rw"].append(tr_f.iloc[-1] - real)
            err[h]["f"].append(lf.index[i + h - 1])
            if h == 1:
                aciertos.append(np.sign(pron - tr_f.iloc[-1]) == np.sign(real - tr_f.iloc[-1]))

    def _u(em, er):
        em, er = np.asarray(em), np.asarray(er)
        return float(np.sqrt(np.mean(em ** 2)) / np.sqrt(np.mean(er ** 2)))

    for h in HORIZONTES:
        em, er = np.array(err[h]["m"]), np.array(err[h]["rw"])
        pre = np.array([f <= CORTE_PARO for f in err[h]["f"]])
        filas.append({"horizonte_m": h, "n": len(em),
                      "U_thiel": _u(em, er),
                      "U_preparo": _u(em[pre], er[pre]) if pre.any() else np.nan,
                      "U_paro": _u(em[~pre], er[~pre]) if (~pre).any() else np.nan,
                      "rmse_modelo": float(np.sqrt(np.mean(em ** 2))),
                      "rmse_naive": float(np.sqrt(np.mean(er ** 2)))})
    bt = pd.DataFrame(filas).set_index("horizonte_m")
    bt.attrs["acierto_direccional_h1"] = float(np.mean(aciertos))
    return bt


# ---------------------------------------------------------------- salida
ETIQUETA = {"entero": "FOB entero 0306.17.10", "l1": "FOB entero L1 (Softrade)",
            "es": "FOB entero a España (INDEC por destino)"}


def correr(objetivo: str = "entero") -> None:
    fob, tan3 = cargar_series(objetivo)
    lf, lt = np.log(fob), np.log(tan3)
    ultimo = fob.index[-1]

    bt = backtest(lf, lt, fob.attrs.get("interpolados"))
    b = _ajustar(lf, lt)

    print(f"{ETIQUETA[objetivo]} — último dato {ultimo}: {fob.iloc[-1]:.2f} USD/kg")
    print(f"Tan3 (captura tangonera 3m): {tan3.iloc[-1]:,.0f} t\n")
    print("Coeficientes (muestra completa): "
          f"a={b[0]:.3f}  logP(-1)={b[1]:.3f}  logTan3(-1)={b[2]:.4f}  "
          f"zafra={b[3]:.4f}  dic_ene={b[4]:.4f}\n")

    print("Backtest (nunca reportar pronóstico sin esto):")
    print(bt.round(3).to_string())
    print(f"acierto direccional h=1: {bt.attrs['acierto_direccional_h1']*100:.0f}%")
    if (bt.U_preparo > 0.95).all():
        print("AVISO: U pre-paro ≈ 1 en todos los horizontes → en tiempos de captura "
              "normal esta serie es random walk; usar el pronóstico como señal "
              "direccional / alarma de shock de oferta, no como nivel.")
    print()

    filas = []
    for h in HORIZONTES:
        lp = _proyectar(lf, lt, h)
        rmse = bt.loc[h, "rmse_modelo"]
        filas.append({
            "mes": str(ultimo + h),
            "pronostico_usd_kg": float(np.exp(lp)),
            "banda_inf": float(np.exp(lp - 1.28 * rmse)),   # 80%
            "banda_sup": float(np.exp(lp + 1.28 * rmse)),
            "U_thiel": float(bt.loc[h, "U_thiel"]),
        })
    pron = pd.DataFrame(filas).set_index("mes")
    print("Pronóstico (banda 80% del backtest):")
    print(pron.round(2).to_string())

    p1 = pron.pronostico_usd_kg.iloc[0] * (1 - COSTO_ESPERA)
    señal = "ESPERAR" if p1 > fob.iloc[-1] else "VENDER AHORA"
    print(f"\nSeñal de timing (umbral {COSTO_ESPERA:.0%}/mes de espera): {señal}")
    print("(regla en backtest extendido: entero +0,9%, L1 +1,1% de ingreso vs "
          "vender siempre al contado; el timing perfecto era +1,7% / +2,1%)")

    out = os.path.join(RAIZ, "salidas",
                       {"entero": "pronostico_fob_entero.xlsx",
                        "l1": "pronostico_fob_l1.xlsx",
                        "es": "pronostico_fob_espana.xlsx"}[objetivo])
    try:
        with pd.ExcelWriter(out) as w:
            pron.to_excel(w, sheet_name="pronostico")
            bt.to_excel(w, sheet_name="backtest")
            pd.DataFrame({"fob_usd_kg": fob, "tan3_t": tan3}).to_excel(w, sheet_name="series")
        print(f"\nGuardado: {out}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {out} (¿abierto en Excel?). "
              "El pronóstico de arriba es válido igual; cerrá el archivo y volvé a correr.")


def main() -> None:
    correr("entero")
    for flag, obj in (("--l1", "l1"), ("--es", "es")):
        if flag in sys.argv[1:]:
            print("\n" + "=" * 64 + "\n")
            correr(obj)


if __name__ == "__main__":
    main()
