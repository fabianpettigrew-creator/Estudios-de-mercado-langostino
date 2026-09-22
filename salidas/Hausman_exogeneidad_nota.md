# Test de exogeneidad de Hausman sobre el sistema por origen

AXIA · nota de método · 22 de septiembre de 2026
Punto 7 de `Verificacion_consistencia_Barten_Tabarestani.md`, el único de esa lista que
puede cambiar el modelo y no sólo el número.

---

## Qué se pregunta

El sistema del §7 trata como predeterminadas las **cantidades** de los cinco orígenes.
Para Argentina eso es defendible: captura salvaje, la fija la biología y el calendario.
Para Ecuador, India y Vietnam es acuicultura, y Tabarestani, Keithly y Marzoughi-Ardakani
(2017) —el antecedente que el estudio cita como el más pertinente— sostienen lo contrario:
en camarón las cantidades importadas son endógenas y los precios de importación exógenos.
Su aporte es el sistema de demanda **mixta**.

El test decide cuál de las dos formas admite el dato. Se corre dos veces:

    sistema INVERSO (el de hoy)   w_i sobre log q  → se testean las CANTIDADES
    sistema DIRECTO (alternativa) w_i sobre log p  → se testean los PRECIOS

y el cruce dice en qué bloque va cada origen.

## Cómo

El Apéndice A de Tabarestani, que es una función de control (Durbin-Wu-Hausman en forma de
regresión aumentada): cada variable se regresa sobre sus rezagos de primer y segundo orden,
estacionalidad y tendencia; los residuos se agregan a todas las ecuaciones; Wald sobre cada
residuo y LR sobre todos juntos. Con adición impuesta se estiman cuatro ecuaciones, así que
cada residuo aporta cuatro coeficientes: Wald por variable contra χ² de 4, LR conjunto
contra χ² de 20.

`hausman_exogeneidad.py`. Corre sobre el panel EUMOFA por origen y repite todo en primeras
diferencias, porque varias series tienen raíz unitaria.

---

## Lo que apareció al validarlo, que es el resultado principal de esta nota

Antes de correrlo contra el dato real lo pasé por `validar_hausman.py`: tres paneles
simulados donde la endogeneidad está puesta a mano, 150 semillas cada uno. Dos con
endogeneidad —para medir **poder**— y uno sin nada —para medir **tamaño**—. Sin el panel
nulo no se puede afirmar que un rechazo signifique algo: un test que rechaza siempre
también acierta en los otros dos.

| | tamaño (nominal 0,05) | poder |
|---|---|---|
| **Wald conjunto**, 20 restricciones | **0,89** | 0,99 |
| **LR conjunto** contra χ²₂₀ = 31,4 | **0,19** | 0,85 |
| **LR conjunto** contra crítico simulado = 37 | **0,05** | 0,78 |

**El Wald conjunto está roto.** Rechaza el 89% de las veces cuando no hay absolutamente
nada que rechazar. Con veinte restricciones y una matriz HAC estimada sobre 160 meses, el
asintótico no llega ni de lejos. Un Wald conjunto significativo sobre el dato real no sería
evidencia de nada.

**El LR contra el χ² también rechaza de más** —19% contra un nominal de 5%—, aunque mucho
menos. Contra el **valor crítico simulado de 37** el tamaño queda en 0,047 y 0,053 y el
poder en 0,78 y 0,92. Ése es el contraste que sirve, y es el que el script usa.

Nada de esto está en el Apéndice A de Tabarestani, que informa Wald y LR sin calibrarlos.
Sus conclusiones las enuncia sobre el LR, que es lo correcto.

**Y la localización por variable no es confiable: acierta 0,38 y 0,65.** Cuando varios
orígenes comparten el mismo shock de demanda, sus residuos de primera etapa quedan
correlacionados entre sí y el contraste de a uno se reparte el crédito: no encuentra nada
en ninguno, o lo encuentra en el que no es. En una de las simulaciones el test declaró
exógenos a los tres orígenes contaminados y endógeno al único limpio.

**Consecuencia práctica, y es la que importa:** este test alcanza para **rechazar el
sistema inverso puro**, no para **repartir los orígenes** entre el bloque directo y el
inverso. La tabla de veredictos por origen que el script imprime es indicativa y hay que
leerla como tal. Para armar el sistema mixto con fundamento hacen falta instrumentos de
verdad —calendario de vedas, temperatura del mar, reclutamiento INIDEP, gasoil—, no rezagos
propios.

### Dos guardarraíles que la validación obligó a agregar

- **Degeneración.** Si los rezagos no predicen la variable, el residuo de primera etapa es
  casi la variable entera, que ya está en el sistema: la regresión aumentada queda casi
  singular y el Wald no distingue nada. En la primera versión del simulado eso daba R² de
  colinealidad de 0,99 y el test declaraba «exógenos» a los tres orígenes contaminados.
  Ahora el script mide ese R² y, por encima de 0,95, devuelve **indeterminado** en lugar de
  exógena. No son lo mismo: uno dice que la variable es predeterminada, el otro que el test
  no contesta.
- **Autocorrelación.** La validez de todo esto descansa en que los rezagos propios no
  correlacionen con el error estructural. Si el error del sistema está autocorrelacionado
  —y Tabarestani encontró correlación serial y la corrigió con un AR(1)— el rezago deja de
  ser instrumento válido. El script informa la ρ de primer orden de los residuos junto con
  el veredicto y avisa cuando pasa de 0,30.

---

## Estado

**Escrito y validado; falta correrlo contra el dato real.** Las bases están en
`OneDrive\BASES DE DATOS` y no en el repositorio, así que acá sólo pude correrlo de punta
a punta sobre paneles simulados. El circuito completo funciona, incluidas la repetición en
diferencias y la salida a Excel.

```
python validar_hausman.py          # 150 semillas por panel, confirma tamaño y poder
python hausman_exogeneidad.py      # el test contra datos/eumofa_camaron_origen.pkl
```

`validar_hausman.py` termina con código 1 si el test deja de estar calibrado, así que
conviene correrlo primero: si el panel de la casa cambia de largo, el valor crítico
simulado se mueve y el script lo dice.

### Cómo leer lo que salga

1. **Mirar primero la primera etapa.** Si el F de los rezagos es chico, para esa variable
   el test no tiene poder y el «exógena» no dice nada.
2. **Después el LR conjunto contra 37**, no contra 31,4 y nunca el Wald.
3. **La tabla por origen, al final y con pinzas.** Sirve para orientar, no para decidir.
4. **Si el LR conjunto rechaza**, el sistema inverso puro del §7 no se sostiene y hay que
   ir al mixto de Tabarestani. Cuáles orígenes van en cada bloque no lo contesta este test.
5. **Si no rechaza**, el sistema inverso queda en pie —con la reserva de que el poder
   contra el crítico simulado es 0,78, así que un no rechazo no es una absolución.

---

### Fuentes

Tabarestani, M., Keithly, W.R. y Marzoughi-Ardakani, H. (2017), «An Analysis of the US
Shrimp Market: A Mixed Demand Approach», *Marine Resource Economics* 32(4), 411-429 —
Apéndice A y cuadro A1. Hausman, J.A. (1978), «Specification tests in econometrics»,
*Econometrica* 46(6).

Código: `hausman_exogeneidad.py` (el test), `validar_hausman.py` (la validación contra
ground truth simulado). Salida: `salidas/hausman_exogeneidad.xlsx`.
