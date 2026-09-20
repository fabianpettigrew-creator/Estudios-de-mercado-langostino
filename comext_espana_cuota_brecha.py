# -*- coding: utf-8 -*-
"""Cuota de origen y brecha de precio en la importación española de camarón
congelado, 2013 a julio de 2026.

Dos preguntas, dos gráficos:

  1. CUOTA. Cuánto del camarón congelado que entra a España viene de cada origen.
     Argentina venía sosteniendo alrededor de un tercio del mercado desde 2013 y en
     2025 cayó a 20,9%, el mínimo de toda la serie, mientras Ecuador pasó a 48,3%.

  2. BRECHA. Por qué. Hasta 2017 el langostino argentino entraba a España MÁS BARATO
     que el vannamei; desde 2018 la relación se dio vuelta y la brecha no paró de
     abrirse: +1,61 EUR/kg en 2025 y +2,20 EUR/kg en lo que va de 2026, o sea un
     langostino que cuesta casi un 50% más que el camarón de cultivo.

FUENTE. Eurostat, base Comext, dataset DS-045409, declarante España, flujo
importación, Nomenclatura Combinada a 8 dígitos, mensual, 2013-01 a 2026-07. Es la
declaración de la aduana española, no un espejo. El valor es CIF en frontera
española. Los datos de 2025 y 2026 son provisionales y Eurostat puede revisarlos.

QUÉ MIDE Y QUÉ NO. Todo el capítulo congelado (NC 0306.16 y 0306.17), que es el 99,6%
de lo que España importa del rubro. El langostino argentino (Pleoticus muelleri) se
clasifica en 0306.17.99 y el vannamei ecuatoriano en 0306.17.92, pero acá los orígenes
se miden por país socio y no por posición, que es lo que corresponde para hablar de
cuota de mercado. Las toneladas son de PRODUCTO tal como entra —entero y cola, todos
los calibres—, no peso entero equivalente, y el precio es un valor unitario que se
mueve también con la mezcla de producto de cada mes: no es una cotización.

Para el panel de cuota se usa una ventana móvil de 12 meses. El langostino argentino
entra concentrado en el cuarto trimestre y el ecuatoriano llega parejo todo el año, de
modo que una cuota mensual o de año parcial estaría sesgada por estacionalidad. La
ventana móvil la saca y además deja llegar la serie hasta julio de 2026.

Uso:  python comext_espana_cuota_brecha.py
Salida: consola
        salidas/espana_cuota_origen_2013_2026.svg   (+ .png)
        salidas/espana_brecha_precio_2013_2026.svg  (+ .png)
        salidas/Espana_cuota_y_brecha_2013_2026.xlsx
"""
from __future__ import annotations

import os
import sys

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from biblioteca import fuente
BASES = os.environ.get("BASES_DIR", fuente("eumofa_a"))
COMEXT = os.path.join(
    BASES, "Importaciones_Espana_langostino_NC8_mensual_2013-2026.xlsx")
SAL = os.path.join(RAIZ, "salidas")

AZUL, ROJO, GRIS = "#1f4e79", "#c0504d", "#9aa7ad"
VERDE, ARENA = "#4f7942", "#c9b48a"
ULTIMO = "2026-07"


# --------------------------------------------------------------------- datos
def cargar() -> pd.DataFrame:
    """Hoja «Datos» de Comext: una fila por mes x NC8 x país. Sólo congelado."""
    if not os.path.exists(COMEXT):
        sys.exit(f"ABORTA: no encontré la base de Comext en {COMEXT}")
    try:
        wb = openpyxl.load_workbook(COMEXT, read_only=True)
    except PermissionError:
        # la base vive en OneDrive: si está abierta en Excel o sincronizando,
        # se lee una copia temporal en lugar de abortar
        import shutil
        import tempfile
        tmp = os.path.join(tempfile.gettempdir(), "_comext_es.xlsx")
        shutil.copy2(COMEXT, tmp)
        print("aviso: la base estaba bloqueada; se leyó una copia temporal")
        wb = openpyxl.load_workbook(tmp, read_only=True)
    ws = wb["Datos"]
    it = ws.iter_rows(values_only=True)
    next(it)
    f = [(r[0], r[1], r[5], r[7], r[9], r[10]) for r in it if r[0] is not None]
    d = pd.DataFrame(f, columns=["anio", "mes", "tipo", "pais", "eur", "t"])
    d = d[d.tipo == "Congelado"].copy()
    d["eur"] = pd.to_numeric(d.eur, errors="coerce").fillna(0.0)
    d["t"] = pd.to_numeric(d.t, errors="coerce").fillna(0.0)
    d["per"] = pd.PeriodIndex(
        d.anio.astype(str) + "-" + d.mes.astype(str).str.zfill(2), freq="M")
    return d


def mensual(d: pd.DataFrame) -> pd.DataFrame:
    """Toneladas y euros por mes, para el total y para cada origen relevante."""
    idx = pd.period_range("2013-01", ULTIMO, freq="M")
    m = pd.DataFrame(index=idx)
    m["t"] = d.groupby("per").t.sum().reindex(idx).fillna(0.0)
    m["eur"] = d.groupby("per").eur.sum().reindex(idx).fillna(0.0)
    for k, pais in (("ar", "Argentina"), ("ec", "Ecuador"), ("cn", "China")):
        s = d[d.pais == pais]
        m[f"{k}_t"] = s.groupby("per").t.sum().reindex(idx).fillna(0.0)
        m[f"{k}_eur"] = s.groupby("per").eur.sum().reindex(idx).fillna(0.0)
        m[f"{k}_p"] = m[f"{k}_eur"] / (m[f"{k}_t"] * 1000.0)
    m["resto_t"] = m.t - m.ar_t - m.ec_t - m.cn_t
    m["p"] = m.eur / (m.t * 1000.0)

    # ventana móvil de 12 meses: cuota sin estacionalidad y precio ponderado
    r = m.rolling(12, min_periods=12).sum()
    for k in ("ar", "ec", "cn"):
        m[f"{k}_cuota12"] = 100.0 * r[f"{k}_t"] / r["t"]
        m[f"{k}_p12"] = r[f"{k}_eur"] / (r[f"{k}_t"] * 1000.0)
    m["resto_cuota12"] = 100.0 * r["resto_t"] / r["t"]
    m["brecha12"] = m.ar_p12 - m.ec_p12
    m["ratio12"] = m.ar_p12 / m.ec_p12
    m["brecha"] = m.ar_p - m.ec_p
    return m


def anual(d: pd.DataFrame) -> pd.DataFrame:
    """Lo mismo por año. 2026 es parcial: enero a julio."""
    a = pd.DataFrame(index=sorted(d.anio.unique()))
    a["t"] = d.groupby("anio").t.sum()
    a["eur"] = d.groupby("anio").eur.sum()
    a["p"] = a.eur / (a.t * 1000.0)
    for k, pais in (("ar", "Argentina"), ("ec", "Ecuador"), ("cn", "China")):
        s = d[d.pais == pais]
        a[f"{k}_t"] = s.groupby("anio").t.sum().reindex(a.index).fillna(0.0)
        a[f"{k}_eur"] = s.groupby("anio").eur.sum().reindex(a.index).fillna(0.0)
        a[f"{k}_p"] = a[f"{k}_eur"] / (a[f"{k}_t"] * 1000.0)
        a[f"{k}_cuota"] = 100.0 * a[f"{k}_t"] / a["t"]
    a["resto_t"] = a.t - a.ar_t - a.ec_t - a.cn_t
    a["resto_cuota"] = 100.0 * a.resto_t / a.t
    a["brecha"] = a.ar_p - a.ec_p
    a["ratio"] = a.ar_p / a.ec_p
    return a


# ------------------------------------------------------------------ gráficos
def _ejes(ax) -> None:
    ax.grid(lw=.4, alpha=.4)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _coma(dec: int):
    from matplotlib.ticker import FuncFormatter
    return FuncFormatter(lambda x, _: f"{x:,.{dec}f}".replace(",", " ")
                         .replace(".", ",").replace(" ", "."))


def grafico_cuota(m: pd.DataFrame, a: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = m.index.to_timestamp()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9.2, 7.0),
                                 gridspec_kw={"height_ratios": [1.3, 1]})
    for ax in (a1, a2):
        _ejes(ax)

    # ---------------------------------------------------------- panel 1
    a1.plot(x, m.ec_cuota12, lw=1.8, color=ROJO, label="Ecuador")
    a1.plot(x, m.ar_cuota12, lw=1.8, color=AZUL, label="Argentina")
    a1.plot(x, m.cn_cuota12, lw=1.3, color=VERDE, label="China")
    a1.plot(x, m.resto_cuota12, lw=1.1, color=GRIS, ls="--",
            label="Resto del mundo")
    a1.set_ylabel("Cuota del volumen importado (%)")
    a1.set_ylim(0, 55)
    a1.yaxis.set_major_formatter(_coma(0))
    a1.legend(frameon=False, fontsize=8.4, loc="upper left", ncol=4)
    a1.set_title("España: de dónde viene el camarón congelado que importa\n"
                 "Cuota de cada origen en el volumen, ventana móvil de 12 meses",
                 fontsize=11, color=AZUL, loc="left")

    ult = m.index[-1]
    sup = m.ec_cuota12 > m.ar_cuota12          # primer mes en que Ecuador pasa
    cruce = sup.idxmax() if sup.any() else None
    for k, col, nom in (("ec", ROJO, "Ecuador"), ("ar", AZUL, "Argentina")):
        v = m[f"{k}_cuota12"].iloc[-1]
        a1.annotate(f"{nom}: {v:.1f}%".replace(".", ","),
                    (ult.to_timestamp(), v), xytext=(6, 0),
                    textcoords="offset points", fontsize=8.6, color=col,
                    va="center", fontweight="bold")
    if cruce is not None:
        a1.axvline(cruce.to_timestamp(), lw=.8, color="#7f7f7f", ls=":")
        a1.annotate(f"primer cruce: Ecuador pasa\na Argentina en {cruce.year}-"
                    f"{cruce.month:02d}",
                    (cruce.to_timestamp(), 43), xytext=(-8, 0),
                    textcoords="offset points", fontsize=8, color="#404040",
                    ha="right", va="top")

    # ---------------------------------------------------------- panel 2
    an = a.loc[2013:2026]
    xb = np.arange(len(an))
    b1 = a2.bar(xb, an.ar_t / 1000, .62, color=AZUL, label="Argentina")
    b2 = a2.bar(xb, an.ec_t / 1000, .62, bottom=an.ar_t / 1000, color=ROJO,
                label="Ecuador")
    b3 = a2.bar(xb, (an.cn_t + an.resto_t) / 1000, .62,
                bottom=(an.ar_t + an.ec_t) / 1000, color=ARENA,
                label="China y resto del mundo")
    for b in (b1, b2, b3):          # el año parcial va rayado
        b[-1].set_hatch("///")
        b[-1].set_alpha(.75)
    a2.set_xticks(xb)
    a2.set_xticklabels([str(y) if y != 2026 else "2026\nene-jul" for y in an.index],
                       fontsize=8.2)
    a2.set_ylabel("Miles de toneladas")
    a2.yaxis.set_major_formatter(_coma(0))
    a2.legend(frameon=False, fontsize=8.4, loc="upper left", ncol=3)
    for i, y in enumerate(an.index):
        a2.annotate(f"{an.ar_cuota[y]:.0f}%", (i, an.ar_t[y] / 2000),
                    fontsize=7.6, color="white", ha="center", va="center",
                    fontweight="bold")
    a2.set_title("Volumen anual por origen, y cuota argentina sobre cada barra",
                 fontsize=10, color=AZUL, loc="left")

    fig.text(.01, .012,
             "Fuente: elaboración propia sobre Eurostat-Comext, dataset DS-045409, "
             "declarante España, flujo importación, NC 8 dígitos, mensual 2013-01 a "
             "2026-07. Camarón y langostino CONGELADO (NC 0306.16\ny 0306.17), que es "
             "el 99,6% de lo que España importa del rubro. Toneladas de producto tal "
             "como entra —entero y cola, todos los calibres—, no peso entero "
             "equivalente. Los orígenes son país socio de\nEurostat: para extra-UE es "
             "país de origen. 2026 es año parcial (enero a julio) y va rayado; 2025 y "
             "2026 son datos provisionales. La ventana móvil de 12 meses del panel "
             "superior saca la\nestacionalidad, que en el caso argentino es fuerte "
             "porque el grueso llega en el cuarto trimestre. "
             "Elaboración: Lic. Fabián Pettigrew · AXIA.",
             fontsize=6.6)
    fig.tight_layout(rect=(0, .085, 1, 1))
    out = os.path.join(SAL, "espana_cuota_origen_2013_2026.svg")
    fig.savefig(out)
    fig.savefig(out.replace(".svg", ".png"), dpi=200)
    plt.close(fig)
    print("Gráfico:", out, "(+ .png)")


def grafico_brecha(m: pd.DataFrame, a: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = m.index.to_timestamp()
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(9.2, 8.2), sharex=True,
                                     gridspec_kw={"height_ratios": [1.5, 1, 1]})
    for ax in (a1, a2, a3):
        _ejes(ax)

    # ---------------------------------------------------------- panel 1
    a1.plot(x, m.ar_p, lw=.8, color=AZUL, alpha=.30)
    a1.plot(x, m.ec_p, lw=.8, color=ROJO, alpha=.30)
    a1.plot(x, m.ar_p12, lw=2.0, color=AZUL,
            label="Langostino argentino (CIF en frontera española)")
    a1.plot(x, m.ec_p12, lw=2.0, color=ROJO,
            label="Camarón ecuatoriano (CIF en frontera española)")
    a1.set_ylabel("Euros por kilo")
    a1.yaxis.set_major_formatter(_coma(2))
    a1.legend(frameon=False, fontsize=8.4, loc="upper left")
    a1.set_title("España: qué paga por el langostino argentino y qué paga por el "
                 "camarón ecuatoriano\nValor unitario CIF. Línea gruesa: ventana "
                 "móvil de 12 meses. Línea fina: mes a mes",
                 fontsize=11, color=AZUL, loc="left")
    for k, col, nom in (("ar", AZUL, "Argentina"), ("ec", ROJO, "Ecuador")):
        v = m[f"{k}_p12"].iloc[-1]
        a1.annotate(f"{nom}: {v:.2f}".replace(".", ","),
                    (m.index[-1].to_timestamp(), v), xytext=(6, 0),
                    textcoords="offset points", fontsize=8.6, color=col,
                    va="center", fontweight="bold")

    # ---------------------------------------------------------- panel 2
    a2.fill_between(x, 0, m.brecha12, where=m.brecha12 >= 0, color=AZUL, alpha=.22)
    a2.fill_between(x, 0, m.brecha12, where=m.brecha12 < 0, color=ROJO, alpha=.22)
    a2.plot(x, m.brecha12, lw=1.8, color=AZUL)
    a2.axhline(0, lw=.9, color="#7f7f7f")
    a2.set_ylabel("Brecha (EUR/kg)")
    a2.set_ylim(-1.05, 2.35)
    a2.yaxis.set_major_formatter(_coma(2))
    a2.annotate("hasta 2017 el langostino argentino\nentraba MÁS BARATO que el "
                "vannamei", (pd.Timestamp("2016-06-01"), -.45),
                xytext=(pd.Timestamp("2013-04-01"), 1.35), fontsize=8.2,
                color=ROJO, va="center",
                arrowprops={"arrowstyle": "-", "lw": .7, "color": "#d9a7a4",
                            "shrinkA": 4, "shrinkB": 4})
    v = m.brecha12.iloc[-1]
    a2.annotate(f"{v:+.2f} EUR/kg".replace(".", ","),
                (m.index[-1].to_timestamp(), v), xytext=(6, 0),
                textcoords="offset points", fontsize=8.6, color=AZUL,
                va="center", fontweight="bold")
    a2.set_title("Brecha absoluta: precio argentino menos precio ecuatoriano",
                 fontsize=10, color=AZUL, loc="left")

    # ---------------------------------------------------------- panel 3
    a3.plot(x, m.ratio12, lw=1.8, color=AZUL)
    a3.axhline(1, lw=.9, color="#7f7f7f")
    a3.set_ylabel("Cociente AR / EC")
    a3.yaxis.set_major_formatter(_coma(2))
    for y0, dx, dy in ((2016, 0, 28), (2020, -52, 22), (2025, -46, 16)):
        if y0 in a.index:
            a3.annotate(f"promedio {y0}: {a.ratio[y0]:.2f}".replace(".", ","),
                        (pd.Timestamp(f"{y0}-07-01"), a.ratio[y0]),
                        xytext=(dx, dy), textcoords="offset points", fontsize=8,
                        color="#404040", ha="center",
                        arrowprops={"arrowstyle": "-", "lw": .7,
                                    "color": "#a8a8a8", "shrinkA": 3,
                                    "shrinkB": 3})
    v = m.ratio12.iloc[-1]
    a3.annotate(f"{v:.2f}".replace(".", ",") + "  →  el langostino cuesta "
                f"{(v - 1) * 100:.0f}% más", (m.index[-1].to_timestamp(), v),
                xytext=(-6, -14), textcoords="offset points", fontsize=8.6,
                color=AZUL, ha="right", va="top", fontweight="bold")
    a3.set_title("Brecha relativa: cuántas veces el precio ecuatoriano",
                 fontsize=10, color=AZUL, loc="left")

    fig.text(.01, .012,
             "Fuente: elaboración propia sobre Eurostat-Comext, dataset DS-045409, "
             "declarante España, flujo importación, NC 8 dígitos, mensual 2013-01 a "
             "2026-07. Camarón y langostino CONGELADO (NC 0306.16\ny 0306.17). El "
             "valor unitario CIF en frontera española es valor declarado sobre kilos: "
             "no es una cotización, se mueve también con la mezcla de producto, "
             "presentación y calibre de cada mes.\nLas dos puntas no son el mismo "
             "producto —el argentino es pesca salvaje, entero y cola; el ecuatoriano "
             "es vannamei de cultivo—, así que la brecha mezcla precio con producto: "
             "lo que importa es\ncómo se movió. La ventana móvil de 12 meses pondera "
             "por volumen. 2025 y 2026 son provisionales. "
             "Elaboración: Lic. Fabián Pettigrew · AXIA.",
             fontsize=6.6)
    fig.tight_layout(rect=(0, .075, 1, 1))
    out = os.path.join(SAL, "espana_brecha_precio_2013_2026.svg")
    fig.savefig(out)
    fig.savefig(out.replace(".svg", ".png"), dpi=200)
    plt.close(fig)
    print("Gráfico:", out, "(+ .png)")


# ---------------------------------------------------------------- planilla
HDR = Font(name="Arial", size=10, bold=True, color="FFFFFF")
AR_ = Font(name="Arial", size=10)
TIT = Font(name="Arial", size=13, bold=True, color="1F4E79")
SUB = Font(name="Arial", size=9, color="5A5A5A")
FA = PatternFill("solid", fgColor="1F4E79")
FG = PatternFill("solid", fgColor="F2F5F8")
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DER = Alignment(horizontal="right")


def _hoja(wb, nombre, titulo, bajada, enc, filas, fmts, anchos):
    ws = wb.create_sheet(nombre)
    ws["A1"] = titulo
    ws["A1"].font = TIT
    ws["A2"] = bajada
    ws["A2"].font = SUB
    ws["A2"].alignment = Alignment(vertical="top", wrap_text=True)
    for j, t in enumerate(enc, start=1):
        c = ws.cell(4, j, t)
        c.font, c.fill, c.alignment = HDR, FA, CEN
    ws.row_dimensions[4].height = 32
    for i, fila in enumerate(filas):
        for j, (v, fm) in enumerate(zip(fila, fmts), start=1):
            c = ws.cell(5 + i, j, None if (isinstance(v, float) and np.isnan(v))
                        else v)
            c.font = AR_
            if fm:
                c.number_format, c.alignment = fm, DER
            if i % 2:
                c.fill = FG
    for j, w in enumerate(anchos, start=1):
        ws.column_dimensions[L(j)].width = w
    ws.freeze_panes = "B5"
    return ws


def planilla(m: pd.DataFrame, a: pd.DataFrame) -> None:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    F2, F0, FP = "#,##0.00", "#,##0", '#,##0.0"%"'

    _hoja(wb, "Anual",
          "España — importación de camarón congelado por origen, 2013 a julio 2026",
          "Eurostat-Comext DS-045409, NC 0306.16 y 0306.17, valor CIF en frontera "
          "española. 2026 es parcial (enero a julio). 2025 y 2026, provisionales.",
          ["Año", "Total (t)", "Total (EUR/kg)", "Argentina (t)", "Argentina cuota",
           "Argentina (EUR/kg)", "Ecuador (t)", "Ecuador cuota", "Ecuador (EUR/kg)",
           "China (t)", "China cuota", "Resto (t)", "Resto cuota",
           "Brecha AR-EC (EUR/kg)", "Cociente AR/EC"],
          [[int(y), a.t[y], a.p[y], a.ar_t[y], a.ar_cuota[y], a.ar_p[y],
            a.ec_t[y], a.ec_cuota[y], a.ec_p[y], a.cn_t[y], a.cn_cuota[y],
            a.resto_t[y], a.resto_cuota[y], a.brecha[y], a.ratio[y]]
           for y in a.index],
          ["0", F0, F2, F0, FP, F2, F0, FP, F2, F0, FP, F0, FP, F2, F2],
          [8, 11, 13, 12, 12, 14, 11, 11, 13, 10, 10, 10, 10, 14, 12])

    _hoja(wb, "Mensual",
          "Serie mensual y ventana móvil de 12 meses",
          "La ventana móvil pondera por volumen dentro de los 12 meses: saca la "
          "estacionalidad, que del lado argentino es fuerte porque el grueso llega en "
          "el cuarto trimestre. Las primeras 11 filas van vacías en las columnas de "
          "ventana móvil porque todavía no hay 12 meses.",
          ["Mes", "Total (t)", "Argentina (t)", "Argentina (EUR/kg)", "Ecuador (t)",
           "Ecuador (EUR/kg)", "Brecha del mes", "Cuota AR 12m", "Cuota EC 12m",
           "Cuota CN 12m", "AR 12m (EUR/kg)", "EC 12m (EUR/kg)", "Brecha 12m",
           "Cociente 12m"],
          [[f"{p.year}-{p.month:02d}", m.t[p], m.ar_t[p], m.ar_p[p], m.ec_t[p],
            m.ec_p[p], m.brecha[p], m.ar_cuota12[p], m.ec_cuota12[p],
            m.cn_cuota12[p], m.ar_p12[p], m.ec_p12[p], m.brecha12[p], m.ratio12[p]]
           for p in m.index],
          [None, "#,##0.0", "#,##0.0", F2, "#,##0.0", F2, F2, FP, FP, FP, F2, F2,
           F2, F2],
          [10, 11, 12, 14, 11, 13, 12, 12, 12, 12, 14, 14, 11, 12])

    notas = [
        ("De dónde sale cada número", True),
        ("Eurostat, base Comext, dataset DS-045409 «EU trade since 1988 by HS2-4-6 "
         "and CN8». Declarante España, flujo importación, Nomenclatura Combinada a 8 "
         "dígitos, mensual, enero de 2013 a julio de 2026. Es la declaración de la "
         "aduana española, no un espejo de lo que declara el exportador.", False),
        ("Se toma todo el capítulo CONGELADO —NC 0306.16 y 0306.17—, que en 2025 fue "
         "el 99,6% del volumen que España importó del rubro. Queda afuera lo vivo, "
         "fresco o refrigerado, lo seco o salado, y los preparados y conservas de la "
         "partida 1605.", False),
        ("", False),
        ("Qué miden las toneladas y qué mide el precio", True),
        ("Las toneladas son de PRODUCTO tal como entra al país: entero y cola, todos "
         "los calibres, todas las presentaciones. No es peso de langostino entero "
         "equivalente y no se puede sumar contra desembarques.", False),
        ("El precio es valor declarado sobre kilos, CIF en frontera española, o sea "
         "que incluye flete y seguro. No es una cotización: se mueve con el precio "
         "pero también con la mezcla de producto y de calibre de cada mes. Por eso no "
         "es comparable con el FOB de despacho de origen, que es más bajo por "
         "construcción.", False),
        ("", False),
        ("La comparación Argentina contra Ecuador no es de producto idéntico", True),
        ("Del lado argentino es pesca salvaje de Pleoticus muelleri, que en la "
         "nomenclatura va a 0306.17.99 —más del 99,9% del volumen de origen "
         "Argentina—. Del lado ecuatoriano es vannamei de cultivo, que va a "
         "0306.17.92. Son dos productos distintos con dos estructuras de costo "
         "distintas, y buena parte de la brecha es diferencia de producto y de "
         "calibre, no sólo de precio. Lo que el gráfico muestra es cómo se movió esa "
         "brecha en el tiempo, que es la pregunta relevante para la sustitución.", False),
        ("", False),
        ("Por qué ventana móvil de 12 meses", True),
        ("El langostino argentino entra concentrado en el cuarto trimestre y el "
         "ecuatoriano llega parejo todo el año. Una cuota mensual, o la de un año "
         "parcial como 2026, quedaría sesgada por esa estacionalidad. La ventana "
         "móvil de 12 meses la elimina y deja que la serie llegue hasta julio de "
         "2026.", False),
        ("", False),
        ("Advertencias", True),
        ("Los datos de 2025 y 2026 son provisionales: Eurostat los revisa.", False),
        ("2026 cubre enero a julio. En los gráficos el año parcial va rayado y en las "
         "tablas está señalado.", False),
        ("El origen es el país socio de Eurostat: para extra-UE es país de origen, "
         "pero para intra-UE es el Estado miembro de expedición. Por eso Portugal, "
         "Bélgica o Países Bajos aparecen como «origen» de producto que en realidad "
         "reexportan.", False),
        ("", False),
        ("Reproducibilidad", True),
        ("«comext_espana_cuota_brecha.py». Elaboración: Lic. Fabián Pettigrew · AXIA.",
         False),
    ]
    ws = wb.create_sheet("Notas")
    ws.column_dimensions["A"].width = 118
    for i, (t, neg) in enumerate(notas, start=1):
        c = ws.cell(i, 1, t)
        c.font = Font(name="Arial", size=10, bold=neg,
                      color="1F4E79" if neg else "1A1A1A")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if not neg and t:
            ws.row_dimensions[i].height = 14 * (1 + len(t) // 108)

    for h in wb.sheetnames:
        wb[h].sheet_properties.tabColor = "7F7F7F" if h == "Notas" else "1F4E79"
    out = os.path.join(SAL, "Espana_cuota_y_brecha_2013_2026.xlsx")
    wb.save(out)
    print("Planilla:", out)


# -------------------------------------------------------------------- main
def main() -> None:
    d = cargar()
    m, a = mensual(d), anual(d)

    print("=" * 96)
    print("ESPAÑA — IMPORTACIÓN DE CAMARÓN CONGELADO POR ORIGEN, 2013 a julio 2026")
    print("=" * 96)
    print(f"Filas de Comext (congelado): {len(d):,}   ·   "
          f"meses: {m.index[0]} a {m.index[-1]}")
    print(f"Control: total 2025 = {a.t[2025]:,.1f} t  ·  "
          f"suma de orígenes = {a.ar_t[2025] + a.ec_t[2025] + a.cn_t[2025] + a.resto_t[2025]:,.1f} t")

    print("\n" + "-" * 96)
    print("ANUAL  (2026 = enero a julio)")
    print("-" * 96)
    print(f"{'Año':>6} {'Total kt':>9} {'AR kt':>8} {'cuota':>7} {'AR €/kg':>8} "
          f"{'EC kt':>8} {'cuota':>7} {'EC €/kg':>8} {'brecha':>8} {'ratio':>6}")
    for y in a.index:
        print(f"{y:>6} {a.t[y] / 1000:9,.1f} {a.ar_t[y] / 1000:8,.1f} "
              f"{a.ar_cuota[y]:6.1f}% {a.ar_p[y]:8.2f} {a.ec_t[y] / 1000:8,.1f} "
              f"{a.ec_cuota[y]:6.1f}% {a.ec_p[y]:8.2f} {a.brecha[y]:+8.2f} "
              f"{a.ratio[y]:6.2f}")

    print("\n" + "-" * 96)
    print("VENTANA MÓVIL DE 12 MESES — último dato")
    print("-" * 96)
    u = m.index[-1]
    print(f"A {u}:  Argentina {m.ar_cuota12[u]:.1f}% de cuota y "
          f"{m.ar_p12[u]:.2f} EUR/kg  ·  Ecuador {m.ec_cuota12[u]:.1f}% y "
          f"{m.ec_p12[u]:.2f} EUR/kg")
    print(f"           brecha {m.brecha12[u]:+.2f} EUR/kg  ·  cociente "
          f"{m.ratio12[u]:.2f}  ·  el langostino cuesta "
          f"{(m.ratio12[u] - 1) * 100:.0f}% más")
    pico = m.ar_cuota12.idxmax()
    piso = m.ar_cuota12.idxmin()
    print(f"Cuota argentina 12m:  máximo {m.ar_cuota12[pico]:.1f}% en {pico}  ·  "
          f"mínimo {m.ar_cuota12[piso]:.1f}% en {piso}")

    grafico_cuota(m, a)
    grafico_brecha(m, a)
    planilla(m, a)


if __name__ == "__main__":
    main()
