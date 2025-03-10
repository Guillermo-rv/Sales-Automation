import os
from dotenv import load_dotenv
from mistralai import Mistral, UserMessage
from langchain_community.chat_models import ChatOpenAI

# Cargar claves desde .env
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Iniciar clientes
mistral_client = Mistral(api_key=MISTRAL_API_KEY)
openai_client = ChatOpenAI(api_key=OPENAI_API_KEY)

def generate_personalized_email(client_data):
    name = client_data["name"]
    company = client_data["company"]
    industry = client_data["industry"]
    position = client_data["position"]

    messages = [
        {"role": "system", "content": "Eres un experto en ventas y generas emails de prospección atractivos y personalizados."},
        {"role": "user", "content": f"""
            Genera un email de prospección para {name}, quien trabaja en {company}.
            Su sector es {industry} y su cargo es {position}.
            El email debe ser formal, breve y persuasivo. No debe parecer automatizado.
        """}
    ]

    response = mistral_client.chat.complete(model="mistral-small", messages=messages)
    return response.choices[0].message.content

# Ejemplo de uso
client_data = {
    "name": "Juan Pérez",
    "company": "FinTech XYZ",
    "industry": "Finanzas",
    "position": "CEO"
}

email_content = generate_personalized_email(client_data)
print("Email generado:\n")
print(email_content)
