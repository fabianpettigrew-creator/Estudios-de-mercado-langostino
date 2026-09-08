# -*- coding: utf-8 -*-
"""Índice mensual de actividad del canal HORECA en los mercados del L1 tangonero.

Reemplaza el índice de cierre construido a mano de la primera versión del modelo por
dato observado de los cuatro destinos, que concentran el 89,7% del volumen del L1
tangonero: España 43,5% · Italia 21,1% · China 13,6% · Japón 11,5%.

Insumo principal: **`HORECA_indice_mensual.xlsx`** (una carpeta más arriba), con una
hoja por país, la comparativa ya rebasada a 2019 = 100 y su propia hoja de metodología:

  · España — INE, Indicadores de Actividad del Sector Servicios, cifra de negocios
    CNAE 56, serie original sin ajustar, 2013-01 a 2026-06, mensual y completa.
  · Italia — ISTAT, fatturato dei servizi, Ateco 56. La serie MENSUAL arranca en
    2021-01; para 2013-2020 sólo existe TRIMESTRAL, que se usa como escalón.
  · China — NBS, ingresos de restauración (餐饮收入), valor corriente mensual.
    El NBS **no publica enero ni febrero por separado**: los difunde acumulados, así
    que a cada uno de esos dos meses se le asigna la mitad del acumulado. Queda
    declarado: es el único supuesto que sobrevive en la construcción del índice.
  · Japón — METI, índice de actividad terciaria, restauración (飲食店、飲食サービス業),
    serie original; 2013-2017 por el índice enlazado y desde 2018 por el base 2020.

Los cuatro se llevan a base 2019 = 100 (cada uno por su propia media de 2019) y se
combinan en una media geométrica ponderada por la participación de cada mercado en el
volumen del L1 tangonero.

Insumo secundario, para contraste: **índice de rigor de OxCGRT** (stringency_index_avg),
promedio mensual nacional de los cuatro países, 2020-01 a 2022-12, cero fuera de la
pandemia. Fuente: https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/
data/timeseries/stringency_index_avg.csv

El control que entra al modelo es la BRECHA del índice respecto de su propia tendencia:
lo que informa como desplazador de demanda es el desvío, no el nivel.

Uso:  python demanda_inversa_horeca.py
Salida: datos/horeca_indice.pkl + salidas/horeca_indice.svg/.png
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
LIBRO = os.path.join(os.path.dirname(RAIZ), "HORECA_indice_mensual.xlsx")

# Participación en el volumen del L1 tangonero (%)
PESOS = {"ES": 43.5, "IT": 21.1, "CN": 13.6, "JP": 11.5}
PAIS = {"ES": "España", "IT": "Italia", "CN": "China", "JP": "Japón"}
DESDE, HASTA = "2013-01", "2026-07"


ES_M = "2013-01=103.5;2013-02=102.8;2013-03=104.3;2013-04=103.2;2013-05=103.7;2013-06=103.7;2013-07=104.4;2013-08=104.2;2013-09=103.9;2013-10=104.7;2013-11=105.2;2013-12=105.5;2014-01=104.6;2014-02=106.0;2014-03=105.7;2014-04=107.1;2014-05=107.3;2014-06=107.1;2014-07=108.0;2014-08=108.2;2014-09=108.6;2014-10=108.8;2014-11=109.2;2014-12=109.2;2015-01=109.4;2015-02=109.0;2015-03=110.7;2015-04=111.3;2015-05=112.1;2015-06=111.3;2015-07=112.4;2015-08=113.4;2015-09=113.5;2015-10=114.5;2015-11=115.5;2015-12=116.1;2016-01=117.7;2016-02=118.7;2016-03=117.2;2016-04=117.3;2016-05=118.8;2016-06=118.7;2016-07=119.2;2016-08=120.1;2016-09=121.4;2016-10=121.4;2016-11=121.7;2016-12=121.3;2017-01=121.8;2017-02=122.2;2017-03=123.1;2017-04=124.8;2017-05=123.4;2017-06=126.6;2017-07=125.3;2017-08=126.0;2017-09=126.4;2017-10=126.6;2017-11=126.6;2017-12=125.5;2018-01=127.5;2018-02=126.8;2018-03=127.3;2018-04=127.5;2018-05=129.4;2018-06=127.8;2018-07=129.0;2018-08=129.8;2018-09=131.4;2018-10=131.9;2018-11=130.4;2018-12=132.9;2019-01=132.7;2019-02=132.1;2019-03=134.5;2019-04=131.8;2019-05=133.4;2019-06=133.1;2019-07=134.2;2019-08=133.2;2019-09=134.2;2019-10=135.2;2019-11=136.7;2019-12=137.4;2020-01=139.2;2020-02=140.1;2020-03=57.2;2020-04=8.2;2020-05=22.5;2020-06=64.8;2020-07=86.1;2020-08=93.9;2020-09=87.9;2020-10=80.4;2020-11=65.8;2020-12=75.0;2021-01=65.7;2021-02=61.7;2021-03=81.0;2021-04=79.7;2021-05=95.2;2021-06=99.3;2021-07=110.4;2021-08=121.6;2021-09=122.0;2021-10=126.4;2021-11=122.3;2021-12=114.7;2022-01=117.5;2022-02=123.2;2022-03=124.4;2022-04=129.8;2022-05=133.5;2022-06=131.6;2022-07=134.9;2022-08=137.5;2022-09=136.4;2022-10=137.9;2022-11=138.3;2022-12=138.3;2023-01=141.8;2023-02=138.0;2023-03=143.7;2023-04=143.5;2023-05=141.6;2023-06=143.7;2023-07=145.0;2023-08=144.5;2023-09=147.8;2023-10=148.6;2023-11=148.1;2023-12=150.6;2024-01=151.2;2024-02=152.5;2024-03=153.5;2024-04=150.6;2024-05=153.3;2024-06=154.0;2024-07=153.9;2024-08=156.8;2024-09=156.2;2024-10=155.9;2024-11=156.9;2024-12=157.6;2025-01=156.5;2025-02=156.7;2025-03=156.1;2025-04=157.8;2025-05=160.0;2025-06=159.7;2025-07=160.0;2025-08=159.2;2025-09=159.5;2025-10=161.7;2025-11=161.8;2025-12=160.3;2026-01=162.6;2026-02=161.8;2026-03=163.7;2026-04=165.0;2026-05=164.5;2026-06=163.3"

IT_Q = "2013-Q1=118.1;2013-Q2=118.3;2013-Q3=118.9;2013-Q4=118.1;2014-Q1=119.8;2014-Q2=117.5;2014-Q3=115.8;2014-Q4=118.8;2015-Q1=117.3;2015-Q2=120.1;2015-Q3=121.5;2015-Q4=120.8;2016-Q1=121.4;2016-Q2=120.8;2016-Q3=123.0;2016-Q4=123.1;2017-Q1=124.4;2017-Q2=125.7;2017-Q3=125.8;2017-Q4=125.8;2018-Q1=126.4;2018-Q2=128.2;2018-Q3=128.0;2018-Q4=129.3;2019-Q1=131.6;2019-Q2=128.2;2019-Q3=129.5;2019-Q4=132.1;2020-Q1=103.6;2020-Q2=45.1;2020-Q3=105.1;2020-Q4=73.7;2021-Q1=83.0;2021-Q2=75.7;2021-Q3=119.0;2021-Q4=122.5;2022-Q1=128.7;2022-Q2=137.0;2022-Q3=143.8;2022-Q4=148.9;2023-Q1=152.8;2023-Q2=155.7;2023-Q3=158.7;2023-Q4=159.3;2024-Q1=162.2;2024-Q2=161.3;2024-Q3=162.1;2024-Q4=164.0;2025-Q1=163.5;2025-Q2=165.2;2025-Q3=165.6;2025-Q4=166.0;2026-Q1=166.3"

RIGOR = {
    "ES": "2020-01=0.4;2020-02=11.1;2020-03=51.7;2020-04=85.2;2020-05=78.6;2020-06=54.2;2020-07=59.5;2020-08=62.8;2020-09=61.0;2020-10=64.7;2020-11=71.3;2020-12=73.4;2021-01=72.7;2021-02=70.3;2021-03=68.7;2021-04=69.4;2021-05=65.0;2021-06=52.5;2021-07=48.6;2021-08=48.0;2021-09=44.7;2021-10=41.9;2021-11=41.2;2021-12=43.1;2022-01=38.6;2022-02=38.5;2022-03=36.0;2022-04=32.1;2022-05=27.6;2022-06=27.6;2022-07=25.1;2022-08=20.8;2022-09=13.9;2022-10=12.9;2022-11=11.1;2022-12=11.1",
    "IT": "2020-01=1.5;2020-02=31.2;2020-03=80.4;2020-04=90.7;2020-05=73.7;2020-06=67.6;2020-07=67.0;2020-08=66.6;2020-09=65.8;2020-10=68.0;2020-11=81.8;2020-12=80.9;2021-01=76.6;2021-02=75.9;2021-03=79.3;2021-04=78.7;2021-05=70.5;2021-06=70.8;2021-07=61.3;2021-08=53.8;2021-09=57.3;2021-10=52.4;2021-11=49.8;2021-12=50.7;2022-01=53.0;2022-02=49.0;2022-03=43.7;2022-04=36.4;2022-05=22.5;2022-06=19.2;2022-07=19.2;2022-08=19.2;2022-09=15.5;2022-10=15.5;2022-11=18.3;2022-12=19.6",
    "JP": "2020-01=2.2;2020-02=21.8;2020-03=41.2;2020-04=45.7;2020-05=42.0;2020-06=27.8;2020-07=28.0;2020-08=32.7;2020-09=34.4;2020-10=35.2;2020-11=36.7;2020-12=42.9;2021-01=49.4;2021-02=49.6;2021-03=44.1;2021-04=45.4;2021-05=49.1;2021-06=53.3;2021-07=51.1;2021-08=51.1;2021-09=51.6;2021-10=47.2;2021-11=47.2;2021-12=47.2;2022-01=47.2;2022-02=47.2;2022-03=46.6;2022-04=45.4;2022-05=44.8;2022-06=39.2;2022-07=37.5;2022-08=37.5;2022-09=36.2;2022-10=31.5;2022-11=31.5;2022-12=32.1",
    "CN": "2020-01=21.6;2020-02=77.0;2020-03=79.5;2020-04=60.2;2020-05=74.7;2020-06=78.5;2020-07=78.2;2020-08=78.2;2020-09=60.1;2020-10=63.1;2020-11=69.5;2020-12=79.1;2021-01=78.2;2021-02=74.1;2021-03=53.0;2021-04=74.5;2021-05=67.8;2021-06=72.3;2021-07=75.3;2021-08=70.8;2021-09=73.2;2021-10=74.1;2021-11=68.1;2021-12=73.3;2022-01=75.3;2022-02=64.2;2022-03=63.3;2022-04=77.6;2022-05=79.2;2022-06=79.2;2022-07=73.6;2022-08=75.2;2022-09=71.6;2022-10=67.3;2022-11=68.7;2022-12=57.6",
}


def _ser(txt: str, freq: str) -> pd.Series:
    s = pd.Series({k: float(v) for k, v in (x.split("=") for x in txt.split(";"))})
    s.index = pd.PeriodIndex(s.index, freq=freq)
    return s.sort_index()


def _libro(hoja: str) -> pd.DataFrame:
    return pd.read_excel(LIBRO, sheet_name=hoja, header=3)


def paises() -> pd.DataFrame:
    """Las cuatro series en base 2019 = 100, con los huecos resueltos."""
    M = pd.period_range(DESDE, HASTA, freq="M")

    c = _libro("Comparativa 2019=100").dropna(subset=["Periodo"])
    c.index = pd.PeriodIndex(c.Periodo.astype(str), freq="M")
    c = c[[PAIS[k] for k in PESOS]].apply(pd.to_numeric, errors="coerce").reindex(M)
    c.columns = list(PESOS)

    # Italia antes de 2021: la trimestral como escalón, con el mismo anclaje de 2019
    q = _libro("Italia trimestral").dropna(subset=["Trimestre"])
    # el ancla viene como par etiqueta/valor: la etiqueta en una columna y el número en la siguiente
    anc = float(pd.to_numeric(q.iloc[:, -1], errors="coerce").dropna().iloc[0])
    qs = pd.Series(pd.to_numeric(q["Índice (2021=100)"], errors="coerce").to_numpy() / anc * 100,
                   index=pd.PeriodIndex(q.Trimestre.astype(str), freq="Q"))
    c["IT"] = c["IT"].fillna(pd.Series({m: qs.get(m.asfreq("Q"), np.nan) for m in M}))

    # China: el NBS difunde enero y febrero acumulados. Se reparte por mitades.
    cn = _libro("China").dropna(subset=["Periodo"])
    cn.index = pd.PeriodIndex(cn.Periodo.astype(str), freq="M")
    ing = pd.to_numeric(cn["Ingresos del mes (miles de mill. CNY)"], errors="coerce")
    idxc = pd.to_numeric(cn["Índice rebasado 2019=100"], errors="coerce")
    ancla = float((ing / idxc * 100).dropna().iloc[0])
    acc = pd.DataFrame({"anio": pd.to_numeric(cn["Año.1"], errors="coerce"),
                        "acc": pd.to_numeric(cn.iloc[:, 7], errors="coerce")}).dropna()
    mitad = {}
    for _, r in acc.iterrows():
        for mes in ("01", "02"):
            mitad[pd.Period(f"{int(r.anio)}-{mes}", freq="M")] = r.acc / 2 / ancla * 100
    c["CN"] = c["CN"].fillna(pd.Series(mitad))
    return c


def armar() -> pd.DataFrame:
    c = paises()
    w = pd.Series(PESOS) / sum(PESOS.values())
    horeca = np.exp((np.log(c[list(PESOS)]) * w).sum(axis=1))
    horeca[c[list(PESOS)].isna().any(axis=1)] = np.nan

    R = pd.DataFrame({k: _ser(v, "M") for k, v in RIGOR.items()}).reindex(c.index).fillna(0.0)
    rigor = (R * w).sum(axis=1)

    out = pd.concat([c.add_prefix("h_"), horeca.rename("horeca_ue"),
                     rigor.rename("rigor"), R.add_prefix("rigor_")], axis=1)
    out.index.name = "per"
    return out


def grafico(d: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    coma = FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", "."))
    col = {"ES": "#1f4e79", "IT": "#c0504d", "CN": "#9bbb59", "JP": "#8064a2"}
    nom = {"ES": "España", "IT": "Italia", "CN": "China", "JP": "Japón"}
    fig, ax = plt.subplots(figsize=(9.4, 4.4))
    x = d.index.to_timestamp()
    for k in PESOS:
        ax.plot(x, d["h_" + k], lw=1.0, color=col[k], alpha=.75, label=nom[k])
    ax.plot(x, d.horeca_ue, lw=2.4, color="#303030",
            label="Índice combinado, ponderado por volumen del L1 tangonero")
    ax.set_ylabel("Índice de actividad, 2019 = 100")
    ax.yaxis.set_major_formatter(coma)
    ax.set_ylim(0, 190)
    ax.grid(axis="y", lw=.4, alpha=.4)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=8.2, ncol=2)
    base = d.loc["2019", "horeca_ue"].mean()
    mn = d.horeca_ue.min()
    ax.annotate(f"abril de 2020: {mn:.1f}".replace(".", ",")
                + f"\n({(mn / base - 1) * 100:.1f}% contra 2019)".replace(".", ","),
                xy=(pd.Timestamp("2020-04-01"), mn), xytext=(pd.Timestamp("2015-01-01"), 30),
                fontsize=8, color="#404040",
                arrowprops=dict(arrowstyle="->", color="#808080", lw=.8))
    fig.text(.01, .015,
             "Fuente: elaboración propia sobre INE (España, CNAE 56), ISTAT (Italia, Ateco 56; mensual desde 2021, "
             "trimestral antes), NBS (China, ingresos HORECA;\nenero y febrero se difunden "
             "acumulados y se reparten por mitades) y METI (Japón, índice de actividad terciaria, "
             "HORECA). Series sin ajuste estacional.", fontsize=6.6)
    fig.tight_layout(rect=(0, .055, 1, 1))
    out = os.path.join(RAIZ, "salidas", "horeca_indice.svg")
    fig.savefig(out); fig.savefig(out.replace(".svg", ".png"), dpi=200)
    print(f"Guardado: {out}")


def main() -> None:
    d = armar()
    out = os.path.join(RAIZ, "datos", "horeca_indice.pkl")
    d.to_pickle(out)
    print(f"Guardado: {out}  ({len(d)} meses, {d.index.min()} a {d.index.max()})")
    base = d.loc["2019", "horeca_ue"].mean()
    print(f"Mínimo del índice: {d.horeca_ue.idxmin()} = {d.horeca_ue.min():.1f} "
          f"({(d.horeca_ue.min() / base - 1) * 100:.1f}% contra el promedio de 2019)")
    print(d.loc["2019-12":"2021-06", ["h_ES", "h_IT", "h_CN", "h_JP", "horeca_ue", "rigor"]].round(1).to_string())
    grafico(d)


if __name__ == "__main__":
    main()
