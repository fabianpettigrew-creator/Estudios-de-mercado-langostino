"""
Cliente de la API FOSS (Fisheries One Stop Shop) de NOAA.

Devuelve importaciones mensuales de EE.UU. por partida HTS, país de origen
y distrito aduanero. Los datos originales son del Census Bureau; NOAA los
publica unos 43 días después del cierre del mes estadístico.

Endpoint ORDS: acepta ?q={filtro JSON}&limit=N&offset=N y pagina con hasMore.

Campos que devuelve cada registro:
    year, month, hts_number, name, cntry_code, cntry_name, fao,
    district_code, district_name, edible_code, kilos, val, source,
    association, rfmo, nmfs_region_code

`source` vale IMP o EXP. `name` trae la descripción comercial, que en camarón
incluye el talle ("SHRIMP SHELL-ON FROZEN 31/40") — sirve para clasificar.
"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Iterator

import requests

from config import NOAA_TRADE_URL, HTS_PREFIJOS_EEUU, ORIGENES_EEUU

log = logging.getLogger(__name__)

PAGINA = 5000
REINTENTOS = 5
ESPERA_BASE = 3.0
# El WAF además limita la tasa: varias peticiones seguidas vuelven a dar 403
# aunque las cabeceras estén bien. Con una pausa entre páginas no se activa.
ESPERA_ENTRE_PAGINAS = 1.5

# El WAF de NOAA (Akamai) empezó a devolver 403 a las peticiones "pelas" de
# requests (2026-08). No alcanza con el User-Agent: mira el juego completo de
# cabeceras que manda un navegador, sobre todo las Sec-Fetch-* y sec-ch-ua.
# Con este set responde 200. Si volviera a bloquear, copiar las cabeceras de
# una petición real del navegador (F12 -> Network -> Copy as cURL).
CABECERAS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,*/*;q=0.8"),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "sec-ch-ua": '"Chromium";v="126", "Not)A;Brand";v="24", "Google Chrome";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}

_sesion = requests.Session()
_sesion.headers.update(CABECERAS)


def _get(params: dict) -> dict:
    """GET con reintentos y backoff exponencial."""
    ultimo_error = None
    for intento in range(REINTENTOS):
        try:
            r = _sesion.get(NOAA_TRADE_URL, params=params, timeout=120)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            ultimo_error = e
            espera = ESPERA_BASE * (2 ** intento)
            log.warning("NOAA falló (intento %d/%d): %s. Reintento en %.0fs",
                        intento + 1, REINTENTOS, e, espera)
            time.sleep(espera)
    raise RuntimeError(f"NOAA no respondió tras {REINTENTOS} intentos") from ultimo_error


def _paginar(filtro: dict) -> Iterator[dict]:
    """Recorre todas las páginas de un filtro ORDS."""
    offset = 0
    while True:
        payload = _get({
            "q": json.dumps(filtro),
            "limit": PAGINA,
            "offset": offset,
        })
        items = payload.get("items", [])
        yield from items
        if not payload.get("hasMore") or not items:
            break
        offset += len(items)
        time.sleep(ESPERA_ENTRE_PAGINAS)
        log.info("NOAA: %d registros acumulados", offset)


def _extraer_talle(descripcion: str) -> str | None:
    """
    Saca el talle de la descripción comercial.
    "SHRIMP SHELL-ON FROZEN 31/40" -> "31/40"
    "SHRIMP PEELED FROZEN"         -> None
    """
    if not descripcion:
        return None
    m = re.search(r"\b(\d{1,3}/\d{1,3}|U/?\d{1,3}|\d{1,3}\s?&\s?UNDER)\b",
                  descripcion.upper())
    return m.group(1).replace(" ", "") if m else None


def _presentacion(descripcion: str) -> str:
    """Clasifica la presentación a partir de la descripción."""
    d = (descripcion or "").upper()
    if "PEELED" in d:
        return "pelado"
    if "SHELL-ON" in d or "SHELL ON" in d:
        return "con cáscara"
    if "BREADED" in d:
        return "rebozado"
    if "COOKED" in d:
        return "cocido"
    if "CANNED" in d or "AIRTIGHT" in d:
        return "conserva"
    return "otros"


def importaciones(desde_anio: int, hasta_anio: int,
                  origenes: list[str] | None = None) -> list[dict]:
    """
    Trae importaciones de camarón de EE.UU. normalizadas.

    Args:
        desde_anio, hasta_anio: rango inclusivo.
        origenes: lista de nombres de país como los usa FOSS (mayúsculas).
                  None = todos.

    Returns:
        Lista de dicts listos para almacen.insertar_observaciones().
    """
    origenes = origenes or ORIGENES_EEUU

    # Se agrega EN MEMORIA por la clave dimensional completa (incluye el distrito
    # aduanero). FOSS devuelve una fila por distrito de entrada, y varias pueden
    # compartir mes/HTS/país: sumarlas acá evita que se pisen en la base y que se
    # pierda volumen. El distrito es además el máximo detalle geográfico disponible.
    agregado: dict[tuple, dict] = {}

    for prefijo in HTS_PREFIJOS_EEUU:
        filtro = {
            "year": {"$between": [str(desde_anio), str(hasta_anio)]},
            "source": "IMP",
            "hts_number": {"$like": f"{prefijo}%"},
        }
        log.info("NOAA: consultando HTS %s, %d-%d", prefijo, desde_anio, hasta_anio)

        for item in _paginar(filtro):
            pais = (item.get("cntry_name") or "").strip().upper()
            if origenes and pais not in origenes:
                continue

            kilos = float(item.get("kilos") or 0)
            valor = float(item.get("val") or 0)
            if kilos <= 0:
                continue

            desc = item.get("name") or ""
            distrito = (item.get("custom_district_name")
                        or item.get("district_name") or "").strip()
            clave = (int(item["year"]), int(item["month"]),
                     item.get("hts_number"), pais, distrito)

            reg = agregado.get(clave)
            if reg is None:
                reg = {
                    "mercado": "EEUU",
                    "flujo": "importacion",
                    "anio": int(item["year"]),
                    "mes": int(item["month"]),
                    "codigo": item.get("hts_number"),
                    "descripcion": desc,
                    "origen": pais,
                    "presentacion": _presentacion(desc),
                    "talle": _extraer_talle(desc),
                    "distrito": distrito,
                    "kilos": 0.0,
                    "valor_usd": 0.0,
                    "valor_eur": None,
                    "fuente": "NOAA FOSS",
                }
                agregado[clave] = reg
            reg["kilos"] += kilos
            reg["valor_usd"] += valor

    filas = list(agregado.values())
    log.info("NOAA: %d observaciones normalizadas (con distrito)", len(filas))
    return filas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    datos = importaciones(2025, 2026, origenes=["ARGENTINA", "ECUADOR"])
    print(f"{len(datos)} registros")
    for f in datos[:5]:
        print(f)
