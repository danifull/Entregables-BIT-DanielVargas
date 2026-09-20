import pandas as pd         
import numpy as np

df = pd.read_csv("animal_data_dirty1.csv", sep=";", encoding="utf-8-sig")

# Diagnóstico inicial

filas, columnas = df.shape
print(f"\n- Filas: {filas}")
print(f"- Columnas: {columnas}")

print("\n- Columnas y tipos de dato:")
print(df.dtypes)

print("\n- Valores faltantes por columna:")
print(df.isnull().sum())

print(f"\n- Registros duplicados: {df.duplicated().sum()}")

print("\n- Categorías sospechosas en 'Animal type':")
print(df["Animal type"].value_counts(dropna=False))

print("\n- Categorías sospechosas en 'Country':")
print(df["Country"].value_counts(dropna=False))

print("\n- Categorías sospechosas en 'Gender':")
print(df["Gender"].value_counts(dropna=False))


# Limpieza de datos

df_limpio = df.copy()
df_limpio = df_limpio.drop(columns=["Animal code"])

antes = len(df_limpio)
df_limpio = df_limpio.drop_duplicates()
print(f"\nDuplicados eliminados: {antes - len(df_limpio)}")

df_limpio = df_limpio.dropna(thresh=5)

df_limpio["Animal type"] = (
    df_limpio["Animal type"]
      .str.lower()                   
      .str.replace("™", "", regex=False)  
      .str.replace("?", "", regex=False) 
      .str.strip()                   
)

correcciones_animal = {
    "red squirrell": "red squirrel",
    "red squirel":   "red squirrel",
    "european bisson": "european bison",
    "european buster": "european bison",
    "ledgehod": "hedgehog",
    "wedgehod": "hedgehog",
}
df_limpio["Animal type"] = df_limpio["Animal type"].replace(correcciones_animal)

df_limpio["Country"] = df_limpio["Country"].str.strip()

correcciones_pais = {
    "PL": "Poland",
    "HU": "Hungary",
    "Hungry": "Hungary",
    "CZ": "Czech Republic",
    "Czech": "Czech Republic",
    "DE": "Germany",
}
df_limpio["Country"] = df_limpio["Country"].replace(correcciones_pais)

df_limpio.loc[df_limpio["Country"].isin(["CC", "Australia"]), "Country"] = np.nan

df_limpio["Observation date"] = pd.to_datetime(
    df_limpio["Observation date"], format="%d.%m.%Y", errors="coerce"
)

for col in ["Weight kg", "Body Length cm"]:
    df_limpio[col] = df_limpio.groupby("Animal type")[col].transform(
        lambda s: s.fillna(s.median())
    )

df_limpio["Gender"] = df_limpio["Gender"].fillna("not determined")

print("\n- Nulos despues de limpiar:")
print(df_limpio.isnull().sum())

print(f"\n- Duplicados despuss de limpiar: {df_limpio.duplicated().sum()}")

print("\n- 'Animal type' despues de estandarizar:")
print(df_limpio["Animal type"].value_counts(dropna=False))

print("\n- 'Country' despues de estandarizar:")
print(df_limpio["Country"].value_counts(dropna=False))

print("\n- Tipos de dato despues de limpiar:")
print(df_limpio.dtypes)

# NumPy

df_limpio["Tamaño"] = np.where(df_limpio["Weight kg"] > 50, "Grande", "Pequeño")

print("\n- Conteo de la nueva variable 'Tamaño':")
print(df_limpio["Tamaño"].value_counts())

peso_promedio = np.nanmean(df_limpio["Weight kg"])
peso_mediana = np.nanmedian(df_limpio["Weight kg"])
peso_desviacion = np.nanstd(df_limpio["Weight kg"])

print(f"\n- Peso promedio (np.nanmean): {peso_promedio:.2f} kg")
print(f"- Peso mediana (np.nanmedian): {peso_mediana:.2f} kg")
print(f"- Desviación estándar del peso (np.nanstd): {peso_desviacion:.2f} kg")


# analisis con groupby()

obs_por_animal = df_limpio.groupby("Animal type").size().sort_values(ascending=False)
print("\n- Número de observaciones por tipo de animal:")
print(obs_por_animal)

peso_por_animal = df_limpio.groupby("Animal type")["Weight kg"].mean().round(2)
print("\n- Peso promedio (kg) por tipo de animal:")
print(peso_por_animal.sort_values(ascending=False))

peso_por_pais = df_limpio.groupby("Country")["Weight kg"].mean().round(2)
print("\n- Peso promedio (kg) por país:")
print(peso_por_pais.sort_values(ascending=False))

long_por_genero = df_limpio.groupby("Gender")["Body Length cm"].mean().round(2)
print("\n- Longitud corporal promedio (cm) por genero:")
print(long_por_genero)

obs_pais_animal = df_limpio.groupby(["Country", "Animal type"]).size().unstack(fill_value=0)
print("\n- Observaciones por país y tipo de animal:")
print(obs_pais_animal)

animal_mas_observado = obs_por_animal.idxmax()
cantidad_mas_observado = obs_por_animal.max()
total_obs = obs_por_animal.sum()
porcentaje = (cantidad_mas_observado / total_obs) * 100

animal_mas_pesado = peso_por_animal.idxmax()
peso_mas_pesado = peso_por_animal.max()
animal_mas_liviano = peso_por_animal.idxmin()
peso_mas_liviano = peso_por_animal.min()

pais_mayor_peso = peso_por_pais.idxmax()
peso_pais_mayor = peso_por_pais.max()

conclusiones = f"""
CONCLUSION 1 — Especie dominante en las observaciones.
  El '{animal_mas_observado}' es la especie más registrada, con
  {cantidad_mas_observado} observaciones que representan aproximadamente el
  {porcentaje:.1f}% del total ({total_obs} registros limpios). Esto indica
  que el esfuerzo de muestreo estuvo concentrado en esta especie o que es
  la más abundante en la región estudiada, y hay que tenerlo en cuenta
  porque el dataset NO está balanceado entre especies.

CONCLUSION 2 — Enorme diferencia de peso entre especies.
  El '{animal_mas_pesado}' tiene el peso promedio más alto ({peso_mas_pesado:.2f} kg),
  mientras que el '{animal_mas_liviano}' tiene el más bajo ({peso_mas_liviano:.2f} kg).
  Esta diferencia de más de {(peso_mas_pesado / peso_mas_liviano):.0f} veces
  explica por qué el promedio general de peso ({peso_promedio:.2f} kg) es
  mucho más alto que la mediana ({peso_mediana:.2f} kg): pocas observaciones
  de animales grandes desplazan el promedio, típico de distribuciones
  orientadas a la derecha.

CONCLUSION 3 — El país influye en el peso promedio observado.
  '{pais_mayor_peso}' presenta el peso promedio más alto por país
  ({peso_pais_mayor:.2f} kg). Esto NO significa que los animales sean más
  pesados ahí por biología, sino que probablemente en ese país se
  observaron especies más grandes (como el bisonte europeo), mientras que
  en otros países predominan especies pequeñas. Es un caso claro donde la
  composición de especies por país sesga el promedio.

CONCLUSION 4 — La calidad original del dataset era pobre.
  Se detectaron y corrigieron 167 filas duplicadas, una columna
  completamente vacía ('Animal code'), y al menos 8 variantes mal escritas
  para 'Animal type' y 6 para 'Country'. Sin esta limpieza, un analisis
  directo habría reportado 12 tipos de animales cuando en realidad son 4,
  y habría contado a "Poland" y "PL" como países distintos. La leccion es
  que en datos recolectados por multiples personas la estandarización
  previa es OBLIGATORIA antes de cualquier analisis.
"""

print(conclusiones)

df_limpio.to_csv("animal_data_limpio.csv", index=False)
print("\nArchivo 'animal_data_limpio.csv'")
