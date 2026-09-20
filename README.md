# Agente de estudios de mercado — langostino

Informe mensual automatizado sobre importaciones de camarón y langostino en
Estados Unidos y la Unión Europea, con foco en la posición argentina frente al
vannamei de cultivo.

## Arquitectura

Tres capas. La ingesta y el almacenamiento son determinísticos, sin modelo de
lenguaje. El agente solo interviene en la capa de análisis y redacción, y solo
puede ver números que salen de la base.

```
fuentes/noaa.py      → API FOSS de NOAA (importaciones de EE.UU.)
fuentes/eurostat.py  → Comext SDMX (importaciones de la UE)
almacen.py           → SQLite: una tabla de observaciones, todo lo demás por consulta
herramientas.py      → las cinco funciones que el agente puede llamar
reporte.py           → Excel + briefing para redactar el informe en Claude.ai
agente.py            → variante automática (requiere API paga, opcional)
ingesta.py           → lo que va en el cron
```

## Instalación

```bash
pip install requests pandas openpyxl
```

No hace falta clave de API para el camino principal (ver abajo).

## Primer arranque

```bash
# 1. Verificá que Comext responde y con qué nombres de dimensión
python -m fuentes.eurostat

# 2. Traé tres años de historia (tarda: son muchas páginas)
python ingesta.py --desde 2023

# 3. Generá el Excel y el briefing del último mes cerrado
python reporte.py 2026 5
```

Si Comext da problemas el primer día, arrancá solo con NOAA:

```bash
python ingesta.py --desde 2023 --sin-ue
```

## Dos formas de producir el informe

**Sin costos (recomendada para empezar).** `reporte.py` genera un Excel con
las series y un briefing en markdown con los números del mes. Se copia el
briefing, se pega en Claude.ai y el informe se redacta ahí en conversación.
Solo requiere Python. Es además la opción con mejor control: vos ves los
números antes de que se escriba una sola línea de análisis.

**Automática.** `agente.py` hace lo mismo sin intervención humana, pero
necesita una clave de API de console.anthropic.com, que se paga por uso
aparte de la suscripción de Claude. Tiene sentido recién cuando el circuito
ya corrió varios meses y confiás en los datos.

Empezá siempre por la primera. La segunda no agrega calidad al análisis:
agrega desatención.

## Antes de darlo por bueno

Tres cosas hay que confirmar contra datos reales, no se pueden dar por
sentadas desde el escritorio:

1. **La partida CN del langostino argentino.** El código asume `03061799`
   ("los demás"), que es donde corresponde clasificar a *Pleoticus muelleri*
   por no ser del género *Penaeus*. Cruzá un mes contra despachos conocidos:
   si aparece volumen argentino en `03061792`, hay clasificación cruzada y el
   filtro tiene que abrirse.

2. **Los nombres de indicador de Comext.** `_detectar_indicadores()` prueba
   varios candidatos y usa el primero que devuelve datos, pero si Eurostat los
   renombra todos vas a ver series vacías, no un error. Una serie en cero
   nunca es un dato: es una falla hasta que se demuestre lo contrario.

3. **Las unidades de cantidad.** Comext históricamente publica en quintales
   (100 kg). El código convierte si el nombre del indicador contiene `100KG`.
   Verificá un mes contra una fuente conocida: un factor 100 de error en
   volumen pasa desapercibido si nadie mira el nivel absoluto.

## Automatización

```cron
0 6 5 * * cd /ruta/langostino_agente && python ingesta.py >> logs/ingesta.log 2>&1
0 8 5 * * cd /ruta/langostino_agente && python reporte.py $(date +\%Y) $(date -d '-2 month' +\%m)
```

Día 5 porque NOAA publica unos 43 días después del cierre del mes estadístico.
La ingesta es idempotente: correrla de más reescribe con los datos revisados,
no duplica.

## Decisiones de diseño

**El precio implícito no se guarda, se calcula.** Es valor sobre kilos del
agregado. Guardarlo invitaría a promediar precios unitarios, que da un número
distinto y equivocado.

**El modelo no calcula.** Las herramientas devuelven cifras ya computadas en
SQL. Si el agente necesita un número que ninguna herramienta da, la respuesta
correcta es decir que no está disponible. Esto no es prudencia excesiva: un
informe que va a cámara empresaria con un dato inventado cuesta más que doce
informes que dicen "no hay dato".

**El agente lee el informe anterior.** Sin eso, un informe mensual repite las
mismas generalidades todo el año. La comparación contra lo dicho el mes pasado
es lo que lo hace valer más que un reporte automático.

## Qué falta

- Salida a Excel y PowerPoint (conectar con el pipeline de C.A.Pe.C.A que ya existe)
- Exportaciones de Ecuador (CNA publica mensual y rápido, pero en PDF/Excel, no API)
- Serie FOB de INDEC para cerrar el circuito origen-destino
- Precios de góndola, para el spread FOB–retail


## Donde estan las bases (actualizado 19/09/2026)

Las bases originales ya no estan en `IA agentes`: se mudaron a la biblioteca
comun `OneDrive\BASES DE DATOS` (ver su LEEME.md). Ningun programa tiene la ruta
escrita a mano: todos la piden con `from biblioteca import fuente`, que lee el
mapa `BASES DE DATOS\rutas_bases.py`.

| Antes (IA agentes)                         | Ahora (BASES DE DATOS)                                        | Clave            |
|--------------------------------------------|---------------------------------------------------------------|------------------|
| Softrade lango 2025 2026                   | 02 Comercio exterior\Softrade\Langostino 2025-2026            | softrade_langostino, aduana_ar, aduana_control |
| Desembarques historicos argentina          | 01 Pesca...\Desembarques SSPyA historicos                     | desembarques_ar  |
| INIDEP LANGOSTINO                          | 01 Pesca...\INIDEP langostino                                 | inidep_langostino|
| ACTAS CFP                                  | 01 Pesca...\Actas CFP                                         | actas_cfp        |
| CSV/XLSX de FAO FishStat y ASFIS           | 01 Pesca...\FAO FishStat                                      | fao_fishstat     |
| EXPO ECUADOR                               | 02 Comercio exterior\Ecuador exportaciones camaron            | expo_ecuador     |
| DATOS PESCA EEUU PROYECTO CLAUDE           | 02 Comercio exterior\EEUU importaciones NOAA                  | eeuu_noaa        |
| TradeMap, Exportadores/Importadores 030617 | 02 Comercio exterior\TradeMap                                 | trademap         |
| DATOS PESCA UE...\Bases para analizar      | 03 Mercado europeo - EUMOFA\EUMOFA (unificada)                | eumofa_ue        |
| Bases para analizar                        | 03 Mercado europeo - EUMOFA\EUMOFA (unificada)                | eumofa_a         |
| Scraping\datos_precios                     | 04 Precios minoristas - Scraping\datos_precios                | scraping_precios |

Quedan en `IA agentes`: HORECA_indice_mensual.xlsx (lo lee demanda_inversa_horeca.py
una carpeta mas arriba), serie_ipi_pesquero.xlsx, produccion_vannamei_langostino_2015-2024.xlsx
y los documentos del estudio.
