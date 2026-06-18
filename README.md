Tarea 2
# Data Cleaning + EDA Analysis - Sensores IoT

## Descripción del proyecto

Este tarea realiza la limpieza, transformación y análisis exploratorio de un dataset de sensores IoT perteneciente a máquinas críticas de una planta industrial.

El objetivo principal es identificar patrones en variables como temperatura, presión, vibración y potencia, con el fin de apoyar decisiones relacionadas con mantenimiento predictivo.

## Archivos principales

- `data/Production_RawDataSet.csv`: dataset original.
- `data/sensores_limpios.csv`: dataset limpio.
- `src/limpieza.py`: script de limpieza de datos.
- `src/eda.py`: script de análisis exploratorio.
- `images/`: visualizaciones generadas durante el EDA.

## Proceso realizado

1. Carga del dataset original.
2. Revisión de estructura, tipos de datos y valores nulos.
3. Limpieza de valores faltantes.
4. Corrección de categorías inconsistentes.
5. Tratamiento de valores extremos y fuera de rango.
6. Estandarización de fechas y columnas.
7. Generación del dataset limpio.
8. Análisis exploratorio de datos.
9. Generación de histogramas, boxplots y matriz de correlación.
10. Interpretación de resultados para mantenimiento predictivo.

## Librerías utilizadas

- pandas
- numpy
- matplotlib
- openpyxl

## Ejecución del proyecto

Para ejecutar la limpieza:

```bash
python src/limpieza.py
```

Para ejecutar el EDA:

```bash
python src/limpieza.py
```

## Resultados principales

El análisis permitió identificar que las variables temperatura, presión y potencia presentan una alta correlación entre sí. Además, la variable vibración mostró un valor atípico relevante, el cual puede representar una señal temprana de falla mecánica.

Estos resultados pueden apoyar la definición de alertas tempranas y planes de mantenimiento preventivo basados en datos.