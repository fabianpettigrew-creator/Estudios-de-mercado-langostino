# -*- coding: utf-8 -*-
"""Premium de precio por destino del entero L1 contra España — dato de la placa 15 del PPT.

Especificación (reconstruida y verificada el 2026-09-05 contra las barras que estaban
escritas a mano en `deck_ceo.js`; reproduce los ocho valores con 0,02 puntos de error):

    WLS de log(FOB unitario) sobre efectos fijos de mes-calendario y de destino,
    ponderado por kilos, errores HC1. Entero calibre L1, TODAS las rutas
    (congelado a bordo y procesado en tierra), serie completa 2013-2026.

El coeficiente de cada destino es el premium contra España a igual mes: aísla el efecto
del destino del momento del año en que compra cada uno.

Depuración previa (la misma de `hedonico.py`): FOB unitario entre 3 y 15 USD/kg y
embarques de 500 kg o más.

Destinos que se muestran: los que pesan **1% o más del valor exportado de L1 en los
últimos cinco años completos (2021-2025)**. La regresión se estima con todos los
destinos —cada uno con su efecto fijo, así ninguno contamina a los demás—, pero la
placa solo grafica los vigentes. Sin este filtro entraban Vietnam, que no despacha L1
desde 2017, y Corea del Sur, con 0,6% del valor; y quedaban afuera Rusia y Francia,
que pesan más que ambos.

Uso:  python premium_destino_placa15.py
Salidas:
    salidas/Premium_destino_L1_placa15.xlsx   tabla completa, para auditar
    salidas/premium_destino_placa15.json      lo que lee deck_ceo.js para la placa
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

SALIDAS = os.path.join(RAIZ, "salidas")
XLSX = os.path.join(SALIDAS, "Premium_destino_L1_placa15.xlsx")
JSON = os.path.join(SALIDAS, "premium_destino_placa15.json")

BASE = "España"
FOB_MIN, FOB_MAX, KG_MIN = 3.0, 15.0, 500.0
ANIOS_VIGENCIA = (2021, 2025)     # cinco años completos
SHARE_MIN = 5.0                   # % del valor de L1 en esa ventana

MAPA = {"ESPAÑA": "España", "ESPANA": "España", "ITALIA": "Italia", "CHINA": "China",
        "JAPON": "Japón", "JAPÓN": "Japón", "ESTADOS UNIDOS": "Estados Unidos",
        "VIETNAM": "Vietnam", "VIET NAM": "Vietnam", "COREA DEL SUR": "Corea del Sur",
        "COREA REPUBLICANA": "Corea del Sur", "COREA, REPUBLICA DE": "Corea del Sur",
        "TAIWAN": "Taiwán", "TAIWÁN": "Taiwán", "GRECIA": "Grecia",
        "FRANCIA": "Francia", "RUSIA": "Rusia"}


def datos() -> pd.DataFrame:
    """Despachos de entero L1, todas las rutas, con el país normalizado."""
    from fuentes import expo
    e = expo.cargar_todos()
    d = e[(e.pres == "entero") & (e.cal == "L1")
          & (e.kg > 0) & (e.fob_tot > 0)].copy()
    d["dest"] = d.destino.str.upper().str.strip().map(MAPA).fillna(d.destino.str.title())
    return d


def vigentes(d: pd.DataFrame) -> pd.DataFrame:
    """Peso de cada destino en el valor exportado de los últimos cinco años."""
    v = d[d.anio.between(*ANIOS_VIGENCIA)]
    r = v.groupby("dest").agg(musd=("fob_tot", lambda s: s.sum() / 1e6),
                              kt=("kg", lambda s: s.sum() / 1e6),
                              despachos=("kg", "size"),
                              anios=("anio", "nunique"))
    r["share_%"] = 100 * r.musd / r.musd.sum()
    return r.sort_values("share_%", ascending=False)


def premium(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """WLS de log(precio) sobre mes-calendario y destino, ponderado por kilos."""
    m = d[(d.fob.between(FOB_MIN, FOB_MAX)) & (d.kg >= KG_MIN)].copy()
    m["per"] = pd.PeriodIndex(m.anio.astype(str) + "-" + m.mes.astype(str).str.zfill(2),
                              freq="M")
    y = np.log(m.fob.to_numpy())
    w = m.kg.to_numpy()
    X = pd.get_dummies(m.per.astype(str), prefix="m", dtype=float)
    X = X.drop(columns=[X.columns[0]])                      # mes base = el primero
    D = pd.get_dummies(m.dest, prefix="d", dtype=float).drop(columns=[f"d_{BASE}"])
    X = sm.add_constant(pd.concat([X.reset_index(drop=True), D.reset_index(drop=True)],
                                  axis=1), has_constant="add")
    res = sm.WLS(y, X.to_numpy(dtype=float), weights=w).fit(cov_type="HC1")
    nom = list(X.columns)

    filas = []
    for c in [c for c in nom if c.startswith("d_")]:
        j = nom.index(c)
        dest = c[2:]
        s = m[m.dest == dest]
        filas.append({"destino": dest,
                      "premium_%": (np.exp(res.params[j]) - 1) * 100,
                      "se_%": res.bse[j] * 100 * np.exp(res.params[j]),
                      "t": res.params[j] / res.bse[j],
                      "fob_medio": (s.fob * s.kg).sum() / s.kg.sum(),
                      "kt_muestra": s.kg.sum() / 1e6,
                      "despachos": len(s)})
    s = m[m.dest == BASE]
    filas.append({"destino": BASE, "premium_%": 0.0, "se_%": np.nan, "t": np.nan,
                  "fob_medio": (s.fob * s.kg).sum() / s.kg.sum(),
                  "kt_muestra": s.kg.sum() / 1e6, "despachos": len(s)})
    diag = {"N": int(res.nobs), "R2": float(res.rsquared),
            "anio_min": int(m.anio.min()), "anio_max": int(m.anio.max()),
            "meses": int(m.per.nunique()), "destinos": int(m.dest.nunique())}
    return pd.DataFrame(filas).sort_values("premium_%", ascending=False), diag


def main() -> None:
    d = datos()
    print(f"Entero L1 · todas las rutas · {d.anio.min()}-{d.anio.max()}: "
          f"{len(d):,} despachos · {d.kg.sum()/1e6:,.1f} kt")

    peso = vigentes(d)
    sel = peso[peso["share_%"] >= SHARE_MIN].index.tolist()
    print(f"\nDestinos con {SHARE_MIN:.0f}% o más del valor de L1 en "
          f"{ANIOS_VIGENCIA[0]}-{ANIOS_VIGENCIA[1]} ({len(sel)}): {', '.join(sel)}")
    fuera = peso[(peso["share_%"] < SHARE_MIN) & (peso.despachos >= 20)]
    if len(fuera):
        print("Quedan afuera por poco valor reciente: "
              + " · ".join(f"{i} {r['share_%']:.2f}%" for i, r in fuera.head(6).iterrows()))

    T, diag = premium(d)
    print(f"\nWLS ponderado por kilos · N = {diag['N']:,} · R² = {diag['R2']:.3f} · "
          f"HC1 · {diag['meses']} meses · base: {BASE}")

    T = T.merge(peso[["share_%"]], left_on="destino", right_index=True, how="left")
    T["en_placa"] = T.destino.isin(sel + [BASE])
    print("\n=== PREMIUM POR DESTINO · entero L1 · serie completa (base España) ===")
    print(T[T.en_placa].round(2).to_string(index=False))

    graf = T[T.en_placa & (T.destino != BASE)].sort_values("premium_%", ascending=False)
    # La base va al gráfico como barra en cero: la tarjeta afirma que España paga el
    # precio más bajo, y con pocos destinos esa afirmación no se veía en ningún lado.
    barras = T[T.en_placa].sort_values("premium_%", ascending=False)
    # La dispersión se mide contra España, que es la base y el destino más barato:
    # es lo que afirma la placa ("España paga el precio más bajo de la tabla").
    caro, disp = graf.destino.iloc[0], graf["premium_%"].max()
    print(f"\nDispersión del más caro al más barato: {disp:.1f} puntos "
          f"({caro} {disp:+.1f}% contra {BASE}, que es la base)")
    print(f"  (entre destinos graficados, sin {BASE}: "
          f"{graf['premium_%'].max() - graf['premium_%'].min():.1f} puntos)")

    os.makedirs(SALIDAS, exist_ok=True)
    with pd.ExcelWriter(XLSX, engine="openpyxl") as xl:
        T.round(3).to_excel(xl, sheet_name="Premium por destino", index=False)
        peso.round(3).to_excel(xl, sheet_name=f"Valor {ANIOS_VIGENCIA[0]}-{ANIOS_VIGENCIA[1]}")
        pd.DataFrame([diag]).to_excel(xl, sheet_name="Diagnóstico", index=False)

    LETRAS = {1: "Un", 2: "Dos", 3: "Tres", 4: "Cuatro", 5: "Cinco", 6: "Seis",
              7: "Siete", 8: "Ocho", 9: "Nueve", 10: "Diez", 11: "Once", 12: "Doce",
              13: "Trece", 14: "Catorce", 15: "Quince"}
    # Los que quedaron afuera, para poder declararlo en las notas del orador sin
    # escribirlo a mano: los de más peso entre los excluidos con historia real.
    ex = peso[(peso["share_%"] < SHARE_MIN) & (peso.despachos >= 50)].head(5)
    excluidos = " · ".join(f"{i} {r['share_%']:.1f}%" for i, r in ex.iterrows())
    payload = {
        "labels": barras.destino.tolist(),
        "values": [round(v, 1) for v in barras["premium_%"]],
        "dispersion_pts": round(disp, 1),
        "dispersion_txt": LETRAS.get(round(disp), f"{disp:.0f}") + " puntos",
        "mas_caro": caro,
        "ventana": f"{diag['anio_min']}-{diag['anio_max']}",
        "N": diag["N"], "R2": round(diag["R2"], 3),
        "corte_%": SHARE_MIN,
        "excluidos": excluidos,
        "nota_orador": (
            "Ojo con leerlo como 'hay que dejar España': son mercados de distinto "
            "tamaño y la capacidad de absorción no es la misma. El punto es que la "
            "diferencia es medible y hoy no se está cobrando. El premium sale de una "
            f"regresión ponderada por kilos sobre {diag['N']:,} despachos de "
            f"{diag['anio_min']}-{diag['anio_max']} (R² {round(diag['R2'], 3)}), con "
            "efecto fijo de mes para que la comparación sea contra España en el mismo "
            f"mes. Se grafican los destinos que pesan {SHARE_MIN:.0f}% o más del valor "
            f"exportado de L1 en {ANIOS_VIGENCIA[0]}-{ANIOS_VIGENCIA[1]}; los mayores "
            f"que quedaron afuera son {excluidos}."
        ).replace(f"{diag['N']:,}", f"{diag['N']:,}".replace(",", ".")),
        "pie": (f"Fuente: registro aduanero de exportación, entero L1 congelado a bordo "
                f"y procesado en tierra, {diag['anio_min']}-{diag['anio_max']}. Premium "
                f"contra España a igual mes, ponderado por kilos. Destinos con "
                f"{SHARE_MIN:.0f}% o más del valor exportado en "
                f"{ANIOS_VIGENCIA[0]}-{ANIOS_VIGENCIA[1]}."),
    }
    with open(JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\nGuardado:\n  {XLSX}\n  {JSON}")


if __name__ == "__main__":
    main()
