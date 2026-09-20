"""Donde estan las bases que usa el estudio de langostino.

Las bases viven en la biblioteca comun BASES DE DATOS del OneDrive. Su
archivo rutas_bases.py es el mapa: dice donde esta cada fuente. Si una base
se muda, se corrige el mapa y este proyecto sigue funcionando sin tocarlo.

Uso:  from biblioteca import fuente;  fuente("desembarques_ar")
"""
import importlib
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))          # Estudios de mercado langostino
ONEDRIVE = os.path.dirname(os.path.dirname(AQUI))           # ...\OneDrive

BIBLIOTECA = [
    os.environ.get("BASES_DE_DATOS"),
    os.path.join(ONEDRIVE, "BASES DE DATOS"),
    os.path.expanduser("~/OneDrive/BASES DE DATOS"),
    "/mnt/user-data/uploads/BASES DE DATOS",
]


def _biblioteca():
    probadas = [c for c in BIBLIOTECA if c]
    for c in probadas:
        if os.path.isfile(os.path.join(c, "rutas_bases.py")):
            return c
    raise FileNotFoundError("No se encontro la biblioteca BASES DE DATOS. Probadas:\n  "
                            + "\n  ".join(probadas))


def fuente(clave, *partes):
    """Ruta de una base de la biblioteca, segun el mapa rutas_bases.py."""
    raiz = _biblioteca()
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    return importlib.import_module("rutas_bases").ruta(clave, *partes)
