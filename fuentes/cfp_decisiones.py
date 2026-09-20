# -*- coding: utf-8 -*-
"""De los 2.884 párrafos con langostino a las DECISIONES efectivas del CFP.

Qué hace, en tres filtros y tres extracciones.

FILTROS
  1. Resolutivo. Se conservan sólo los párrafos con fórmula de decisión —«se
     decide», «se acuerda», «autorizar», «disponer», «habilitar», «prorrogar»,
     «ratificar»—. El resto es temario, nota recibida o deliberación. Nótese
     que las actas NO usan «se resuelve» ni «se aprueba»: se verificó sobre el
     corpus y dan cero.
  2. Temario. Se descartan los párrafos que arrancan con numeración de tema y
     nombran dos o más especies distintas: son el orden del día, no decisiones.
  3. Deliberación. «Tomar conocimiento», «evaluar» y «considerar» sin fórmula
     resolutiva quedan afuera.

EXTRACCIONES
  fecha_acta      cuatro redacciones distintas más un patrón de reserva anclado
                  en el año del nombre del archivo, porque el extractor de PDF
                  parte los números («a los 2 1 días») y la fórmula de apertura
                  cambia entre años.
  fecha_vigencia  «a partir de la hora 0:00 del día viernes 1° de noviembre».
                  El año sale del acta, con salto de año si la vigencia cae en
                  enero-febrero y el acta es de noviembre-diciembre.
  coordenadas     paralelos y meridianos del rectángulo. Se acotan a la ventana
                  geográfica de la pesquería —latitud 38 a 55 S, longitud 55 a
                  70 O— para no levantar números que no son coordenadas.

Y una categoría que apareció leyendo el corpus y no estaba prevista: la
DELEGACIÓN. «Autorizar a la Autoridad de Aplicación a disponer el cierre… si
los rendimientos así lo aconsejaran» no es un cierre efectivo, es una
habilitación condicional. Va marcada aparte: para el modelo no es un evento de
oferta hasta que se ejerce.

AUDITORÍA. Dentro de cada año el número de acta y la fecha de reunión tienen
que crecer juntos. Toda violación se informa: es la señal de que el patrón de
reserva agarró una fecha del cuerpo del acta en vez de la de la reunión.

Salida: salidas/cfp_langostino_decisiones.xlsx

Uso:  python -m fuentes.cfp_decisiones
"""
from __future__ import annotations

import os
import re
import sys
import warnings

import pandas as pd

warnings.simplefilter("ignore")
sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR = fuente("actas_cfp")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MES = {m: i + 1 for i, m in enumerate(MESES)}
MES["setiembre"] = 9
_M = "|".join(list(MES))

RESOLUTIVO = re.compile(
    r"\bse decide\b|\bse acuerda\b|\bautorizar\b|\bdisponer\b|\bhabilitar\b|"
    r"\bprorrogar\b|\bratificar\b", re.I)
DELEGACION = re.compile(
    r"autorizar a la autoridad de aplicaci[oó]n|facultar a la autoridad|"
    r"si (?:los|las|el|la)[^.]{0,80}(?:aconsejar|lo justificar)", re.I)
OTRAS_ESPECIES = re.compile(
    r"merluza|calamar|polaca|vieira|anchoita|centolla|abadejo|corvina", re.I)

ACCION = [
    ("cierre", r"\bel cierre\b|\bcierre (?:parcial|total|del|de la|a la)|"
               r"\bcerrad[ao]\b|\bveda\w*\b"),
    ("suspensión", r"suspen(?:der|si[oó]n|de)\b"),
    ("prórroga", r"prorrog\w+|pr[oó]rrog\w+"),
    ("apertura", r"\bla apertura\b|\bapertura a la pesca\b|habilit\w+|"
                 r"\bse abre\b|reapertur\w+"),
    # La prospección es evento de oferta aunque no lo parezca: es la marea
    # exploratoria que el CFP dispone ANTES de abrir, y mueve esfuerzo real.
    # Estaba cayendo en «otra» —39 párrafos— hasta que se leyó el corpus.
    ("prospección", r"prospecci[oó]n|prospectiv[ao]|marea de investigaci[oó]n"),
    ("cuota/captura", r"captura m[aá]xima|\bcupo\b|\bcuota\b|tonelad"),
]

# Temario. El filtro por numeración al inicio del párrafo no alcanza: el
# extractor de PDF antepone el número de página, así que el orden del día
# arranca con «2 justificación de…» y se cuela. La marca robusta es la
# numeración de SUBTEMA repetida —«1.3.», «2.1.»— tres o más veces.
RE_TEMARIO = re.compile(r"\b\d{1,2}\.\d{1,2}\.")

# Vigencia. Dos familias, y la distinción importa: «a partir de» abre el
# período y «hasta» lo cierra. Se guardan con etiqueta, no se mezclan.
# El día viene a veces partido por el extractor de PDF —«del d ía viernes»—,
# de ahí el `d\s*[ií]\s*a` en lugar de `día`.
_DIA = r"d\s*[ií]\s*a"
RE_VIG = [
    ("desde", r"a partir de (?:la|las) hora[s]?\s*\d{1,2}[:.]\d{2}\s*(?:horas?\s*)?"
              rf"del {_DIA}(?:\s+\w+)?\s+(\d{{1,2}})[°º]?\s+de\s+({_M})"),
    ("desde", rf"a partir del {_DIA}(?:\s+\w+)?\s+(\d{{1,2}})[°º]?\s+de\s+({_M})"),
    ("hasta", r"hasta (?:la|las)\s*\d{1,2}[:.]\d{2}\s*(?:horas?\s*)?"
              rf"del {_DIA}(?:\s+\w+)?\s+(\d{{1,2}})[°º]?\s+de\s+({_M})"),
    ("hasta", rf"hasta el {_DIA}(?:\s+\w+)?\s+(\d{{1,2}})[°º]?\s+de\s+({_M})"),
    ("hasta", rf"hasta el\s+(\d{{1,2}})[°º]?\s+de\s+({_M})"),
    ("desde", rf"a partir de(?:l)?\s+(\d{{1,2}})[°º]?\s+de\s+({_M})"),
]
RE_LAT = re.compile(r"(\d{2})\s*[°º]\s*(\d{1,2})?\s*['´’]?\s*(?:de\s+latitud\s+)?"
                    r"(?:S\b|Sur\b|sur\b)")
RE_LON = re.compile(r"(\d{2})\s*[°º]\s*(\d{1,2})?\s*['´’]?\s*(?:de\s+longitud\s+)?"
                    r"(?:W\b|O\b|Oeste\b|oeste\b|w\b|o\b)")
RE_PARAL = re.compile(r"paralelos?\s+((?:\d{1,2}[°º]?\s*\d{0,2}['´’]?\s*"
                      r"(?:y|a|al|,)?\s*){1,4})", re.I)
RE_MERID = re.compile(r"meridianos?\s+((?:\d{1,2}[°º]?\s*\d{0,2}['´’]?\s*"
                      r"(?:y|a|al|,)?\s*){1,4})", re.I)


def _norm(t: str) -> str:
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"(?<=\d)\s+(?=\d)", "", t)   # une dígitos partidos por el PDF


def fecha_acta(t: str, anio: int):
    t = _norm(t)
    pats = [
        rf"a\s+los?\s+(\d{{1,2}})\s+d[ií]as?\s+del\s+mes\s+de\s+({_M})\s+de\s+{anio}",
        rf"del\s+mes\s+de\s+(\d{{1,2}})\s+de\s+({_M})\s+de\s+{anio}",
        rf"[Ee]l\s+d[ií]a\s+(\d{{1,2}})[°º]?\s+del\s+mes\s+de\s+({_M})\s+de\s+{anio}",
        rf"(\d{{1,2}})[°º]?\s+de\s+({_M})\s+de\s+{anio}",     # patrón de reserva
    ]
    for i, pat in enumerate(pats):
        m = re.search(pat, t, re.I)
        if m and m.group(2).lower() in MES:
            return f"{anio}-{MES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}", i
    return None, None


def fecha_vigencia(p: str, fecha_ref: str | None):
    """Devuelve (fecha, 'desde'|'hasta') o (None, None)."""
    if not fecha_ref:
        return None, None
    a, m_ref = int(fecha_ref[:4]), int(fecha_ref[5:7])
    for clase, pat in RE_VIG:
        m = re.search(pat, p, re.I)
        if not m:
            continue
        mes = m.group(2).lower()
        if mes not in MES:
            continue
        mm = MES[mes]
        # el acta de nov-dic que fija vigencia en ene-feb habla del año siguiente
        anio = a + 1 if (m_ref >= 11 and mm <= 2) else a
        return f"{anio}-{mm:02d}-{int(m.group(1)):02d}", clase
    return None, None


def _grados(txt: str, lim: tuple[int, int]) -> list[float]:
    """Grados decimales de un fragmento, acotados a la ventana de la pesquería."""
    out = []
    for m in re.finditer(r"(\d{1,3})\s*[°º]?\s*(\d{1,2})?\s*['´’]?", txt):
        g = int(m.group(1))
        if not (lim[0] <= g <= lim[1]):
            continue
        out.append(round(g + (int(m.group(2)) / 60 if m.group(2) else 0), 3))
    return out


def coords(p: str) -> dict:
    lats = [round(int(a) + (int(b) / 60 if b else 0), 3)
            for a, b in RE_LAT.findall(p) if 38 <= int(a) <= 55]
    lons = [round(int(a) + (int(b) / 60 if b else 0), 3)
            for a, b in RE_LON.findall(p) if 55 <= int(a) <= 70]
    for blo in RE_PARAL.findall(p):
        lats += _grados(blo, (38, 55))
    for blo in RE_MERID.findall(p):
        lons += _grados(blo, (55, 70))
    lats, lons = sorted(set(lats)), sorted(set(lons))
    return {"lat_min_S": lats[0] if lats else None,
            "lat_max_S": lats[-1] if lats else None,
            "lon_min_O": lons[0] if lons else None,
            "lon_max_O": lons[-1] if lons else None,
            "n_lat": len(lats), "n_lon": len(lons)}


def accion(p: str) -> str:
    for nombre, pat in ACCION:
        if re.search(pat, p, re.I):
            return nombre
    return "otra"


def procesar() -> pd.DataFrame:
    import pypdf
    filas, fechas = [], []
    for anio_s in sorted(x for x in os.listdir(DIR) if x.isdigit()):
        anio = int(anio_s)
        d = os.path.join(DIR, anio_s)
        for n in sorted(x for x in os.listdir(d) if x.lower().endswith(".pdf")):
            try:
                r = pypdf.PdfReader(os.path.join(d, n))
                t = "\n".join((pg.extract_text() or "") for pg in r.pages)
            except Exception:
                continue
            if not t:
                continue
            fa, via = fecha_acta("\n".join((pg.extract_text() or "")
                                           for pg in r.pages[:2]), anio)
            m = re.search(r"ACTA\s+CFP\s+N?[°ºo]?\s*(\d+)", n, re.I)
            nro = int(m.group(1)) if m else None
            fechas.append({"anio": anio, "acta": nro, "archivo": n,
                           "fecha_acta": fa, "patron": via})
            trozos = [_norm(x).strip()
                      for x in re.split(r"\n\s*\n|(?<=\.)\n(?=[A-ZÁÉÍÓÚ])", t)]
            for i, p in enumerate(trozos):
                if len(p) < 60 or "langostino" not in p.lower():
                    continue
                if not RESOLUTIVO.search(p):
                    continue
                # temario: numeración de subtema repetida, o encabezado de tema
                # con varias especies. Hacen falta las dos reglas.
                if len(RE_TEMARIO.findall(p)) >= 3:
                    continue
                if re.match(r"^\d{1,2}[\.\)]\s", p) and \
                        len(set(x.lower() for x in OTRAS_ESPECIES.findall(p))) >= 2:
                    continue

                # VENTANA AMPLIADA. La decisión y su fecha de vigencia suelen
                # caer en trozos distintos —«…disponer el cierre.» / «El mismo
                # regirá a partir de la hora 0:00 del día…»— y por eso la fecha
                # se recuperaba en menos de un cuarto de los casos. Se busca
                # primero en el trozo propio y, si no está, en los dos
                # siguientes. Queda registrado DE DÓNDE salió: una fecha tomada
                # del contexto puede pertenecer a otra decisión, y el que
                # codifique tiene que poder distinguirlo sin abrir el PDF.
                vent = " ".join(trozos[i:i + 3])[:3000]
                fv, clase = fecha_vigencia(p, fa)
                origen = "propio" if fv else ""
                if not fv:
                    fv, clase = fecha_vigencia(vent, fa)
                    origen = "contexto" if fv else "sin fecha"
                c = coords(p)
                orig_c = "propio" if c["n_lat"] or c["n_lon"] else ""
                if not (c["n_lat"] or c["n_lon"]):
                    c = coords(vent)
                    orig_c = "contexto" if (c["n_lat"] or c["n_lon"]) else "sin coord"

                f = {"anio": anio, "acta": nro, "archivo": n, "fecha_acta": fa,
                     "accion": accion(p),
                     "delegacion": bool(DELEGACION.search(p)),
                     "fecha_vigencia": fv, "clase_fecha": clase,
                     "origen_fecha": origen}
                f.update(c)
                f["origen_coord"] = orig_c
                f["parrafo"] = p[:2000]
                f["contexto"] = vent[len(p):][:1200]
                filas.append(f)
    return pd.DataFrame(filas), pd.DataFrame(fechas)


def main() -> None:
    t, F = procesar()
    print(f"Actas leídas: {len(F)} · con fecha resuelta: {F.fecha_acta.notna().sum()}")
    print("Patrón usado para la fecha (3 = el de reserva, revisar):")
    print("  " + F.patron.value_counts(dropna=False).to_dict().__str__())

    # auditoría: dentro del año, acta y fecha crecen juntas
    mal = []
    for anio, g in F.dropna(subset=["fecha_acta", "acta"]).groupby("anio"):
        g = g.sort_values("acta")
        f = pd.to_datetime(g.fecha_acta)
        for i in range(1, len(g)):
            if f.iloc[i] < f.iloc[i - 1]:
                mal.append(f"{g.archivo.iloc[i]} ({g.fecha_acta.iloc[i]}) va antes "
                           f"que {g.archivo.iloc[i-1]} ({g.fecha_acta.iloc[i-1]})")
    print(f"\nAuditoría de fechas — inconsistencias: {len(mal)}")
    for x in mal[:8]:
        print("   ·", x)

    print(f"\nDecisiones resolutivas sobre langostino: {len(t):,} "
          f"(de 2.884 párrafos con la palabra)")
    print("\nPor acción:")
    print(t.accion.value_counts().to_string())
    print(f"\nDelegaciones (condicionales, NO son evento de oferta): "
          f"{int(t.delegacion.sum())}")
    print(f"Con fecha de vigencia extraída: {t.fecha_vigencia.notna().sum()}")
    print(f"Con rectángulo de coordenadas:  {(t.n_lat > 0).sum()} con latitud, "
          f"{(t.n_lon > 0).sum()} con longitud")
    print("\nPor año y acción:")
    print(pd.crosstab(t.anio, t.accion).to_string())

    ef = t[(~t.delegacion) & t.accion.isin(["apertura", "cierre", "suspensión",
                                            "prórroga", "prospección"])]
    print(f"\nEVENTOS DE OFERTA efectivos (sin delegaciones): {len(ef)}")
    print(f"   de ellos con fecha de vigencia: {ef.fecha_vigencia.notna().sum()}")
    print(f"   de ellos con coordenadas:       {(ef.n_lat > 0).sum()}")
    print("\n   de dónde salió la fecha (contexto = revisar, puede ser de otra "
          "decisión):")
    print("     " + ef.origen_fecha.value_counts().to_dict().__str__())
    print("   de dónde salieron las coordenadas:")
    print("     " + ef.origen_coord.value_counts().to_dict().__str__())

    p = os.path.join(RAIZ, "salidas", "cfp_langostino_decisiones.xlsx")
    try:
        with pd.ExcelWriter(p, engine="openpyxl") as w:
            t.to_excel(w, sheet_name="decisiones", index=False)
            ef.to_excel(w, sheet_name="eventos_oferta", index=False)
            F.to_excel(w, sheet_name="actas", index=False)
            pd.crosstab(t.anio, t.accion).to_excel(w, sheet_name="resumen")
            for h in w.book.worksheets:
                h.freeze_panes = "A2"
                for col in h.columns:
                    L = col[0].column_letter
                    h.column_dimensions[L].width = 70 if col[0].value == "parrafo" else 15
        print(f"\nGuardado: {p}")
    except PermissionError:
        print(f"\nAVISO: no pude escribir {p} (¿abierto en Excel?)")


if __name__ == "__main__":
    main()
