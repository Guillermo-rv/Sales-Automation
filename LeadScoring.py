import os
import pandas as pd
import smtplib
import requests
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 🚀 Cargar variables de entorno
load_dotenv()
EMAIL_SENDER = os.getenv("GMAIL_EMAIL")
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_HOOK")  # Opcional

# 📥 Cargar archivo de leads
file_path = r"C:\Users\guill\OneDrive - IE University\Sales-AI\leads.xlsx"
try:
    df = pd.read_excel(file_path)
    print(f"✅ Leads cargados correctamente: {df.shape[0]} filas")
except Exception as e:
    print(f"❌ Error al cargar el archivo: {e}")
    exit()

print("📊 Columnas disponibles:", list(df.columns))

# 🧠 Scoring manual

def score_lead(lead):
    score = 0
    if lead['Web_Visits'] > 5:
        score += 2
    if lead['Email_Open_Rate (%)'] > 50:
        score += 2
    if lead['Social_Interactions'] > 3:
        score += 1
    if lead['Previous_Purchases'] > 1:
        score += 3
    if lead['Time_on_Site (s)'] > 100:
        score += 1
    return score

def classify_lead(lead):
    score = score_lead(lead)
    if score >= 6:
        return "Hot 🔥"
    elif score >= 3:
        return "Warm ⚡"
    else:
        return "Cold ❄️"

# 🧠 Nodo del grafo

def lead_scoring_node(state):
    lead = state["lead"]
    score = score_lead(lead)
    classification = classify_lead(lead)
    lead['Score'] = score
    lead['Classification'] = classification
    lead['Conversion Probability (%)'] = round((score / 9) * 100, 1)
    return {"lead": lead}

# 🛠️ Grafo de decisión
class LeadState(TypedDict):
    lead: dict

def build_sales_agent_graph():
    builder = StateGraph(LeadState)
    builder.add_node("Scoring", lead_scoring_node)
    builder.set_entry_point("Scoring")
    return builder.compile()

# 🧠 Generar email con Mistral

def generate_email_with_mistral(lead):
    print("🧠 Generando email con Mistral...")
    prompt = f"""
    Write a short, professional sales email in English to {lead['First_Name']} from the company {lead['Company']}.
    Mention their interest in {lead['Interested_Product']} and suggest a custom offer or next step.
    Be warm, friendly, and helpful.
    Sign the email as Guillermo from the Sales Automation Team.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ Error usando Mistral: {e}")
    return None

# 📧 Envío de email

def send_email_to_lead(lead):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = f"[TEST] Simulated offer for {lead['First_Name']} from {lead['Company']}"

    body = generate_email_with_mistral(lead) or f"Hi {lead['First_Name']},\n\nThanks for your interest in {lead['Interested_Product']}. We'll be in touch!\n\nBest, Guillermo."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📩 Email enviado a {EMAIL_RECIPIENT} (simulando lead {lead['Email']})")
    except Exception as e:
        print(f"❌ Error al enviar el email: {e}")

    # Zapier opcional
    if ZAPIER_WEBHOOK_URL:
        try:
            zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json=lead)
            if zapier_response.status_code == 200:
                print("🔗 Lead enviado correctamente a Zapier")
            else:
                print(f"⚠️ Fallo al enviar a Zapier: {zapier_response.status_code}")
        except Exception as e:
            print(f"❌ Error al conectar con Zapier: {e}")

# 🚀 Punto de entrada
if __name__ == "__main__":
    graph = build_sales_agent_graph()
    leads_with_scores = []
    for _, row in df.iterrows():
        lead = row.to_dict()
        result = graph.invoke({"lead": lead})
        leads_with_scores.append(result["lead"])

    df_result = pd.DataFrame(leads_with_scores)
    output_path = "leads_classified.xlsx"
    df_result.to_excel(output_path, index=False)
    print(f"✅ Clasificación completada y guardada en: {output_path}")

    # Solo un email de prueba
    hot_leads = df_result[df_result['Classification'] == "Hot 🔥"]
    if not hot_leads.empty:
        lead = hot_leads.iloc[0].to_dict()
        print(f"\n➡️ Simulando envío de prueba a: {lead['First_Name']} ({lead['Email']})")
        send_email_to_lead(lead)
    else:
        print("⚠️ No hay leads 'Hot' para enviar un email de prueba.")
