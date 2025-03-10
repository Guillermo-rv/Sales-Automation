
import os
import pandas as pd
import numpy as np
import faiss
import joblib
from dotenv import load_dotenv
from mistralai import Mistral

#  Cargar variables de entorno
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError(" ERROR: API Key de Mistral.")

# Cargar el dataset y el modelo entrenado
print(" Cargando dataset y modelo...")
file_path = "Leads_B2B.xlsx"
df = pd.read_excel(file_path)

# Selección
features = [
    "Crecimiento_Empleados(%)", "Ingresos_Anuales(€M)",
    "Presencia_Global(Países)", "Interacción_Correos(%)",
    "Tamaño_Equipo_IT"
]
X = df[features].values

#  Normalizar
print(" Normalizando datos...")
scaler = joblib.load("scaler.pkl")
X_scaled = scaler.transform(X)

# 🔹 Crear índice FAISS
print(" Creando índice FAISS...")
dimension = X_scaled.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(X_scaled)

#  Guardar índice FAISS
faiss.write_index(index, "faiss_leads.index")
print(" Índice FAISS creado y guardado como 'faiss_leads.index'")

#  Función para buscar leads similares
def find_similar_leads(query_data, k=5):
    query_scaled = scaler.transform([query_data])
    distances, indices = index.search(query_scaled, k)
    return df.iloc[indices[0]], distances[0]

#  Función para analizar leads con Mistral AI
def analyze_leads_with_mistral(leads_df):
    lead_summary = leads_df.to_string(index=False)
    messages = [
        {"role": "system", "content": "Eres un experto en ventas B2B y análisis de datos. Tu tarea es analizar leads y recomendar estrategias de conversión."},
        {"role": "user", "content": f"""Aquí están los 5 leads más similares encontrados:\n\n{lead_summary}\n
        1. ¿Cuál de estos leads tiene más probabilidad de conversión?
        2. ¿Por qué?
        3. ¿Qué estrategia de venta recomendarías para este lead?"""}
    ]

    try:
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(model="mistral-small", messages=messages)
        print("\n Análisis de Mistral AI:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error al obtener el análisis de Mistral AI: {e}")

#  Prueba de búsqueda y análisis
if __name__ == "__main__":
    print(" Cargando dataset y modelo...")

    query_example = df.iloc[10][features].values
    similar_leads, dists = find_similar_leads(query_example)

    print("\n Leads más similares encontrados:")
    print(similar_leads)
    print("\n Distancias FAISS:", dists)

    analyze_leads_with_mistral(similar_leads)


    '''

 Leads más similares encontrados:
       Nombre   Apellido             Empresa  ... Interacción_Correos(%) Tamaño_Equipo_IT  Lead_Score
10   Patricia    Sánchez      Visionary Tech  ...              62.962834              215       30.40
131    Manuel     Moreno  Global IT Services  ...              76.088598              218       34.66
356    Silvia      Pérez           SecureNet  ...              82.164157              151       33.55
92     Manuel       Díaz         CloudSphere  ...              78.250014              182       36.62
137    Lorena  Hernández    NextGen Software  ...              73.788042               97       33.21

[5 rows x 11 columns]

 Distancias FAISS: [0.         0.57884604 0.7349969  0.82012147 1.1726848 ]

     Análisis de Mistral AI:
1. El lead con más probabilidad de conversión es Manuel Moreno, de Global IT Services en la industria de Salud, ubicado en EE.UU.      
2. Manuel Moreno tiene el lead score más alto (34.66), lo que sugiere que ha mostrado un mayor nivel de interés o engagement con nuestra empresa o productos. Además, su empresa ha experimentado un crecimiento significativo en ingresos anuales y empleados, lo que podría indicar una mayor capacidad y propensión para invertir en soluciones tecnológicas. La industria de Salud también está experimentando un crecimiento importante y digitalización, lo que podría aumentar su necesidad de servicios o productos tecnológicos.
3. Para Manuel Moreno, recomendaría una estrategia de venta basada en el valor y la asesoría. Dado que su empresa está en una industria en crecimiento y experimentando un aumento en ingresos y empleados, es probable que estén buscando soluciones tecnológicas que les ayuden a mantener y acelerar ese crecimiento. Enfocaría mi enfoque en demostrar cómo nuestros productos o servicios pueden ayudarlo a lograr sus objetivos de negocio y a superar los desafíos específicos de su industria. Además, dado su alto lead score, es probable que ya haya mostrado interés en nuestra empresa, por lo que sería importante aprovechar esa oportunidad para profundizar en la conversación y ofrecerle soluciones personalizadas y adaptadas a sus necesidades.

    '''
