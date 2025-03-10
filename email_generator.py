import os
from dotenv import load_dotenv
from mistralai import Mistral, UserMessage  

# Cargar claves desde .env
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

print(f"Mistral API Key cargada: {MISTRAL_API_KEY}")

# Iniciar Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

# Función para generar emails de prospección
def generate_email(name, company, industry, position):
    messages = [
        {"role": "system", "content": "Eres un experto en ventas y generas emails de prospección atractivos y personalizados."},
        {"role": "user", "content": f"""
            Genera un email de prospección para {name}, quien trabaja en {company}.
            Su sector es {industry} y su cargo es {position}.
            El email debe ser formal, breve y persuasivo. No debe parecer automatizado.
        """}
    ]

    # Obtener respuesta del modelo Mistral
    response = client.chat.complete(model="mistral-small", messages=messages)

    return response.choices[0].message.content

# Prueba del generador
if __name__ == "__main__":
    email_text = generate_email("Juan Pérez", "FinTech XYZ", "Finanzas", "CEO")
    print("Email generado:\n")
    print(email_text)

'''
Email generado:

Subject: Exclusive Insights to Elevate FinTech XYZ to New Heights

Dear Juan Pérez,

I hope this email finds you well. I am writing to introduce myself as an expert in the fintech sector, with a proven track record of helping businesses like yours thrive and stay ahead of the competition.

Having researched FinTech XYZ, I am impressed by your commitment to innovation and dedication to serving your clients. I believe that my services can help you further enhance your offerings and expand your market reach.

Here's what sets me apart:

1. In-depth sector expertise: I have spent over a decade specializing in fintech, staying up-to-date with the latest trends and technologies to provide you with actionable insights.
2. Customized strategies: I understand that every business is unique, and I tailor my approach to meet your specific needs and goals, ensuring maximum impact.  
3. Proven results: My clients have experienced increased revenue, improved customer satisfaction, and strengthened market positions, thanks to my strategic guidance.

To demonstrate my value, I would like to offer you a complimentary consultation, during which I will share exclusive fintech insights tailored to FinTech XYZ and provide recommendations for your growth.

Please let me know if you are interested in scheduling a call or if you have any questions. I look forward to the opportunity to collaborate and help you elevate FinTech XYZ to new heights.

Warm regards,

[Your Name]
[Your Title]
[Your Phone Number]
[Your Email Address]

'''
