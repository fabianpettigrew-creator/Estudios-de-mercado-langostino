"""
Reintento automático de la ingesta de NOAA mientras su API está en mantenimiento.

Pensado para correr cada ~30 min desde el Programador de tareas de Windows
(tarea "ReintentoNOAA_Langostino", creada aparte).

Comportamiento:
  - Si la API FOSS de NOAA sigue caída (redirige a la página de mantenimiento,
    no devuelve JSON): registra el intento y sale con código 0. La próxima
    corrida de la tarea vuelve a probar.
  - Si NOAA ya responde: corre la ingesta completa (NOAA + UE, idempotente),
    genera el reporte del último período disponible y se autoelimina del
    Programador para no seguir corriendo.

No requiere clave de API. Usa el mismo entorno que el resto del pipeline.
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

import requests

BASE = Path(__file__).parent
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "reintento_noaa.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("reintento_noaa")

from config import DB_PATH, NOAA_TRADE_URL  # noqa: E402
import almacen  # noqa: E402

TASK_NAME = "ReintentoNOAA_Langostino"


def noaa_operativa() -> bool:
    """True si la API FOSS devuelve JSON (no la página de mantenimiento)."""
    try:
        r = requests.get(NOAA_TRADE_URL, params={"limit": 1}, timeout=30)
    except Exception as e:  # noqa: BLE001
        log.warning("NOAA no respondió: %s", e)
        return False
    ct = r.headers.get("content-type", "")
    if "application/json" in ct.lower():
        return True
    log.info("NOAA sigue en mantenimiento (content-type=%s, url final=%s)", ct, r.url)
    return False


def main() -> int:
    if not noaa_operativa():
        return 0

    log.info("NOAA operativa. Corriendo ingesta completa (NOAA + UE)...")
    ingesta = subprocess.run(
        [sys.executable, str(BASE / "ingesta.py"), "--desde", "2024"],
        cwd=str(BASE),
    )
    if ingesta.returncode != 0:
        log.error("La ingesta terminó con código %s. No autoelimino la tarea; "
                  "reintentará en la próxima corrida.", ingesta.returncode)
        return ingesta.returncode

    ultimo = almacen.ultimo_periodo(ruta=DB_PATH)
    if ultimo:
        anio, mes = ultimo
        log.info("Generando reporte de %04d-%02d...", anio, mes)
        subprocess.run(
            [sys.executable, str(BASE / "reporte.py"), str(anio), str(mes)],
            cwd=str(BASE),
        )
    else:
        log.warning("La base quedó sin período; no genero reporte.")

    log.info("NOAA ingerida. Autoeliminando la tarea programada '%s'.", TASK_NAME)
    subprocess.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
