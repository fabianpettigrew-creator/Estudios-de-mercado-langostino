"""
Exportación desagregada a Excel.

Vuelca la tabla de observaciones al máximo detalle disponible, con nombres de
país completos y una fila por (mercado, período, HTS/CN, país, presentación,
talle, distrito). Pensado para trabajar los datos a mano: filtrar, pivotear,
graficar.

A diferencia de reporte.py (que agrega para el briefing), acá NO se agrega nada:
es el grano más fino que hay en la base.

Uso:
    python exportar.py                # todos los períodos
    python exportar.py --desde 2025-01
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from almacen import conexion
from config import DB_PATH, SALIDAS_DIR, nombre_pais

log = logging.getLogger(__name__)


def _cultivo(descripcion: str) -> str:
    """cultivo / salvaje a partir de la descripción de NOAA (FARMED/WILD)."""
    d = (descripcion or "").upper()
    if "FARMED" in d:
        return "cultivo"
    if "WILD" in d:
        return "salvaje"
    return ""


def _agua(descripcion: str) -> str:
    """Agua templada/fría según la descripción de NOAA."""
    d = (descripcion or "").upper()
    if "WARM-WATER" in d or "WARMWATER" in d:
        return "templada"
    if "COLD-WATER" in d or "COLDWATER" in d:
        return "fría"
    return ""


def exportar(desde: str | None = None, ruta_db: Path | str = DB_PATH) -> Path:
    try:
        import pandas as pd
    except ImportError:
        raise SystemExit("Falta pandas. Instalalo con:  pip install pandas openpyxl")

    where = ""
    params: tuple = ()
    if desde:
        anio, mes = (int(x) for x in desde.split("-"))
        where = "WHERE (anio > ? OR (anio = ? AND mes >= ?))"
        params = (anio, anio, mes)

    with conexion(ruta_db) as con:
        filas = con.execute(f"""
            SELECT mercado, fuente, anio, mes, codigo, descripcion, origen,
                   presentacion, talle, distrito, kilos, valor_usd, valor_eur
            FROM observaciones
            {where}
            ORDER BY mercado, anio, mes, codigo, origen, distrito
        """, params).fetchall()

    if not filas:
        raise SystemExit("No hay observaciones para exportar. ¿Corriste ingesta.py?")

    registros = []
    for f in filas:
        kilos = f["kilos"] or 0
        val_usd = f["valor_usd"]
        val_eur = f["valor_eur"]
        moneda = "USD" if f["mercado"] == "EEUU" else "EUR"
        valor = val_usd if moneda == "USD" else val_eur
        precio = round(valor / kilos, 2) if (valor and kilos) else None
        registros.append({
            "pais": nombre_pais(f["origen"]),
            "origen_raw": f["origen"],
            "mercado": f["mercado"],
            "fuente": f["fuente"],
            "periodo": f"{f['anio']}-{f['mes']:02d}",
            "anio": f["anio"],
            "mes": f["mes"],
            "codigo": f["codigo"],
            "descripcion": f["descripcion"],
            "cultivo": _cultivo(f["descripcion"]),
            "agua": _agua(f["descripcion"]),
            "presentacion": f["presentacion"],
            "talle": f["talle"],
            "distrito": f["distrito"],
            "kilos": kilos,
            "toneladas": round(kilos / 1000, 3),
            "valor_usd": val_usd,
            "valor_eur": val_eur,
            "precio_por_kg": precio,
            "moneda": moneda,
        })

    df = pd.DataFrame(registros)

    SALIDAS_DIR.mkdir(parents=True, exist_ok=True)
    destino = SALIDAS_DIR / "desagregado.xlsx"

    with pd.ExcelWriter(destino, engine="openpyxl") as xls:
        # Hoja principal: todo al máximo detalle
        df.to_excel(xls, sheet_name="Detalle", index=False)

        # Codebook de HTS de EE.UU. (el HTS ya trae especie/talle/presentación)
        us = df[df["mercado"] == "EEUU"]
        if not us.empty:
            cod_us = (us.groupby(["codigo", "descripcion", "agua", "cultivo",
                                  "presentacion", "talle"], dropna=False)
                        .agg(toneladas=("toneladas", "sum"))
                        .reset_index()
                        .sort_values("codigo"))
            cod_us.to_excel(xls, sheet_name="Codigos_EEUU", index=False)

        # Codebook de CN8 de la UE
        ESPECIE_CN = {
            "03061791": "Parapenaeus longirostris (gamba blanca)",
            "03061792": "género Penaeus (incl. vannamei de cultivo)",
            "03061793": "familia Pandalidae (excl. Pandalus)",
            "03061794": "género Crangon (excl. Crangon crangon)",
            "03061799": "los demás (langostino argentino, Pleoticus muelleri)",
        }
        ue = df[df["mercado"].str.startswith("UE:")]
        if not ue.empty:
            cod_ue = (ue.groupby("codigo").agg(toneladas=("toneladas", "sum")).reset_index())
            cod_ue["especie"] = cod_ue["codigo"].map(ESPECIE_CN)
            cod_ue = cod_ue[["codigo", "especie", "toneladas"]].sort_values("codigo")
            cod_ue.to_excel(xls, sheet_name="Codigos_UE", index=False)

        # Diccionario de países (raw -> completo)
        paises = (df[["origen_raw", "pais", "mercado"]]
                  .drop_duplicates()
                  .sort_values(["mercado", "pais"]))
        paises.to_excel(xls, sheet_name="Paises", index=False)

    log.info("Excel desagregado: %s (%d filas)", destino, len(df))
    return destino


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="Exporta las observaciones desagregadas a Excel")
    p.add_argument("--desde", help="período mínimo AAAA-MM (por defecto, todo)")
    args = p.parse_args()

    destino = exportar(args.desde)
    print("\n" + "=" * 70)
    print(f"EXCEL DESAGREGADO: {destino}")
    print("=" * 70)
    print("Hoja 'Detalle': una fila por observación, al máximo detalle.")
    print("Hojas 'Codigos_EEUU' / 'Codigos_UE': qué significa cada HTS/CN.")
    print("Hoja 'Paises': códigos de origen -> nombre completo.")


if __name__ == "__main__":
    main()
