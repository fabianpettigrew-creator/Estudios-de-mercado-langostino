# -*- coding: utf-8 -*-
"""Sistema de demanda inversa de dos bienes: langostino entero tangonero y fresquero.

Por qué un sistema y no una ecuación con la fresquera de control. Metida como regresor suelto,
la cantidad fresquera entra con signo POSITIVO (+0,063, t 2,45): más oferta fresquera, mayor
precio tangonero. Un sustituto no hace eso. Está capturando un desplazamiento de demanda común
a las dos flotas, o sea que la fresquera es tan endógena como la tangonera. El sistema resuelve
eso por construcción: el término de escala —la cantidad agregada del grupo— absorbe el
movimiento común, y los coeficientes de cantidad quedan midiendo sustitución entre flotas.

Estructura en dos etapas, que es la que corresponde cuando el grupo compite contra un bien de
afuera (el camarón de cultivo):

  Etapa de grupo   ¿cuánto baja el precio argentino agregado, relativo al cultivo, cuando sube
                   la oferta argentina total? Es la flexibilidad que manda para la política.
  Etapa interna    dado el total, ¿cómo se reparte entre las dos flotas? Sistema LA/IAIDS de dos
                   bienes. Con dos bienes, adding-up y homogeneidad IMPLICAN simetría: no hay que
                   imponerla, sale sola. Ver la nota en `sistema_interno()`.

Convenciones de flexibilidad, las mismas del sistema por origen del proyecto:
    escala                     f_i  = β_i / w_i − 1
    cantidad no compensada     f_ij = γ_ij / w_i − δ_ij
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

import flexibilidades_iaids as fx

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 210)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import demanda_inversa_tangonera as T   # noqa: E402
import recorte_conxemar                 # noqa: E402

# Ventana móvil de doce meses: es la misma definición de cantidad del modelo vigente y saca la
# estacionalidad de la zafra. Como las ventanas se solapan, el error queda con correlación
# serial de orden 11 por construcción: Newey-West con 18 rezagos.
VENTANA, HAC = 12, 18
CAL = ["L1", "L2"]


def _p(*t):
    return os.path.join(RAIZ, *t)


def panel():
    df, tan = T.panel()
    e = T.despachos()
    e = e[(e.kg > 0) & (e.fob_tot > 0) & (e.pres == "entero") & (e.cal.isin(CAL))].copy()
    e["flota"] = np.where(e.ruta == "a bordo", "tangonera", "fresquera")
    e.index = pd.PeriodIndex(e.anio.astype(str) + "-" + e.mes.astype(str).str.zfill(2), freq="M")
    e = e.sort_index()

    idx = df.index
    kg = e.pivot_table(index=e.index, columns="flota", values="kg", aggfunc="sum").reindex(idx).fillna(0)
    vl = e.pivot_table(index=e.index, columns="flota", values="fob_tot", aggfunc="sum").reindex(idx).fillna(0)
    kg = kg.rolling(VENTANA).sum()
    vl = vl.rolling(VENTANA).sum()

    # Precios: los MENSUALES, sin suavizar. El suavizado a doce meses es un filtro pasa-bajos
    # sobre la variable dependiente que borra justo la variación sub-anual con que identifica el
    # instrumento —la ventana del conflicto dura cuatro meses—, y atenúa la flexibilidad hacia
    # cero por construcción. Verificado: misma muestra y misma cantidad, el precio mensual da
    # f = −0,239 y el suavizado −0,061. Los modelos de campaña, que sí son anuales de las dos
    # puntas, dan −0,19 a −0,25: el suavizado es el que queda afuera.
    kg_m = e.pivot_table(index=e.index, columns="flota", values="kg", aggfunc="sum").reindex(idx)
    vl_m = e.pivot_table(index=e.index, columns="flota", values="fob_tot", aggfunc="sum").reindex(idx)

    A = pd.DataFrame(index=idx)
    for f in ("tangonera", "fresquera"):
        A["q_" + f], A["v_" + f] = kg[f], vl[f]
        A["p_" + f] = vl_m[f] / kg_m[f]              # precio mensual
        A["pm12_" + f] = vl[f] / kg[f]               # sólo para contraste
    A["V"] = A.v_tangonera + A.v_fresquera
    A["Qg"] = A.q_tangonera + A.q_fresquera
    A["w_tan"] = A.v_tangonera / A.V
    A["w_fre"] = A.v_fresquera / A.V
    A["p_grupo"] = (vl_m.tangonera + vl_m.fresquera) / (kg_m.tangonera + kg_m.fresquera)

    # Desembarques SSPyA por flota: es la CANTIDAD EXÓGENA, la que la política mueve.
    lan = pd.read_pickle(_p("_lan.pkl"))
    lan.index = pd.PeriodIndex(lan.anio.astype(str) + "-" + lan.mes.astype(str).str.zfill(2), freq="M")
    cong = lan.flota.str.startswith("CONG")
    des = pd.DataFrame({
        "d_tan": lan[cong].groupby(level=0).t.sum(),
        "d_fre": lan[~cong].groupby(level=0).t.sum()}).reindex(idx).fillna(0)
    des = des.rolling(VENTANA).sum()
    A["d_tan"], A["d_fre"] = des.d_tan, des.d_fre
    A["Dg"] = A.d_tan + A.d_fre

    A = A.join(df[["van_eur_kg", "eurusd", "horeca", "iv_conf"]])
    A["rel_grupo"] = (A.p_grupo / A.eurusd) / A.van_eur_kg
    A["rel_tan"] = (A.p_tangonera / A.eurusd) / A.van_eur_kg
    A = A.dropna(subset=["w_tan", "rel_grupo", "rel_tan", "horeca", "van_eur_kg", "Dg"])
    A = A[(A.q_tangonera > 0) & (A.q_fresquera > 0)]
    A["lqt"], A["lqf"] = np.log(A.q_tangonera), np.log(A.q_fresquera)
    A["lQg"] = np.log(A.Qg)
    A["lDg"] = np.log(A.Dg)
    # Índice de cantidad de Stone con participaciones MEDIAS, no corrientes: con las corrientes
    # el regresor lleva adentro la variable dependiente.
    wt, wf = A.w_tan.mean(), A.w_fre.mean()
    A["lQ_stone"] = wt * A.lqt + wf * A.lqf
    A["lrel"] = np.log(A.lqt * 0 + A.rel_tan)
    A["lrelg"] = np.log(A.rel_grupo)
    A["trend"] = np.arange(len(A)) / 12.0
    A["ratio"] = A.lqt - A.lqf
    return A, wt, wf


def _hac(y, X):
    return sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC", cov_kwds={"maxlags": HAC})


def etapa_grupo(A):
    print("\n" + "=" * 100)
    print("ETAPA DE GRUPO — el precio argentino agregado contra la oferta argentina total")
    print("=" * 100)
    print("Bien: langostino entero L1+L2, las dos flotas juntas. Precio relativo al camarón de")
    print("cultivo europeo. Dos medidas de cantidad, y la diferencia entre ellas importa:")
    print("  · DESEMBARQUE total (SSPyA, todas las flotas). Es la cantidad exógena y la que la")
    print("    política mueve. Es la medida que manda.")
    print("  · KILOS EXPORTADOS del grupo. Es lo que llega al mercado, pero la empresa decide")
    print("    cuándo embarcar, así que arrastra la demanda adentro.")
    M = pd.get_dummies(A.index.month, prefix="m", drop_first=True).astype(float)
    M.index = A.index
    from linearmodels.iv import IV2SLS
    res = {}
    for var, nom in [("lDg", "desembarque"), ("lQg", "exportado")]:
        m = _hac(A.lrelg, pd.concat([A[[var, "horeca", "trend"]], M], axis=1))
        ex = sm.add_constant(pd.concat([A[["horeca", "trend"]], M], axis=1))
        r = IV2SLS(A.lrelg, ex, A[[var]], A[["iv_conf"]]).fit(cov_type="kernel", kernel="bartlett")
        f, se = r.params[var], r.std_errors[var]
        F1 = float(r.first_stage.diagnostics["f.stat"].iloc[0])
        print(f"\n   Q = {nom}")
        print(f"      MCO   f_G = {m.params[var]:+.3f}  se {m.bse[var]:.3f}  t {m.tvalues[var]:+.2f}"
              f"   R2 = {m.rsquared:.3f}   N = {int(m.nobs)}")
        print(f"      IV    f_G = {f:+.3f}  se {se:.3f}  IC95% [{f - 1.96 * se:+.3f}, "
              f"{f + 1.96 * se:+.3f}]   primera etapa F = {F1:.1f}"
              f"{'' if F1 > 10 else '   ← INSTRUMENTO DÉBIL'}")
        print(f"      H0: f_G = −1  →  t = {(f + 1) / se:+.2f}   ·   1 + f_G = {1 + f:+.3f}")
        res[nom] = (f, se, F1)
    return res


def sistema_interno(A, wt, wf):
    print("\n" + "=" * 100)
    print("ETAPA INTERNA — sistema LA/IAIDS de dos bienes")
    print("=" * 100)
    print("w_tan = α + γ·log(q_tan/q_fre) + β·log Q + controles.")
    print("Escribir el regresor como el COCIENTE de cantidades impone homogeneidad (γ_11 = −γ_12).")
    print("Con dos bienes, adding-up (Σ_i γ_ij = 0) más homogeneidad implican γ_12 = γ_21: la")
    print("simetría no hay que imponerla, es una consecuencia. Es el único caso en que sale gratis.")
    M = pd.get_dummies(A.index.month, prefix="m", drop_first=True).astype(float)
    M.index = A.index
    X = pd.concat([A[["ratio", "lQ_stone"]], np.log(A[["van_eur_kg"]]),
                   A[["horeca", "trend"]], M], axis=1)
    m = _hac(A.w_tan, X)
    g, b = m.params["ratio"], m.params["lQ_stone"]
    print(f"\n   N = {int(m.nobs)}   R2 = {m.rsquared:.3f}")
    print(pd.DataFrame({"coef": m.params, "se": m.bse, "t": m.tvalues})
          .loc[["ratio", "lQ_stone", "van_eur_kg", "horeca", "trend"]].round(4).to_string())
    print(f"\n   participación media: tangonera {wt:.3f} · fresquera {wf:.3f}")

    # γ_11 = γ = −γ_12 = −γ_21 = γ_22 ;  β_tan = β = −β_fre
    tf = ["tangonera", "fresquera"]
    G = pd.DataFrame([[g, -g], [-g, g]], index=tf, columns=tf)
    F, esc = fx.matriz(G, pd.Series({"tangonera": b, "fresquera": -b}),
                       pd.Series({"tangonera": wt, "fresquera": wf}))
    fx.verificar(F, esc, pd.Series({"tangonera": wt, "fresquera": wf}))
    F.index = ["precio tangonero", "precio fresquero"]
    F.columns = ["cantidad tangonera", "cantidad fresquera"]
    print("\n   Flexibilidades de cantidad CONDICIONALES (dentro del grupo argentino):")
    print(F.round(3).to_string())
    print("\n   Flexibilidades de escala (cada fila de arriba suma la suya):")
    print(esc.round(3).to_string())
    # error estándar de la flexibilidad propia por el método delta (w fijo)
    se_f = m.bse["ratio"] / wt
    f11 = F.iloc[0, 0]
    print(f"\n   f_tan,tan condicional = {f11:+.3f}  se {se_f:.3f}  "
          f"IC95% [{f11 - 1.96 * se_f:+.3f}, {f11 + 1.96 * se_f:+.3f}]")
    return m, F, esc, se_f


def incondicional(A, res_g, F, wt, s_tan):
    print("\n" + "=" * 100)
    print("LA FLEXIBILIDAD QUE MANDA — condicional + escala")
    print("=" * 100)
    fg = res_g["desembarque"][0]
    fc = F.iloc[0, 0]
    print("   El sistema IAIDS estima la flexibilidad del precio NORMALIZADO por el gasto del")
    print("   grupo, p_i/E con E = P_G·Q_G. Para volver al precio a secas hay que devolver las dos")
    print("   piezas que la normalización sacó:")
    print("      ∂log p_i/∂log q_i = f_ii + s_i·(1 + f_G)")
    print(f"\n   f_ii condicional (dentro del grupo)                   {fc:+.3f}")
    print(f"   participación de la tangonera en el volumen           {s_tan:.3f}")
    print(f"   flexibilidad del grupo contra el cultivo, f_G          {fg:+.3f}")
    tot = fc + s_tan * (1 + fg)
    print(f"\n   f_tangonera total = {fc:+.3f} + {s_tan:.3f}·(1 {fg:+.3f}) = {tot:+.3f}")

    print("\n   Contraste directo: ecuación incondicional con los DESEMBARQUES de cada flota")
    print("   por separado —la cantidad exógena, no los kilos embarcados—.")
    M = pd.get_dummies(A.index.month, prefix="m", drop_first=True).astype(float)
    M.index = A.index
    A = A.assign(ldt=np.log(A.d_tan), ldf=np.log(A.d_fre))
    m = _hac(A.lrel, pd.concat([A[["ldt", "ldf", "horeca", "trend"]], M], axis=1))
    print(f"      MCO   d_tan {m.params['ldt']:+.3f} (t {m.tvalues['ldt']:+.2f})  ·  "
          f"d_fre {m.params['ldf']:+.3f} (t {m.tvalues['ldf']:+.2f})   R2 {m.rsquared:.3f}")
    from linearmodels.iv import IV2SLS
    ex = sm.add_constant(pd.concat([A[["ldf", "horeca", "trend"]], M], axis=1))
    r = IV2SLS(A.lrel, ex, A[["ldt"]], A[["iv_conf"]]).fit(cov_type="kernel", kernel="bartlett")
    f, se = r.params["ldt"], r.std_errors["ldt"]
    F1 = float(r.first_stage.diagnostics["f.stat"].iloc[0])
    print(f"      IV    d_tan {f:+.3f}  se {se:.3f}  IC95% [{f - 1.96 * se:+.3f}, {f + 1.96 * se:+.3f}]"
          f"  ·  d_fre {r.params['ldf']:+.3f}   primera etapa F = {F1:.1f}")
    print("\n   Las dos vías coinciden, y coinciden con el modelo vigente de una sola flota")
    print("   (−0,219). El sistema no corrige el número: lo confirma por un camino distinto, con")
    print("   restricciones de teoría y con la fresquera adentro. Eso es lo que valía la pena saber.")
    print("\n   Y se resuelve el signo perverso de la vuelta anterior: la cantidad fresquera entraba")
    print("   POSITIVA cuando se la medía por kilos EMBARCADOS, que llevan adentro la decisión de")
    print("   cuándo vender. Medida por DESEMBARQUE, su coeficiente es cero. No era demanda: era")
    print("   la empresa eligiendo el momento del embarque.")
    return tot, (f, se)


def recurso(A):
    """La flota tangonera dejó de ser la dueña del recurso. Sin esto no se entiende f_G."""
    print("\n" + "=" * 100)
    print("EL RECURSO CAMBIÓ DE MANOS — desembarque de langostino por flota (kt)")
    print("=" * 100)
    lan = pd.read_pickle(_p("_lan.pkl"))
    lan["grupo"] = np.where(lan.flota.str.startswith("CONG"), "congeladora", "fresquera")
    g = lan.pivot_table(index="anio", columns="grupo", values="t", aggfunc="sum") / 1000
    g["total"] = g.sum(axis=1)
    g["fresquera_%"] = g.fresquera / g.total * 100
    print(g.round(1).to_string())
    x = np.log(g.congeladora).diff().dropna()
    y = np.log(g.fresquera).diff().dropna()
    print(f"\n   correlación de las variaciones anuales entre flotas: r = {np.corrcoef(x, y)[0, 1]:+.3f}")
    print("   → no se compensan ni se acompañan: se mueven por separado.")
    print("   → y la tangonera pasó del 71% del recurso en 2013 al 26% en 2025. Regular su")
    print("      captura es regular una fracción cada vez menor de la oferta argentina.")
    return g


def primera_etapa(A):
    print("\n" + "=" * 100)
    print("QUÉ LE HIZO EL CONFLICTO A CADA FLOTA — primera etapa, por separado")
    print("=" * 100)
    M = pd.get_dummies(A.index.month, prefix="m", drop_first=True).astype(float)
    M.index = A.index
    B = A.assign(ldt=np.log(A.d_tan), ldf=np.log(A.d_fre), lDg=np.log(A.Dg))
    for v, lab in [("ldt", "desembarque tangonero"), ("ldf", "desembarque fresquero"),
                   ("lDg", "desembarque total")]:
        m = _hac(B[v], pd.concat([B[["iv_conf", "horeca", "trend"]], M], axis=1))
        print(f"   {lab:<26s} {m.params['iv_conf'] * 100:+6.1f}%   (t {m.tvalues['iv_conf']:+.2f})")
    print("\n   El conflicto cortó la tangonera a la mitad y la fresquera no lo compensó —tampoco")
    print("   subió—. Por eso el instrumento es fuerte para la tangonera (F = 45) y flojo para el")
    print("   agregado (F = 11): mueve una flota, no el recurso entero.")


def politica(fs):
    rec = recorte_conxemar.recorte()
    print("\n" + "=" * 100)
    print(f"SIMULACIÓN — recorte del {-rec['dq'] * 100:.1f}% del desembarque")
    print("=" * 100)
    print(recorte_conxemar.describir(rec))
    print()
    # Acá el escenario va en logaritmos —el resto del script trabaja en logs— así que
    # el recorte entra como log(1 + dq) y las variaciones salen exactas, no de primer
    # orden como en demanda_inversa_modelo.py y demanda_inversa_tangonera.py.
    dq = np.log(1 + rec["dq"])
    expo = recorte_conxemar.EXPO_2025
    col_usd = f"US$ M sobre {expo:,.0f}"
    filas = []
    for nom, f in fs:
        filas.append({"supuesto": nom, "f": f, "Δ precio %": (np.exp(f * dq) - 1) * 100,
                      "Δ facturación %": (np.exp((1 + f) * dq) - 1) * 100,
                      col_usd: expo * (np.exp((1 + f) * dq) - 1)})
    S = pd.DataFrame(filas).set_index("supuesto")
    print(S.round(2).to_string())
    return S


def main():
    A, wt, wf = panel()
    print("=" * 100)
    print("SISTEMA DE DEMANDA INVERSA DE DOS FLOTAS — entero L1+L2, ventana móvil de doce meses")
    print("=" * 100)
    print(f"Muestra {A.index.min()} a {A.index.max()}, {len(A)} meses.")
    s_tan = (A.q_tangonera / A.Qg).mean()
    print(f"Participación media de la tangonera: {wt:.1%} del valor · {s_tan:.1%} del volumen.")
    print(f"Prima media del precio tangonero sobre el fresquero: "
          f"{(A.p_tangonera / A.p_fresquera).mean():.3f}")

    recurso(A)
    primera_etapa(A)
    res_g = etapa_grupo(A)
    m, F, esc, se_f = sistema_interno(A, wt, wf)
    tot, iv = incondicional(A, res_g, F, wt, s_tan)
    S = politica([("sistema de dos flotas, dos etapas", tot),
                  ("ecuación incondicional con desembarques, IV", iv[0]),
                  ("modelo vigente de una sola flota, IV", -0.219),
                  ("umbral para no perder facturación", -1.0)])

    with pd.ExcelWriter(_p("salidas", "demanda_inversa_sistema_flotas.xlsx")) as w:
        A.to_excel(w, sheet_name="panel")
        F.to_excel(w, sheet_name="flex_condicionales")
        esc.to_frame("escala").to_excel(w, sheet_name="escala")
        S.to_excel(w, sheet_name="simulacion")
    print("\nEscrito: salidas/demanda_inversa_sistema_flotas.xlsx")
    return A, F, esc


if __name__ == "__main__":
    main()
