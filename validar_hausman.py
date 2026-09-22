# -*- coding: utf-8 -*-
"""Validación de `hausman_exogeneidad.py` contra un dato de ground truth conocido.

Por qué hace falta. El test de Hausman puede fallar de dos maneras y las dos son
silenciosas: no detectar una endogeneidad que está (poco poder) o marcar como endógena
una variable que no lo es (tamaño mal calibrado). Con el dato real no hay forma de
saberlo, porque justamente lo que se ignora es la verdad. Con un panel simulado sí:
uno arma la endogeneidad a mano y después mira si el test la encuentra donde la puso.

Se arman dos paneles, no uno. Un solo panel no puede tener a la vez cantidades exógenas
y precios exógenos para el mismo origen: si el precio sale de p = w·X/q y la cantidad
lleva adentro el shock de demanda, el precio lo hereda. Las dos formas son mutuamente
excluyentes por construcción, que es exactamente el motivo por el que existe el sistema
mixto. Así que cada panel valida un bloque:

    panel A — generado desde el sistema INVERSO
              cantidades exógenas:  AR, RE          (salvaje, predeterminado)
              cantidades endógenas: EC, IN, VN      (contaminadas con el shock u_t)
              → el test de CANTIDADES tiene que marcar exactamente esas tres

    panel B — generado desde el sistema DIRECTO
              precios exógenos:  EC, IN, VN         (tomadores del precio mundial)
              precios endógenos: AR, RE
              → el test de PRECIOS tiene que marcar exactamente esos dos

    panel C — nulo: NADA es endógeno, el shock entra sólo por el error
              → el test no tiene que rechazar. Sin esto no se puede afirmar que un
                rechazo signifique algo: un test que rechaza siempre también acierta
                en A y en B.

Cada panel se corre sobre muchas semillas, porque una sola extracción no distingue un
test que funciona de uno que tuvo suerte. Se mide la tasa de rechazo: en el panel C es
el TAMAÑO y tiene que quedar cerca del 5%; en A y en B es el PODER y tiene que ser alto.

Uso:  python validar_hausman.py
"""
from __future__ import annotations

import os
import sys
import warnings

import numpy as np
import pandas as pd

import hausman_exogeneidad as hx

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))

ORIGENES = hx.ORIGENES
T_IDX = pd.period_range("2013-01", "2026-07", freq="M")
NIVEL = hx.NIVEL

# Peso del shock de demanda dentro de la variable contaminada. Tiene que ser chico
# frente a la parte AR: con una contaminación grande la serie se vuelve casi ruido
# blanco, los rezagos dejan de predecir, el residuo de primera etapa pasa a ser la
# variable entera y el test queda degenerado en lugar de endógeno. Con LAM = 0,9 el
# panel A daba R2 de colinealidad de 0,99 y el test declaraba exógenos a los tres
# orígenes contaminados. Con 0,15 la primera etapa conserva F entre 17 y 27.
LAM = 0.15


def _gamma(rng, n=5, escala=0.012):
    """Matriz γ simétrica con filas y columnas de suma cero: homogeneidad y adición."""
    A = rng.standard_normal((n, n)) * escala
    A = (A + A.T) / 2
    A = A - A.mean(axis=0, keepdims=True) - A.mean(axis=1, keepdims=True) + A.mean()
    return A


def _proceso(rng, T, mu, contaminante=None, lam=0.0):
    """AR(2) con estacionalidad. El AR es lo que le da poder a la primera etapa; sin
    rezagos que predigan, el residuo es la variable entera y el test no distingue nada."""
    e = rng.standard_normal(T) * 0.18
    x = np.zeros(T)
    for t in range(2, T):
        x[t] = 0.55 * x[t - 1] + 0.20 * x[t - 2] + e[t]
    est = 0.22 * np.sin(2 * np.pi * np.arange(T) / 12) + 0.10 * np.cos(4 * np.pi * np.arange(T) / 12)
    y = mu + x + est
    if contaminante is not None:
        y = y + lam * contaminante
    return y


def _shares(rng, L, G, beta, a, u, theta):
    """w_i = a_i + Σ_j γ_ij·L_j + β_i·escala + ε_i, con Σ_i ε_i = 0 para que Σ_i w_i = 1.

    L entra en DESVÍOS respecto de su media, no en niveles. Con log q en niveles —que
    van de 0,8 a 2,3— los términos γ_ij·L_j se comen a las a_i: en la primera versión
    la participación de Vietnam se iba a 0,012 contra una media objetivo de 0,091, se
    activaba el recorte a cero y la renormalización rompía la linealidad. El test
    entonces no fallaba por falta de poder sino porque el sistema que se le daba a
    estimar no era el que se creía haber generado.
    """
    T, n = L.shape
    Lc = L - L.mean(axis=0, keepdims=True)         # desvíos: la constante absorbe el nivel
    esc = Lc @ a                                   # índice de Stone con las w medias
    ruido = rng.standard_normal((T, n)) * 0.006
    ruido = ruido - ruido.mean(axis=1, keepdims=True)
    eps = np.outer(u, theta) + ruido
    Wm = a + Lc @ G.T + np.outer(esc, beta) + eps
    assert Wm.min() > 0.01, f"participación generada fuera de rango: {Wm.min():.4f}"
    assert np.allclose(Wm.sum(axis=1), 1.0), "las participaciones no suman uno"
    return Wm


def panel_inverso(semilla=11):
    """Cantidades exógenas en AR y RE, contaminadas en EC, IN y VN."""
    rng = np.random.default_rng(100 + semilla)
    T = len(T_IDX)
    a = np.array([0.146, 0.261, 0.164, 0.091, 0.338])
    mu = np.log(np.array([3.5, 7.0, 4.5, 2.2, 9.0]))
    u = rng.standard_normal(T)                     # shock de demanda no observado
    endog = {"AR": 0.0, "EC": LAM, "IN": LAM, "VN": LAM, "RE": 0.0}
    L = np.column_stack([_proceso(rng, T, mu[k], u, endog[c]) for k, c in enumerate(ORIGENES)])
    G = _gamma(rng)
    beta = np.array([0.03, -0.02, 0.01, -0.015, -0.005])
    theta = np.array([0.020, -0.012, 0.008, -0.010, -0.006])
    Wm = _shares(rng, L, G, beta, a, u, theta)
    X = 60e6 * np.exp(np.cumsum(rng.standard_normal(T) * 0.02))   # gasto del grupo
    Q = pd.DataFrame(np.exp(L), index=T_IDX, columns=ORIGENES)
    V = pd.DataFrame(Wm * X[:, None], index=T_IDX, columns=ORIGENES)
    return V, Q, {c: (endog[c] == 0.0) for c in ORIGENES}


def panel_directo(semilla=23):
    """Precios exógenos en EC, IN y VN; contaminados en AR y RE."""
    rng = np.random.default_rng(200 + semilla)
    T = len(T_IDX)
    a = np.array([0.146, 0.261, 0.164, 0.091, 0.338])
    mu = np.log(np.array([6.3, 5.7, 6.7, 8.5, 6.0]))
    u = rng.standard_normal(T)
    endog = {"AR": LAM, "EC": 0.0, "IN": 0.0, "VN": 0.0, "RE": LAM}
    LP = np.column_stack([_proceso(rng, T, mu[k], u, endog[c]) for k, c in enumerate(ORIGENES)])
    G = _gamma(rng)
    beta = np.array([0.03, -0.02, 0.01, -0.015, -0.005])
    theta = np.array([0.020, -0.012, 0.008, -0.010, -0.006])
    Wm = _shares(rng, LP, G, beta, a, u, theta)
    X = 60e6 * np.exp(np.cumsum(rng.standard_normal(T) * 0.02))
    P = pd.DataFrame(np.exp(LP), index=T_IDX, columns=ORIGENES)
    V = pd.DataFrame(Wm * X[:, None], index=T_IDX, columns=ORIGENES)
    Q = V / (P * 1e6)                              # la cantidad ajusta: q = w·X/p
    return V, Q, {c: (endog[c] == 0.0) for c in ORIGENES}


def panel_nulo(semilla=5):
    """Nulo del bloque de CANTIDADES: q exógena, el shock entra sólo por el error.

    No sirve como nulo del bloque de precios: acá el precio sale de p = w·X/q, así que
    lleva adentro el error del sistema y es endógeno por construcción. Las dos formas
    son mutuamente excluyentes, que es justamente por lo que existe el sistema mixto.
    """
    rng = np.random.default_rng(1000 + semilla)
    T = len(T_IDX)
    a = np.array([0.146, 0.261, 0.164, 0.091, 0.338])
    mu = np.log(np.array([3.5, 7.0, 4.5, 2.2, 9.0]))
    u = rng.standard_normal(T)
    L = np.column_stack([_proceso(rng, T, mu[k]) for k in range(len(ORIGENES))])
    G = _gamma(rng)
    beta = np.array([0.03, -0.02, 0.01, -0.015, -0.005])
    theta = np.array([0.020, -0.012, 0.008, -0.010, -0.006])
    Wm = _shares(rng, L, G, beta, a, u, theta)
    X = 60e6 * np.exp(np.cumsum(rng.standard_normal(T) * 0.02))
    Q = pd.DataFrame(np.exp(L), index=T_IDX, columns=ORIGENES)
    V = pd.DataFrame(Wm * X[:, None], index=T_IDX, columns=ORIGENES)
    return V, Q, {c: True for c in ORIGENES}


def panel_nulo_directo(semilla=5):
    """Nulo del bloque de PRECIOS: p exógeno, la cantidad ajusta."""
    rng = np.random.default_rng(2000 + semilla)
    T = len(T_IDX)
    a = np.array([0.146, 0.261, 0.164, 0.091, 0.338])
    mu = np.log(np.array([6.3, 5.7, 6.7, 8.5, 6.0]))
    u = rng.standard_normal(T)
    LP = np.column_stack([_proceso(rng, T, mu[k]) for k in range(len(ORIGENES))])
    G = _gamma(rng)
    beta = np.array([0.03, -0.02, 0.01, -0.015, -0.005])
    theta = np.array([0.020, -0.012, 0.008, -0.010, -0.006])
    Wm = _shares(rng, LP, G, beta, a, u, theta)
    X = 60e6 * np.exp(np.cumsum(rng.standard_normal(T) * 0.02))
    P = pd.DataFrame(np.exp(LP), index=T_IDX, columns=ORIGENES)
    V = pd.DataFrame(Wm * X[:, None], index=T_IDX, columns=ORIGENES)
    return V, (V / (P * 1e6)), {c: True for c in ORIGENES}


def _contraste(obtenido: pd.DataFrame, verdad: dict) -> bool:
    """¿El test localizó la endogeneidad exactamente donde se la puso?"""
    return all((obtenido.loc[c, "veredicto"] == ("exógena" if verdad[c] else "ENDÓGENA"))
               for c in ORIGENES)


def _correr(constructor, bloque: str, semilla: int, individuales: bool = True):
    """Arma un panel y le pasa el test. bloque: 'q' testea cantidades, 'p' precios."""
    V, Q, verdad = constructor(semilla)
    W = V.div(V.sum(axis=1), axis=0)
    if bloque == "q":
        RES, diag = hx.primera_etapa(np.log(Q))
        REG = hx.reg_inversa(Q, W)
    else:
        P = V / (Q * 1e6)
        RES, diag = hx.primera_etapa(np.log(P))
        REG = hx.reg_directa(P, V, W)
    ind, conj, _ = hx.nucleo(W, REG, RES, individuales=individuales)
    return ind, conj, verdad, diag


def monte_carlo(constructor, bloque: str, nombre: str, semillas, crit=None) -> dict:
    """Pasada rápida: sólo el contraste conjunto, que es el que decide."""
    lr_, wa, est = [], [], []
    for sem in semillas:
        _, conj, _, _ = _correr(constructor, bloque, sem, individuales=False)
        lr_.append(conj["p_LR"] < NIVEL)
        wa.append(conj["p_Wald"] < NIVEL)
        est.append(conj["LR"])
    est = np.array(est)
    r = {"panel": nombre, "n": len(est),
         "rechazo_LR": float(np.mean(lr_)), "rechazo_Wald": float(np.mean(wa)),
         "LR_p95": float(np.percentile(est, 95))}
    if crit is not None:
        r["rechazo_LR_crit_sim"] = float(np.mean(est > crit))
    return r


def localizacion(constructor, bloque: str, semillas) -> float:
    """Fracción de semillas en que el test de a una variable acierta los cinco casos."""
    ok = []
    for sem in semillas:
        ind, _, verdad, _ = _correr(constructor, bloque, sem)
        ok.append(_contraste(ind, verdad))
    return float(np.mean(ok))


def main() -> None:
    print("=" * 92)
    print("VALIDACIÓN DEL TEST DE HAUSMAN CONTRA GROUND TRUTH SIMULADO")
    print("=" * 92)
    sem = range(int(os.environ.get("SEMILLAS", 40)))

    print("\nUna corrida en detalle de cada panel con endogeneidad puesta:")
    for constructor, bloque, nombre in [
            (panel_inverso, "q", "panel A · CANTIDADES (decide la forma inversa)"),
            (panel_directo, "p", "panel B · PRECIOS (decide la forma directa)")]:
        ind, conj, verdad, diag = _correr(constructor, bloque, 0)
        print(f"\n{nombre}")
        print("primera etapa, F de los rezagos: "
              + " · ".join(f"{c} {diag.loc[c, 'F_rezagos']:.0f}" for c in ORIGENES))
        t = ind[["Wald", "p_Wald", "R2_col", "veredicto"]].copy()
        t["verdad"] = [("exógena" if verdad[c] else "ENDÓGENA") for c in t.index]
        print(t.round(3).to_string())
        print(f"conjunto: Wald = {conj['Wald']:.1f} (gl {conj['gl']}), "
              f"p = {conj['p_Wald']:.4f} → "
              f"{'RECHAZA' if conj['p_Wald'] < NIVEL else 'no rechaza'}")

    print("\n" + "=" * 92)
    print(f"MONTE CARLO — {len(sem)} semillas por panel")
    print("=" * 92)
    print("Paso 1 — tamaño bajo el nulo y valor crítico simulado del LR conjunto.")
    n_q = monte_carlo(panel_nulo, "q", "C nulo · cantidades", sem)
    n_p = monte_carlo(panel_nulo_directo, "p", "C nulo · precios", sem)
    crit = max(n_q["LR_p95"], n_p["LR_p95"])
    print(f"  percentil 95 del LR bajo el nulo: cantidades {n_q['LR_p95']:.1f} · "
          f"precios {n_p['LR_p95']:.1f}")
    print(f"  chi-cuadrado de 20 al 5%: {31.41:.1f}   →   valor crítico a usar: {crit:.1f}")

    print("\nPaso 2 — poder, medido contra el valor crítico simulado.")
    R = pd.DataFrame([
        monte_carlo(panel_nulo, "q", "C nulo · cantidades", sem, crit),
        monte_carlo(panel_nulo_directo, "p", "C nulo · precios", sem, crit),
        monte_carlo(panel_inverso, "q", "A · cantidades endógenas", sem, crit),
        monte_carlo(panel_directo, "p", "B · precios endógenos", sem, crit),
    ]).set_index("panel")
    print(R.round(3).to_string())
    print("\n  En las dos primeras filas no hay nada que rechazar: eso es el TAMAÑO,")
    print("  nominal 0,05. En las dos últimas es el PODER. rechazo_LR usa el chi-cuadrado")
    print("  asintótico; rechazo_LR_crit_sim usa el valor crítico simulado de arriba.")

    sem_loc = range(min(len(sem), 40))
    loc_a = localizacion(panel_inverso, "q", sem_loc)
    loc_b = localizacion(panel_directo, "p", sem_loc)

    tam = R.loc[["C nulo · cantidades", "C nulo · precios"], "rechazo_LR_crit_sim"].max()
    tam_asin = R.loc[["C nulo · cantidades", "C nulo · precios"], "rechazo_LR"].max()
    tam_w = R.loc[["C nulo · cantidades", "C nulo · precios"], "rechazo_Wald"].max()
    pod = R.loc[["A · cantidades endógenas", "B · precios endógenos"],
                "rechazo_LR_crit_sim"].min()

    print("\n" + "=" * 92)
    print("LECTURA")
    print("=" * 92)
    ok_tam = tam <= 0.10
    ok_pod = pod >= 0.70
    print(f"  Wald conjunto, tamaño:                      {tam_w:.2f}  "
          f"{'ok' if tam_w <= 0.10 else '← ROTO, no usar'}")
    print(f"  LR conjunto con chi-cuadrado, tamaño:       {tam_asin:.2f}  "
          f"{'ok' if tam_asin <= 0.10 else '← sobredimensionado'}")
    print(f"  LR conjunto con crítico simulado, tamaño:   {tam:.2f}  "
          f"{'ok' if ok_tam else '← MAL CALIBRADO'}")
    print(f"  LR conjunto con crítico simulado, poder:    {pod:.2f}  "
          f"{'ok' if ok_pod else '← BAJO'}")
    print(f"  localización por variable: panel A {loc_a:.2f} · panel B {loc_b:.2f}")
    print()
    if ok_tam and ok_pod:
        print(f"  SIRVE, con una condición: el contraste CONJUNTO leído por LR contra el")
        print(f"  valor crítico simulado ({crit:.0f}, no el chi-cuadrado de 31,4). Así no")
        print("  rechaza cuando no hay nada y rechaza cuando hay algo. Es lo que puede")
        print("  decidir si el sistema inverso puro se sostiene.")
        print(f"  Poner CRITICO_LR = {crit:.0f} en hausman_exogeneidad.py.")
    else:
        print("  El contraste conjunto NO está en condiciones de decidir nada.")
    if min(loc_a, loc_b) < 0.80:
        print()
        print("  La LOCALIZACIÓN por variable no es confiable. En el panel A los tres")
        print("  orígenes contaminados comparten el mismo shock, sus residuos de primera")
        print("  etapa quedan correlacionados entre sí y el contraste de a uno se reparte")
        print("  el crédito hasta no encontrar nada en ninguno —o encontrarlo en el que no")
        print("  es—. O sea: el test puede decir CUÁNTA endogeneidad hay, pero no DÓNDE.")
        print("  Consecuencia práctica: alcanza para rechazar el sistema inverso puro, no")
        print("  para repartir los orígenes entre el bloque directo y el inverso. Para eso")
        print("  hacen falta instrumentos de verdad, no rezagos propios.")
    sys.exit(0 if (ok_tam and ok_pod) else 1)


if __name__ == "__main__":
    main()
