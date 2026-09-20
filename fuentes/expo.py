"""
Exportación argentina de langostino (Softrade) — carga limpia y consultable.

Deduplicación: el dato aduanero trae despachos declarados más de una vez (doble
conteo, ~3-9% del volumen). Este módulo los remueve de dos formas:
  1) Si el archivo trae la columna 'Revisión Claude (motivo de la marca)'
     (anotación fila por fila), excluye lo marcado como Duplicado/Subítem/
     Fila-principal-sin-FOB/precio-fuera-de-rango.
  2) Si no, deduplica por 7 campos clave (fecha, NCM, destino, FOB unitario,
     FOB total, kilos, descripción) — un match exacto en los 7 es artefacto,
     no un despacho genuino repetido.

Los $/kg NO se ven afectados por el doble conteo (son ratio valor/kg); lo que
corrige es el VOLUMEN absoluto. Calibre/presentación salen del campo AI(...) en
'Marca o Descripcion': entero L1>L2>L3, cola C1>C2>CR, pelado devenado por count.
La PRESENTACIÓN sale del sufijo SIM, que la codifica oficialmente (ver SIM_PRES).
"""
from __future__ import annotations

import glob
import os
import re
import warnings

import pandas as pd

warnings.simplefilter("ignore")  # silencia el aviso de estilo de openpyxl

# Carpeta con los .xlsx de exportación (fuera del proyecto, junto a los de Softrade).
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
EXPO_DIR = fuente("softrade_langostino", "EXPO ARGENTINA LANGO")

FLAG_COL = "Revisión Claude (motivo de la marca)"
CLAVE = ["Fecha", "NCM-SIM", "País de Destino", "U$S Unitario",
         "U$S FOB", "Kgs. Netos", "Marca o Descripcion"]
_PROBLEMAS = ("duplicado", "subitem", "subítem", "fila principal", "fuera de tod")


def _es_problema(v) -> bool:
    v = str(v).lower()
    return any(k in v for k in _PROBLEMAS)


# El campo AI(...) no tiene formato fijo: el mismo grado aparece como "C1", "C1L",
# "C1S", "COLA 1" o "LANG COLA C_MIX" según el exportador. Estos patrones cubren las
# variantes observadas en 2022-2026. Los puntos y guiones bajos se normalizan a espacio
# para que "L.1" y "C_MIX" caigan en el mismo molde que "L1" y "CMIX".
_RE_CR = re.compile(r"COLA\s*ROTA|\bROTA\b|\bCR\b")
_RE_CM = re.compile(r"\bCM\b|\bCMIX\b|\bC\s?MIX\b|COLA\s*MIX")
_RE_CGRADO = re.compile(r"\bC\s?([012])\s?[LS]?\b")
_RE_COLA = re.compile(r"COLA|SIN\s*CABEZA|S/\s?CABEZA|HEADLESS")
_RE_LGRADO = re.compile(r"\bL\s?([123])\b|ENTERO\s*([123])\b|\bLANG?\s*([123])\b")
_RE_ENTERO = re.compile(r"ENTERO|WHOLE|\bHOSO\b")


def _norm(ai: str) -> str:
    """Puntos y guiones bajos a espacio: 'L.1' -> 'L 1', 'C_MIX' -> 'C MIX'."""
    return re.sub(r"[._]", " ", ai.upper())


# La presentación NO hace falta adivinarla del texto: la apertura SIM la codifica.
# Fuente: VUCE, posición 0306.17.90 (consultada 2026-08-09). Estructura del sufijo:
# primer dígito = tamaño de envase (1: <=1 kg · 2: 1-2 kg · 9: >2 kg), segundo dígito
# = 1 langostinos / 9 otras especies, y el resto la presentación.
# Todo 0306.17.90 es COLA: pelado, devenado y easy peel son presentaciones de la cola,
# no categorías aparte. 0306.17.10 es el entero con cabeza.
SIM_PRES = {
    "111C": "pelado ahumado", "191D": "pelado ahumado",
    "911W": "pelado ahumado", "991X": "pelado ahumado",
    "113G": "pelado devenado", "211H": "pelado devenado", "913A": "pelado devenado",
    "114J": "easy peel", "212K": "easy peel", "914C": "easy peel",
    "115L": "pelado", "213M": "pelado", "915E": "pelado",
    "119V": "cola", "219A": "cola", "919N": "cola",          # «los demás» = cola sin pelar
    "199W": "otra especie", "290G": "otra especie", "999P": "otra especie",
}
SIM_ENVASE = {"1": "≤1 kg", "2": "1-2 kg", "9": ">2 kg"}


def _presentacion(ai: str) -> str:
    a = _norm(ai)
    if "PEL" in a and "DEV" in a:
        return "pelado devenado"
    if "PEL" in a or "P&D" in a:
        return "pelado"
    cola = bool(_RE_COLA.search(a) or _RE_CGRADO.search(a) or _RE_CM.search(a)
                or _RE_CR.search(a))
    ent = bool(_RE_ENTERO.search(a) or _RE_LGRADO.search(a))
    if cola and not ent:
        return "cola"
    if ent:
        return "entero"
    return "otro"


# Tramos de piezas por kilo de cada grado, según los sufijos oficiales del NCM
# (0306.17). Permiten asignar grado a las filas que solo declaran el conteo
# ("COLA 45/55 PPK"): 45-55 cae dentro de 30-55, o sea C1.
TRAMOS_ENTERO = [("L1", 11, 20), ("L2", 21, 30), ("L3", 31, 40),
                 ("L4", 41, 60), ("L5", 61, 80), ("L6", 81, 999)]
TRAMOS_COLA = [("C1", 30, 55), ("C2", 56, 100), ("C3", 101, 150)]
_RE_CONTEO = re.compile(r"\b(\d{1,3})\s*/\s*(\d{1,3})\b")
# Hasta 2017 la descripción no trae el campo AI(...) ni el conteo con barra: el
# calibre viene en prosa ("DE 11 HASTA 20 PIEZAS POR kg"). Los cortes de esa
# prosa (11-20, 21-30, 31-40, 41-60, 61-80) son los mismos tramos oficiales de
# TRAMOS_ENTERO, así que el grado se recupera sin supuesto adicional.
_RE_DE_HASTA = re.compile(r"DE\s+(\d{1,3})\s+HASTA\s+(\d{1,3})\s+PIEZAS")
# El conteo viene en dos unidades: piezas por kilo (norma argentina, "PPK") y piezas
# por LIBRA ("PPL", "P/LB"), que es la norma de EE.UU. y aparece sobre todo en el
# producto que va allá. Mezclarlas corre el grado 2,2 veces.
LB_A_KG = 2.20462
_RE_PPL = re.compile(r"PPL|P\s?/\s?LB|PZ\s?/\s?LB|POR LIBRA|\bLB\b")
_RE_PPK = re.compile(r"PPK|PZ\s?/\s?K|P\s?/\s?K|POR KG|\bKG\b")
# Piso físico del conteo por kilo en la cola según los tramos oficiales (30 pzas/kg).
# Un "16/20" de cola no puede ser por kilo: serían colas de 50-60 gramos.
MIN_KG_COLA = 28


# Grado "U" de la norma estadounidense: U15 = under 15, menos de 15 piezas por libra.
_RE_U = re.compile(r"\bU\s?/?\s?(\d{1,3})\b")


def _por_conteo(a: str, tramos, es_cola: bool) -> str | None:
    """Grado a partir del conteo declarado, normalizado a piezas por kilo."""
    m = _RE_CONTEO.search(a) or _RE_DE_HASTA.search(a)
    if not m:
        u = _RE_U.search(a)
        if not u:
            return None
        medio = int(u.group(1)) * LB_A_KG        # el "U" siempre viene en libras
        for nombre, a_, b_ in tramos:
            if a_ <= medio <= b_:
                return nombre
        return tramos[0][0] if medio < tramos[0][1] else None
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo > hi or hi > 999:
        return None
    medio = (lo + hi) / 2
    if _RE_PPL.search(a):                       # declarado en libras
        medio *= LB_A_KG
    elif not _RE_PPK.search(a) and es_cola and medio < MIN_KG_COLA:
        medio *= LB_A_KG                        # sin unidad, pero imposible por kilo
    for nombre, a_, b_ in tramos:
        if a_ <= medio <= b_:
            return nombre
    return None


def _calibre(ai: str, pres: str) -> str:
    a = _norm(ai)
    if pres == "entero":
        m = _RE_LGRADO.search(a)
        if m:
            return f"L{next(g for g in m.groups() if g)}"
        return _por_conteo(a, TRAMOS_ENTERO, False) or "s/d"
    if pres == "cola":
        if _RE_CR.search(a):
            return "CR"
        if _RE_CM.search(a):
            return "CM"
        m = _RE_CGRADO.search(a)
        if m:
            return f"C{m.group(1)}"
        return _por_conteo(a, TRAMOS_COLA, True) or "s/d"
    g = _por_conteo(a, TRAMOS_COLA, True)      # el pelado usa la misma escala que la cola
    if g:
        return g
    m = _RE_CONTEO.search(a)
    return f"{m.group(1)}/{m.group(2)}" if m else "s/d"


def cargar(path: str) -> pd.DataFrame:
    """Carga un archivo de exportación, deduplicado y parseado."""
    d = pd.read_excel(path, sheet_name="Detalle")
    d["fob_dec"] = pd.to_numeric(d["U$S Unitario"], errors="coerce")
    d["fob_tot"] = pd.to_numeric(d["U$S FOB"], errors="coerce")
    d["kg"] = pd.to_numeric(d["Kgs. Netos"], errors="coerce")
    d["fecha"] = pd.to_datetime(d["Fecha"], errors="coerce")

    # El unitario declarado tiene erratas de unidad (alguna fila viene en US$/tonelada:
    # una sola de 2022 traía 6624 en vez de 6,62 y levantaba el promedio del año 15%).
    # FOB total y kilos son campos primarios, así que el precio se deriva de ellos y el
    # unitario declarado queda solo como control.
    # Moneda: parte de los despachos se pactan en euros (5-8% de las filas). Las columnas
    # 'FOB Divisa' / 'Unitario Divisa' vienen en esa moneda original y NO se usan acá:
    # además de estar sin convertir, se apoyan en otra base de cantidad ('Cantidad.1').
    # 'U$S FOB' ya viene convertido y cierra contra 'U$S Unitario' x 'Kgs. Netos' en el
    # 100% de las filas, así que todo el análisis se hace sobre las columnas en dólares.
    implicito = d["fob_tot"] / d["kg"]
    d["fob"] = implicito.where(implicito.notna() & (implicito > 0), d["fob_dec"])
    d["fob_discrepa"] = ((implicito - d["fob_dec"]).abs() / d["fob_dec"]) > 0.05

    antes = len(d)
    if FLAG_COL in d.columns:                       # depuración anotada
        d = d[~d[FLAG_COL].map(_es_problema)]
        metodo = "anotación Revisión Claude"
    else:                                           # dedup por clave
        claves = [c for c in CLAVE if c in d.columns]
        d = d[~d.duplicated(subset=claves, keep="first")]
        metodo = f"dedup {len(claves)} campos"

    # Despacho fraccionado sin prorratear (208 filas en 2018, 31 en 2019, 3 en 2022):
    # el FOB total corresponde a 'Cantidad' (FOB = unitario × Cantidad, exacto) pero
    # los kilos netos son solo la fracción despachada, así que FOB÷kg da hasta 100×
    # el precio real. El unitario declarado es plausible; aun así se EXCLUYE la fila
    # (no se reconstruye): mismo criterio conservador que con los subítems duplicados.
    cant = pd.to_numeric(d["Cantidad"], errors="coerce")
    frac = (((d["fob_tot"] - d["fob_dec"] * cant).abs() / d["fob_tot"]) < 0.02) \
        & (cant > d["kg"] * 1.1)
    d = d[~frac.fillna(False)]

    # Subítems duplicados (criterio de la revisión anotada, automatizado): si la suma
    # de 'Cantidad.1' del despacho es un múltiplo entero ≥2 de los kilos netos, los
    # renglones de detalle vinieron repetidos y no se sabe si la cifra buena es la
    # suma o los kilos → se excluye la principal por ambigüedad.
    if "Identificador" in d.columns and "Item" in d.columns:
        gr = d["Identificador"].astype(str) + "|" + d["Item"].astype(str)
        c1 = pd.to_numeric(d["Cantidad.1"], errors="coerce").fillna(0)
        suma_c1 = c1.groupby(gr).transform("sum")
        razon = suma_c1 / d["kg"].where(d["kg"] > 0)
        multi = (razon > 1.95) & ((razon - razon.round()).abs() < 0.02)
        d = d[~multi.fillna(False)]

    d = d[(d["kg"] > 0) & (d["fob"] > 0)].copy()

    # Banda residual de plausibilidad sobre el precio implícito. No es un filtro de
    # producto barato (las cabezas a 0,9-1,2 US$/kg pasan): 0,3-30 solo puede atrapar
    # erratas del registro que los controles estructurales no explican.
    d = d[(d["fob"] >= 0.3) & (d["fob"] <= 30)]
    d["ai"] = (d["Marca o Descripcion"].astype(str)
               .str.extract(r"AI\(([^)]*)\)")[0].fillna("").str.upper())
    # Presentación: primero el código SIM (oficial, cubre 99,8%); el texto queda de
    # respaldo para las pocas filas sin sufijo reconocible. El CALIBRE sí sale del
    # texto: la nomenclatura no lo codifica.
    sim = d["NCM-SIM"].astype(str).str.replace(".", "", regex=False)
    d["sim"] = sim
    d["envase"] = sim.str[-4].map(SIM_ENVASE)
    pres_sim = sim.str[-4:].map(SIM_PRES)
    pres_sim = pres_sim.mask(sim.str.startswith("03061710"), "entero")
    d["pres"] = pres_sim.fillna(d["ai"].map(_presentacion))
    d.loc[d["pres"] == "entero", "envase"] = None
    # Para el CALIBRE, si no hay campo AI(...) se cae al texto completo: hasta 2017
    # el grado viaja en prosa. El respaldo es solo para el calibre — la presentación
    # sigue saliendo del sufijo SIM, que es oficial y no depende de la redacción.
    d["_caltxt"] = d["ai"].where(d["ai"].str.strip() != "",
                                 d["Marca o Descripcion"].astype(str).str.upper())
    d["cal"] = d.apply(
        lambda r: _calibre(r["_caltxt"], "entero" if r["pres"] == "entero"
                           else "cola" if r["pres"] == "cola" else "pelado"), axis=1)

    # SA01 en la descripción marca CONGELADO A BORDO (buque congelador); SA00, procesado
    # en tierra. Validado contra los desembarques por flota: la participación de SA01 en
    # la exportación replica la de la flota tangonera congelera con r = +1,00 (2020-2025).
    sa = d["Marca o Descripcion"].astype(str).str.extract(r"SA(\d{2})")[0]
    # Respaldo para 2013-2017, igual que con el calibre: antes de que existiera el
    # sufijo, la leyenda «CONGELADO A BORDO» viaja en prosa en la misma descripción.
    # OJO: no hay leyenda equivalente para el procesado en tierra, así que en esos
    # años la marca «a bordo» es AFIRMATIVA y el resto queda en «s/d» — nunca se
    # infiere «en tierra» por descarte. Cobertura del entero: 68-70% en 2013-2016,
    # hueco real de jun a nov de 2017 (la descripción viene vacía en ese tramo).
    txt = d["Marca o Descripcion"].astype(str).str.upper().str.contains(
        "CONGELADO A BORDO", na=False)
    ruta = pd.Series("s/d", index=d.index, dtype=object)
    ruta[sa.notna()] = "en tierra"
    ruta[sa == "01"] = "a bordo"
    ruta[sa.isna() & txt] = "a bordo"
    d["ruta"] = ruta
    d["anio"] = d["fecha"].dt.year
    d["mes"] = d["fecha"].dt.month
    d.attrs["dedup"] = (antes, len(d), metodo)
    # «desc» es el campo libre del que ya salen talla, presentación y marca de
    # congelado a bordo; se devuelve tal cual para poder auditarlo (glaseo.py).
    d["desc"] = d["Marca o Descripcion"]
    return d[["fecha", "anio", "mes", "País de Destino", "fob", "fob_dec",
              "fob_discrepa", "fob_tot", "kg", "ai", "sim", "envase", "pres", "cal",
              "ruta", "desc"]].rename(columns={"País de Destino": "destino"})


def cargar_todos(carpeta: str = EXPO_DIR) -> pd.DataFrame:
    """Concatena todos los .xlsx de exportación de la carpeta (limpios)."""
    # La carpeta también aloja archivos que no son despachos (nomenclador, auxiliares):
    # se reconocen porque no traen la hoja 'Detalle'.
    files = [f for f in glob.glob(os.path.join(carpeta, "*.xlsx")) if "~$" not in f]
    # El mismo export puede estar dos veces con distinto nombre (p.ej. el volcado
    # crudo "detalle_ARexportDetalladas_*" y su copia renombrada "ARGENTINA EXPO ...").
    # La dedup por 7 campos corre DENTRO de cada archivo, así que una segunda copia
    # duplicaría el período entero. El hash no alcanza —basta anotar la revisión en
    # una para que difiera—, así que la regla es por PERÍODO: si todos los meses que
    # trae un archivo ya vinieron en otro, se omite. Se cargan primero los archivos
    # con nombre propio, que son los que llevan la revisión anotada fila por fila.
    files.sort(key=lambda f: (os.path.basename(f).lower().startswith("detalle_"), f))
    fr, periodos = [], set()
    for f in files:
        try:
            hojas = pd.ExcelFile(f).sheet_names
        except Exception:
            continue
        if "Detalle" not in hojas:
            continue
        d = cargar(f)
        prop = set(zip(d["anio"], d["mes"]))
        if prop and prop <= periodos:
            print(f"  · omitido {os.path.basename(f)}: período ya cargado")
            continue
        periodos |= prop
        fr.append(d)
    D = pd.concat(fr, ignore_index=True)
    # Los años 2013-2019 llegan solo por el volcado crudo, cuyo VOLUMEN está inflado
    # hasta 1,45x por doble conteo que la dedup no ve (2018: 270 kt contra 186 kt
    # oficiales). Su PRECIO, en cambio, coincide con el oficial dentro del 1% en el
    # entero y del 3% en la cola —el doble conteo se cancela en el cociente—, así que
    # esos años sirven para $/kg, calibre y destino, nunca para nivel de volumen.
    # La columna lo deja explícito para que ningún cálculo lo use por descuido.
    D["vol_confiable"] = D["anio"] >= 2020
    return D


# --------------------------------------------------------------------------
# Consultas
# --------------------------------------------------------------------------
def _wav(s: pd.DataFrame) -> float:
    return (s["fob"] * s["kg"]).sum() / s["kg"].sum()


def resumen_anual(d: pd.DataFrame) -> pd.DataFrame:
    g = d.groupby("anio").apply(lambda s: pd.Series({
        "kt": s["kg"].sum() / 1e6,
        "valor_MUSD": (s["fob"] * s["kg"]).sum() / 1e6,
        "fob_medio": _wav(s),
    }))
    return g.round(2)


def precio_por_calibre(d: pd.DataFrame, pres: str) -> pd.DataFrame:
    s = d[d["pres"] == pres]
    g = s.groupby("cal").apply(lambda x: pd.Series({
        "kt": x["kg"].sum() / 1e6, "fob": _wav(x)}))
    return g.sort_values("fob", ascending=False).round(2)


# Rendimiento a materia prima, en cadena y con los mismos valores para las dos flotas,
# por indicación de la industria (24-ago-2026):
#     entero → cola             0,55   (antes 0,62)
#     cola   → pelado devenado  0,70   →  sobre materia prima: 0,55 × 0,70 = 0,385 (antes 0,43)
RENDIMIENTO = {"entero": 1.00, "cola": 0.55, "pelado devenado": 0.385,
               "pelado": 0.385, "otro": 0.75}


def validar_volumen(d: pd.DataFrame, captura_kt: dict) -> pd.DataFrame:
    """Test de imposibilidad: el producto exportado, llevado a peso de langostino
    entero capturado, no puede superar la captura del año.

    La deduplicación por 7 campos NO alcanza en los años de boom: 2020 y 2021 dan
    115% y 123% de la captura, físicamente imposible. Para VOLUMEN hay que usar la
    serie oficial de aduana; Softrade sirve para precio, calibre, destino y ruta,
    que son ratios y no se ven afectados por el doble conteo.
    """
    filas = []
    for a, s in d.groupby("anio"):
        mp = (s["kg"] / s["pres"].map(RENDIMIENTO).fillna(0.75)).sum() / 1e6
        c = captura_kt.get(a)
        filas.append({"anio": a, "expo_kt": s["kg"].sum() / 1e6, "mp_equiv_kt": mp,
                      "captura_kt": c,
                      "mp_sobre_captura": (mp / c * 100) if c else None,
                      "confiable": (c is None) or (mp / c <= 0.92)})
    return pd.DataFrame(filas).set_index("anio").round(1)


def precio_por_destino(d: pd.DataFrame, pres: str | None = None,
                       cal: str | None = None, min_kt: float = 0.3) -> pd.DataFrame:
    s = d
    if pres:
        s = s[s["pres"] == pres]
    if cal:
        s = s[s["cal"] == cal]
    g = s.groupby("destino").apply(lambda x: pd.Series({
        "kt": x["kg"].sum() / 1e6, "fob": _wav(x)}))
    return g[g["kt"] >= min_kt].sort_values("fob", ascending=False).round(2)


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    d = cargar_todos()
    print(f"Cargado y deduplicado: {len(d):,} filas · {d['anio'].min()}-{d['anio'].max()}\n")
    print("=== Volumen y precio anual (LIMPIO) ===")
    print(resumen_anual(d).to_string())
    print("\n=== FOB entero por calibre (todos los años) ===")
    print(precio_por_calibre(d, "entero").to_string())
    print("\n=== Entero L1: quién paga más (>=0.5 kt) ===")
    print(precio_por_destino(d, "entero", "L1", min_kt=0.5).head(8).to_string())
