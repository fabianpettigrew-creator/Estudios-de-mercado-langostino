# -*- coding: utf-8 -*-
"""Un precio CIF de ingreso al mercado europeo por flota y por talla.

LA IDEA. Ninguna fuente publica un CIF abierto por calibre: EUMOFA declara todo el
congelado argentino como PR1 Whole/Gutted, sin talla y sin flota. Pero el mismo
embarque se observa dos veces —FOB de despacho del lado argentino, con talla, flota y
destino; CIF de importación del lado europeo, oficial pero agregado— y la diferencia
entre los dos es el flete más el seguro. Si esa cuña se puede atribuir, el CIF por
segmento se construye: CIF_s = FOB_s + w.

EL PROBLEMA DE IDENTIFICACIÓN. La cuña agregada es UNA ecuación por mes y los segmentos
son muchos, así que atribuirla exige un supuesto. El supuesto natural es que el flete se
cobra POR KILO de producto congelado y no por su valor: un pallet de entero L1 y uno de
cola ocupan el mismo lugar en el contenedor. Si eso es cierto, w es común a todos los
segmentos y queda identificada por el agregado.

EL TEST QUE DECIDE. El supuesto es contrastable, y es lo que hace este guion. EUMOFA
abre el CIF por país declarante, y los destinos tienen mezclas de producto y niveles de
precio muy distintos —España compra a 5,90 EUR/kg, Bélgica a 7,64—. Entonces:

    · si el flete es por kilo, la cuña en EUR/kg debe ser parecida entre destinos
      aunque el FOB no lo sea;
    · si es ad valorem —seguro, comisión, margen—, lo parecido debe ser la cuña en
      PORCENTAJE del FOB, y la cuña en euros debe escalar con el precio.

Se estiman las dos y se comparan. El ganador dice cómo repartir la cuña por segmento.

Uso:  python cif_por_destino.py
Salida: consola + salidas/cif_por_destino.xlsx
"""
from __future__ import annotations

import glob
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 210)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from biblioteca import fuente
EUMOFA = fuente("eumofa_ue")
COLS = ["year", "month", "country", "flow_type", "intra_extra_EU", "partner_contry",
        "main_commercial_species", "preservation", "value(EUR)", "volume(kg)"]
CONGELADO = ["PS2 Frozen", "PS5 Unspecified"]

# país declarante de EUMOFA → grafías del destino en la base de comercio
PAISES = {
    "Spain": ["ESPAÑA", "ESPANA"],
    "Italy": ["ITALIA"],
    "France": ["FRANCIA"],
    "Greece": ["GRECIA"],
    "Portugal": ["PORTUGAL"],
    "Netherlands": ["PAISES BAJOS", "PAÍSES BAJOS", "HOLANDA"],
    "Belgium": ["BELGICA", "BÉLGICA"],
    "Denmark": ["DINAMARCA"],
    "Germany": ["ALEMANIA"],
    "Poland": ["POLONIA"],
}
MIN_KT = 3.0        # un destino entra al test si mueve al menos esto en el período
# Arranca en 2020 y no en 2013: antes de 2020 el VOLUMEN del despacho tiene doble
# conteo que lo infla hasta 1,45x, y acá el volumen no es decorativo —se usa para
# reconciliar los dos universos y para ponderar—, así que contamina la cuña.
DESDE = "2020-01"
MAXLAG = 3          # meses de tránsito a probar


def _p(*t):
    return os.path.join(RAIZ, *t)


# ------------------------------------------------------------------- EUMOFA
def cif_eumofa() -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(
        EUMOFA, "EUMOFA BASES", "DESCARGA MASIVA", "EXPO IMPO", "EU",
        "*_Trade_data_reported_by_EU_countries.csv")))
    parcial = os.path.join(EUMOFA, "2026_Trade_data_reported_by_EU_countries.csv")
    if os.path.exists(parcial):
        files.append(parcial)
    tr = []
    for f in files:
        d = pd.read_csv(f, sep=";", dtype=str, low_memory=False,
                        usecols=lambda c: c in COLS)
        tr.append(d[(d.flow_type == "Import") & (d.intra_extra_EU == "Extra EU")
                    & (d.partner_contry == "Argentina")
                    & d.main_commercial_species.str.startswith("Shrimp", na=False)
                    & d.preservation.isin(CONGELADO)])
    d = pd.concat(tr, ignore_index=True)
    d["eur"] = pd.to_numeric(d["value(EUR)"], errors="coerce")
    d["kg"] = pd.to_numeric(d["volume(kg)"], errors="coerce")
    d = d[(d.kg > 0) & (d.eur > 0)]
    d["per"] = pd.PeriodIndex(
        pd.to_numeric(d.year).astype(int).astype(str) + "-"
        + pd.to_numeric(d.month).astype(int).astype(str).str.zfill(2), freq="M")
    g = (d[d.country.isin(PAISES)].groupby(["country", "per"])[["eur", "kg"]].sum()
         .reset_index())
    g["cif_eur_kg"] = g.eur / g.kg
    g["kt_cif"] = g.kg / 1e6
    return g[g.per >= pd.Period(DESDE)]


# -------------------------------------------------------------- despachos
def fob_despacho():
    """FOB por destino y mes, en euros. Devuelve el agregado (para la cuña) y el
    detalle por flota y calibre (para aplicarla)."""
    from fuentes import expo
    import demanda_inversa_modelo as M0
    fx = pd.Series({k: float(v) for k, v in (x.split("=") for x in M0.FX.split(";"))})
    fx.index = pd.PeriodIndex(fx.index, freq="M")

    e = expo.cargar_todos()
    d = e[(e.kg > 0) & (e.fob_tot > 0)].copy()
    d["dest"] = d.destino.astype(str).str.upper().str.strip()
    inv = {g: p for p, gs in PAISES.items() for g in gs}
    d["country"] = d.dest.map(inv)
    d = d[d.country.notna()].copy()
    d["per"] = pd.PeriodIndex(d.anio.astype(str) + "-"
                              + d.mes.astype(str).str.zfill(2), freq="M")
    d["eurusd"] = d.per.map(fx)
    d["fob_eur"] = d.fob_tot / d.eurusd
    d["flota"] = np.where(d.ruta == "a bordo", "tangonera", "fresquera")

    g = d.groupby(["country", "per"]).agg(kg=("kg", "sum"),
                                          fob=("fob_eur", "sum")).reset_index()
    g["fob_eur_kg"] = g.fob / g.kg
    g["kt_fob"] = g.kg / 1e6
    return g[g.per >= pd.Period(DESDE)], d


# ------------------------------------------------------------------ tránsito
def alinear(C: pd.DataFrame, F: pd.DataFrame) -> dict:
    """El despacho se cuenta cuando sale y la importación cuando entra. El rezago de
    tránsito se elige por la correlación de VOLÚMENES, que no depende de precios."""
    out = {}
    for pais in sorted(set(C.country) & set(F.country)):
        c = C[C.country == pais].set_index("per").kt_cif
        f = F[F.country == pais].set_index("per").kt_fob
        mejor, best = 0, -9
        for L in range(0, MAXLAG + 1):
            j = pd.concat([f, c.shift(-L).rename("c")], axis=1).dropna()
            if len(j) < 24:
                continue
            r = j.kt_fob.corr(j.c)
            if r > best:
                mejor, best = L, r
        out[pais] = (mejor, best)
    return out


def main() -> None:
    print("=" * 105)
    print("UN CIF POR FLOTA Y POR TALLA, RECONSTRUIDO CONTRA LA BASE OFICIAL")
    print("=" * 105)
    C = cif_eumofa()
    F, det = fob_despacho()
    print(f"EUMOFA: {len(C):,} filas país-mes · {C.kt_cif.sum():,.0f} kt")
    print(f"Despachos a esos destinos: {F.kt_fob.sum():,.0f} kt")

    # -------------------------------------------------- 1. reconciliación
    print("\n" + "-" * 105)
    print("1. ¿HABLAN DEL MISMO EMBARQUE? RECONCILIACIÓN DE VOLÚMENES")
    print("-" * 105)
    rec = (C.groupby("country").kt_cif.sum().to_frame()
           .join(F.groupby("country").kt_fob.sum()))
    rec["cobertura"] = rec.kt_fob / rec.kt_cif
    lags = alinear(C, F)
    rec["rezago_meses"] = [lags.get(p, (np.nan, np.nan))[0] for p in rec.index]
    rec["corr_volumen"] = [lags.get(p, (np.nan, np.nan))[1] for p in rec.index]
    rec = rec.sort_values("kt_cif", ascending=False)
    print(rec.round(3).to_string())
    print("\n   La cobertura cercana a uno dice que las dos fuentes ven el mismo flujo.")
    print("   El rezago es el tránsito: el despacho sale un mes y entra al mes o dos.")

    # -------------------------------------------------- 2. la cuña por destino
    print("\n" + "-" * 105)
    print("2. LA CUÑA POR DESTINO, YA ALINEADA POR TRÁNSITO")
    print("-" * 105)
    filas, panel = [], []
    grandes = rec[rec.kt_cif >= MIN_KT].index.tolist()
    for pais in grandes:
        L = int(lags[pais][0])
        c = C[C.country == pais].set_index("per")[["cif_eur_kg", "kt_cif"]]
        f = F[F.country == pais].set_index("per")[["fob_eur_kg", "kt_fob"]]
        j = pd.concat([f, c.shift(-L)], axis=1).dropna()
        j = j[(j.kt_fob > 0.02)]                      # meses con embarque real
        j["w"] = j.cif_eur_kg - j.fob_eur_kg
        j["w_pct"] = j.w / j.fob_eur_kg * 100
        j["country"] = pais
        panel.append(j.reset_index())
        filas.append({"destino": pais, "rezago": L, "N": len(j),
                      "fob": j.fob_eur_kg.mean(), "cif": j.cif_eur_kg.mean(),
                      "w_eur_kg": j.w.mean(), "w_pct": j.w_pct.mean(),
                      "sd_w": j.w.std(), "kt": j.kt_cif.sum()})
    W = pd.DataFrame(filas).set_index("destino").sort_values("kt", ascending=False)
    print(W.round(3).to_string())
    PAN = pd.concat(panel, ignore_index=True)

    # -------------------------------------------------- 3. el test
    print("\n" + "-" * 105)
    print("3. EL TEST: ¿EL FLETE ES POR KILO O POR VALOR?")
    print("-" * 105)
    disp_eur = W.w_eur_kg.std() / W.w_eur_kg.mean()
    disp_pct = W.w_pct.std() / W.w_pct.mean()
    print(f"   Dispersión entre destinos de la cuña en EUR/kg:  "
          f"{disp_eur:.3f} (media {W.w_eur_kg.mean():.3f})")
    print(f"   Dispersión entre destinos de la cuña en % del FOB: "
          f"{disp_pct:.3f} (media {W.w_pct.mean():.1f}%)")
    gana = "POR KILO (aditiva)" if disp_eur < disp_pct else "POR VALOR (ad valorem)"
    print(f"   → la representación más estable entre destinos es la {gana}.")

    # OJO: NO se puede regresar w contra FOB. Como w = CIF − FOB, el FOB está a los dos
    # lados y cualquier error de medición en él fabrica pendiente negativa. Hay que
    # regresar CIF contra FOB, donde el supuesto se lee en la pendiente:
    #     flete por kilo  →  pendiente 1, constante = w
    #     ad valorem      →  pendiente 1+τ, constante 0
    print("\n   Regresión CIF = a + b·FOB (w contra FOB no sirve: el FOB queda a los")
    print("   dos lados y el error de medición fabrica pendiente negativa).")
    for etq, D in [("pares destino-mes", PAN),
                   ("promedios por destino", PAN.groupby("country")
                    [["fob_eur_kg", "cif_eur_kg"]].mean().reset_index())]:
        m = sm.OLS(D.cif_eur_kg, sm.add_constant(D.fob_eur_kg)).fit(cov_type="HC1")
        b, se = m.params.fob_eur_kg, m.bse.fob_eur_kg
        t1 = (b - 1) / se
        print(f"      {etq:<22s} N={int(m.nobs):>4}  a = {m.params.const:+.3f}  "
              f"b = {b:+.3f} (se {se:.3f})  H0: b = 1 → t = {t1:+.2f}  "
              + ("no rechaza pendiente 1" if abs(t1) < 1.96 else "RECHAZA pendiente 1"))

    # -------------------------------- 4. el CIF por flota y talla, construido
    print("\n" + "-" * 105)
    print("4. EL CIF RECONSTRUIDO POR FLOTA Y TALLA")
    print("-" * 105)
    wk = W.w_eur_kg.to_dict()
    seg = det[det.country.isin(grandes) & (det.pres.isin(["entero", "cola"]))].copy()
    seg["w"] = seg.country.map(wk)
    seg = seg.dropna(subset=["w"])
    seg["cal2"] = np.where(seg.cal.isin(["L1", "L2"]), seg.cal, "otras")
    g = (seg.groupby(["pres", "cal2", "flota"])
         .apply(lambda x: pd.Series({
             "kt": x.kg.sum() / 1e6,
             "fob_eur_kg": x.fob_eur.sum() / x.kg.sum(),
             "cif_eur_kg": (x.fob_eur.sum() + (x.w * x.kg).sum()) / x.kg.sum()})))
    g["w"] = g.cif_eur_kg - g.fob_eur_kg
    g["w_pct"] = g.w / g.fob_eur_kg * 100
    print(g[g.kt > 1].sort_values("kt", ascending=False).round(3).to_string())
    print("\n   ADVERTENCIA DE LECTURA. Que la cuña en euros salga parecida entre")
    print("   segmentos NO es un hallazgo: es la aritmética del supuesto, porque el CIF")
    print("   de cada segmento se construyó sumándole la MISMA cuña del destino. Lo")
    print("   único que el cuadro agrega es el reparto: la misma cuña pesa distinto")
    print("   según el valor del producto, y por eso el sesgo FOB/CIF no es neutro")
    print("   entre calibres. La validez de todo esto depende del test de la sección 3,")
    print("   no de este cuadro.")

    try:
        out = _p("salidas", "cif_por_destino.xlsx")
        with pd.ExcelWriter(out) as w:
            rec.round(4).to_excel(w, sheet_name="reconciliacion")
            W.round(4).to_excel(w, sheet_name="cuna_por_destino")
            p = PAN.copy()
            p["per"] = p.per.astype(str)
            p.round(4).to_excel(w, sheet_name="panel", index=False)
            g.round(4).to_excel(w, sheet_name="cif_por_segmento")
        print(f"\nGuardado: {out}")
    except PermissionError:
        print("\nAVISO: no pude escribir el xlsx (¿abierto en Excel?).")


if __name__ == "__main__":
    main()
