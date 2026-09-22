# -*- coding: utf-8 -*-
"""De coeficientes del LA/IAIDS a flexibilidades. Una sola definición.

Estaba escrita por separado en `demanda_inversa_modelo.py` y en `iaids_simetria.py`,
y en las dos le faltaba el mismo término. Vive acá por el mismo motivo que el recorte
en `recorte_conxemar.py`: dos copias de una fórmula son dos fuentes.

El sistema es

    w_i = a_i + Σ_j γ_ij·log q_j + β_i·log Q ,   log Q = Σ_k w̄_k·log q_k   (Stone)

con w_i = π_i·q_i la participación del origen i en el valor del grupo y π_i = p_i/E el
precio normalizado por el gasto del grupo. De ahí

    dw_i = Σ_j γ_ij·dlog q_j + β_i·dlog Q        y        dlog π_i = dw_i/w_i − dlog q_i

y como dlog Q = Σ_k w_k·dlog q_k, cada casilla se lleva un pedazo del efecto escala:

    f_ij  =  γ_ij / w_i  +  β_i·w_j / w_i  −  δ_ij          (no compensada)
    f_i^escala  =  β_i / w_i  −  1

El término β_i·w_j/w_i es el que faltaba. Sin él la homogeneidad Σ_j γ_ij = 0 hace que
toda fila sume exactamente −1, la matriz contradice la columna de escala y la propia de
Argentina sale −0,267 en lugar de −0,241. Es el análogo inverso de la ecuación (20) de
Barten y Bettendorf (1989) y la forma estándar del AIDS inverso de Eales y Unnevehr.

La identidad que hay que poder verificar siempre, y que `verificar()` controla:

    Σ_j f_ij  =  f_i^escala
"""
from __future__ import annotations

import pandas as pd


def matriz(G: pd.DataFrame, b: pd.Series, w: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
    """Flexibilidades no compensadas y de escala.

    G: matriz γ_ij (fila i = ecuación del origen i), ya con homogeneidad y adición
       resueltas.  b: los β_i, el coeficiente del índice de Stone.  w: participaciones
       medias en el valor del grupo.
    """
    bienes = list(G.index)
    F = pd.DataFrame(index=bienes, columns=bienes, dtype=float)
    for i in bienes:
        for j in bienes:
            F.loc[i, j] = (G.loc[i, j] + b[i] * w[j]) / w[i] - (1.0 if i == j else 0.0)
    esc = pd.Series({i: b[i] / w[i] - 1.0 for i in bienes}, name="escala")
    return F, esc


def verificar(F: pd.DataFrame, esc: pd.Series, w: pd.Series, tol: float = 1e-3) -> None:
    """Corta si la matriz no cumple las dos identidades que no dependen del dato.

        escala   Σ_j f_ij = f_i^escala
        adición  Σ_i w_i·f_ij = −w_j

    La tolerancia es floja a propósito: las dos identidades valen exactamente cuando
    las participaciones suman uno, y con w redondeadas a tres decimales no lo hacen.
    El error que motivó este módulo abre brechas de 0,10 a 0,18, cien veces la tolerancia.
    """
    bienes = list(F.index)
    for i in bienes:
        d = F.loc[i].sum() - esc[i]
        if abs(d) > tol:
            raise AssertionError(
                f"fila {i}: Σ_j f_ij = {F.loc[i].sum():+.6f} contra escala "
                f"{esc[i]:+.6f} (brecha {d:+.6f}). Falta el término β_i·w_j/w_i.")
    for j in bienes:
        d = (w * F[j]).sum() + w[j]
        if abs(d) > tol:
            raise AssertionError(
                f"columna {j}: Σ_i w_i·f_ij = {(w * F[j]).sum():+.6f} contra "
                f"−w_j = {-w[j]:+.6f} (brecha {d:+.6f}). Falla la adición.")


def antonelli(G: pd.DataFrame, w: pd.Series) -> pd.DataFrame:
    """Matriz de sustitución de Antonelli:  h_ij = γ_ij − w_i·δ_ij + w_i·w_j.

    Es la que tiene que ser semidefinida negativa —condición (17) de Barten y
    Bettendorf— para que las flexibilidades propias sean interpretables.
    """
    bienes = list(G.index)
    H = pd.DataFrame(index=bienes, columns=bienes, dtype=float)
    for i in bienes:
        for j in bienes:
            H.loc[i, j] = G.loc[i, j] - (w[i] if i == j else 0.0) + w[i] * w[j]
    return H


def negatividad(G: pd.DataFrame, w: pd.Series) -> dict:
    """Diagnóstico de la condición (17). No corta: informa.

    Devuelve la diagonal de Antonelli, los autovalores de la parte simétrica y el
    veredicto. Una diagonal positiva dice que un origen no es sustituto de sí mismo,
    que es el síntoma habitual de una ecuación mal identificada.
    """
    import numpy as np

    H = antonelli(G, w)
    A = H.to_numpy()
    ev = np.linalg.eigvalsh((A + A.T) / 2)
    return {"H": H,
            "diagonal": pd.Series(np.diag(A), index=H.index),
            "autovalores": ev,
            "sdn": bool((ev <= 1e-9).all()),
            "asimetria_max": float(np.abs(A - A.T).max())}


def informar_negatividad(G: pd.DataFrame, w: pd.Series) -> dict:
    """Imprime el diagnóstico de (17) en el formato del resto del proyecto."""
    d = negatividad(G, w)
    print("\nNegatividad (Barten ec. 17) — diagonal de Antonelli:")
    for i, v in d["diagonal"].items():
        print(f"   {i}: {v:+.4f}" + ("" if v < 0 else "   ← POSITIVA, no es sustituto de sí mismo"))
    print(f"   autovalores de (H+H')/2: {d['autovalores'].round(5)}")
    print(f"   semidefinida negativa: {'sí' if d['sdn'] else 'NO — las propias no son interpretables'}")
    print(f"   mayor asimetría |h_ij − h_ji|: {d['asimetria_max']:.4f}")
    return d
