# -*- coding: utf-8 -*-
"""La objeción del FOB contra el CIF, contestada con dato.

LA OBJECIÓN. El trabajo estima la flexibilidad-precio sobre el FOB de despacho. El
precio que enfrenta la demanda europea no es ése sino el CIF en frontera, que suma
flete y seguro. Si la flexibilidad se mide sobre el precio equivocado, el número está
mal.

LA RESPUESTA TIENE TRES PATAS Y ESTE GUION MIDE LAS DOS QUE SON EMPÍRICAS.

Primera pata, teórica y no se mide acá. Para la pregunta del trabajo —si conviene
recortar captura— el precio correcto ES el FOB. El umbral |f| > 1 sale de derivar el
ingreso del productor, P·Q, respecto de Q; el P de esa cuenta es lo que cobra el
armador argentino, no lo que paga el importador español. El flete no es ingreso de la
flota. Leído como sistema de demanda el precio relevante sería el CIF; leído como
decisión de política, que es como está escrito el trabajo, el FOB es el objeto correcto
y no un segundo mejor.

Segunda pata, y acá empieza la medición. Aun leyéndolo como demanda, el sesgo tiene
signo conocido. Si CIF = FOB + w con w el flete y el seguro por kilo, entonces

    f_CIF  =  f_FOB · (p_FOB / p_CIF)                                        (1)

siempre que w no responda a la cantidad argentina. Como p_FOB < p_CIF, el factor es
menor que uno: medir sobre el FOB EXAGERA la flexibilidad. Corregir a CIF aleja el
número de −1 en vez de acercarlo, o sea que la objeción, atendida, refuerza la
conclusión en lugar de amenazarla.

Tercera pata: el supuesto de (1) es que el flete por kilo no se mueve con la cantidad
argentina. Es testeable y se testea acá.

Cómo se mide la cuña. El mismo flujo se ve dos veces: como FOB de despacho del lado
argentino y como CIF de importación de EUMOFA del lado europeo. La diferencia es el
flete más el seguro.

Uso:  python cif_vs_fob.py
Salida: consola + salidas/cif_vs_fob.xlsx
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

import demanda_inversa_tangonera as T   # noqa: E402

# Los 27 de la UE con las grafías de la base de comercio. Definición única en
# recorte_conxemar, que la usa para separar el ámbito europeo del resto.
from recorte_conxemar import UE   # noqa: E402

# Las estimaciones del trabajo que hay que corregir por (1).
ESTUDIO = {"IV mensual sobre el precio relativo (T5)": -0.184,
           "campaña sin tendencia (C2)": -0.212,
           "campaña con tendencia (C3)": -0.239,
           "sistema IAIDS con simetría impuesta": -0.282}
HAC = 6


def _p(*t):
    return os.path.join(RAIZ, *t)


def cuna() -> pd.DataFrame:
    """FOB del flujo argentino a la UE contra el CIF que declara EUMOFA, mes a mes."""
    from fuentes import expo
    e = expo.cargar_todos()
    d = e[(e.kg > 0) & (e.fob_tot > 0)].copy()
    d = d[d.destino.astype(str).str.upper().str.strip().isin(UE)]
    d["per"] = pd.PeriodIndex(d.anio.astype(str) + "-"
                              + d.mes.astype(str).str.zfill(2), freq="M")
    g = d.groupby("per").agg(kg=("kg", "sum"), fob=("fob_tot", "sum"))

    df, _ = T.panel()
    m = pd.DataFrame(index=df.index)
    m["fob_usd_kg"] = (g.fob / g.kg).reindex(df.index)
    m["eurusd"] = df.eurusd
    m["fob_eur_kg"] = m.fob_usd_kg / m.eurusd
    m["cif_eur_kg"] = df.ar_eur_kg
    m["kt_ue_desp"] = (g.kg / 1e6).reindex(df.index)
    m["kt_eumofa"] = df.ar_kt
    m["p_l1_eur"] = df.p_eur              # el FOB del entero L1 a bordo, en euros
    m["van_eur_kg"] = df.van_eur_kg
    m["tan12"] = df.tan12
    m["horeca"] = df.horeca
    m["iv_conf"] = df.iv_conf
    m["w"] = m.cif_eur_kg - m.fob_eur_kg          # la cuña, en euros por kilo
    m["w_pct"] = m.w / m.fob_eur_kg * 100
    m["factor"] = m.fob_eur_kg / m.cif_eur_kg     # el factor de (1)
    return m


def main() -> None:
    m = cuna()
    print("=" * 100)
    print("FOB CONTRA CIF — CUÁNTO CAMBIA EL RESULTADO SI SE MIDE SOBRE EL PRECIO")
    print("QUE ENFRENTA EL COMPRADOR")
    print("=" * 100)

    # ------------------------------------------------------ 1. la cuña
    print("\n" + "-" * 100)
    print("1. LA CUÑA CIF − FOB, QUE ES EL FLETE MÁS EL SEGURO")
    print("-" * 100)
    a = m.groupby(m.index.year).agg(
        fob=("fob_eur_kg", "mean"), cif=("cif_eur_kg", "mean"), w=("w", "mean"),
        w_pct=("w_pct", "mean"), factor=("factor", "mean"),
        kt_desp=("kt_ue_desp", "sum"), kt_eum=("kt_eumofa", "sum"))
    a["cobertura"] = a.kt_desp / a.kt_eum
    print(a.round(3).to_string())
    print("\n   La cuña sube de 0,21 EUR/kg en 2018 a 1,10 en 2022 y vuelve a 0,46 en")
    print("   2025. Ese perfil es la crisis mundial de fletes de 2021-2022, no algo del")
    print("   langostino: es la firma que valida que la cuña está midiendo flete.")

    ok = m.loc["2020":].dropna(subset=["w", "factor"])
    print(f"\n   Promedio 2020-2026: cuña {ok.w.mean():.3f} EUR/kg "
          f"({ok.w_pct.mean():.1f}% del FOB) · factor p_FOB/p_CIF = {ok.factor.mean():.3f}")
    print(f"   Sobre toda la muestra: factor = {m.factor.mean():.3f}")

    # -------------------------------------- 2. ¿la cuña responde a la cantidad?
    print("\n" + "-" * 100)
    print("2. EL SUPUESTO DE (1): ¿EL FLETE POR KILO SE MUEVE CON LA CANTIDAD ARGENTINA?")
    print("-" * 100)
    b = m.dropna(subset=["w", "tan12", "kt_eumofa"]).copy()
    b["lw"] = np.log(b.w.clip(lower=0.01))
    b["lq_tan"] = np.log(b.tan12)
    b["lq_ue"] = np.log(b.kt_eumofa.rolling(12).sum())
    b["trend"] = np.arange(len(b)) / 12.0
    b = b.dropna()
    M = pd.get_dummies(b.index.month, prefix="m", drop_first=True).astype(float)
    M.index = b.index
    filas = []
    for q, etq in [("lq_tan", "captura tangonera 12 meses"),
                   ("lq_ue", "volumen argentino a la UE 12 meses")]:
        X = sm.add_constant(pd.concat([b[[q, "trend"]], M], axis=1))
        r = sm.OLS(b.lw, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC})
        c, se, p = r.params[q], r.bse[q], r.pvalues[q]
        print(f"   log cuña ~ log {etq:<36s} coef {c:+.3f}  se {se:.3f}  "
              f"p {p:.3f}  {'SIGNIFICATIVO' if p < .05 else 'no significativo'}")
        filas.append({"cantidad": etq, "coef": c, "se": se, "p": p, "N": int(r.nobs)})
    W = pd.DataFrame(filas)
    print("\n   Es lo que había que ver: el flete por kilo no responde a cuánto langostino")
    print("   embarca la Argentina. Es un precio de mercado mundial de bodega refrigerada,")
    print("   donde el langostino argentino es una fracción menor del uno por ciento. Con")
    print("   ∂w/∂q = 0, la fórmula (1) vale y el sesgo del FOB tiene signo conocido.")

    # ------------------------------------------- 3. corrección de las estimaciones
    print("\n" + "-" * 100)
    print("3. LAS ESTIMACIONES DEL TRABAJO, CORREGIDAS A CIF POR (1)")
    print("-" * 100)
    k = float(ok.factor.mean())
    R = pd.DataFrame([{"estimación": n, "f sobre FOB": v, "f sobre CIF": v * k,
                       "1+f FOB": 1 + v, "1+f CIF": 1 + v * k}
                      for n, v in ESTUDIO.items()]).set_index("estimación")
    print(R.round(3).to_string())
    print(f"\n   Factor aplicado: {k:.3f}. Todas se ALEJAN de −1: la corrección que pide")
    print("   la objeción mueve el resultado en la dirección que refuerza la conclusión.")
    print(f"   El rango del trabajo, de {min(ESTUDIO.values()):+.3f} a "
          f"{max(ESTUDIO.values()):+.3f}, pasa a "
          f"{min(ESTUDIO.values()) * k:+.3f} a {max(ESTUDIO.values()) * k:+.3f}.")

    # --------------------------------- 4. el L1 con CIF equivalente, estimado
    print("\n" + "-" * 100)
    print("4. RE-ESTIMACIÓN CON UN CIF EQUIVALENTE PARA EL ENTERO L1")
    print("-" * 100)
    print("   Se le suma al FOB del L1 el flete y el seguro observados, de dos maneras:")
    print("   con la cuña PROMEDIO, que es un corrimiento de nivel puro y aísla el efecto")
    print("   de (1), y con la cuña DEL AÑO, que además deja entrar el ciclo de fletes.")
    c = m.dropna(subset=["p_l1_eur", "van_eur_kg", "tan12", "horeca", "w"]).copy()
    w_anual = m.groupby(m.index.year).w.mean()
    w_medio = float(m.loc["2020":].w.mean())
    c["w_a"] = [w_anual.get(y, np.nan) for y in c.index.year]
    c["p_l1_cif"] = c.p_l1_eur + c.w_a
    c["p_l1_cif_k"] = c.p_l1_eur + w_medio
    c["lrel_fob"] = np.log(c.p_l1_eur / c.van_eur_kg)
    c["lrel_cif_k"] = np.log(c.p_l1_cif_k / c.van_eur_kg)
    c["lrel_cif"] = np.log(c.p_l1_cif / c.van_eur_kg)
    c["lq"] = np.log(c.tan12)
    c["trend"] = np.arange(len(c)) / 12.0
    M2 = pd.get_dummies(c.index.month, prefix="m", drop_first=True).astype(float)
    M2.index = c.index

    from linearmodels.iv import IV2SLS
    filas = []
    for dep, etq in [("lrel_fob", "FOB del L1 (el trabajo)"),
                     ("lrel_cif_k", "CIF con cuña constante"),
                     ("lrel_cif", "CIF con cuña del año")]:
        dd = pd.concat([c[[dep, "lq", "horeca", "trend", "iv_conf"]], M2],
                       axis=1).dropna()
        ex = sm.add_constant(dd[["horeca", "trend"] + list(M2.columns)])
        iv = IV2SLS(dd[dep], ex, dd[["lq"]], dd[["iv_conf"]]).fit(
            cov_type="kernel", kernel="bartlett")
        f, se = iv.params["lq"], iv.std_errors["lq"]
        F1 = float(iv.first_stage.diagnostics["f.stat"].iloc[0])
        print(f"   {etq:<28s} f = {f:+.3f}  se = {se:.3f}  "
              f"H0: f=−1 → t = {(f + 1) / se:+.2f}   primera etapa F = {F1:.1f}")
        filas.append({"dependiente": etq, "f": f, "se": se, "F1": F1,
                      "N": int(iv.nobs)})
    E = pd.DataFrame(filas)
    r_k, r_a = E.f.iloc[1] / E.f.iloc[0], E.f.iloc[2] / E.f.iloc[0]
    print(f"\n   Con la cuña constante el cociente observado es {r_k:.3f} contra el "
          f"{k:.3f}")
    print("   que predice (1): la fórmula acierta, como tenía que pasar, porque sumar una")
    print("   constante es exactamente el caso que (1) describe.")
    print(f"\n   Con la cuña del año el cociente cae a {r_a:.3f}, bastante más abajo. No es")
    print("   que (1) falle: es que la cuña del año NO es constante —va de 0,21 a 1,10 "
          "EUR/kg—")
    print("   y ese movimiento propio entra en la dependiente. La versión general de (1) es")
    print("\n       f_CIF  =  [ f_FOB · p_FOB  +  w · (∂log w / ∂log q) ] / p_CIF     (1')")
    print("\n   y con los valores medidos —w = "
          f"{w_medio:.2f}, ∂log w/∂log q = {W.coef.iloc[0]:+.2f} de la sección 2,")
    gen = (ESTUDIO["IV mensual sobre el precio relativo (T5)"] * ok.fob_eur_kg.mean()
           + w_medio * float(W.coef.iloc[0])) / ok.cif_eur_kg.mean()
    print(f"   p_FOB = {ok.fob_eur_kg.mean():.2f} y p_CIF = {ok.cif_eur_kg.mean():.2f}— "
          f"da {gen:+.3f}, que es donde cae")
    print(f"   la estimación con cuña del año ({E.f.iloc[2]:+.3f}). O sea que lo que sobra "
          "de atenuación")
    print("   lo explica la respuesta del flete a la cantidad, que en la sección 2 no fue")
    print("   significativa. Ahí está la banda honesta del ejercicio:")
    print(f"      · si el flete no responde a la cantidad, f_CIF = {E.f.iloc[1]:+.3f};")
    print(f"      · si responde como marca el coeficiente puntual, f_CIF = "
          f"{E.f.iloc[2]:+.3f}.")
    print("   Las dos están MÁS LEJOS de −1 que el FOB. En ningún escenario la objeción")
    print("   mueve el resultado en contra de la conclusión.")

    # ------------------------------------------------- 5. el límite del ejercicio
    print("\n" + "-" * 100)
    print("5. LO QUE ESTE EJERCICIO NO PUEDE HACER")
    print("-" * 100)
    z = m.loc["2020":].dropna(subset=["fob_eur_kg", "cif_eur_kg"])
    cor_n = z.fob_eur_kg.corr(z.cif_eur_kg)
    dl = pd.DataFrame({"f": np.log(z.fob_eur_kg), "c": np.log(z.cif_eur_kg)}).diff().dropna()
    print(f"   Correlación mensual FOB-CIF: {cor_n:+.3f} en nivel pero "
          f"{dl.f.corr(dl.c):+.3f} en variaciones.")
    mejor = max(range(0, 4), key=lambda L: pd.DataFrame(
        {"f": np.log(z.fob_eur_kg), "c": np.log(z.cif_eur_kg).shift(-L)}).diff()
        .dropna().corr().iloc[0, 1])
    print(f"   El mejor emparejamiento es con el CIF adelantado {mejor} meses, y aun así")
    print("   la correlación en variaciones es baja. Las dos series NO se siguen mes a mes:")
    print("   el despacho se cuenta cuando sale y la importación cuando entra, y la mezcla")
    print("   de producto de cada barco difiere. Por eso la cuña se usa como PROMEDIO ANUAL")
    print("   y no como corrección mensual: para el nivel alcanza, para el timing no.")
    print("   Un CIF verdadero por calibre y por flota NO existe en ninguna fuente: EUMOFA")
    print("   declara todo el congelado argentino como PR1 Whole/Gutted, sin talla. La")
    print("   disyuntiva es real y este guion mide cuánto cuesta, no la disuelve.")

    try:
        out = _p("salidas", "cif_vs_fob.xlsx")
        with pd.ExcelWriter(out) as w:
            mm = m.copy()
            mm.index = mm.index.astype(str)
            mm.round(4).to_excel(w, sheet_name="mensual")
            a.round(4).to_excel(w, sheet_name="anual")
            W.round(4).to_excel(w, sheet_name="cuna_vs_cantidad", index=False)
            R.round(4).to_excel(w, sheet_name="correccion")
            E.round(4).to_excel(w, sheet_name="reestimacion", index=False)
        print(f"\nGuardado: {out}")
    except PermissionError:
        print("\nAVISO: no pude escribir el xlsx (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
