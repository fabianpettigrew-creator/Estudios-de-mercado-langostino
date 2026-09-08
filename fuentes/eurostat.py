"""
Cliente de Comext (Eurostat) para importaciones de camarón de la UE.

Comext no se sirve por la API SDMX estándar de Eurostat: tiene un endpoint
propio en /api/comext/dissemination. No permite bajar un dataset completo,
hay que filtrar sí o sí.

La clave SDMX del dataset DS-059322 sigue el orden:
    FREQ . REPORTER . PARTNER . PRODUCT . FLOW . INDICATORS

    FREQ       M (mensual) o A (anual)
    REPORTER   país declarante: EU27_2020, ES, IT, FR...
    PARTNER    socio: AR, EC, IN...
    PRODUCT    código CN8 sin puntos
    FLOW       1 = importación, 2 = exportación
    INDICATORS VALUE_EUR, QUANTITY_KG (ver descubrir_dimensiones)

Cualquier posición se puede dejar vacía para pedir todos los valores.
Pedimos SDMX-CSV, que trae encabezados nombrados y evita parsear XML.

NOTA: si Eurostat renombra un código de indicador, la consulta devuelve 404
o vacío. Corré descubrir_dimensiones() para ver los códigos vigentes antes de
dar por buena una serie en cero.
"""

from __future__ import annotations

import csv
import io
import logging
import time
import xml.etree.ElementTree as ET

import requests

from config import (
    EUROSTAT_DATA,
    EUROSTAT_DATAFLOW,
    EUROSTAT_DATASET,
    CN_CODIGOS_UE,
    ORIGENES_UE,
    REPORTERS_UE,
)

log = logging.getLogger(__name__)

REINTENTOS = 3
ESPERA_BASE = 3.0

# Nombres de indicador habituales. El primero que devuelva datos gana.
CANDIDATOS_VALOR = ["VALUE_EUR", "VALUE_IN_EUROS", "VALUE"]
CANDIDATOS_CANTIDAD = ["QUANTITY_KG", "QUANTITY_IN_100KG", "QUANTITY"]


def _get(url: str, params: dict) -> requests.Response:
    ultimo_error = None
    for intento in range(REINTENTOS):
        try:
            r = requests.get(url, params=params, timeout=180)
            # 404 = clave sin datos. 400 = clave inválida (p.ej. un indicador
            # candidato que este dataset no reconoce): Comext responde
            # INVALID_QUERY_DIMENSION_VALUE. En el sondeo de _detectar_indicadores
            # eso significa "probá el siguiente candidato", no un error de red.
            if r.status_code in (400, 404):
                return r
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            ultimo_error = e
            espera = ESPERA_BASE * (2 ** intento)
            log.warning("Eurostat falló (intento %d/%d): %s. Reintento en %.0fs",
                        intento + 1, REINTENTOS, e, espera)
            time.sleep(espera)
    raise RuntimeError(f"Eurostat no respondió tras {REINTENTOS} intentos") from ultimo_error


def descubrir_dimensiones() -> dict:
    """
    Consulta la definición del dataflow y devuelve el orden de dimensiones.

    Corré esto una vez al montar el sistema y cada vez que una serie venga
    vacía sin razón aparente. Evita hardcodear códigos que Eurostat cambia.
    """
    url = f"{EUROSTAT_DATAFLOW}/{EUROSTAT_DATASET}"
    r = _get(url, {"references": "all", "detail": "full"})
    if r.status_code != 200:
        log.error("No se pudo leer el dataflow (%d)", r.status_code)
        return {}

    ns = {"str": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}
    raiz = ET.fromstring(r.content)
    dims = {}
    for d in raiz.iter():
        if d.tag.endswith("}Dimension") and d.get("id"):
            dims[d.get("position") or len(dims)] = d.get("id")
    log.info("Dimensiones de %s: %s", EUROSTAT_DATASET, dims)
    return dims


def _clave(reporter: str, partner: str, producto: str,
           flujo: str, indicador: str) -> str:
    return f"M.{reporter}.{partner}.{producto}.{flujo}.{indicador}"


def _consultar(clave: str, desde: str, hasta: str | None) -> list[dict]:
    """Devuelve las filas de SDMX-CSV para una clave dada."""
    params = {"format": "SDMX-CSV", "startPeriod": desde}
    if hasta:
        params["endPeriod"] = hasta

    url = f"{EUROSTAT_DATA}/{EUROSTAT_DATASET}/{clave}"
    r = _get(url, params)
    if r.status_code in (400, 404) or not r.text.strip():
        return []
    return list(csv.DictReader(io.StringIO(r.text)))


def _detectar_indicadores(reporter: str, producto: str, desde: str) -> tuple[str, str]:
    """Prueba los nombres candidatos y devuelve los que efectivamente traen datos."""
    valor = cantidad = None
    for cand in CANDIDATOS_VALOR:
        if _consultar(_clave(reporter, "", producto, "1", cand), desde, None):
            valor = cand
            break
    for cand in CANDIDATOS_CANTIDAD:
        if _consultar(_clave(reporter, "", producto, "1", cand), desde, None):
            cantidad = cand
            break
    if not valor or not cantidad:
        raise RuntimeError(
            "No se identificaron los códigos de indicador de Comext. "
            "Corré descubrir_dimensiones() y actualizá CANDIDATOS_* en este módulo."
        )
    log.info("Eurostat: indicadores detectados -> valor=%s cantidad=%s", valor, cantidad)
    return valor, cantidad


def importaciones(desde: str, hasta: str | None = None,
                  reporters: list[str] | None = None,
                  productos: list[str] | None = None,
                  socios: list[str] | None = None) -> list[dict]:
    """
    Trae importaciones de camarón de la UE normalizadas.

    Args:
        desde, hasta: períodos "AAAA-MM". hasta=None trae hasta el último dato.
        reporters: declarantes. Por defecto los de config.
        productos: códigos CN8. Por defecto los de config.
        socios: orígenes. None = todos.

    Returns:
        Lista de dicts listos para almacen.insertar_observaciones().
    """
    reporters = reporters or REPORTERS_UE
    productos = productos or CN_CODIGOS_UE
    socios = socios if socios is not None else ORIGENES_UE

    ind_valor, ind_cant = _detectar_indicadores(reporters[0], productos[0], desde)

    # Se acumula por (reporter, socio, producto, período) porque valor y
    # cantidad vienen en consultas separadas.
    acumulado: dict[tuple, dict] = {}

    for reporter in reporters:
        for producto in productos:
            for indicador, campo in ((ind_valor, "valor_eur"), (ind_cant, "kilos")):
                filas = _consultar(
                    _clave(reporter, "", producto, "1", indicador), desde, hasta
                )
                log.info("Eurostat: %s/%s/%s -> %d filas",
                         reporter, producto, indicador, len(filas))

                for fila in filas:
                    socio = (fila.get("partner") or fila.get("PARTNER") or "").strip()
                    if socios and socio not in socios:
                        continue
                    periodo = (fila.get("TIME_PERIOD") or fila.get("time") or "").strip()
                    if "-" not in periodo:
                        continue
                    try:
                        valor = float(fila.get("OBS_VALUE") or 0)
                    except ValueError:
                        continue

                    anio, mes = periodo.split("-")[:2]
                    clave = (reporter, socio, producto, periodo)
                    reg = acumulado.setdefault(clave, {
                        "mercado": f"UE:{reporter}",
                        "flujo": "importacion",
                        "anio": int(anio),
                        "mes": int(mes),
                        "codigo": producto,
                        "descripcion": None,
                        "origen": socio,
                        "presentacion": None,
                        "talle": None,
                        "distrito": "",
                        "kilos": 0.0,
                        "valor_usd": None,
                        "valor_eur": 0.0,
                        "fuente": "Eurostat Comext",
                    })

                    # QUANTITY_IN_100KG viene en quintales: pasar a kilos.
                    if campo == "kilos" and "100KG" in indicador:
                        valor *= 100
                    reg[campo] = valor

    filas = [r for r in acumulado.values() if r["kilos"] > 0]
    log.info("Eurostat: %d observaciones normalizadas", len(filas))
    return filas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    print(descubrir_dimensiones())
    datos = importaciones("2025-01", reporters=["EU27_2020"], productos=["03061799"])
    print(f"{len(datos)} registros")
    for f in datos[:5]:
        print(f)
