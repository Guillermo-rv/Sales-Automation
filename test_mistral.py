import os
from dotenv import load_dotenv
import requests

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API Key de Mistral
api_key = os.getenv("MISTRAL_API_KEY")

# Verificar que la API Key se haya cargado correctamente
if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key de Mistral. Verifica el archivo .env y que esté en .gitignore.")

# Definir la URL de la API de Mistral
url = "https://api.mistral.ai/v1/chat/completions"

# Configurar los datos de la petición
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "mistral-tiny",
    "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}]
}

# Enviar la solicitud a la API de Mistral
response = requests.post(url, json=data, headers=headers)

# Mostrar la respuesta
if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"❌ Error {response.status_code}: {response.text}")

