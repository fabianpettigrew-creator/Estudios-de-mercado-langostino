# -*- coding: utf-8 -*-
"""Ecuador como control del competidor — y la tendencia que resulta no existir.

La carpeta «EXPO ECUADOR» trae la exportación ecuatoriana de camarón por subpartida de diez
dígitos y país de destino. Hay dos juegos de archivos y se usa el MENSUAL —«EXPO 2013 - 2021
MENSUAL.xlsx» y «EXPO 2022 - 2026 MENSUAL.xlsx», enero de 2013 a junio de 2026—, que es el que
permite meter a Ecuador en el modelo mensual sin interpolar nada. Los trece archivos anuales
sueltos dicen lo mismo agregado y quedan de contraste.

Para qué sirve. Hasta ahora el competidor entraba al modelo por el precio de importación de
camarón de cultivo de EUMOFA: un promedio de canasta sobre todas las tallas, presentaciones y
orígenes que entran a la Unión Europea. Con Ecuador se puede armar un control mucho mejor
emparejado: el precio del camarón ecuatoriano puesto en España, Italia y Francia, que son los
tres mercados del L1 tangonero.

Y ahí aparece el resultado que importa, con una corrección que hay que leer completa. La
tendencia del precio relativo del L1 depende de contra QUÉ se lo mida:

    canasta EUMOFA                      +2,13% por año   (t = 4,93)
    Ecuador a España, Italia y Francia  −0,14%           (t = −0,21)
    España contra España                +1,11% por año   (t = +2,43)

La comparación limpia es la última: precio del L1 argentino embarcado a España contra precio
del camarón ecuatoriano embarcado a España, mismo mercado y mismo mes. Ahí la tendencia es
REAL pero vale la MITAD de lo que marcaba la canasta de EUMOFA. El agregado de los tres
mercados da cero por su propia contaminación de composición —Ecuador se corrió hacia Italia y
Francia, que pagan más que España—, así que no es el que hay que citar.

Conclusión: la mitad de la «prima del salvaje que se ensancha» era artefacto del control
—Ecuador multiplicó su volumen con tallas chicas que van a China a precio bajando, y eso hunde
la canasta de EUMOFA más rápido que al langostino salvaje— y la otra mitad es una ampliación
genuina de la prima argentina en España.

La flexibilidad aguanta las tres versiones: entre −0,19 y −0,40.
"""
from __future__ import annotations

import glob
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 205)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402

EXPO_EC = os.environ.get("EXPO_ECUADOR_DIR", os.path.join(RAIZ, "..", "EXPO ECUADOR"))
MENSUALES = ("EXPO 2013 - 2021 MENSUAL.xlsx", "EXPO 2022 - 2026 MENSUAL.xlsx")
# Los archivos mensuales traen sólo la partida 0306.17. Los anuales traían además 0306.16
# —«decápodos de agua fría», que en Ecuador es una clasificación de arrastre de los primeros
# años: 73 kt en 2013 cayendo a 18 kt en 2024—, así que en 2013-2017 el volumen de la serie
# mensual queda 20-30% por debajo del de la anual. No afecta al PRECIO, que es el uso principal;
# sí hace que la expansión ecuatoriana se lea 5,6 veces en vez de 6,4. Se excluye además el
# camarón de río (macrobrachium), que no compite con el langostino.
EXCLUIR = ("0306179100",)
MES = {"Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Ago": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dic": 12}
# Códigos ISO: el archivo mensual trae el país por código, que es estable, y por nombre, que no.
UE = ["ESP", "ITA", "FRA", "NLD", "BEL", "DEU", "PRT", "DNK", "LTU", "POL", "GRC", "SWE",
      "IRL", "ROU", "LVA", "EST", "FIN", "AUT", "CZE", "BGR", "HRV", "SVN", "HUN", "MLT",
      "CYP", "SVK", "LUX"]
L1MKT = ["ESP", "ITA", "FRA"]               # los tres mercados del L1 tangonero
CHINA = "CHN"
HAC = 6


def _p(*t):
    return os.path.join(RAIZ, *t)


def cargar_ecuador() -> pd.DataFrame:
    """Los dos archivos mensuales, hoja «Columnas», encabezado en la fila 7 (índice 6).

    Período viene como «2022 / 01 - Ene»; FOB en miles de dólares; TM en toneladas netas.
    """
    fr = []
    for nom in MENSUALES:
        f = os.path.join(EXPO_EC, nom)
        d = pd.read_excel(f, sheet_name="Columnas", header=6).dropna(axis=1, how="all")
        d.columns = [str(c).strip() for c in d.columns]
        d = d.rename(columns={"Período": "per", "Código Subpartida": "sp", "Subpartida": "desc",
                              "Código País Destino": "iso", "País Destino": "pais",
                              "TM (Peso Neto)": "t", "FOB": "fob_mil"})
        fr.append(d[d.per.notna()][["per", "sp", "desc", "iso", "pais", "t", "fob_mil"]])
    E = pd.concat(fr, ignore_index=True)
    E["sp"] = E.sp.astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(10)
    pe = E.per.astype(str).str.extract(r"(\d{4})\s*/\s*(\d{2})")
    E["anio"] = pe[0].astype(int)
    E["mes"] = pe[1].astype(int)
    E["periodo"] = pd.PeriodIndex(pe[0] + "-" + pe[1], freq="M")
    E["iso"] = E.iso.astype(str).str.strip()
    for c in ("t", "fob_mil"):
        E[c] = pd.to_numeric(E[c], errors="coerce")
    E = E[E.t.notna() & (E.t > 0) & ~E.sp.isin(EXCLUIR)]
    return E.reset_index(drop=True)


def resumen(cam: pd.DataFrame) -> pd.DataFrame:
    def agg(d, por="anio"):
        g = d.groupby(por).agg(kt=("t", "sum"), fob=("fob_mil", "sum"))
        g["usd_kg"] = g.fob * 1000 / (g.kt * 1000)
        return g
    tot, chi = agg(cam), agg(cam[cam.iso == CHINA])
    ue, l1 = agg(cam[cam.iso.isin(UE)]), agg(cam[cam.iso.isin(L1MKT)])
    R = pd.DataFrame({
        "total_kt": tot.kt / 1000, "usd_kg_total": tot.usd_kg,
        "China_kt": chi.kt / 1000, "China_%": chi.kt / tot.kt * 100, "usd_kg_China": chi.usd_kg,
        "UE_kt": ue.kt / 1000, "UE_%": ue.kt / tot.kt * 100, "usd_kg_UE": ue.usd_kg,
        "ES_IT_FR_kt": l1.kt / 1000, "usd_kg_ES_IT_FR": l1.usd_kg})
    print("=" * 105)
    print("ECUADOR — EXPORTACIÓN DE CAMARÓN (0306.17), MENSUAL, ENE-2013 A JUN-2026")
    print("=" * 105)
    print(R.round(2).to_string())
    print(f"\n   volumen: {R.total_kt.iloc[0]:.0f} kt en {R.index[0]} → {R.total_kt.iloc[-1]:.0f} kt "
          f"en {R.index[-1]}  ({R.total_kt.iloc[-1] / R.total_kt.iloc[0]:.1f} veces)")
    print(f"   China:   {R['China_%'].iloc[0]:.1f}% del volumen → {R['China_%'].iloc[-1]:.1f}%")
    print(f"   precio a China contra precio a la UE, {R.index[-1]}: "
          f"{R.usd_kg_China.iloc[-1]:.2f} contra {R.usd_kg_UE.iloc[-1]:.2f} USD/kg "
          f"({R.usd_kg_China.iloc[-1] / R.usd_kg_UE.iloc[-1] - 1:+.0%})")
    return R


def series_mensuales(cam: pd.DataFrame, idx) -> pd.DataFrame:
    """Precio y volumen ecuatorianos, mensuales, sin interpolar nada."""
    def agg(d, pre):
        g = d.groupby("periodo").agg(t=("t", "sum"), fob=("fob_mil", "sum"))
        return pd.DataFrame({pre + "_kt": g.t / 1000, pre + "_usd": g.fob * 1000 / (g.t * 1000)})
    S = pd.concat([agg(cam, "ec"), agg(cam[cam.iso.isin(L1MKT)], "ecl1"),
                   agg(cam[cam.iso.isin(UE)], "ecue"), agg(cam[cam.iso == CHINA], "ecchn")],
                  axis=1).reindex(idx)
    S["ec_chi_pc"] = S.ecchn_kt / S.ec_kt * 100
    # La cantidad relevante como desplazador es el flujo acumulado de doce meses, igual que del
    # lado argentino: el precio de un mes responde al stock que llegó al mercado, no al embarque
    # de ese mes.
    for c in ("ec_kt", "ecl1_kt", "ecue_kt"):
        S[c + "12"] = S[c].rolling(12).sum()
    return S


def panel(R: pd.DataFrame, cam: pd.DataFrame):
    df, tan = T.panel()
    idx = df.index
    S = series_mensuales(cam, idx)
    df = df.join(S)
    df["ec_p"] = df.ecl1_usd            # precio ecuatoriano en España, Italia y Francia
    df["ec_q"] = df.ec_kt12             # oferta ecuatoriana total, doce meses
    e = T.despachos()
    e = e[(e.kg > 0) & (e.fob_tot > 0) & (e.pres == "entero")
          & (e.cal.isin(["L1", "L2"])) & (e.ruta == "a bordo")].copy()
    e.index = pd.PeriodIndex(e.anio.astype(str) + "-" + e.mes.astype(str).str.zfill(2), freq="M")
    e = e.sort_index()
    df["p_ab"] = (e.groupby(level=0).fob_tot.sum() / e.groupby(level=0).kg.sum()).reindex(idx)
    df["rel_eumofa"] = (df.p_ab / df.eurusd) / df.van_eur_kg
    df["rel_ecuador"] = df.p_ab / df.ec_p               # los dos en dólares
    B = df.dropna(subset=["rel_eumofa", "rel_ecuador", "tan12", "horeca", "ec_q"]).copy()
    B["lq"] = np.log(B.tan12)
    B["lecq"] = np.log(B.ec_q)
    B["lecp"] = np.log(B.ec_p)
    B["trend"] = np.arange(len(B)) / 12.0
    return B


def contraste(B):
    from linearmodels.iv import IV2SLS
    M = pd.get_dummies(B.index.month, prefix="m", drop_first=True).astype(float)
    M.index = B.index
    print("\n" + "=" * 105)
    print("LA TENDENCIA SIN NOMBRE ERA EL CONTROL")
    print("=" * 105)
    print(f"Muestra {B.index.min()} a {B.index.max()}, {len(B)} meses.")

    def ols(dep, X, nom):
        m = sm.OLS(np.log(B[dep]), sm.add_constant(pd.concat([B[X], M], axis=1))).fit(
            cov_type="HAC", cov_kwds={"maxlags": HAC})
        s = " · ".join(f"{v} {m.params[v]:+.3f} (t {m.tvalues[v]:+.2f})" for v in X)
        print(f"   MCO {nom:<40s} R2={m.rsquared:.3f}  {s}")

    def iv(dep, X, nom):
        ex = sm.add_constant(pd.concat([B[X], M], axis=1))
        r = IV2SLS(np.log(B[dep]), ex, B[["lq"]], B[["iv_conf"]]).fit(
            cov_type="kernel", kernel="bartlett")
        f, se = r.params["lq"], r.std_errors["lq"]
        otros = " · ".join(f"{v} {r.params[v]:+.3f}" for v in X if v != "horeca")
        print(f"   IV  {nom:<40s} f={f:+.3f} se {se:.3f} "
              f"IC[{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]  {otros}")

    print("\n   Dependiente: precio del L1 relativo a la CANASTA DE EUMOFA (el control actual)")
    ols("rel_eumofa", ["lq", "horeca", "trend"], "con tendencia")
    ols("rel_eumofa", ["lq", "horeca", "lecq"], "tendencia → oferta ecuatoriana")
    iv("rel_eumofa", ["horeca", "trend"], "con tendencia")
    iv("rel_eumofa", ["horeca", "lecq"], "tendencia → oferta ecuatoriana")

    print("\n   Dependiente: precio del L1 relativo al CAMARÓN ECUATORIANO en España, Italia y Francia")
    ols("rel_ecuador", ["lq", "horeca", "trend"], "con tendencia")
    ols("rel_ecuador", ["lq", "horeca"], "sin tendencia")
    iv("rel_ecuador", ["horeca", "trend"], "con tendencia")
    iv("rel_ecuador", ["horeca"], "sin tendencia")

    a, b = B.loc[:"2018-12"].rel_ecuador.mean(), B.loc["2019-01":].rel_ecuador.mean()
    print(f"\n   Prima del L1 tangonero sobre el camarón ecuatoriano en sus tres mercados:")
    print(f"      2013-2018 {a:.3f}   ·   2019-2026 {b:.3f}   ·   toda la serie {B.rel_ecuador.mean():.3f}")
    print("      Clavada. No hay prima que se ensanche: había una canasta que se hundía.")


def tres_referencias(cam: pd.DataFrame):
    """El mismo modelo contra tres definiciones del competidor. La tercera es la limpia."""
    from linearmodels.iv import IV2SLS
    df, tan = T.panel()
    idx = df.index

    def precio_ec(iso):
        z = cam[cam.iso.isin(iso)].groupby("periodo").agg(t=("t", "sum"), fob=("fob_mil", "sum"))
        return (z.fob * 1000 / (z.t * 1000)).reindex(idx)

    df["ec_esp"] = precio_ec(["ESP"])
    df["ec_l1"] = precio_ec(L1MKT)
    e = T.despachos()
    sel = ((e.kg > 0) & (e.fob_tot > 0) & (e.pres == "entero")
           & (e.cal.isin(["L1", "L2"])) & (e.ruta == "a bordo"))
    for nom, z in [("p_tot", e[sel]),
                   ("p_esp", e[sel & e.destino.astype(str).str.upper().str.contains("ESPA")])]:
        z = z.copy()
        z.index = pd.PeriodIndex(z.anio.astype(str) + "-" + z.mes.astype(str).str.zfill(2), freq="M")
        df[nom] = (z.groupby(level=0).fob_tot.sum() / z.groupby(level=0).kg.sum()).reindex(idx)
    df["r_eumofa"] = (df.p_tot / df.eurusd) / df.van_eur_kg
    df["r_ec_l1"] = df.p_tot / df.ec_l1
    df["r_ec_esp"] = df.p_esp / df.ec_esp
    B = df.dropna(subset=["r_eumofa", "r_ec_l1", "r_ec_esp", "tan12", "horeca"]).copy()
    B["lq"] = np.log(B.tan12)
    B["trend"] = np.arange(len(B)) / 12.0
    M = pd.get_dummies(B.index.month, prefix="m", drop_first=True).astype(float)
    M.index = B.index

    print("\n" + "=" * 105)
    print("TRES DEFINICIONES DEL COMPETIDOR — y por qué la tercera es la que vale")
    print("=" * 105)
    print(f"Muestra {B.index.min()} a {B.index.max()}, {len(B)} meses.")
    filas = []
    for dep, nom in [("r_eumofa", "canasta EUMOFA (el control actual)"),
                     ("r_ec_l1", "Ecuador a España, Italia y Francia"),
                     ("r_ec_esp", "España contra España — mismo mercado, mismo mes")]:
        m = sm.OLS(np.log(B[dep]), sm.add_constant(pd.concat([B[["lq", "horeca", "trend"]], M],
                                                             axis=1))).fit(
            cov_type="HAC", cov_kwds={"maxlags": HAC})
        ex = sm.add_constant(pd.concat([B[["horeca", "trend"]], M], axis=1))
        r = IV2SLS(np.log(B[dep]), ex, B[["lq"]], B[["iv_conf"]]).fit(
            cov_type="kernel", kernel="bartlett")
        ex0 = sm.add_constant(pd.concat([B[["horeca"]], M], axis=1))
        r0 = IV2SLS(np.log(B[dep]), ex0, B[["lq"]], B[["iv_conf"]]).fit(
            cov_type="kernel", kernel="bartlett")
        print(f"   {nom:<48s} tendencia {m.params['trend'] * 100:+5.2f}%/año "
              f"(t {m.tvalues['trend']:+5.2f})   f con tendencia {r.params['lq']:+.3f}   "
              f"f sin tendencia {r0.params['lq']:+.3f} (se {r0.std_errors['lq']:.3f})")
        filas.append({"referencia": nom, "tendencia_%_anual": m.params["trend"] * 100,
                      "t": m.tvalues["trend"], "f_con_tendencia": r.params["lq"],
                      "f_sin_tendencia": r0.params["lq"], "se": r0.std_errors["lq"]})
    print("\n   El agregado de los tres mercados da cero por contaminación propia: Ecuador se")
    print("   corrió hacia Italia y Francia, que pagan más que España. La comparación de un solo")
    print("   mercado saca esa composición y deja +1,11%/año, la mitad de lo que marca EUMOFA.")
    return B, pd.DataFrame(filas)


def softrade_espana():
    """Despachos transacción por transacción de Ecuador a España, 0306.17.99, 2020 a jul-2026."""
    fs = sorted(glob.glob(os.path.join(EXPO_EC, "Softrade_EC_export_*.xlsx")))
    if not fs:
        return None
    S = pd.concat([pd.read_excel(f, sheet_name="Exportaciones") for f in fs], ignore_index=True)
    S.columns = [str(c).strip() for c in S.columns]
    S["Fecha"] = pd.to_datetime(S["Fecha"], errors="coerce")
    S["anio"] = S.Fecha.dt.year
    S["kg"] = pd.to_numeric(S["Kgs. Netos"], errors="coerce")
    S["fob"] = pd.to_numeric(S["U$S FOB"], errors="coerce")
    S = S[(S.kg > 0) & (S.fob > 0)].copy()
    d = S["Descripción Comercial"].astype(str).str.upper()
    t = d.str.extract(r"(?:T\.?\s*|TALLA\s*)(\d{1,3})\s*[-/]\s*(\d{1,3})")
    S["t0"] = pd.to_numeric(t[0], errors="coerce")
    S["t1"] = pd.to_numeric(t[1], errors="coerce")
    S["mid"] = (S.t0 + S.t1) / 2
    S["pelado"] = d.str.contains("PELAD|TAIL OFF|PUD|P&D|DESVENAD", na=False)

    print("\n" + "=" * 105)
    print("DESPACHOS ECUADOR → ESPAÑA, 0306.17.99, TRANSACCIÓN POR TRANSACCIÓN")
    print("=" * 105)
    print(f"{len(S)} despachos · {S.kg.sum() / 1e6:.1f} kt · {S.Fecha.min():%b-%Y} a {S.Fecha.max():%b-%Y}")

    print("\n   ATENCIÓN — este flujo es mayormente INTRA-GRUPO, así que sus valores unitarios")
    print("   son en buena parte precios de transferencia y no precios de mercado:")
    ex = S.groupby(S.Exportador.astype(str).str.strip()).kg.sum().sort_values(ascending=False)
    co = S.groupby(S.Comprador.astype(str).str.strip()).kg.sum().sort_values(ascending=False)
    print(f"      Promarisco S.A. (brazo ecuatoriano de Pescanova) embarca "
          f"{ex.iloc[0] / S.kg.sum():.0%} de los kilos")
    pes = co[co.index.str.contains("Pescanova", case=False)].sum()
    print(f"      Pescanova España, en sus distintas grafías, recibe {pes / S.kg.sum():.0%}")

    E = S[S.t0.notna() & ~S.pelado]
    print(f"\n   Cobertura de talla en la descripción: {S.t0.notna().mean():.1%} de las filas y "
          f"sólo {S.loc[S.t0.notna(), 'kg'].sum() / S.kg.sum():.1%} de los kilos, y se desploma")
    print("   después de 2021. No alcanza para armar una serie de precio emparejada por talla.")
    b = E.assign(banda=E.t0.astype(int).astype(str) + "-" + E.t1.astype(int).astype(str))
    g = b.groupby("banda").apply(lambda x: pd.Series(
        {"kt": x.kg.sum() / 1e6, "usd_kg": x.fob.sum() / x.kg.sum(), "n": len(x)}))
    print("\n   Precio por banda de talla (piezas por kilo, producto entero):")
    print(g[g.kt > 0.05].sort_values("kt", ascending=False).round(2).to_string())

    # UNIDAD DEL CONTEO. La descripción comercial NUNCA declara si la talla va en
    # piezas por kilo o por libra: ni una sola fila con talla trae la marca. La
    # unidad se INFIERE de la forma de la banda, y conviven dos convenciones:
    #   · bandas de decena (20/30 … 80/100), que es como grada la UE, por KILO
    #   · escalera estándar de EE.UU. (16/20, 21/25, 26/30 … 71/90), por LIBRA
    #   · bandas irregulares y errores de tipeo (40/48, 24/40, 80/10, 60/40)
    # Leer la escalera americana como si fuera por kilo fabrica pendiente: esas
    # filas traen números bajos y precio alto (6,61 contra 4,79 USD/kg), o sea
    # parecen «camarón grande y caro». Con ellas adentro el gradiente da −0,277;
    # convertidas a piezas por kilo da −0,112. Como el dato no permite decidir
    # cuál de las dos lecturas corresponde, el gradiente que se reporta se estima
    # sobre la submuestra homogénea de bandas de decena, que no obliga a elegir.
    ESCALERA_LB = {"16/20", "21/25", "26/30", "31/35", "36/40", "41/50", "51/60",
                   "61/70", "71/90", "11/15", "91/110"}
    BANDAS_KG = {"20/30", "30/40", "40/50", "50/60", "60/70", "70/80", "80/100",
                 "90/120", "100/120"}
    E = E.assign(cod=E.t0.astype(int).astype(str) + "/" + E.t1.astype(int).astype(str))
    E = E.assign(fam=np.where(E.cod.isin(ESCALERA_LB), "libra",
                              np.where(E.cod.isin(BANDAS_KG), "kilo", "otra")))
    rep = E.groupby("fam").kg.sum() / E.kg.sum() * 100
    print("\n   Unidad del conteo: la descripción no la declara en ninguna fila. Por la forma")
    print("   de la banda, {:.1f}% de los kilos está en bandas de decena (convención UE, por"
          .format(rep.get("kilo", 0.0)))
    print("   kilo), {:.1f}% en la escalera estándar de EE.UU. (por libra) y {:.1f}% en bandas"
          .format(rep.get("libra", 0.0), rep.get("otra", 0.0)))
    print("   irregulares. El gradiente se estima sólo sobre las primeras.")

    def _gradiente(sub, etiqueta):
        A = pd.get_dummies(sub.anio, prefix="a", drop_first=True).astype(float)
        m = sm.WLS(np.log(sub.fob / sub.kg),
                   sm.add_constant(pd.concat([np.log(sub[["mid"]]), A], axis=1)),
                   weights=sub.kg).fit(cov_type="HC1")
        g = m.params["mid"]
        tal = (sub.mid * sub.kg).sum() / sub.kg.sum()
        return g, m.tvalues["mid"], int(m.nobs), tal, np.exp(-g * np.log(tal / 15.5))

    E2 = E[(E.mid > 10) & (E.mid < 120) & (E.fam == "kilo")].copy()
    g_t, t_t, n_t, tal_ec, aj = _gradiente(E2, "homogénea")
    print(f"\n   Gradiente precio-talla: {g_t:+.3f} (t {t_t:+.2f}, N = {n_t}), sobre bandas de")
    print(f"   decena solamente. Rango medido: {E2.mid.min():.0f} a {E2.mid.max():.0f} piezas por kilo.")
    print(f"   Ecuador embarca a España un promedio de {tal_ec:.0f} piezas por kilo. El L1 argentino")
    print(f"   son 11 a 20, o sea 15,5 de media: es unas {tal_ec / 15.5:.1f} veces más grande.")
    print(f"   Con ese gradiente, un camarón ecuatoriano del tamaño del L1 valdría {aj:.2f} veces el")
    print(f"   promedio ecuatoriano a España ({aj - 1:+.0%}).")

    todo = E[(E.mid > 10) & (E.mid < 120)].copy()
    g_a, t_a, n_a, _, aj_a = _gradiente(todo, "todo como kilo")
    conv = todo.assign(mid=todo.mid.where(todo.fam != "libra", todo.mid * 2.20462))
    g_c, t_c, n_c, _, aj_c = _gradiente(conv, "libra convertida")
    print("\n   Sensibilidad a la lectura de la unidad (por qué importa):")
    print(f"     todo leído como por kilo      gradiente {g_a:+.3f} (t {t_a:+.2f})  ajuste {aj_a:.2f}x")
    print(f"     escalera convertida a kilo    gradiente {g_c:+.3f} (t {t_c:+.2f})  ajuste {aj_c:.2f}x")
    print(f"     sólo bandas de decena         gradiente {g_t:+.3f} (t {t_t:+.2f})  ajuste {aj:.2f}x")

    print("\n   OJO, tres salvedades. Primera: la unidad del conteo es inferida, no declarada.")
    print("   Segunda: NINGUNA de estas filas declara presentación, así que el gradiente mezcla")
    print("   entero con cabeza y descabezado con caparazón, que para el mismo animal tienen")
    print(f"   conteos por kilo muy distintos. Tercera: el gradiente se mide entre {E2.mid.min():.0f} y "
          f"{E2.mid.max():.0f}")
    print("   piezas por kilo y el L1 está en 15,5, así que el ajuste es extrapolación fuera de")
    print("   muestra, y sobre un flujo mayormente intra-grupo. Es indicativo, no establecido.")
    return S


def main():
    cam = cargar_ecuador()
    R = resumen(cam)
    B = panel(R, cam)
    contraste(B)
    B3, T3 = tres_referencias(cam)
    SO = softrade_espana()
    with pd.ExcelWriter(_p("salidas", "ecuador_competidor.xlsx")) as w:
        R.to_excel(w, sheet_name="ecuador_anual")
        cam.groupby(["anio", "sp", "desc"]).agg(
            t=("t", "sum"), fob_mil=("fob_mil", "sum")).to_excel(w, sheet_name="por_subpartida")
        cam.groupby(["anio", "pais"]).agg(
            t=("t", "sum"), fob_mil=("fob_mil", "sum")).to_excel(w, sheet_name="por_destino")
        cam.groupby(["periodo", "iso"]).agg(
            t=("t", "sum"), fob_mil=("fob_mil", "sum")).to_excel(w, sheet_name="mensual_destino")
        B[["p_ab", "van_eur_kg", "ec_p", "ec_q", "ec_chi_pc", "ecl1_kt", "ecue_usd",
           "ecchn_usd", "rel_eumofa", "rel_ecuador", "tan12", "horeca"]].to_excel(
               w, sheet_name="panel_mensual")
        T3.to_excel(w, sheet_name="tres_referencias", index=False)
        B3[["p_tot", "p_esp", "ec_esp", "ec_l1", "van_eur_kg",
            "r_eumofa", "r_ec_l1", "r_ec_esp"]].to_excel(w, sheet_name="panel_referencias")
        if SO is not None:
            SO[["Fecha", "anio", "NANDINA", "Exportador", "Comprador", "kg", "fob",
                "t0", "t1", "mid", "pelado", "Descripción Comercial"]].to_excel(
                    w, sheet_name="softrade_espana", index=False)
    print("\nEscrito: salidas/ecuador_competidor.xlsx")
    return R, B


if __name__ == "__main__":
    main()
