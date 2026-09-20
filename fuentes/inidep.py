# -*- coding: utf-8 -*-
"""Campañas de evaluación de biomasa de langostino del INIDEP.

Para qué. El modelo necesita un desplazador de oferta que no dependa del precio.
Las actas del CFP dan el calendario regulatorio; el índice de biomasa
pre-temporada da la otra mitad: cuánto recurso hay antes de que se decida
cuánto pescar. Es la variable que la literatura usa como instrumento natural en
pesquerías, y el INIDEP la estima campaña por campaña.

De dónde sale. El repositorio institucional del INIDEP («Mar Abierto») corre
sobre DSpace 7. La interfaz pública está en marabierto.inidep.edu.ar pero la API
responde en marabiertonew.inidep.edu.ar/server/api — la primera devuelve 404
sobre /server/api, cosa que hay que saber o se pierde media hora.

Dos campañas por año, y la distinción importa: la número 01 es la de otoño,
previa a la apertura de aguas nacionales, y es la que sirve como índice
PRE-TEMPORADA. La 02 es primaveral y llega cuando la temporada ya corrió.

Uso:
    python -m fuentes.inidep --listar          inventario de campañas
    python -m fuentes.inidep --bajar           descarga los PDF
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

API = "https://marabiertonew.inidep.edu.ar/server/api"
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR = fuente("inidep_langostino")
UA = "Mozilla/5.0 (compatible; AXIA/1.0; investigacion economica pesquera)"
PAUSA = 1.0
_CTX = ssl.create_default_context()

# Códigos de campaña, en cuatro redacciones vistas en el repositorio:
#   BS-01/2020 · BS 2023/02 · EH-01/16 · OB01/14
# El año va en cuatro dígitos o en dos, y el número de campaña puede ir antes o
# después. Aceptar sólo el año de cuatro dígitos —como hacía la primera versión—
# hacía desaparecer 2014, 2015 y 2016 sin error alguno: la campaña existía y el
# parser la ignoraba en silencio.
RE_CAMP_AA = re.compile(r"\b([A-Z]{2})[\s-]?(\d{4})/(\d{1,2})\b")    # BS 2023/02
RE_CAMP_NN = re.compile(r"\b([A-Z]{2})[\s-]?(\d{1,2})/(\d{2,4})\b")  # BS-01/2020


def _anio4(a: int) -> int:
    """Año de dos dígitos a cuatro. La serie del langostino no llega a 1990."""
    return a if a >= 1000 else (2000 + a if a <= 60 else 1900 + a)


def _get(url: str, binario: bool = False, intentos: int = 3):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=90, context=_CTX) as r:
                d = r.read()
            return d if binario else d.decode("utf-8", "replace")
        except Exception:
            if i == intentos - 1:
                raise
            time.sleep(3 * (i + 1))


def _campania(titulo: str):
    """Devuelve (barco, numero, anio) de la campaña, o (None, None, None)."""
    t = titulo.upper()
    m = RE_CAMP_AA.search(t)            # año primero: BS 2023/02
    if m and 2000 <= int(m.group(2)) <= 2100:
        return m.group(1), int(m.group(3)), int(m.group(2))
    m = RE_CAMP_NN.search(t)            # número primero: BS-01/2020, EH-01/16
    if m:
        return m.group(1), int(m.group(2)), _anio4(int(m.group(3)))
    return None, None, None


def buscar(consulta: str = "langostino biomasa") -> list[dict]:
    """Todos los ítems que responden a la consulta, paginando."""
    salida, pag = [], 0
    while True:
        u = (f"{API}/discover/search/objects?query="
             f"{urllib.parse.quote(consulta)}&size=50&page={pag}&dsoType=item")
        d = json.loads(_get(u))
        sr = d["_embedded"]["searchResult"]
        objs = sr["_embedded"]["objects"]
        for o in objs:
            it = o["_embedded"]["indexableObject"]
            md = it.get("metadata", {})

            def _m(k):
                v = md.get(k)
                return v[0]["value"] if v else ""

            tit = _m("dc.title")
            barco, nro, anio = _campania(tit)
            salida.append({
                "id": it["uuid"], "titulo": tit,
                "fecha": _m("dc.date.issued"),
                "barco": barco, "campania_n": nro, "campania_anio": anio,
                "tipo": _m("dc.type"),
            })
        tot = sr["page"]["totalPages"]
        pag += 1
        if pag >= tot:
            break
        time.sleep(0.4)
    return salida


def pdf_de(item_id: str) -> str | None:
    """URL del primer PDF del ítem."""
    try:
        d = json.loads(_get(f"{API}/core/items/{item_id}/bundles"))
    except Exception:
        return None
    for b in d.get("_embedded", {}).get("bundles", []):
        if b.get("name") != "ORIGINAL":
            continue
        href = b["_links"]["bitstreams"]["href"]
        try:
            bs = json.loads(_get(href))
        except Exception:
            return None
        for x in bs.get("_embedded", {}).get("bitstreams", []):
            if x.get("name", "").lower().endswith(".pdf") or \
                    "pdf" in str(x.get("metadata", {})).lower():
                return x["_links"]["content"]["href"]
    return None


def listar() -> None:
    import pandas as pd
    r = pd.DataFrame(buscar())
    print(f"Ítems que responden a «langostino biomasa»: {len(r)}")
    c = r.dropna(subset=["campania_anio"]).copy()
    c["campania_anio"] = c.campania_anio.astype(int)
    c["campania_n"] = c.campania_n.astype(int)
    print(f"Con campaña identificable en el título: {len(c)}")
    print("\nCampañas por año y número (01 = pre-temporada, 02 = primaveral):")
    print(pd.crosstab(c.campania_anio, c.campania_n).to_string())
    print("\nDetalle:")
    print(c.sort_values(["campania_anio", "campania_n"])
          [["campania_anio", "campania_n", "barco", "fecha", "titulo"]]
          .to_string(index=False, max_colwidth=78))
    os.makedirs(DIR, exist_ok=True)
    r.to_csv(os.path.join(DIR, "inventario_campanias.csv"), index=False,
             encoding="utf-8-sig")
    print(f"\nGuardado: {os.path.join(DIR, 'inventario_campanias.csv')}")
    return r


def bajar() -> None:
    import pandas as pd
    os.makedirs(DIR, exist_ok=True)
    r = pd.DataFrame(buscar())
    c = r.dropna(subset=["campania_anio"])
    ok = err = salt = 0
    for _, x in c.iterrows():
        nom = (f"{int(x.campania_anio)}_{int(x.campania_n):02d}_{x.barco}_"
               f"{re.sub(r'[^A-Za-z0-9]+', '-', x.titulo)[:70]}.pdf")
        p = os.path.join(DIR, nom)
        if os.path.exists(p) and os.path.getsize(p) > 4096:
            salt += 1
            continue
        u = pdf_de(x.id)
        if not u:
            err += 1
            continue
        try:
            d = _get(u, binario=True)
            if not d.startswith(b"%PDF"):
                err += 1
                continue
            open(p, "wb").write(d)
            ok += 1
            time.sleep(PAUSA)
        except Exception:
            err += 1
    print(f"Bajados {ok} · ya estaban {salt} · fallaron {err}")
    print(f"Destino: {DIR}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--bajar":
        bajar()
    elif a and a[0] == "--listar":
        listar()
    else:
        print(__doc__)
