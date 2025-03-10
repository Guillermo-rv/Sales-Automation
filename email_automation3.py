import os
import smtplib
import email.message
from dotenv import load_dotenv
from mistralai import Mistral  # Importamos Mistral
from email_generator import generate_email  # Importamos la función generadora

# 🔹 Cargar variables de entorno desde .env
load_dotenv()

#  Obtener credenciales desde .env
EMAIL_ADDRESS = os.getenv("GMAIL_EMAIL")
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

#  Iniciar el cliente de Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

#  Función para enviar correos
def send_email(to_email, subject, body):
    msg = email.message.EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body, subtype="plain", charset="utf-8")  

    try:
        #  Conectar con el servidor SMTP de Gmail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f" Correo enviado con éxito a {to_email}")
    except Exception as e:
        print(f" Error al enviar el correo: {e}")

#  Generar y enviar email automáticamente
if __name__ == "__main__":
    email_text = generate_email("Juan Pérez", "FinTech XYZ", "Finanzas", "CEO")  # Personaliza con tus datos
    send_email(EMAIL_RECIPIENT, " Prospección Automática", email_text)
