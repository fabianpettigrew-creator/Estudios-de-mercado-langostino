# -*- coding: utf-8 -*-
"""Verificación de consistencia interna del sistema de demanda inversa por origen.

No estima nada: toma la matriz de flexibilidades y las flexibilidades de escala tal como
están publicadas en `salidas/Demanda_inversa_L1_resultados.md` §2 y en el anexo (A.15/A.16)
y controla las identidades que la teoría obliga a cumplir. Corre sin las bases: los números
de entrada son los del informe.

Las tres identidades que se controlan, con la notación del anexo
(w_i = a_i + Σ_j γ_ij·log q_j + β_i·log Q):

    adición       Σ_i w_i·f_ij = −w_j
    escala        Σ_j f_ij     = f_i^escala          ← la que falla
    negatividad   H = [γ_ij − w_i·δ_ij + w_i·w_j] semidefinida negativa   (Barten ec. 17)

Uso:  python verificar_sistema_inverso.py
"""
from __future__ import annotations

import numpy as np

ORIGENES = ["AR", "EC", "IN", "VN", "RE"]

# participación media en el valor importado extra-UE (§2 del informe de resultados)
W = np.array([0.146, 0.261, 0.164, 0.091, 0.337])

# flexibilidades de cantidad no compensadas, tal como se publican (fila = precio de i)
F_PUB = np.array([
    [-0.267, -0.128, -0.246, -0.100, -0.259],
    [-0.152, -0.397, -0.113, -0.113, -0.225],
    [-0.125, -0.210, -0.254, -0.106, -0.305],
    [-0.106, -0.335, -0.302, -0.025, -0.232],
    [-0.110, -0.219, -0.088, -0.081, -0.502],
])

# flexibilidad de escala publicada en el mismo párrafo
ESC_PUB = np.array([-0.82, -0.83, -1.14, -1.17, -1.10])


def main() -> None:
    n = len(ORIGENES)
    print("=" * 78)
    print("VERIFICACIÓN DEL SISTEMA DE DEMANDA INVERSA POR ORIGEN")
    print("=" * 78)

    print("\n1. ADICIÓN   Σ_i w_i·f_ij = −w_j")
    for j, o in enumerate(ORIGENES):
        print(f"   {o}: {W @ F_PUB[:, j]:+.4f}   contra  {-W[j]:+.4f}")
    print("   → se cumple.")

    print("\n2. ESCALA   Σ_j f_ij = f_i^escala")
    for i, o in enumerate(ORIGENES):
        s = F_PUB[i].sum()
        print(f"   {o}: fila = {s:+.4f}   escala publicada = {ESC_PUB[i]:+.3f}   "
              f"brecha = {s - ESC_PUB[i]:+.3f}")
    print("   → NO se cumple. Todas las filas suman exactamente −1, que es lo que da")
    print("     f_ij = γ_ij/w_i − δ_ij cuando se omite el término β_i·w_j/w_i.")

    # reconstrucción: γ_ij = w_i·(f_ij^pub + δ_ij);  β_i = (f_i^escala + 1)·w_i
    G = (F_PUB + np.eye(n)) * W[:, None]
    B = (ESC_PUB + 1.0) * W
    F_OK = G / W[:, None] + np.outer(B, W) / W[:, None] - np.eye(n)

    print("\n3. MATRIZ CORREGIDA   f_ij = γ_ij/w_i + β_i·w_j/w_i − δ_ij")
    print("   " + "".join(f"{o:>9}" for o in ORIGENES) + f"{'suma':>9}")
    for i, o in enumerate(ORIGENES):
        print(f"   {o} " + "".join(f"{x:+9.3f}" for x in F_OK[i]) + f"{F_OK[i].sum():+9.3f}")
    print(f"\n   propia de Argentina: publicada {F_PUB[0, 0]:+.3f} → corregida {F_OK[0, 0]:+.3f}")
    print("   el titular no cambia de lado: sigue muy lejos de −1.")

    print("\n4. NEGATIVIDAD (Barten ec. 17)   H = γ_ij − w_i·δ_ij + w_i·w_j")
    H = G - np.diag(W) + np.outer(W, W)
    print("   diagonal de H (debe ser negativa en los cinco):")
    for i, o in enumerate(ORIGENES):
        marca = "" if H[i, i] < 0 else "   ← POSITIVA"
        print(f"      {o}: {H[i, i]:+.4f}{marca}")
    ev = np.linalg.eigvalsh((H + H.T) / 2)
    print(f"   autovalores de (H+H')/2: {np.round(ev, 5)}")
    print(f"   semidefinida negativa: {'sí' if (ev <= 1e-9).all() else 'NO'}")

    print("\n5. SIMETRÍA DE ANTONELLI   γ_ij = γ_ji")
    peor = np.unravel_index(np.abs(H - H.T).argmax(), H.shape)
    print(f"   mayor discrepancia: |h_{ORIGENES[peor[0]]},{ORIGENES[peor[1]]} − "
          f"h_{ORIGENES[peor[1]]},{ORIGENES[peor[0]]}| = {np.abs(H - H.T).max():.4f}")
    print(f"   h_AR,EC = {H[0, 1]:+.4f}   h_EC,AR = {H[1, 0]:+.4f}   (signos opuestos)")
    print("   contra una diagonal cuyo menor valor absoluto es "
          f"{np.abs(np.diag(H)).min():.4f}.")


if __name__ == "__main__":
    main()
