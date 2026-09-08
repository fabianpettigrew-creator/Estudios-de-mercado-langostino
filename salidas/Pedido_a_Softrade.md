# Pedido a Softrade

AXIA · 22 de agosto de 2026 · para reenviar al proveedor

Quedan **cuatro** pedidos. El primero de la lista original se descartó: era limitación del
registro de origen, no de la extracción.
Todo lo que sigue está verificado sobre las descargas que ya tenemos —base de exportación
argentina, langostino, partidas 0306.17.10 y 0306.17.90, 2013 a 2026— y en cada punto va la
evidencia para que del otro lado no haya que adivinar de qué se habla.

---

## 1. ~~Junio a octubre de 2017~~ — DESCARTADO

**No hay que pedirlo.** Confirmado con la industria: el tramo en que la columna
`Marca o Descripcion` viene con el literal «No disponible» —junio a septiembre de 2017 en el
100% de los despachos, octubre en el 29%— es una **limitación del registro de origen**, no de
la extracción. El proveedor no lo tiene.

Queda resuelto por otra vía, sin pedirle nada a nadie: como el 94-97% del entero embarcado
entre mayo y octubre es congelado a bordo, el FOB del entero del registro oficial de aduana en
esos meses sirve de proxy del precio tangonero, no tiene huecos y recupera las campañas
2015/2016 y 2017/2018. Ver la sección correspondiente de
`Demanda_inversa_tangonera_resultados.md`.

## 2. El campo `Exportador` viene «No disponible» en toda la serie

**Qué pasa.** La columna **`Exportador`** existe en todas las descargas, de 2013 a 2026, y en
**todas** trae el literal «No disponible». Cero filas con dato, en catorce años.

**Para qué lo queremos.** Para controlar por composición de vendedores —saber si un movimiento
de precio es de mercado o de mezcla de exportadores— y para asignar flota por empresa en los
años en que la descripción no declara la forma de congelado.

**La pregunta concreta.** ¿El plan contratado puede incluir la razón social del exportador?
¿Se puede aplicar **retroactivamente** a la serie histórica o sólo de acá en adelante? Si hay
un costo adicional, cuál.

*(Nota: desde 2018 la descripción trae la marca comercial en el bloque `AA(...)` —Conarpesa,
Arbumasa, Pesquera Santa Cruz, Pescanova, Moscuzza, Empesur, Vieirasa, Profand— y con eso
identificamos la firma en el 97,9% de los despachos de entero. O sea que para 2018-2026 hay un
sustituto; el campo formal serviría sobre todo para 2013-2017 y para no depender de la marca.)*

---

## 3. Falta la columna `Condición de Venta` en la descarga de 2023

**Qué pasa.** El archivo de 2023 no trae la columna **`Condición de Venta`** (FOB / CFR / FCA /
CIF). Todas las demás descargas, de 2020 a 2026, sí la traen.

**Por qué importa.** La composición se mueve fuerte: en 2020 el 35% de los despachos de entero
eran CFR y en 2024 el 2%. Un cambio de mix de esa magnitud se cuela en el valor unitario si no
se controla, y para controlarlo hace falta la serie completa.

**La pregunta concreta.** Re-descargar 2023 con esa columna, y confirmar que está disponible
también para 2013-2019.

---

## 4. ¿Existe el sufijo de valor como campo estructurado?

**Qué pasa.** Desde diciembre de 2017 la descripción viene ya parseada en bloques:
`AA(marca)-AI(calibre)-AJ(envase)-CA00-CB00-SA00-NA01-NB01-`. Nosotros la volvemos a partir
con expresiones regulares para sacar marca, calibre y el sufijo **SA**, que es el que marca
congelado a bordo.

**La pregunta concreta.** ¿Tienen esos sufijos de valor como **columnas separadas** en la base?
Si es así, pedimos que vengan así en la descarga: elimina de un saque el riesgo de parseo y
homogeneiza el tratamiento de las dos épocas.

---

## 5. ~~Enero a junio de 2016~~ — también descartado

Misma explicación: la descripción está presente pero ninguna de las 4.204 filas de esos meses
trae calibre ni la leyenda de congelado a bordo. Es la práctica de declaración de la época, no
un recorte de la extracción. También queda cubierto por el proxy de temporada.

---

## 6. Base de Ecuador: no viene declarada la unidad del conteo de talla

**Qué pasa.** En la base de exportación de Ecuador a España (0306.17.99, 2020 a julio de
2026) la talla viaja sólo dentro de `Descripción Comercial`, con la forma `T. 30/40`, y
**nunca se declara la unidad**: ninguna de las 716 filas con talla dice si el conteo es por
kilo o por libra. Y conviven las dos convenciones: el **93,7%** de los kilos está en bandas
de decena —20/30 a 80/100, que es como grada la Unión Europea, por kilo—, el **4,8%** en la
escalera estándar de Estados Unidos —16/20, 21/25, 26/30 hasta 71/90, que se cuenta por
libra— y el **1,5%** en bandas irregulares con errores de tipeo evidentes (`80/10`, `60/40`
invertido).

**Por qué importa.** Del lado argentino el nomenclador define el calibre en piezas por kilo
(NA01 = 11 a 20 = L1), así que toda comparación de talla contra el competidor cuelga de esta
unidad. Leyendo todo como por kilo el gradiente precio-talla da −0,277; convirtiendo la
escalera americana a piezas por kilo, −0,112. El descuento estimado del L1 argentino contra
producto ecuatoriano comparable se mueve entre el **6% y el 23%** según cómo se lean 108
filas. Hoy reportamos la submuestra homogénea para no tener que decidirlo, pero es un parche.

**Y falta la presentación.** Ninguna de esas filas declara si es HOSO —entero con cabeza— o
HLSO —descabezado con caparazón—. Para el mismo animal el conteo por kilo cambia mucho entre
una y otra, así que la estimación mezcla dos productos distintos.

**La pregunta concreta.** ¿La base tiene la unidad del conteo y la presentación como campos
estructurados? Si no los tiene, ¿pueden confirmar con la fuente cuál es la convención con que
se declara la talla, y si es uniforme a lo largo de la serie?

---

## Prioridad, si hay que elegir

1. **Exportador** — es el único que abre una línea de trabajo nueva.
2. **Unidad del conteo de talla en la base de Ecuador** — sin eso, el descuento por talla
   queda con un rango de 6% a 23% y no se puede publicar como número.
3. Condición de venta de 2023 y sufijos como columnas — son de higiene, pero baratos.

---

### Borrador de correo

> Estimados,
>
> Estamos trabajando con la base de exportación de langostino que nos proveen (partidas
> 0306.17.10 y 0306.17.90, período 2013-2026) y necesitamos consultarles cuatro puntos:
>
> 1. La columna **`Exportador`** trae «No disponible» en todas las filas de toda la serie.
>    ¿Puede habilitarse en nuestro plan? ¿Aplica retroactivamente a la serie histórica?
>    Si tiene costo adicional, agradecemos la cotización.
>
> 2. El archivo de **2023** no incluye la columna **`Condición de Venta`**, que sí está en el
>    resto de los años. ¿Pueden re-generarlo con esa columna? ¿Está disponible también para
>    2013-2019?
>
> 3. Desde diciembre de 2017 la descripción viene estructurada en bloques `AA(...)-AI(...)-
>    SA00-`. ¿Disponen de esos **sufijos de valor como campos separados** en la base? De ser
>    así, preferiríamos recibirlos como columnas.
>
> 4. En la base de **exportación de Ecuador** (0306.17.99 a España, 2020-2026) la talla
>    aparece dentro de la descripción comercial, con la forma `T. 30/40`, pero sin indicar
>    si el conteo es **por kilo o por libra** —y en la misma serie conviven bandas de las dos
>    convenciones—. ¿Disponen de la unidad del conteo y de la presentación (HOSO / HLSO) como
>    campos estructurados? Si no, ¿pueden confirmarnos cuál es la convención de la fuente?
>
> Quedamos a disposición para cualquier aclaración.
