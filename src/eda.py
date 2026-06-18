import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Carga del .csv limpio
BASE_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE_DIR / "data" / "sensores_limpios.csv")

# Convertir fechas
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], errors="coerce")
df["time_stamp"] = pd.to_datetime(df["time_stamp"], errors="coerce")

print("====================================")
print("DESCRIPCIÓN DEL DATASET")
print("====================================")
print("Filas y columnas:", df.shape)
print("\nPrimeras filas:")
print(df.head())

print("\nInformación general:")
print(df.info())

print("\nValores nulos:")
print(df.isnull().sum())

# Estadística descriptiva igual que en el de limpieza.py
print("\n====================================")
print("ESTADÍSTICA DESCRIPTIVA")
print("====================================")
print(df.describe())

# Columnas numéricas principales
columnas_numericas = [
    "temperatura_c",
    "presion_psi",
    "vibracion_mm_s",
    "potencia_kw"
]

# Medidas de tendencia central esto segun el inge en la presentacion
print("\n====================================")
print("MEDIDAS DE TENDENCIA CENTRAL")
print("====================================")

for col in columnas_numericas:
    print(f"\nVariable: {col}")
    print("Media:", df[col].mean())
    print("Mediana:", df[col].median())
    print("Moda:", df[col].mode()[0])
    print("Desviación estándar:", df[col].std())
    print("Mínimo:", df[col].min())
    print("Máximo:", df[col].max())

# Distribución de variables categóricas, igual lo saque de la presentacion del inge
print("\n====================================")
print("VARIABLES CATEGÓRICAS")
print("====================================")

categoricas = [
    "maquina_id",
    "estado_operativo",
    "inspectedby",
    "tecnico_responsable",
    "lote_produccion"
]

for col in categoricas:
    print(f"\nFrecuencia de {col}:")
    print(df[col].value_counts())

# Histogramas, igual lo saque de la presentacion del inge
for col in columnas_numericas:
    plt.figure(figsize=(8, 5))
    plt.hist(df[col], bins=10)
    plt.title(f"Histograma de {col}")
    plt.xlabel(col)
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.savefig(BASE_DIR / "images" / f"histograma_{col}.png", bbox_inches="tight")
    plt.show()

# Boxplots para evaluar outliers, esto lo tenia en una imagen en la presentacion
for col in columnas_numericas:
    plt.figure(figsize=(8, 5))
    plt.boxplot(df[col])
    plt.title(f"Boxplot de {col}")
    plt.ylabel(col)
    plt.grid(True)
    plt.savefig(BASE_DIR / "images" / f"boxplot_{col}.png", bbox_inches="tight")
    plt.show()

# Matriz de correlación, esta es nueva pero me resulto interesante para el EDA
correlacion = df[columnas_numericas].corr()

print("\n====================================")
print("MATRIZ DE CORRELACIÓN")
print("====================================")
print(correlacion)

plt.figure(figsize=(8, 6))
plt.imshow(correlacion)
plt.colorbar()
plt.xticks(range(len(columnas_numericas)), columnas_numericas, rotation=45)
plt.yticks(range(len(columnas_numericas)), columnas_numericas)
plt.title("Mapa de correlación de variables numéricas")

# itero sobre el mapa y muestro los valores
for i in range(len(columnas_numericas)):
    for j in range(len(columnas_numericas)):
        plt.text(j, i, round(correlacion.iloc[i, j], 2),
                 ha="center", va="center")

plt.savefig(BASE_DIR / "images" / "mapa_correlacion.png", bbox_inches="tight")
plt.show()

# Promedios por máquina
promedio_maquina = df.groupby("maquina_id")[columnas_numericas].mean()

print("\n====================================")
print("PROMEDIOS POR MÁQUINA")
print("====================================")
print(promedio_maquina)

promedio_maquina.plot(kind="bar", figsize=(10, 6))
plt.title("Promedio de variables por máquina")
plt.xlabel("Máquina")
plt.ylabel("Promedio")
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig(BASE_DIR / "images" / "promedios_por_maquina.png", bbox_inches="tight")
plt.show()

# Estado operativo por máquina
estado_maquina = pd.crosstab(df["maquina_id"], df["estado_operativo"])

print("\n====================================")
print("ESTADO OPERATIVO POR MÁQUINA")
print("====================================")
print(estado_maquina)

estado_maquina.plot(kind="bar", figsize=(10, 6))
plt.title("Estado operativo por máquina")
plt.xlabel("Máquina")
plt.ylabel("Cantidad de registros")
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig(BASE_DIR / "images" / "estado_operativo_por_maquina.png", bbox_inches="tight")
plt.show()

print("\nEDA finalizado.")
print("Se generaron gráficas PNG en la carpeta images")