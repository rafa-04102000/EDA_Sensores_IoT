import pandas as pd
import numpy as np
from pathlib import Path

# Cargo el .csv original pandas lo convierte a dataframe, con el separador ";" aunque en el .csv este por celdas
BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / "data" / "Production_RawDataSet.csv", sep=";")

print("Dataset original:", df.shape)

# 1. Normalizar nombres de columnas
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Columnas normalizadas:")
print(df.columns)

# 2. Convertir fecha_hora a formato datetime
df["fecha_hora"] = pd.to_datetime(
    df["fecha_hora"],
    errors="coerce",
    dayfirst=True
)

# 3. Convertir time_stamp a datetime
# Algunos datos tienen minutos inválidos, por eso use errors='coerce'
df["time_stamp"] = pd.to_datetime(
    df["time_stamp"],
    errors="coerce"
)

# 4. Reemplazar valores imposibles por NaN
# tome los valores de referencia para estandarizar
# Temperatura industrial razonable: 0 a 200 °C
df.loc[
    (df["temperatura_c"] < 0) | (df["temperatura_c"] > 200),
    "temperatura_c"
] = np.nan

# Presión razonable: 0 a 150 psi
df.loc[
    (df["presion_psi"] < 0) | (df["presion_psi"] > 150),
    "presion_psi"
] = np.nan

# Vibración razonable: 0 a 50 mm/s
df.loc[
    (df["vibracion_mm_s"] < 0) | (df["vibracion_mm_s"] > 50),
    "vibracion_mm_s"
] = np.nan

# Potencia razonable: 1 a 50 kW
df.loc[
    (df["potencia_kw"] < 1) | (df["potencia_kw"] > 50),
    "potencia_kw"
] = np.nan

# 5. Limpiar categorías
# LOTX001 este sera el estandar el LOT/001 lo cambio, y el tecnico zzzzzzzz lo pongo como nulo

df["inspectedby"] = df["inspectedby"].str.strip().str.lower()
df["estado_operativo"] = df["estado_operativo"].str.strip().str.upper()
df["maquina_id"] = df["maquina_id"].str.strip().str.upper()
df["tecnico_responsable"] = df["tecnico_responsable"].str.strip().str.title()
df["lote_produccion"] = df["lote_produccion"].str.strip().str.upper()

# cambio el lote_produccion inconsistente
df["lote_produccion"] = df["lote_produccion"].replace({
    "LOT/001": "LOT-001",
    "LOTX001": "LOT-001"
})

# tecnico inválido
df["tecnico_responsable"] = df["tecnico_responsable"].replace({
    "Zzzzzzzz": np.nan
})


# 6. Completar valores faltantes

# Para variables numéricas use la mediana
columnas_numericas = [
    "temperatura_c",
    "presion_psi",
    "vibracion_mm_s",
    "potencia_kw"
]

for col in columnas_numericas:
    df[col] = df[col].fillna(df[col].median())

# Para variables categóricas puse "No especificado"
columnas_categoricas = [
    "inspectedby",
    "maquina_id",
    "tecnico_responsable",
    "lote_produccion"
]

for col in columnas_categoricas:
    df[col] = df[col].fillna("No especificado")

# 7. Eliminar duplicados exactos
df = df.drop_duplicates()
# aca anteriormente me salian en 0 asi que no creo que quite nada

# 8. Eliminar fechas fuera de rango lógico
# Segun el .csv origina solo habia entre 2025 y 2026, dejamos solo estos años 2025 y 2026
df = df[
    (df["fecha_hora"].dt.year >= 2025) &
    (df["fecha_hora"].dt.year <= 2026)
]

# 9. Resultado final
print("\nDataset limpio:", df.shape)
print("\nValores nulos después de limpieza:")
print(df.isnull().sum())
# toddavia marca unos en los campos time_stamp

print("\nEstadística después de limpieza:")
print(df.describe())

# 10. Guardo el dataset limpio
df.to_csv(BASE_DIR / "data" / "sensores_limpios.csv", index=False, encoding="utf-8")

print("\nSe creo el dataset limpio: ./data/sensores_limpios.csv")