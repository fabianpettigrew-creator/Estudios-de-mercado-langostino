"""
Configuración central del sistema de estudios de mercado de langostino.

Todo lo que puede cambiar sin tocar la lógica vive acá: códigos arancelarios,
países de interés, endpoints y parámetros del modelo.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Rutas
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "datos" / "mercado.db"
SALIDAS_DIR = BASE_DIR / "salidas"
INFORMES_DIR = BASE_DIR / "informes"

# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------
# FOSS migró a la nube (jul-2026): el host st.nmfs.noaa.gov/ords fue reemplazado
# por apps-st.fisheries.noaa.gov/ods (context root "ods", no "ords"). Misma API
# ORDS, mismos campos. El viejo host redirige a una página de mantenimiento.
NOAA_TRADE_URL = "https://apps-st.fisheries.noaa.gov/ods/foss/trade_data/"
NOAA_METADATA_URL = "https://apps-st.fisheries.noaa.gov/ods/foss/metadata-catalog/trade_data/"

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/comext/dissemination"
EUROSTAT_DATAFLOW = f"{EUROSTAT_BASE}/sdmx/2.1/dataflow/ESTAT"
EUROSTAT_DATA = f"{EUROSTAT_BASE}/sdmx/2.1/data"

# Dataset Comext. DS-045409 ("EU trade since 1988 by HS2-4-6 and CN8") es el
# que hoy trae el detalle CN8, imprescindible para abrir por especie.
# El anterior DS-059322 fue retirado del servicio de diseminación (jul-2026):
# devolvía 404 en todas las consultas. Indicadores vigentes en DS-045409:
# VALUE_IN_EUROS y QUANTITY_IN_100KG (ya contemplados en CANDIDATOS_* de eurostat.py).
EUROSTAT_DATASET = "DS-045409"

# --------------------------------------------------------------------------
# Códigos arancelarios
# --------------------------------------------------------------------------
# Estados Unidos: HTS a 10 dígitos. FOSS los devuelve completos, así que
# filtramos por prefijo. 0306.17 = camarones congelados (excepto agua fría).
HTS_PREFIJOS_EEUU = ["030617"]

# Unión Europea: Nomenclatura Combinada a 8 dígitos.
#   03061791  Parapenaeus longirostris (gamba blanca)
#   03061792  género Penaeus (incluye vannamei de cultivo)
#   03061793  familia Pandalidae, excepto género Pandalus
#   03061794  género Crangon, excepto Crangon crangon
#   03061799  los demás  <-- acá cae el langostino argentino (Pleoticus muelleri)
#
# VERIFICADO (2026-08-01) contra los datos de Comext: de las importaciones
# argentinas a UE-27 en 2024-2026, el 99,9% (156.687 t) cae en 03061799 y solo
# 172 t (0,1%) en 03061792. No hay clasificación cruzada relevante; el filtro
# queda como está. Re-verificar si algún mes el peso de AR en 03061792 sube.
# (Pleoticus muelleri no es Penaeus; el riesgo era que algún despachante lo
#  clasificara mal, pero los datos muestran que no ocurre a escala material.)
CN_CODIGOS_UE = ["03061791", "03061792", "03061793", "03061794", "03061799"]
CN_LANGOSTINO_ARG = "03061799"

# --------------------------------------------------------------------------
# Orígenes de interés
# --------------------------------------------------------------------------
# Nombres tal como los devuelve FOSS (campo cntry_name, en mayúsculas).
ORIGENES_EEUU = [
    "ARGENTINA", "ECUADOR", "INDIA", "INDONESIA", "VIETNAM",
    "THAILAND", "MEXICO", "PERU", "CHINA",
]

# Códigos de socio Comext (ISO-2 en el dataset nuevo).
ORIGENES_UE = ["AR", "EC", "IN", "ID", "VN", "TH", "CN", "GL"]

# Reporters Comext. EU27_2020 es el agregado; agregá países sueltos
# (ES, IT, FR) si querés abrir por mercado nacional.
REPORTERS_UE = ["EU27_2020", "ES", "IT", "FR"]

# --------------------------------------------------------------------------
# Nombres completos de país
# --------------------------------------------------------------------------
# Mapea el identificador de origen tal como queda en la base (ISO-2 para la UE,
# nombre en inglés y mayúsculas para NOAA) a un nombre completo legible. Se usa
# en las salidas Excel; la base sigue guardando el código/nombre crudo.
PAISES = {
    # ISO-2 Comext
    "AR": "Argentina", "EC": "Ecuador", "IN": "India", "ID": "Indonesia",
    "VN": "Vietnam", "TH": "Tailandia", "CN": "China", "GL": "Groenlandia",
    "MX": "México", "PE": "Perú",
    # Nombres NOAA (cntry_name en mayúsculas)
    "ARGENTINA": "Argentina", "ECUADOR": "Ecuador", "INDIA": "India",
    "INDONESIA": "Indonesia", "VIETNAM": "Vietnam", "THAILAND": "Tailandia",
    "MEXICO": "México", "PERU": "Perú", "CHINA": "China",
}


def nombre_pais(origen: str) -> str:
    """Nombre completo de país a partir del origen crudo. Si no está en el mapa,
    devuelve el original con capitalización de título (no se pierde nada)."""
    if not origen:
        return ""
    return PAISES.get(origen, PAISES.get(origen.upper(), origen.title()))

# --------------------------------------------------------------------------
# Agente
# --------------------------------------------------------------------------
MODELO = "claude-sonnet-4-6"
MAX_ITERACIONES = 25
MAX_TOKENS = 4000

# Umbral en desvíos estándar para marcar un mes como anómalo.
UMBRAL_ANOMALIA = 2.0

# Cuántos meses de historia mira el agente por defecto.
VENTANA_MESES = 36
