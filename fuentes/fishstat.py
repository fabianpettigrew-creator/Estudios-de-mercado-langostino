"""
Acceso a FishStat (FAO Global Production): captura + acuicultura por país,
especie ASFIS y año, 1950-2023. Base local datos/fishstat.db (bulk FAO 2025.1.0).

Fuente distingue captura (wild) de acuicultura (freshwater/brackish/marine).
Cantidad en toneladas peso vivo.
"""
from __future__ import annotations
import sqlite3, os

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos", "fishstat.db")

# Códigos ASFIS de interés para el proyecto langostino
PNV = "PNV"   # Penaeus vannamei  (vannamei de cultivo — sustituto principal)
LAA = "LAA"   # Pleoticus muelleri (langostino argentino — objetivo)
GIT = "GIT"   # Penaeus monodon   (tigre gigante)


def _con():
    return sqlite3.connect(DB)


def serie_produccion(sp_a3: str, tipo: str | None = None,
                     iso3: str | None = None, desde: int = 1950) -> list[dict]:
    """Serie anual de producción (toneladas) de una especie.
    tipo: 'captura' | 'acuicultura' | None (ambas). iso3: país (None = mundo)."""
    q = """SELECT p.anio, SUM(p.valor) t
           FROM produccion p JOIN fuente f ON p.source=f.source
           {joinp} WHERE p.sp_a3=? AND p.anio>=? AND p.measure='Q_tlw' """
    params = [sp_a3, desde]
    joinp = ""
    if iso3:
        joinp = "JOIN pais c ON p.country_un=c.country_un"
        q += "AND c.iso3=? ";
    if tipo:
        q += "AND f.tipo=? "
    q = q.format(joinp=joinp)
    if iso3: params.append(iso3)
    if tipo: params.append(tipo)
    q += "GROUP BY p.anio ORDER BY p.anio"
    with _con() as con:
        return [{"anio": a, "toneladas": round(t or 0)} for a, t in con.execute(q, params)]


def top_paises(sp_a3: str, anio: int, tipo: str | None = None, n: int = 10) -> list[dict]:
    """Ranking de países por producción de una especie en un año."""
    q = """SELECT c.pais, SUM(p.valor) t
           FROM produccion p JOIN fuente f ON p.source=f.source
           JOIN pais c ON p.country_un=c.country_un
           WHERE p.sp_a3=? AND p.anio=? AND p.measure='Q_tlw' """
    params = [sp_a3, anio]
    if tipo:
        q += "AND f.tipo=? "; params.append(tipo)
    q += "GROUP BY c.pais ORDER BY t DESC LIMIT ?"; params.append(n)
    with _con() as con:
        tot = 0
        rows = con.execute(q, params).fetchall()
        tot_all = con.execute(
            "SELECT SUM(p.valor) FROM produccion p JOIN fuente f ON p.source=f.source "
            "WHERE p.sp_a3=? AND p.anio=? AND p.measure='Q_tlw'"
            + (" AND f.tipo=?" if tipo else ""), params[:2] + ([tipo] if tipo else [])
        ).fetchone()[0] or 1
    return [{"pais": pa, "toneladas": round(t or 0), "cuota_pct": round(100*(t or 0)/tot_all, 1)}
            for pa, t in rows]


if __name__ == "__main__":
    import sys
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass
    print("VANNAMEI (PNV) acuicultura — top productores 2023:")
    for r in top_paises(PNV, 2023, "acuicultura", 8):
        print(f"  {r['pais']:22} {r['toneladas']:>12,} t  {r['cuota_pct']:>5}%")
    print("\nLANGOSTINO ARGENTINO (LAA) captura — Argentina, últimos años:")
    for r in serie_produccion(LAA, "captura", "ARG", desde=2015):
        print(f"  {r['anio']}  {r['toneladas']:>10,} t")
