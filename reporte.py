"""
Reporte mensual sin API.

Reemplaza a agente.py. Hace dos cosas:

  1. Un Excel con las series, para archivar y graficar.
  2. Un briefing de texto compacto, para copiar y pegar en Claude.ai y que
     el informe lo redactemos ahí en conversación.

El briefing está pensado para que entre entero en un mensaje de chat: lleva
los números que importan y nada más. No requiere clave de API ni gasto alguno.

Uso:
    python reporte.py 2026 5
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from almacen import conexion, informe_anterior
from config import DB_PATH, SALIDAS_DIR
from herramientas import (
    comparar_origenes,
    consultar_serie,
    detectar_anomalias,
    resumen_periodo,
)

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Excel
# --------------------------------------------------------------------------

def generar_excel(anio: int, mes: int, ruta_db: Path | str = DB_PATH) -> Path:
    """Vuelca las series a un Excel con una hoja por mercado."""
    try:
        import pandas as pd
    except ImportError:
        raise SystemExit(
            "Falta pandas. Instalalo con:  pip install pandas openpyxl"
        )

    SALIDAS_DIR.mkdir(parents=True, exist_ok=True)
    destino = SALIDAS_DIR / f"series_{anio}_{mes:02d}.xlsx"

    with conexion(ruta_db) as con:
        mercados = [f["mercado"] for f in con.execute(
            "SELECT DISTINCT mercado FROM observaciones ORDER BY mercado"
        ).fetchall()]
        origenes = {
            m: [f["origen"] for f in con.execute(
                "SELECT DISTINCT origen FROM observaciones WHERE mercado = ?", (m,)
            ).fetchall()]
            for m in mercados
        }

    with pd.ExcelWriter(destino, engine="openpyxl") as xls:
        # Hoja 1: resumen del mes
        resumen = resumen_periodo(anio, mes, ruta_db)
        pd.DataFrame(resumen["mercados"]).to_excel(
            xls, sheet_name="Resumen", index=False
        )

        # Una hoja por mercado, con la serie total y la de cada origen
        for mercado in mercados:
            bloques = []
            total = consultar_serie(mercado, meses=60, ruta=ruta_db)["serie"]
            df_total = pd.DataFrame(total)
            df_total.insert(0, "origen", "TOTAL")
            bloques.append(df_total)

            for origen in sorted(origenes[mercado]):
                serie = consultar_serie(mercado, origen, meses=60, ruta=ruta_db)["serie"]
                if not serie:
                    continue
                df = pd.DataFrame(serie)
                df.insert(0, "origen", origen)
                bloques.append(df)

            hoja = mercado.replace(":", "_")[:31]
            pd.concat(bloques, ignore_index=True).to_excel(
                xls, sheet_name=hoja, index=False
            )

            # Tabla pivote de precios, cómoda para graficar
            pivote = pd.concat(bloques).pivot_table(
                index="periodo", columns="origen", values="precio_por_kg"
            )
            pivote.to_excel(xls, sheet_name=f"{hoja[:24]}_precios")

    log.info("Excel generado: %s", destino)
    return destino


# --------------------------------------------------------------------------
# Briefing para el chat
# --------------------------------------------------------------------------

def _tabla(filas: list[dict], columnas: list[tuple[str, str]]) -> str:
    """Arma una tabla markdown compacta."""
    if not filas:
        return "_sin datos_\n"
    cab = " | ".join(t for t, _ in columnas)
    sep = " | ".join("---" for _ in columnas)
    cuerpo = "\n".join(
        " | ".join(str(f.get(c, "")) if f.get(c) is not None else "-"
                   for _, c in columnas)
        for f in filas
    )
    return f"{cab}\n{sep}\n{cuerpo}\n"


def generar_briefing(anio: int, mes: int, ruta_db: Path | str = DB_PATH,
                     meses_serie: int = 13) -> str:
    """
    Arma el texto que se pega en Claude.ai para redactar el informe.

    Incluye: resumen del mes, ranking de orígenes por mercado, serie reciente
    de precios y anomalías detectadas.
    """
    partes: list[str] = []
    partes.append(f"# Datos de mercado — {mes:02d}/{anio}\n")
    partes.append(
        "Fuentes: NOAA FOSS (importaciones EE.UU.) y Eurostat Comext (UE). "
        "Precios calculados como valor sobre kilos del agregado.\n"
    )

    # --- Resumen general ---
    resumen = resumen_periodo(anio, mes, ruta_db)
    partes.append("## Resumen del mes\n")
    partes.append(_tabla(resumen["mercados"], [
        ("Mercado", "mercado"), ("Moneda", "moneda"),
        ("Toneladas", "toneladas"), ("Precio/kg", "precio_por_kg"),
        ("Var. vol. i.a. %", "var_volumen_ia_pct"),
        ("Var. precio i.a. %", "var_precio_ia_pct"),
    ]))

    mercados = [m["mercado"] for m in resumen["mercados"]]

    # --- Por mercado ---
    for mercado in mercados:
        partes.append(f"\n## {mercado}\n")

        ranking = comparar_origenes(mercado, anio, mes, ruta=ruta_db)
        partes.append(f"### Orígenes en {mes:02d}/{anio} "
                      f"(total {ranking['total_toneladas']} t)\n")
        partes.append(_tabla(ranking["ranking"], [
            ("Origen", "origen"), ("Toneladas", "toneladas"),
            ("Cuota %", "cuota_pct"), ("Precio/kg", "precio_por_kg"),
            ("Var. vol. i.a. %", "var_volumen_ia_pct"),
            ("Var. precio i.a. %", "var_precio_ia_pct"),
        ]))

        # Serie de precios de los últimos meses, por origen relevante
        partes.append(f"### Precio por kg, últimos {meses_serie} meses\n")
        principales = [r["origen"] for r in ranking["ranking"][:5]]
        filas_serie: dict[str, dict] = {}
        for origen in principales:
            serie = consultar_serie(mercado, origen, meses=meses_serie, ruta=ruta_db)
            for punto in serie["serie"]:
                filas_serie.setdefault(punto["periodo"], {"periodo": punto["periodo"]})
                filas_serie[punto["periodo"]][origen] = punto["precio_por_kg"]
        columnas = [("Período", "periodo")] + [(o, o) for o in principales]
        partes.append(_tabla(list(filas_serie.values()), columnas))

        # Anomalías del origen argentino
        arg = "ARGENTINA" if mercado == "EEUU" else "AR"
        anom = detectar_anomalias(mercado, arg, ruta=ruta_db)
        if anom.get("anomalias"):
            partes.append(f"### Meses atípicos en el precio argentino\n")
            partes.append(f"(media {anom['variacion_media_pct']}%, "
                          f"desvío {anom['desvio_estandar_pct']}%)\n\n")
            partes.append(_tabla(anom["anomalias"], [
                ("Período", "periodo"), ("Variación %", "variacion_pct"),
                ("Desvíos", "desvios"),
            ]))

    # --- Cadena de valor: FOB -> CIF -> gondola ---
    # Une exportacion (FOB), mercado.db (CIF) y el panel de retail. Opcional: si
    # falta alguna fuente (los Excel de exportacion o el CSV de retail), se saltea
    # sin romper el briefing mensual. Genera ademas los SVG en salidas/.
    try:
        import cascade
        partes.append("\n" + cascade.briefing_y_graficos())
    except Exception as e:
        log.warning("Cadena de valor no incluida (falta fuente o error): %s", e)

    # --- Informe anterior ---
    anterior = informe_anterior(anio, mes, ruta_db)
    if anterior:
        partes.append("\n## Lo que dijimos el mes pasado\n")
        partes.append(anterior[:2000] + ("..." if len(anterior) > 2000 else ""))

    partes.append(
        "\n---\n\n**Pedido:** redactá el informe mensual de mercado con estos "
        "datos. Recordá que el langostino argentino es salvaje y premium, "
        "mientras el grueso del mercado es vannamei de cultivo: analizá la "
        "sustitución. Si está la sección de cadena de valor (FOB→CIF→góndola), "
        "usala para explicar dónde se captura el margen y por qué el 'premium' de "
        "EE.UU. es presentación (tratala como direccional, no como serie firme). "
        "Marcá qué cambió respecto del mes anterior y distinguí los datos de las "
        "hipótesis. No agregues cifras que no estén acá."
    )

    return "\n".join(partes)


def main(anio: int, mes: int, ruta_db: Path | str = DB_PATH) -> None:
    SALIDAS_DIR.mkdir(parents=True, exist_ok=True)

    briefing = generar_briefing(anio, mes, ruta_db)
    destino_txt = SALIDAS_DIR / f"briefing_{anio}_{mes:02d}.md"
    destino_txt.write_text(briefing, encoding="utf-8")

    try:
        destino_xls = generar_excel(anio, mes, ruta_db)
    except SystemExit as e:
        destino_xls = None
        log.warning("%s", e)

    print("\n" + "=" * 70)
    print(f"BRIEFING guardado en: {destino_txt}")
    if destino_xls:
        print(f"EXCEL    guardado en: {destino_xls}")
    print("=" * 70)
    print("\nAbrí el briefing, copiá todo y pegalo en Claude.ai.")
    print("El informe lo redactamos ahí, en conversación.\n")
    print("-" * 70)
    print(briefing[:1500])
    if len(briefing) > 1500:
        print(f"\n[...{len(briefing) - 1500} caracteres más en el archivo]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="Genera el Excel y el briefing del mes")
    p.add_argument("anio", type=int)
    p.add_argument("mes", type=int)
    args = p.parse_args()
    main(args.anio, args.mes)
