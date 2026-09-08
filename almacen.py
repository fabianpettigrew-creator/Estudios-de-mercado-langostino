"""
Almacén de series mensuales en SQLite.

Una sola tabla de observaciones al máximo detalle disponible. Todo lo demás
(agregados, precios implícitos, variaciones) se calcula por consulta, así no
hay tablas derivadas que se desincronicen.

El precio implícito es valor / kilos. No se guarda: se calcula al vuelo, para
que agregar correctamente sea imposible de hacer mal — el promedio de precios
unitarios no es el precio unitario del agregado.
"""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from config import DB_PATH

log = logging.getLogger(__name__)

ESQUEMA = """
CREATE TABLE IF NOT EXISTS observaciones (
    id            INTEGER PRIMARY KEY,
    mercado       TEXT    NOT NULL,   -- EEUU, UE:ES, UE:EU27_2020...
    flujo         TEXT    NOT NULL,   -- importacion / exportacion
    anio          INTEGER NOT NULL,
    mes           INTEGER NOT NULL,
    codigo        TEXT    NOT NULL,   -- HTS10 o CN8
    descripcion   TEXT,
    origen        TEXT    NOT NULL,
    -- Estas dos van con '' en vez de NULL a propósito: SQLite trata cada NULL
    -- como distinto de los demás, así que una constraint UNIQUE que incluya
    -- columnas nulas nunca dispara y la ingesta duplicaría en cada corrida.
    presentacion  TEXT    NOT NULL DEFAULT '',
    talle         TEXT    NOT NULL DEFAULT '',
    -- Distrito aduanero de entrada (solo EE.UU./NOAA; '' en la UE). Va en la
    -- clave UNIQUE: sin él, las varias filas por distrito de un mismo mes/HTS/país
    -- colisionaban y la ingesta pisaba en vez de sumar, perdiendo hasta ~80% del
    -- volumen. Preservarlo arregla el conteo y agrega el máximo detalle disponible.
    distrito      TEXT    NOT NULL DEFAULT '',
    kilos         REAL    NOT NULL,
    valor_usd     REAL,
    valor_eur     REAL,
    fuente        TEXT    NOT NULL,
    cargado_en    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (mercado, flujo, anio, mes, codigo, origen, presentacion, talle, distrito)
);

CREATE INDEX IF NOT EXISTS ix_obs_periodo ON observaciones (anio, mes);
CREATE INDEX IF NOT EXISTS ix_obs_origen  ON observaciones (origen, mercado);
CREATE INDEX IF NOT EXISTS ix_obs_codigo  ON observaciones (codigo);

-- Registro de qué se descargó y cuándo. Sirve para saber si un mes ya cerró
-- o si todavía puede venir revisado.
CREATE TABLE IF NOT EXISTS cargas (
    id          INTEGER PRIMARY KEY,
    fuente      TEXT NOT NULL,
    desde       TEXT NOT NULL,
    hasta       TEXT NOT NULL,
    filas       INTEGER NOT NULL,
    ejecutado   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Informes anteriores, para que el agente compare contra lo que ya dijo.
CREATE TABLE IF NOT EXISTS informes (
    id          INTEGER PRIMARY KEY,
    anio        INTEGER NOT NULL,
    mes         INTEGER NOT NULL,
    texto       TEXT    NOT NULL,
    generado    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (anio, mes)
);
"""


@contextmanager
def conexion(ruta: Path | str = DB_PATH):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(ruta)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def inicializar(ruta: Path | str = DB_PATH) -> None:
    with conexion(ruta) as con:
        con.executescript(ESQUEMA)
    log.info("Base inicializada en %s", ruta)


def insertar_observaciones(filas: list[dict], ruta: Path | str = DB_PATH) -> int:
    """
    Inserta o actualiza observaciones. Idempotente: volver a correr la ingesta
    del mismo mes pisa los valores viejos con los revisados en vez de duplicar.
    """
    if not filas:
        return 0

    sql = """
    INSERT INTO observaciones
        (mercado, flujo, anio, mes, codigo, descripcion, origen,
         presentacion, talle, distrito, kilos, valor_usd, valor_eur, fuente)
    VALUES
        (:mercado, :flujo, :anio, :mes, :codigo, :descripcion, :origen,
         COALESCE(:presentacion, ''), COALESCE(:talle, ''), COALESCE(:distrito, ''),
         :kilos, :valor_usd, :valor_eur, :fuente)
    ON CONFLICT (mercado, flujo, anio, mes, codigo, origen, presentacion, talle, distrito)
    DO UPDATE SET
        kilos      = excluded.kilos,
        valor_usd  = excluded.valor_usd,
        valor_eur  = excluded.valor_eur,
        cargado_en = datetime('now');
    """
    with conexion(ruta) as con:
        con.executemany(sql, filas)
    log.info("%d observaciones guardadas", len(filas))
    return len(filas)


def registrar_carga(fuente: str, desde: str, hasta: str, filas: int,
                    ruta: Path | str = DB_PATH) -> None:
    with conexion(ruta) as con:
        con.execute(
            "INSERT INTO cargas (fuente, desde, hasta, filas) VALUES (?,?,?,?)",
            (fuente, desde, hasta, filas),
        )


def guardar_informe(anio: int, mes: int, texto: str,
                    ruta: Path | str = DB_PATH) -> None:
    with conexion(ruta) as con:
        con.execute(
            """INSERT INTO informes (anio, mes, texto) VALUES (?,?,?)
               ON CONFLICT (anio, mes) DO UPDATE SET
                 texto = excluded.texto, generado = datetime('now')""",
            (anio, mes, texto),
        )


def informe_anterior(anio: int, mes: int,
                     ruta: Path | str = DB_PATH) -> str | None:
    """Devuelve el informe del mes previo, si existe."""
    mes_ant, anio_ant = (12, anio - 1) if mes == 1 else (mes - 1, anio)
    with conexion(ruta) as con:
        fila = con.execute(
            "SELECT texto FROM informes WHERE anio = ? AND mes = ?",
            (anio_ant, mes_ant),
        ).fetchone()
    return fila["texto"] if fila else None


def ultimo_periodo(mercado: str | None = None,
                   ruta: Path | str = DB_PATH) -> tuple[int, int] | None:
    """Último (año, mes) con datos. Sirve para saber desde dónde actualizar."""
    sql = "SELECT anio, mes FROM observaciones"
    params: tuple = ()
    if mercado:
        sql += " WHERE mercado = ?"
        params = (mercado,)
    sql += " ORDER BY anio DESC, mes DESC LIMIT 1"

    with conexion(ruta) as con:
        fila = con.execute(sql, params).fetchone()
    return (fila["anio"], fila["mes"]) if fila else None
