# pip install scikit-learn pandas numpy

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# ====================
# 1. Se crean datos de simulacion
# ====================
# Para que salgan resultados parecidos
np.random.seed(42)

# Datos normales (Compras comunes) o Gastos normales
datos_normales = np.random.normal(loc=200, scale=50, size=100)

#Evitar valores negativos (seguridad)
datos_normales = np.clip(datos_normales, a_min=1, a_max=None)

# Datos anomalos (compras muy altas o fuera de lugar)
datos_anomalos = np.array([1000,5000,8500])

#unimos todo los datos
datos = np.concatenate([datos_normales,datos_anomalos])

# convertir a DataFrame
df = pd.DataFrame(datos, columns=["monto_compra"])

# ====================
# 2. Creacion del modelo
# ====================
# Modelo no supervisado
modelo = IsolationForest(contamination=0.05, random_state=42)
modelo.fit(df[["monto_compra"]])

# ====================
# 3. Deteccion de Anomalias
# ====================

# Predic devuelve:
# 1 = normal
# -1 = anormal

df["anomalia"] = modelo.predict(df[["monto_compra"]])
df["resultado"] = df["anomalia"].map({1: "Normal", -1: "Anomalo"})

# ====================
# 4. Resultados
# ====================

print("\n Resultados principales")
print(df.sort_values(by="monto_compra", ascending=False). head(10))

# ====================
# 5. Probar con nuevos valores
# ====================

nuevo = pd.DataFrame([[250],[1800]], columns=["monto_compra"])
pred = modelo.predict(nuevo)

# print("\n Resultados nuevos")
# for valor, p in zip(nuevo["monto_compra"], pred):
#     if p==-1:
#         print(f"Q{valor} is ANOMALO")
#     else:
#         print(f"Q{valor} is Normalito")
