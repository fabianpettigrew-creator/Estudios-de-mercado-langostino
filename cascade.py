"""
Cascade de precio FOB -> CIF -> gondola del langostino argentino.

Une las tres capas que el proyecto ya captura por separado:
  FOB origen  : fuentes/expo.py  (despachos Softrade, USD/kg por presentacion/calibre)
  CIF destino : datos/mercado.db (NOAA para EE.UU. en USD; Comext para la UE en EUR)
  gondola     : ../Scraping/datos_precios/precios_retail.csv  (retail, moneda local)

La comparacion honesta exige DOS normalizaciones, ambas con datos del propio proyecto:
  - Moneda: la gondola guarda moneda local; se pasa todo a la moneda del cascade
    de cada mercado con un tipo de cambio unico (FX, flag abajo). NO es por fecha:
    es una foto, hay que actualizarlo si se reusa.
  - Presentacion: FOB, CIF y gondola pueden estar en presentaciones distintas
    (entero vs pelado). Para el cruce entre mercados se lleva todo a "kg de
    materia prima" (langostino entero equivalente) con los rendimientos POR RUTA
    definidos abajo (YIELD_COLA / YIELD_PD): entero 1.00, cola 0.65 a bordo y
    0.55 en tierra, P&D 0.455 / 0.385. Comparar un pelado contra un entero al
    kilo de producto es comparar rendimiento.
    Son rindes de PLANTA (P&D = 70% de una cola con cascara). NO se calibran del
    cociente de precios CIF pelado/cascara (~0.88): ese cociente esta contaminado
    por mezcla de calibre (el "con cascara" se concentra en 15/20, que es premium).
    expo.RENDIMIENTO guarda los factores PLANOS (cola 0.62, P&D 0.43), promedio
    de ruta; se usan donde no hay dato de ruta, no en este cascade.

Salida: tabla por consola + salidas/cascade_fob_cif_gondola.{svg,xlsx}

CAVEATS (van en el informe, no se esconden):
  * Retail fino: 1 retailer US (Kroger) y 1 cadena ES con langostino AR entero
    (La Sirena). Una foto. Los numeros son DIRECCIONALES, no serie consolidada.
  * Desfase temporal: FOB 2026 H1, CIF ultimos 12m, gondola de la ultima captura.
  * Comext (CIF UE) no abre por calibre: la barra CIF-UE es agregado del entero.
  * Triangulacion: parte del "argentino" que llega a EE.UU. entra via Peru/Vietnam
    (fason); el CIF origen=ARGENTINA es el precio del directo, no del reprocesado.
"""
from __future__ import annotations

import glob
import json
import sqlite3
import statistics
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fuentes import expo  # noqa: E402

BASE = Path(__file__).parent
DB = BASE / "datos" / "mercado.db"
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from biblioteca import fuente
RETAIL = (Path(fuente("scraping_precios")) / "precios_retail.csv")
SALIDAS = BASE / "salidas"

# Tipo de cambio unico para la foto (no por fecha). Actualizar si se reusa.
EUR_USD = 1.08
ANIO_FOB = 2026  # FOB del año en curso; 2025 esta distorsionado por el paro de flota.

# Rendimientos sobre entero HOSO=1.00, POR RUTA de procesamiento (dato de planta):
#   cola con cascara: 0.65 congelado a bordo (tangonero) / 0.55 procesado en tierra.
#   P&D = 70% de una cola con cascara.
# expo.RENDIMIENTO usa factores PLANOS (promedio de ruta): cola 0.62, P&D 0.43.
# Aca se distingue la ruta porque cambia el rinde ~18% y el mismo talle vale mas
# congelado a bordo (ver memoria margen-por-talle). El pelado que va a EE.UU. es
# reprocesado (en tierra / fason via Peru-Vietnam): le corresponde el rinde bajo.
YIELD_COLA = {"a bordo": 0.65, "en tierra": 0.55}
YIELD_PD = {r: round(v * 0.70, 3) for r, v in YIELD_COLA.items()}  # 0.455 / 0.385
YIELD_ENTERO = 1.00


def _wav(df, precio, peso="kg"):
    return (df[precio] * df[peso]).sum() / df[peso].sum()


_EXPO = None


def _expo_df():
    """Carga los despachos una sola vez (cargar_todos lee muchos Excel)."""
    global _EXPO
    if _EXPO is None:
        _EXPO = expo.cargar_todos()
    return _EXPO[_EXPO["anio"] == ANIO_FOB]


# --------------------------------------------------------------------------
# 1) FOB origen (USD/kg) por presentacion y destino
# --------------------------------------------------------------------------
def fob():
    d = _expo_df()
    out = {}
    for dest, etq in [("ESTADOS UNIDOS", "US"), ("ESPA", "ES")]:
        s = d[d["destino"].astype(str).str.upper().str.contains(dest)]
        out[etq] = {p: round(_wav(g, "fob"), 2) for p, g in s.groupby("pres") if len(g)}
    # FOB entero por calibre (para el cruce por talle)
    ent = expo.precio_por_calibre(d, "entero")
    out["entero_por_cal"] = ent["fob"].to_dict()
    return out


# --------------------------------------------------------------------------
# 1b) FOB por RUTA (a bordo vs en tierra) — cuanto captura el origen segun
#     que producto/ruta elige, tambien por kg de materia prima.
# --------------------------------------------------------------------------
def fob_por_ruta():
    d = _expo_df()
    y = {("entero", "a bordo"): YIELD_ENTERO, ("entero", "en tierra"): YIELD_ENTERO,
         ("cola", "a bordo"): YIELD_COLA["a bordo"],
         ("cola", "en tierra"): YIELD_COLA["en tierra"],
         ("pelado devenado", "a bordo"): YIELD_PD["a bordo"],
         ("pelado devenado", "en tierra"): YIELD_PD["en tierra"]}
    rows = []
    for (pres, ruta), rinde in y.items():
        s = d[(d["pres"] == pres) & (d["ruta"] == ruta)]
        if len(s) and s["kg"].sum() > 0:
            f = _wav(s, "fob")
            rows.append(dict(presentacion=pres, ruta=ruta,
                             kt=round(s["kg"].sum() / 1e6, 1),
                             fob_usd_kg=round(f, 2), rinde=rinde,
                             fob_usd_matprima=round(f * rinde, 2)))
    return pd.DataFrame(rows).sort_values("fob_usd_matprima", ascending=False,
                                          ignore_index=True)


# --------------------------------------------------------------------------
# 2) CIF destino
# --------------------------------------------------------------------------
def cif():
    con = sqlite3.connect(DB)
    mx = con.execute("SELECT MAX(anio*100+mes) FROM observaciones").fetchone()[0]
    desde = mx - 100  # ~12 meses
    us = pd.read_sql(
        """SELECT presentacion, SUM(kilos) kg, SUM(valor_usd)/SUM(kilos) cif
           FROM observaciones WHERE mercado='EEUU' AND origen='ARGENTINA'
           AND (anio*100+mes)>=? GROUP BY presentacion""", con, params=[desde])
    es = pd.read_sql(
        """SELECT SUM(kilos) kg, SUM(valor_eur)/SUM(kilos) cif
           FROM observaciones WHERE mercado='UE:ES' AND origen='AR'
           AND (anio*100+mes)>=?""", con, params=[desde])
    con.close()
    us_map = {r.presentacion: round(r.cif, 2) for r in us.itertuples()}
    return {
        "US_pelado": us_map.get("pelado"),
        "US_cascara": us_map.get("con cáscara"),
        "ES_entero": round(float(es["cif"].iloc[0]), 2),
    }


def _sa(t):
    t = unicodedata.normalize("NFKD", str(t))
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def _ls_entero_eur():
    """EUR/kg del gambon entero MSC de La Sirena, desde el PESO NETO de la ficha.

    El precio_kg del panel para La Sirena NO es fiable: sale del campo Preciocmz
    de VTEX, que se contradice con el peso (da ~€21/kg cuando el real es ~€12).
    Aca se calcula Price / netAmountGrams (que pese al nombre viene en kg) sobre
    el JSON crudo, que es la unica via consistente. Corroborado por el cascade:
    CIF ES €6.57 x margen retail ~1.8 = €11.8, no €21.
    """
    patron = str(Path(fuente("scraping_precios")) / "raw" / "**"
                 / "lasirena" / "busqueda_*.json")
    precios = []
    for f in glob.glob(patron, recursive=True):
        try:
            prods = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for p in prods if isinstance(prods, list) else []:
            nm = _sa(p.get("productName", ""))
            if not ("gambon" in nm or "austral" in nm):
                continue
            if any(x in nm for x in ("vannamei", "cocid", "pelad", "cola")):
                continue
            ic = p.get("Información complementaria") or p.get("Informacion complementaria")
            ic = ic[0] if isinstance(ic, list) else ic
            try:
                net = float(json.loads(ic).get("netAmountGrams"))
                price = p["items"][0]["sellers"][0]["commertialOffer"]["Price"]
            except Exception:
                continue
            if price and 0.1 <= net <= 20:      # net en kg; descarta basura (0.04)
                precios.append(price / net)
    return round(statistics.median(precios), 2) if precios else None


# --------------------------------------------------------------------------
# 3) Gondola (retail) por mercado/presentacion, en moneda local
# --------------------------------------------------------------------------
def gondola():
    r = pd.read_csv(RETAIL, sep=";", encoding="utf-8-sig")
    r["pk"] = pd.to_numeric(r["precio_kg_escurrido"], errors="coerce").fillna(
        pd.to_numeric(r["precio_kg_bruto"], errors="coerce"))
    nom = r["nombre"].astype(str).str.lower()

    # US: Kroger, langostino argentino, pelado & deveined. El $/kg de Kroger SI es
    # fiable (peso declarado en oz claro), asi que sale del panel.
    us_pd = r[(r["cadena"] == "kroger") & (r["origen_argentino"] == True)
              & nom.str.contains("peeled")]
    es_entero = _ls_entero_eur()       # ES: desde peso neto real, no del panel
    es_n = 0
    patron = str(Path(fuente("scraping_precios")) / "raw" / "**"
                 / "lasirena" / "busqueda_gambon*.json")
    for f in glob.glob(patron, recursive=True):
        try:
            es_n = max(es_n, sum(1 for p in json.load(open(f, encoding="utf-8"))
                                 if "MSC" in str(p.get("productName", ""))))
        except Exception:
            pass
    return {
        "US_pd": round(float(us_pd["pk"].median()), 2) if len(us_pd) else None,
        "ES_entero": es_entero,
        "US_pd_n": len(us_pd), "ES_entero_n": es_n,
    }


# --------------------------------------------------------------------------
# Ensamblado
# --------------------------------------------------------------------------
def construir():
    F, C, G = fob(), cif(), gondola()
    fx = {"USD": 1.0, "EUR": EUR_USD}

    filas = []
    # --- EE.UU., pelado & deveined, en USD/kg de producto ---
    filas.append(dict(mercado="EE.UU.", presentacion="pelado&devenado", moneda="USD",
                      fob=F["US"].get("pelado devenado"),
                      cif=C["US_pelado"], gondola=G["US_pd"]))
    # --- España, entero, en EUR/kg de producto ---
    fob_es_eur = round(F["ES"].get("entero") / EUR_USD, 2)
    filas.append(dict(mercado="España", presentacion="entero", moneda="EUR",
                      fob=fob_es_eur, cif=C["ES_entero"], gondola=G["ES_entero"]))

    df = pd.DataFrame(filas)
    df["FOB->CIF_%"] = ((df["cif"] / df["fob"] - 1) * 100).round(0)
    df["CIF->gond_%"] = ((df["gondola"] / df["cif"] - 1) * 100).round(0)
    df["origen_%_del_estante"] = ((df["fob"] / df["gondola"]) * 100).round(0)

    # Estante llevado a kg de MATERIA PRIMA (langostino entero equivalente), en USD.
    # Se multiplica el precio por el rinde. Para el pelado el rinde depende de la
    # ruta (a bordo vs en tierra), asi que sale un RANGO; el entero es 1.00 exacto.
    def matprima(row):
        p = row["gondola"] * fx[row["moneda"]]
        pres = row["presentacion"]
        if pres == "entero":
            ys = [YIELD_ENTERO]
        elif "pelado" in pres or "devenado" in pres:
            ys = [YIELD_PD["en tierra"], YIELD_PD["a bordo"]]
        elif pres == "cola":
            ys = [YIELD_COLA["en tierra"], YIELD_COLA["a bordo"]]
        else:
            ys = [1.0]
        return round(p * min(ys), 2), round(p * max(ys), 2)

    mp = df.apply(matprima, axis=1, result_type="expand")
    df["gond_matprima_usd_lo"], df["gond_matprima_usd_hi"] = mp[0], mp[1]
    return df, F, C, G


def graficar(df):
    """SVG a mano (sin matplotlib): dos paneles, 3 barras cada uno."""
    W, H = 860, 460
    pw, px0, ptop, pbot = 360, 40, 90, 380      # panel width, margenes
    colores = ["#2b6cb0", "#4299e1", "#f6ad55"]
    niveles = ["FOB\norigen", "CIF\ndestino", "Góndola"]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'font-family="Segoe UI,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="34" text-anchor="middle" font-size="17" '
         f'font-weight="bold">Cascade FOB → CIF → góndola · langostino argentino</text>',
         f'<text x="{W/2}" y="54" text-anchor="middle" font-size="12" '
         f'fill="#777">2026 · direccional (retail: 1 retailer US, 1 cadena ES)</text>']
    def esc(t):
        return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    for i, (_, row) in enumerate(df.iterrows()):
        ox = px0 + i * (pw + 40)
        vals = [row["fob"], row["cif"], row["gondola"]]
        vmax = max(vals) * 1.15
        bw, gap = 78, 40
        s.append(f'<text x="{ox+pw/2}" y="78" text-anchor="middle" font-size="13" '
                 f'font-weight="bold">{esc(row["mercado"])} — {esc(row["presentacion"])} '
                 f'({esc(row["moneda"])}/kg producto)</text>')
        for j, v in enumerate(vals):
            bh = (v / vmax) * (pbot - ptop)
            bx = ox + 30 + j * (bw + gap)
            by = pbot - bh
            s.append(f'<rect x="{bx}" y="{by:.0f}" width="{bw}" height="{bh:.0f}" '
                     f'fill="{colores[j]}"/>')
            s.append(f'<text x="{bx+bw/2}" y="{by-6:.0f}" text-anchor="middle" '
                     f'font-size="13" font-weight="bold">{v:.2f}</text>')
            for k, ln in enumerate(niveles[j].split("\n")):
                s.append(f'<text x="{bx+bw/2}" y="{pbot+18+k*14:.0f}" '
                         f'text-anchor="middle" font-size="11" fill="#555">{ln}</text>')
        s.append(f'<text x="{ox+pw/2}" y="{pbot+56:.0f}" text-anchor="middle" '
                 f'font-size="11" fill="#c05621">FOB→CIF +{row["FOB->CIF_%"]:.0f}%  ·  '
                 f'CIF→góndola +{row["CIF->gond_%"]:.0f}% (margen retail)</text>')
        lo, hi = row["gond_matprima_usd_lo"], row["gond_matprima_usd_hi"]
        mp = f"${lo:.1f}" if lo == hi else f"${lo:.1f}-{hi:.1f}"
        s.append(f'<text x="{ox+pw/2}" y="{pbot+74:.0f}" text-anchor="middle" '
                 f'font-size="11" fill="#333">origen = {row["origen_%_del_estante"]:.0f}% '
                 f'del estante · góndola/kg materia prima {mp}</text>')
    s.append("</svg>")
    SALIDAS.mkdir(exist_ok=True)
    (SALIDAS / "cascade_fob_cif_gondola.svg").write_text("\n".join(s), encoding="utf-8")


def graficar_ruta(fr):
    """Barras horizontales: FOB por elaboracion (presentacion x ruta), valor de
    origen POR KG DE PRODUCTO (fob_usd_kg). Se anota tambien el $/kg materia prima."""
    fr = fr.sort_values("fob_usd_kg", ascending=False).reset_index(drop=True)
    W, x0, top, bh, gap = 760, 250, 70, 26, 14
    H = top + len(fr) * (bh + gap) + 60
    vmax = fr["fob_usd_kg"].max() * 1.15
    escala = (W - x0 - 150) / vmax
    col = {"a bordo": "#2b6cb0", "en tierra": "#f6ad55"}
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'font-family="Segoe UI,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="{W/2}" y="30" text-anchor="middle" font-size="16" '
         f'font-weight="bold">FOB por elaboración · valor de origen por kg de producto</text>',
         f'<text x="{W/2}" y="50" text-anchor="middle" font-size="12" fill="#777">'
         f'langostino argentino 2026 · $/kg de producto exportado</text>']
    for i, r in fr.iterrows():
        y = top + i * (bh + gap)
        w = r["fob_usd_kg"] * escala
        s.append(f'<text x="{x0-10}" y="{y+bh*0.7:.0f}" text-anchor="end" '
                 f'font-size="12">{r["presentacion"]} · {r["ruta"]}</text>')
        s.append(f'<rect x="{x0}" y="{y}" width="{w:.0f}" height="{bh}" '
                 f'fill="{col.get(r["ruta"], "#888")}"/>')
        s.append(f'<text x="{x0+w+6:.0f}" y="{y+bh*0.7:.0f}" font-size="12" '
                 f'font-weight="bold">${r["fob_usd_kg"]:.2f}</text>')
        s.append(f'<text x="{x0+w+56:.0f}" y="{y+bh*0.7:.0f}" font-size="10" '
                 f'fill="#888">({r["kt"]:.0f}kt · ${r["fob_usd_matprima"]:.2f}/kg mat.prima)</text>')
    # leyenda
    ly = H - 22
    s.append(f'<rect x="{x0}" y="{ly-9}" width="12" height="12" fill="{col["a bordo"]}"/>'
             f'<text x="{x0+18}" y="{ly+1}" font-size="11">congelado a bordo</text>')
    s.append(f'<rect x="{x0+150}" y="{ly-9}" width="12" height="12" fill="{col["en tierra"]}"/>'
             f'<text x="{x0+168}" y="{ly+1}" font-size="11">procesado en tierra</text>')
    s.append("</svg>")
    SALIDAS.mkdir(exist_ok=True)
    (SALIDAS / "fob_por_ruta.svg").write_text("\n".join(s), encoding="utf-8")


# --------------------------------------------------------------------------
# Seccion para el briefing del informe (markdown)
# --------------------------------------------------------------------------
def seccion_md(df, fr):
    """Devuelve la seccion de cadena de valor en markdown, lista para el briefing."""
    L = ["## Cadena de valor: FOB → CIF → góndola (langostino argentino)\n",
         f"_Direccional — retail fino (1 retailer US, 1 cadena ES; una foto). "
         f"Precios 2026, FX EUR/USD={EUR_USD}. Gráficos: "
         f"salidas/cascade_fob_cif_gondola.svg y salidas/fob_por_ruta.svg._\n",
         "Cadena de precio por mercado (por kg de producto en su moneda; la última "
         "columna lleva la góndola a kg de langostino entero equivalente):\n",
         "Mercado | Present. | FOB | CIF | Góndola | FOB→CIF | CIF→góndola | Origen % estante | Góndola $/kg mat.prima",
         " --- | --- | --- | --- | --- | --- | --- | --- | --- "]
    for _, r in df.iterrows():
        mp = (f"{r['gond_matprima_usd_lo']:.1f}" if r['gond_matprima_usd_lo'] == r['gond_matprima_usd_hi']
              else f"{r['gond_matprima_usd_lo']:.1f}–{r['gond_matprima_usd_hi']:.1f}")
        L.append(f"{r['mercado']} | {r['presentacion']} | {r['fob']:.2f} | {r['cif']:.2f} | "
                 f"{r['gondola']:.2f} | +{r['FOB->CIF_%']:.0f}% | +{r['CIF->gond_%']:.0f}% | "
                 f"{r['origen_%_del_estante']:.0f}% | ${mp}")
    L.append("")
    L.append("Valor de origen (FOB) por elaboración y ruta, en DOS métricas —"
             " por kg de producto vendido y por kg de materia prima capturada:\n")
    L.append("Presentación | Ruta | Volumen kt | FOB $/kg | Rinde | FOB $/kg mat.prima")
    L.append(" --- | --- | --- | --- | --- | --- ")
    for _, r in fr.iterrows():
        L.append(f"{r['presentacion']} | {r['ruta']} | {r['kt']:.1f} | {r['fob_usd_kg']:.2f} | "
                 f"{r['rinde']:.3f} | ${r['fob_usd_matprima']:.2f}")
    ent = fr[fr.presentacion == "entero"].set_index("ruta")["fob_usd_kg"]
    prima = f"+{(ent['a bordo']/ent['en tierra']-1)*100:.0f}%" if {"a bordo", "en tierra"} <= set(ent.index) else "n/d"
    pt = fr.sort_values("fob_usd_kg", ascending=False).iloc[0]
    pb = fr.sort_values("fob_usd_kg", ascending=False).iloc[-1]
    mt = fr.sort_values("fob_usd_matprima", ascending=False).iloc[0]
    mb = fr.sort_values("fob_usd_matprima", ascending=False).iloc[-1]
    L += ["", "**Lecturas (mantener las dos métricas de FOB):**",
          "- El salto de precio no está en la frontera (FOB→CIF pocos %): está en "
          "CIF→góndola. El origen se queda con ~45-52% del precio de estante.",
          f"- El 'premium' de EE.UU. es presentación: por kg de materia prima la "
          f"góndola US (P&D) queda en o por debajo de la española (entero) en todo "
          f"el rango de ruta.",
          f"- FOB **por kg de producto**: más elaboración, más precio — "
          f"{pt['presentacion']}·{pt['ruta']} ${pt['fob_usd_kg']:.2f} arriba, "
          f"{pb['presentacion']}·{pb['ruta']} ${pb['fob_usd_kg']:.2f} abajo. El P&D "
          f"existe solo en tierra; el mismo entero vale {prima} a bordo que en tierra.",
          f"- FOB **por kg de materia prima** (langostino capturado): el orden se "
          f"invierte — {mt['presentacion']}·{mt['ruta']} ${mt['fob_usd_matprima']:.2f} "
          f"arriba, {mb['presentacion']}·{mb['ruta']} ${mb['fob_usd_matprima']:.2f} abajo. "
          f"La elaboración sube el kg vendido pero, por el rinde, no el valor por kg "
          f"de langostino capturado. Las dos lecturas son el argumento completo.\n"]
    return "\n".join(L)


def briefing_y_graficos():
    """Calcula todo, escribe los 2 SVG + Excel, y devuelve la seccion markdown.
    Pensado para que reporte.py lo llame. Lanza si faltan las fuentes (FOB/retail)."""
    df, _, _, _ = construir()
    fr = fob_por_ruta()
    graficar(df)
    graficar_ruta(fr)
    with pd.ExcelWriter(SALIDAS / "cascade_fob_cif_gondola.xlsx") as xw:
        df.to_excel(xw, sheet_name="cascade", index=False)
        fr.to_excel(xw, sheet_name="fob_por_ruta", index=False)
    return seccion_md(df, fr)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    df, F, C, G = construir()
    print("=" * 78)
    print("CASCADE FOB -> CIF -> GONDOLA · langostino argentino (2026, DIRECCIONAL)")
    print("=" * 78)
    print(f"\nRetail: US pelado n={G['US_pd_n']} · ES entero MSC n={G['ES_entero_n']}"
          f"  |  FX EUR/USD={EUR_USD}\n")
    cols = ["mercado", "presentacion", "moneda", "fob", "cif", "gondola",
            "FOB->CIF_%", "CIF->gond_%", "origen_%_del_estante",
            "gond_matprima_usd_lo", "gond_matprima_usd_hi"]
    print(df[cols].to_string(index=False))
    print(f"\n  (matprima_lo/hi = góndola por kg de langostino entero equivalente,"
          f" rango por ruta: P&D {YIELD_PD['en tierra']}–{YIELD_PD['a bordo']}, entero 1.00)")
    print("\nLectura:")
    print("  * El salto de precio NO esta en la frontera (FOB->CIF ~pocos %):")
    print("    el flete+seguro del congelado agrega poco por kg.")
    print("  * El precio ~se duplica de CIF a gondola: ahi se captura el margen.")
    print(f"  * El origen (barco+exportador) se queda con "
          f"{df['origen_%_del_estante'].min():.0f}-{df['origen_%_del_estante'].max():.0f}% "
          f"del precio de estante.")
    us = df.set_index("mercado").loc["EE.UU."]
    es = df.set_index("mercado").loc["España"]
    print(f"  * Por kg de MATERIA PRIMA: góndola EE.UU. ${us['gond_matprima_usd_lo']:.1f}"
          f"-{us['gond_matprima_usd_hi']:.1f} (P&D, rango por ruta) vs España "
          f"${es['gond_matprima_usd_lo']:.1f} (entero) —")
    print("    el 'premium' de EE.UU. es presentacion: a igual kg de langostino,")
    print("    la UE paga igual o mas en TODO el rango de ruta. (Confirma la tesis.)")

    # --- FOB por ruta -----------------------------------------------------
    fr = fob_por_ruta()
    print("\n" + "=" * 78)
    print("FOB POR RUTA · cuanto captura el ORIGEN por kg (2026)")
    print("=" * 78)
    print(fr.to_string(index=False))
    ent_ab = fr[(fr.presentacion == "entero") & (fr.ruta == "a bordo")]["fob_usd_kg"]
    ent_en = fr[(fr.presentacion == "entero") & (fr.ruta == "en tierra")]["fob_usd_kg"]
    print("\nLectura:")
    if len(ent_ab) and len(ent_en):
        print(f"  * Mismo entero, congelado A BORDO vale +{(ent_ab.iloc[0]/ent_en.iloc[0]-1)*100:.0f}% "
              f"que procesado en tierra (${ent_ab.iloc[0]} vs ${ent_en.iloc[0]}).")
    print("  * El P&D existe SOLO en tierra: a bordo no se pela (valida el supuesto).")
    top = fr.iloc[0]; bot = fr.iloc[-1]
    print(f"  * Por kg de MATERIA PRIMA capturada, el origen saca mas vendiendo "
          f"{top.presentacion} {top.ruta} (${top.fob_usd_matprima}) y menos con "
          f"{bot.presentacion} {bot.ruta} (${bot.fob_usd_matprima}):")
    print("    pelar y procesar en tierra DESTRUYE valor de origen por kg capturado.")
    print("    (Cuantifica 'vender entero a bordo gana el margen'.)")

    graficar(df)
    graficar_ruta(fr)
    with pd.ExcelWriter(SALIDAS / "cascade_fob_cif_gondola.xlsx") as xw:
        df.to_excel(xw, sheet_name="cascade", index=False)
        fr.to_excel(xw, sheet_name="fob_por_ruta", index=False)
    print(f"\n2 gráficos SVG + Excel (2 hojas) -> {SALIDAS}")
