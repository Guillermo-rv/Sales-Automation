import pandas as pd

# Cargar el archivo de Excel
file_path = "Leads_B2B.xlsx"
df = pd.read_excel(file_path)

# 🔹 Exploración rápida de datos
print("📊 Primeras filas del dataset:")
print(df.head())  # Primeras 5 filas

print("\n🔹 Información general del dataset:")
print(df.info())  # Información sobre tipos de datos y valores nulos

print("\n📌 Descripción estadística:")
print(df.describe())  # Resumen estadístico de las columnas numéricas

print("\n🧐 Valores nulos en cada columna:")
print(df.isnull().sum())  # Recuento de valores nulos por columna

print("\n📈 Distribución de 'Lead Score':")
print(df["Lead_Score"].describe())  # Distribución del lead score

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# 📌 Cargar el dataset
file_path = "Leads_B2B.xlsx"
df = pd.read_excel(file_path)

# 📊 Explorar el dataset
def explore_data(df):
    print("📊 Primeras filas del dataset:")
    print(df.head())
    print("\n🔹 Información general del dataset:")
    print(df.info())
    print("\n📌 Descripción estadística:")
    print(df.describe())
    print("\n🧐 Valores nulos en cada columna:")
    print(df.isnull().sum())

explore_data(df)

# 🔹 Seleccionar características clave para el modelo
features = [
    "Crecimiento_Empleados(%)", "Ingresos_Anuales(€M)", "Presencia_Global(Países)",
    "Interacción_Correos(%)", "Tamaño_Equipo_IT"
]
X = df[features]
y = (df["Lead_Score"] > 40).astype(int)  # 1 = Alta conversión, 0 = Baja conversión

# 🔄 Normalización
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 🏋️‍♂️ División de datos
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 🌲 Entrenar modelo de clasificación
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 💾 Guardar modelo y escalador
joblib.dump(model, "lead_scoring_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Modelo entrenado y guardado como 'lead_scoring_model.pkl'")
print("✅ Escalador guardado como 'scaler.pkl'")
