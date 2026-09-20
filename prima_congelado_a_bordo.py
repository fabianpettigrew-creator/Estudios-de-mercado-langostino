# -*- coding: utf-8 -*-
"""La prima de congelar a bordo, por calibre del entero — reconstrucción desde la base.

Por qué existe este script. La tabla «prima de congelar a bordo por calibre»
(L1 US$0,77 · L2 US$0,56 · L3 US$0,45) viajaba en dos planillas de `salidas/`
—`L1_por_flota_2018_2026.xlsx` hoja «8 Calibre x flota» y
`Anexo_datos_propuesta.xlsx` hoja «A4 Prima por calibre»— sin ningún script que
las generara: era el único número del capítulo de producto que no se podía
regenerar. Esto lo reconstruye desde el dato transaccional.

Especificación
--------------
Universo      despachos de langostino ENTERO, calibres L1, L2 y L3.
Ruta          `ruta` del cargador: «a bordo» (sufijo SIM SA01 o, hasta 2017,
              la leyenda «CONGELADO A BORDO» en la descripción) contra
              «en tierra» (cualquier otro sufijo SA). Los «s/d» se excluyen:
              la marca de a bordo es afirmativa y nunca se infiere por descarte.
Período       2018-2026 por defecto. Antes de 2018 no existe el sufijo y la ruta
              sale de la prosa, con 68-70% de cobertura y un hueco de jun a nov
              de 2017: mezclar esos años ensucia la comparación.
Precio        FOB unitario promedio ponderado por kilos dentro de cada celda.
Depuración    la misma de `hedonico.py` y `premium_destino_placa15.py`:
              FOB unitario entre 3 y 15 USD/kg y embarques de 500 kg o más.

Qué NO es. Es una diferencia de promedios ponderados, no un coeficiente: no
controla destino ni mes, así que arrastra el mix de compradores y de estación de
cada flota. La versión controlada del mismo fenómeno —a igual mes y destino—
está en `hedonico.py`. Y es un promedio del período: año por año el orden entre
calibres NO se sostiene (ver la hoja «Por año» de la salida), así que la lectura
«la prima crece con el tamaño» vale para el agregado 2018-2026 y no para
cualquier año suelto.

Uso:  python prima_congelado_a_bordo.py [--desde 2018] [--hasta 2026]
Salida:  salidas/Prima_congelado_a_bordo_por_calibre.xlsx
"""
from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

SALIDAS = os.path.join(RAIZ, "salidas")
XLSX = os.path.join(SALIDAS, "Prima_congelado_a_bordo_por_calibre.xlsx")

CALIBRES = ["L1", "L2", "L3"]
FOB_MIN, FOB_MAX, KG_MIN = 3.0, 15.0, 500.0
DESDE, HASTA = 2018, 2026

# Valores publicados en el estudio (sección 2) y en las dos planillas viejas.
# El script los usa sólo para reportar si la reconstrucción los reproduce.
PUBLICADO = {"L1": 0.77, "L2": 0.56, "L3": 0.45}
TOLERANCIA = 0.02


def datos(desde: int, hasta: int) -> pd.DataFrame:
    """Despachos de entero L1-L3 con ruta de proceso conocida, ya depurados."""
    from fuentes import expo
    e = expo.cargar_todos()
    d = e[(e.pres == "entero")
          & (e.cal.isin(CALIBRES))
          & (e.ruta.isin(["a bordo", "en tierra"]))
          & (e.anio.between(desde, hasta))
          & (e.kg >= KG_MIN)
          & (e.fob.between(FOB_MIN, FOB_MAX))].copy()
    return d


def _wav(g: pd.DataFrame) -> float:
    """FOB unitario promedio ponderado por kilos."""
    return (g.fob * g.kg).sum() / g.kg.sum()


def tabla(d: pd.DataFrame) -> pd.DataFrame:
    """Una fila por calibre: FOB de cada ruta, brecha en dólares y en porcentaje."""
    filas = []
    for cal in CALIBRES:
        c = d[d.cal == cal]
        ab, ti = c[c.ruta == "a bordo"], c[c.ruta == "en tierra"]
        if ab.empty or ti.empty:
            continue
        f_ab, f_ti = _wav(ab), _wav(ti)
        filas.append({
            "calibre": cal,
            "FOB a bordo": f_ab,
            "FOB en tierra": f_ti,
            "brecha US$/kg": f_ab - f_ti,
            "brecha %": 100 * (f_ab / f_ti - 1),
            "kt a bordo": ab.kg.sum() / 1e6,
            "kt en tierra": ti.kg.sum() / 1e6,
            "despachos a bordo": len(ab),
            "despachos en tierra": len(ti),
        })
    return pd.DataFrame(filas).set_index("calibre")


def por_anio(d: pd.DataFrame) -> pd.DataFrame:
    """La misma brecha abierta por año: es donde se ve que el orden no se sostiene."""
    filas = []
    for (anio, cal), c in d.groupby(["anio", "cal"]):
        ab, ti = c[c.ruta == "a bordo"], c[c.ruta == "en tierra"]
        if ab.empty or ti.empty:
            continue
        filas.append({"anio": int(anio), "calibre": cal,
                      "brecha US$/kg": _wav(ab) - _wav(ti),
                      "kt a bordo": ab.kg.sum() / 1e6,
                      "kt en tierra": ti.kg.sum() / 1e6})
    p = pd.DataFrame(filas)
    if p.empty:
        return p
    return p.pivot(index="anio", columns="calibre", values="brecha US$/kg")


def cobertura(d: pd.DataFrame, e_todo: pd.DataFrame, desde: int, hasta: int):
    """Cuánto del entero queda afuera por «s/d» o por la depuración de precio."""
    base = e_todo[(e_todo.pres == "entero") & (e_todo.cal.isin(CALIBRES))
                  & (e_todo.anio.between(desde, hasta))]
    return {"kt del entero L1-L3 en el período": base.kg.sum() / 1e6,
            "kt que entran al cálculo": d.kg.sum() / 1e6,
            "cobertura %": 100 * d.kg.sum() / base.kg.sum()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--desde", type=int, default=DESDE)
    ap.add_argument("--hasta", type=int, default=HASTA)
    a = ap.parse_args()

    from fuentes import expo
    e_todo = expo.cargar_todos()
    d = datos(a.desde, a.hasta)
    t = tabla(d)
    p = por_anio(d)
    cob = cobertura(d, e_todo, a.desde, a.hasta)

    print("\nPRIMA DE CONGELAR A BORDO POR CALIBRE DEL ENTERO · %d-%d"
          % (a.desde, a.hasta))
    print(t.round(3).to_string())
    print("\nBrecha US$/kg por año (el orden entre calibres no se sostiene):")
    print(p.round(2).to_string() if not p.empty else "  sin datos")
    print("\nCobertura:")
    for k, v in cob.items():
        print("  %-38s %8.1f" % (k, v))

    print("\nContra lo publicado en el estudio (sección 2):")
    ok = True
    for cal, ref in PUBLICADO.items():
        if cal not in t.index:
            print("  %s  sin dato reconstruido" % cal)
            ok = False
            continue
        got = t.loc[cal, "brecha US$/kg"]
        marca = "coincide" if abs(got - ref) <= TOLERANCIA else "NO COINCIDE"
        ok &= abs(got - ref) <= TOLERANCIA
        print("  %s  publicado %.2f  ·  reconstruido %.3f  ·  %s"
              % (cal, ref, got, marca))
    print("  → %s" % ("la tabla publicada se reproduce." if ok else
                      "la tabla publicada NO se reproduce: revisar antes de citarla."))

    os.makedirs(SALIDAS, exist_ok=True)
    with pd.ExcelWriter(XLSX, engine="openpyxl") as w:
        nota = pd.DataFrame({
            "Prima de congelar a bordo por calibre del entero · %d-%d"
            % (a.desde, a.hasta): [
                "FOB unitario promedio ponderado por kilos, base de comercio "
                "(transaccional, FOB, precio/calibre).",
                "Ruta: «a bordo» = sufijo SIM SA01 (marca afirmativa); «en tierra» = "
                "otro sufijo SA. Los «s/d» se excluyen.",
                "Depuración: FOB unitario entre %.0f y %.0f USD/kg, embarques de "
                "%.0f kg o más." % (FOB_MIN, FOB_MAX, KG_MIN),
                "Diferencia de promedios: NO controla destino ni mes, así que "
                "arrastra el mix de compradores y de estación de cada flota.",
                "El orden entre calibres es un resultado del período agrupado; "
                "año por año no se sostiene (ver hoja «Por año»).",
                "Cobertura: %.1f%% de los kilos de entero L1-L3 del período."
                % cob["cobertura %"],
            ]})
        nota.to_excel(w, sheet_name="Nota", index=False)
        t.round(4).to_excel(w, sheet_name="Prima por calibre")
        if not p.empty:
            p.round(3).to_excel(w, sheet_name="Por año")
    print("\nEscrito: %s" % XLSX)


if __name__ == "__main__":
    main()
