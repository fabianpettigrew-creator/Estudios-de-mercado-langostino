"""
Ingesta mensual. Esto es lo que va en el cron.

    0 6 5 * *  cd /ruta/langostino_agente && python ingesta.py

Corre el día 5 de cada mes: NOAA publica con unos 43 días de retraso, así que
en cualquier fecha del mes vas a estar trayendo el mes anterior al anterior.
La ingesta es idempotente, así que correr de más no rompe nada: reescribe los
valores con los revisados.
"""

from __future__ import annotations

import argparse
import logging
from datetime import date

import almacen
from config import DB_PATH
from fuentes import eurostat, noaa

log = logging.getLogger(__name__)


def actualizar(desde_anio: int, hasta_anio: int, saltear_ue: bool = False) -> dict:
    """Trae ambas fuentes y las deja en la base. Devuelve el conteo por fuente."""
    almacen.inicializar(DB_PATH)
    resultado = {}

    # ---- Estados Unidos ----
    try:
        filas = noaa.importaciones(desde_anio, hasta_anio)
        n = almacen.insertar_observaciones(filas, DB_PATH)
        almacen.registrar_carga("NOAA FOSS", str(desde_anio), str(hasta_anio), n, DB_PATH)
        resultado["EEUU"] = n
    except Exception as e:
        log.error("Falló la ingesta de NOAA: %s", e)
        resultado["EEUU"] = f"error: {e}"

    # ---- Unión Europea ----
    if not saltear_ue:
        try:
            desde = f"{desde_anio}-01"
            filas = eurostat.importaciones(desde)
            n = almacen.insertar_observaciones(filas, DB_PATH)
            almacen.registrar_carga("Eurostat Comext", desde, str(hasta_anio), n, DB_PATH)
            resultado["UE"] = n
        except Exception as e:
            log.error("Falló la ingesta de Eurostat: %s", e)
            resultado["UE"] = f"error: {e}"

    ultimo = almacen.ultimo_periodo(ruta=DB_PATH)
    resultado["ultimo_periodo"] = f"{ultimo[0]}-{ultimo[1]:02d}" if ultimo else None
    return resultado


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    hoy = date.today()
    p = argparse.ArgumentParser(description="Actualiza las series de mercado")
    p.add_argument("--desde", type=int, default=hoy.year - 3,
                   help="año inicial (por defecto, 3 años atrás)")
    p.add_argument("--hasta", type=int, default=hoy.year)
    p.add_argument("--sin-ue", action="store_true",
                   help="saltear Eurostat (útil para probar solo NOAA)")
    args = p.parse_args()

    for clave, valor in actualizar(args.desde, args.hasta, args.sin_ue).items():
        print(f"{clave}: {valor}")
