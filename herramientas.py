"""
Herramientas del agente.

Regla de oro: el modelo no calcula ni recuerda cifras. Toda cifra que aparezca
en el informe sale de una de estas funciones, que leen la base. Si el modelo
quiere un número que ninguna herramienta devuelve, la respuesta correcta es
que no lo tiene, no que lo estime.

Cada función tiene su esquema JSON en ESQUEMAS, que es lo que se le pasa a la
API en el parámetro `tools`.
"""

from __future__ import annotations

import logging
import statistics
from pathlib import Path

from almacen import conexion, informe_anterior
from config import DB_PATH, UMBRAL_ANOMALIA, VENTANA_MESES

log = logging.getLogger(__name__)


def _moneda(mercado: str) -> str:
    return "valor_eur" if mercado.startswith("UE") else "valor_usd"


def _filtros(mercado: str | None, origen: str | None,
             codigo: str | None) -> tuple[str, list]:
    cond, params = ["1=1"], []
    if mercado:
        cond.append("mercado = ?")
        params.append(mercado)
    if origen:
        cond.append("origen = ?")
        params.append(origen.upper())
    if codigo:
        cond.append("codigo LIKE ?")
        params.append(f"{codigo}%")
    return " AND ".join(cond), params


# --------------------------------------------------------------------------
# Herramientas
# --------------------------------------------------------------------------

def consultar_serie(mercado: str, origen: str | None = None,
                    codigo: str | None = None, meses: int = VENTANA_MESES,
                    ruta: Path | str = DB_PATH) -> dict:
    """
    Serie mensual de volumen, valor y precio implícito.

    El precio se calcula como suma de valor sobre suma de kilos del agregado,
    nunca como promedio de precios unitarios.
    """
    campo = _moneda(mercado)
    where, params = _filtros(mercado, origen, codigo)

    sql = f"""
        SELECT anio, mes,
               SUM(kilos)      AS kilos,
               SUM({campo})    AS valor
        FROM observaciones
        WHERE {where} AND {campo} IS NOT NULL
        GROUP BY anio, mes
        ORDER BY anio DESC, mes DESC
        LIMIT ?
    """
    with conexion(ruta) as con:
        filas = con.execute(sql, [*params, meses]).fetchall()

    serie = []
    for f in reversed(filas):
        kilos, valor = f["kilos"] or 0, f["valor"] or 0
        serie.append({
            "periodo": f"{f['anio']}-{f['mes']:02d}",
            "toneladas": round(kilos / 1000, 1),
            "valor_miles": round(valor / 1000, 1),
            "precio_por_kg": round(valor / kilos, 2) if kilos else None,
        })

    return {
        "mercado": mercado,
        "origen": origen or "todos",
        "codigo": codigo or "todos",
        "moneda": "EUR" if campo == "valor_eur" else "USD",
        "observaciones": len(serie),
        "serie": serie,
    }


def comparar_origenes(mercado: str, anio: int, mes: int,
                      codigo: str | None = None,
                      ruta: Path | str = DB_PATH) -> dict:
    """
    Ranking de orígenes en un mes, con variación interanual por origen.
    """
    campo = _moneda(mercado)
    where, params = _filtros(mercado, None, codigo)

    sql = f"""
        SELECT origen,
               SUM(kilos)   AS kilos,
               SUM({campo}) AS valor
        FROM observaciones
        WHERE {where} AND anio = ? AND mes = ? AND {campo} IS NOT NULL
        GROUP BY origen
        ORDER BY kilos DESC
    """
    with conexion(ruta) as con:
        actual = con.execute(sql, [*params, anio, mes]).fetchall()
        previo = {
            f["origen"]: (f["kilos"], f["valor"])
            for f in con.execute(sql, [*params, anio - 1, mes]).fetchall()
        }

    total = sum(f["kilos"] or 0 for f in actual) or 1
    ranking = []
    for f in actual:
        kilos, valor = f["kilos"] or 0, f["valor"] or 0
        k_ant, v_ant = previo.get(f["origen"], (0, 0))
        precio = valor / kilos if kilos else None
        precio_ant = v_ant / k_ant if k_ant else None
        ranking.append({
            "origen": f["origen"],
            "toneladas": round(kilos / 1000, 1),
            "cuota_pct": round(100 * kilos / total, 1),
            "precio_por_kg": round(precio, 2) if precio else None,
            "var_volumen_ia_pct": round(100 * (kilos - k_ant) / k_ant, 1) if k_ant else None,
            "var_precio_ia_pct": (
                round(100 * (precio - precio_ant) / precio_ant, 1)
                if precio and precio_ant else None
            ),
        })

    return {
        "mercado": mercado,
        "periodo": f"{anio}-{mes:02d}",
        "codigo": codigo or "todos",
        "moneda": "EUR" if campo == "valor_eur" else "USD",
        "total_toneladas": round(total / 1000, 1),
        "ranking": ranking,
    }


def detectar_anomalias(mercado: str, origen: str | None = None,
                       codigo: str | None = None,
                       variable: str = "precio_por_kg",
                       umbral: float = UMBRAL_ANOMALIA,
                       ruta: Path | str = DB_PATH) -> dict:
    """
    Marca meses que se apartan de la media histórica más de `umbral` desvíos.

    Trabaja sobre la variación mensual, no sobre el nivel: una serie con
    tendencia da falsos positivos si se mira el nivel crudo.
    """
    serie = consultar_serie(mercado, origen, codigo, meses=120, ruta=ruta)["serie"]
    valores = [(p["periodo"], p[variable]) for p in serie if p.get(variable)]

    if len(valores) < 12:
        return {"error": "serie demasiado corta para evaluar anomalías",
                "observaciones": len(valores)}

    variaciones = [
        (valores[i][0], 100 * (valores[i][1] - valores[i - 1][1]) / valores[i - 1][1])
        for i in range(1, len(valores)) if valores[i - 1][1]
    ]
    solo_var = [v for _, v in variaciones]
    media = statistics.mean(solo_var)
    desvio = statistics.pstdev(solo_var) or 1e-9

    anomalias = [
        {"periodo": p, "variacion_pct": round(v, 1),
         "desvios": round((v - media) / desvio, 2)}
        for p, v in variaciones if abs((v - media) / desvio) >= umbral
    ]

    return {
        "mercado": mercado,
        "origen": origen or "todos",
        "variable": variable,
        "variacion_media_pct": round(media, 2),
        "desvio_estandar_pct": round(desvio, 2),
        "umbral_desvios": umbral,
        "anomalias": anomalias[-12:],
    }


def resumen_periodo(anio: int, mes: int, ruta: Path | str = DB_PATH) -> dict:
    """Foto del mes en todos los mercados cargados, con comparación interanual."""
    with conexion(ruta) as con:
        mercados = [f["mercado"] for f in con.execute(
            "SELECT DISTINCT mercado FROM observaciones ORDER BY mercado"
        ).fetchall()]

    resumen = []
    for m in mercados:
        campo = _moneda(m)
        with conexion(ruta) as con:
            fila = con.execute(
                f"""SELECT SUM(kilos) k, SUM({campo}) v FROM observaciones
                    WHERE mercado = ? AND anio = ? AND mes = ?""",
                (m, anio, mes),
            ).fetchone()
            ant = con.execute(
                f"""SELECT SUM(kilos) k, SUM({campo}) v FROM observaciones
                    WHERE mercado = ? AND anio = ? AND mes = ?""",
                (m, anio - 1, mes),
            ).fetchone()

        k, v = fila["k"] or 0, fila["v"] or 0
        k_ant, v_ant = ant["k"] or 0, ant["v"] or 0
        if not k:
            continue
        resumen.append({
            "mercado": m,
            "moneda": "EUR" if campo == "valor_eur" else "USD",
            "toneladas": round(k / 1000, 1),
            "precio_por_kg": round(v / k, 2),
            "var_volumen_ia_pct": round(100 * (k - k_ant) / k_ant, 1) if k_ant else None,
            "var_precio_ia_pct": (
                round(100 * ((v / k) - (v_ant / k_ant)) / (v_ant / k_ant), 1)
                if k_ant and v_ant else None
            ),
        })

    return {"periodo": f"{anio}-{mes:02d}", "mercados": resumen}


def ver_informe_anterior(anio: int, mes: int,
                         ruta: Path | str = DB_PATH) -> dict:
    """Trae el informe del mes previo para comparar afirmaciones."""
    texto = informe_anterior(anio, mes, ruta)
    return {"disponible": texto is not None,
            "texto": texto or "No hay informe del mes anterior."}


# --------------------------------------------------------------------------
# Esquemas para la API
# --------------------------------------------------------------------------

ESQUEMAS = [
    {
        "name": "consultar_serie",
        "description": (
            "Serie mensual de volumen, valor y precio implícito por kilo. "
            "Es la herramienta principal: usala antes de afirmar cualquier "
            "cifra sobre evolución de precios o volúmenes."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mercado": {"type": "string",
                            "description": "EEUU, UE:EU27_2020, UE:ES, UE:IT, UE:FR"},
                "origen": {"type": "string",
                           "description": "País de origen. ARGENTINA, ECUADOR, INDIA "
                                          "para EEUU; AR, EC, IN para la UE. Omitir "
                                          "para el total del mercado."},
                "codigo": {"type": "string",
                           "description": "Prefijo de partida. 030617 para EEUU, "
                                          "03061799 para langostino argentino en la UE."},
                "meses": {"type": "integer",
                          "description": "Cantidad de meses hacia atrás. Por defecto 36."},
            },
            "required": ["mercado"],
        },
    },
    {
        "name": "comparar_origenes",
        "description": (
            "Ranking de países de origen en un mes dado, con cuota de mercado, "
            "precio y variación interanual de cada uno. Usala para ubicar a "
            "Argentina frente a Ecuador, India y el resto."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mercado": {"type": "string"},
                "anio": {"type": "integer"},
                "mes": {"type": "integer"},
                "codigo": {"type": "string"},
            },
            "required": ["mercado", "anio", "mes"],
        },
    },
    {
        "name": "detectar_anomalias",
        "description": (
            "Identifica meses cuya variación se aparta de la media histórica "
            "más allá de un umbral de desvíos estándar. Usala para encontrar "
            "qué merece explicación en el informe."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mercado": {"type": "string"},
                "origen": {"type": "string"},
                "codigo": {"type": "string"},
                "variable": {"type": "string",
                             "enum": ["precio_por_kg", "toneladas", "valor_miles"]},
                "umbral": {"type": "number"},
            },
            "required": ["mercado"],
        },
    },
    {
        "name": "resumen_periodo",
        "description": (
            "Foto de un mes en todos los mercados cargados, con variación "
            "interanual de volumen y precio. Buen punto de partida del informe."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "anio": {"type": "integer"},
                "mes": {"type": "integer"},
            },
            "required": ["anio", "mes"],
        },
    },
    {
        "name": "ver_informe_anterior",
        "description": (
            "Devuelve el informe del mes previo. Consultalo siempre antes de "
            "redactar, para señalar qué cambió y qué se confirmó, y para no "
            "repetir las mismas observaciones."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "anio": {"type": "integer"},
                "mes": {"type": "integer"},
            },
            "required": ["anio", "mes"],
        },
    },
]

REGISTRO = {
    "consultar_serie": consultar_serie,
    "comparar_origenes": comparar_origenes,
    "detectar_anomalias": detectar_anomalias,
    "resumen_periodo": resumen_periodo,
    "ver_informe_anterior": ver_informe_anterior,
}


def ejecutar(nombre: str, argumentos: dict, ruta: Path | str = DB_PATH) -> dict:
    """Despacha una llamada de herramienta. Los errores vuelven como dato."""
    fn = REGISTRO.get(nombre)
    if not fn:
        return {"error": f"herramienta desconocida: {nombre}"}
    try:
        return fn(**argumentos, ruta=ruta)
    except TypeError as e:
        return {"error": f"argumentos inválidos para {nombre}: {e}"}
    except Exception as e:
        log.exception("Error ejecutando %s", nombre)
        return {"error": f"{type(e).__name__}: {e}"}
