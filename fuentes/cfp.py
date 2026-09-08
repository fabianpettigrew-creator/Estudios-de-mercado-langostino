# -*- coding: utf-8 -*-
"""Actas del Consejo Federal Pesquero — descarga y consulta.

Para qué. El modelo de demanda inversa del langostino identifica el efecto de
la cantidad sobre el precio con un solo episodio: el paro de 2025. El test de
permutación de `permutacion.py` muestra que con un único shock el parámetro
queda en la mediana de su propia distribución de placebos. La salida es tener
variación exógena de oferta en todos los años, y la fuente son las actas del
CFP: es el órgano que abre y cierra subáreas durante la temporada.

De dónde sale. cfp.gob.ar publica las actas por año en `actas-cfp?anio=AAAA` y
los PDF cuelgan de `/actas/`. Los nombres NO son regulares —hay variantes con
«FONAPE», «Cierre», sufijos de fecha—, así que el listado se parsea y no se
adivina. Es un sitio público del Estado; la descarga va con pausa entre pedidos
y es idempotente: lo ya bajado no se vuelve a pedir.

Qué NO cubre. Las zafras provinciales de Chubut y Santa Cruz se abren y cierran
por disposición provincial, no por acta del CFP, y no están en este sitio. El
langostino de aguas provinciales necesita esa segunda fuente.

Uso:
    python -m fuentes.cfp --bajar 2013 2026
    python -m fuentes.cfp --indice        # arma el índice de lo descargado
"""
from __future__ import annotations

import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://cfp.gob.ar"
DIR = r"C:\Users\fmpet\OneDrive\IA agentes\ACTAS CFP"
UA = "Mozilla/5.0 (compatible; AXIA/1.0; investigacion economica pesquera)"
PAUSA = 1.0          # segundos entre pedidos, para no golpear el sitio
_CTX = ssl.create_default_context()


def _traer(url: str, binario: bool = False, intentos: int = 3):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=90, context=_CTX) as r:
                d = r.read()
            return d if binario else d.decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as e:
            if i == intentos - 1:
                raise
            time.sleep(3 * (i + 1))
    raise RuntimeError("inalcanzable")


def listar(anio: int) -> list[tuple[str, str]]:
    """Devuelve [(url absoluta, nombre de archivo)] de las actas de un año."""
    h = _traer(f"{BASE}/actas-cfp?anio={anio}")
    vistos, salida = set(), []
    for href in re.findall(r'href="([^"]*?/actas/[^"]+\.pdf)"', h, re.I):
        if href in vistos:
            continue
        vistos.add(href)
        nombre = urllib.parse.unquote(href.rsplit("/", 1)[-1])
        url = href if href.startswith("http") else BASE + urllib.parse.quote(href)
        salida.append((url, nombre))
    return salida


def bajar(desde: int = 2013, hasta: int = 2026) -> None:
    os.makedirs(DIR, exist_ok=True)
    tot_ok = tot_salt = tot_err = 0
    for anio in range(desde, hasta + 1):
        try:
            actas = listar(anio)
        except Exception as e:
            print(f"{anio}: NO pude listar ({e})")
            continue
        dest = os.path.join(DIR, str(anio))
        os.makedirs(dest, exist_ok=True)
        ok = salt = err = 0
        for url, nombre in actas:
            p = os.path.join(dest, nombre)
            if os.path.exists(p) and os.path.getsize(p) > 4096:
                salt += 1
                continue
            try:
                d = _traer(url, binario=True)
                if not d.startswith(b"%PDF"):
                    err += 1
                    continue
                with open(p, "wb") as f:
                    f.write(d)
                ok += 1
                time.sleep(PAUSA)
            except Exception:
                err += 1
        tot_ok += ok; tot_salt += salt; tot_err += err
        print(f"{anio}: {len(actas):3d} actas · bajadas {ok:3d} · ya estaban "
              f"{salt:3d} · fallaron {err}")
    print(f"\nTotal: {tot_ok} bajadas, {tot_salt} ya estaban, {tot_err} fallaron")
    print(f"Destino: {DIR}")


def indice() -> None:
    """Inventario de lo descargado, por año."""
    import pandas as pd
    filas = []
    for anio in sorted(os.listdir(DIR)):
        d = os.path.join(DIR, anio)
        if not os.path.isdir(d):
            continue
        for n in sorted(os.listdir(d)):
            if n.lower().endswith(".pdf"):
                m = re.search(r"ACTA\s+CFP\s+(\d+)", n, re.I)
                filas.append({"anio": int(anio), "acta": int(m.group(1)) if m else None,
                              "archivo": n,
                              "kb": round(os.path.getsize(os.path.join(d, n)) / 1024, 1)})
    t = pd.DataFrame(filas)
    print(t.groupby("anio").agg(actas=("archivo", "size"),
                                mb=("kb", lambda x: round(x.sum() / 1024, 1))).to_string())
    print(f"\nTOTAL: {len(t)} actas · {t.kb.sum()/1024:.1f} MB")
    return t


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--bajar":
        bajar(int(a[1]) if len(a) > 1 else 2013, int(a[2]) if len(a) > 2 else 2026)
    elif a and a[0] == "--indice":
        indice()
    else:
        print(__doc__)
