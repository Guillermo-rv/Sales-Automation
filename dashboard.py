import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 📄 Cargar leads clasificados
st.set_page_config(page_title="Sales AI Dashboard", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700&display=swap');

    html, body, .stApp {
        background-color: #080C0A;
        color: white;
        font-family: 'Bricolage Grotesque', sans-serif;
    }

    .stMetric {
        font-size: 18px !important;
    }

    h1, h2, h3, h4 {
        color: #FFFFFF;
        font-weight: 700;
    }

    .stButton > button {
        background-color: #346E4A;
        color: white;
        border: none;
        padding: 0.5rem 1.2rem;
        font-size: 16px;
        border-radius: 10px;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #479DBB;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* 🔧 Métricas */
    div[data-testid="metric-container"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
    }

    div[data-testid="metric-container"] > label {
        font-size: 1.1rem;
        color: #AFAFAF !important;
    }

    div[data-testid="metric-container"] > div {
        font-size: 2rem;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sales Automation Dashboard")

# Cargar datos
try:
    df = pd.read_excel("leads_classified.xlsx")
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Panel resumen
total_leads = len(df)
hot = len(df[df['Classification'] == "Hot 🔥"])
warm = len(df[df['Classification'] == "Warm ⚡"])
cold = len(df[df['Classification'] == "Cold ❄️"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", total_leads)
col2.metric("Hot 🔥", hot)
col3.metric("Warm ⚡", warm)
col4.metric("Cold ❄️", cold)

st.markdown("---")

# 🎨 Gráfico de pastel Plotly con colores personalizados
colors = {
    "Hot 🔥": "#7971CA",     # morado corporativo
    "Warm ⚡": "#346E4A",    # verde corporativo
    "Cold ❄️": "#479DBB"     # azul complementario
}

fig = px.pie(df, names='Classification', title='Lead Classification Distribution',
             color='Classification', color_discrete_map=colors)
fig.update_traces(
    textfont_size=16,
    textinfo='label+percent',
    insidetextfont=dict(color='white')
)
fig.update_layout(
    paper_bgcolor='#080C0A',
    plot_bgcolor='#080C0A',
    font=dict(color='white', family='Bricolage Grotesque')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 📋 Tabla con acciones simuladas por lead
def simulate_action(row):
    if row['Classification'] == "Hot 🔥":
        return "📩 Email sent"
    elif row['Classification'] == "Warm ⚡":
        return "🔔 Nurture sequence"
    else:
        return "📥 Added to newsletter"

df['Action Taken'] = df.apply(simulate_action, axis=1)

st.subheader("📋 Lead Summary Table")
st.dataframe(df[['First_Name', 'Last_Name', 'Company', 'Classification', 'Action Taken']])

# 🔝 Top Hot Leads by Probability
st.markdown("### 🔝 Top Hot Leads by Conversion Probability")
top_hot = df[df['Classification'] == "Hot 🔥"].sort_values(by='Conversion Probability (%)', ascending=False)
st.dataframe(top_hot[['First_Name', 'Last_Name', 'Company', 'Conversion Probability (%)']].head(5))

# 📈 Conversion Probability Chart (Top 10 Hot)
fig_bar = px.bar(
    top_hot.head(10),
    x='First_Name',
    y='Conversion Probability (%)',
    color='Company',
    title='Top Hot Leads by Conversion Probability',
    text='Conversion Probability (%)'
)
fig_bar.update_traces(textposition='outside', textfont=dict(color='white'))
fig_bar.update_layout(paper_bgcolor='#080C0A', plot_bgcolor='#080C0A', font=dict(color='white'))
st.plotly_chart(fig_bar, use_container_width=True)


st.markdown("---")

# ⚡ Sección de notificaciones simuladas en tiempo real
st.subheader("⚡ Real-Time Notifications")
notifications = []
for index, row in df.iterrows():
    name = f"{row['First_Name']} {row['Last_Name']}"
    company = row['Company']
    classification = row['Classification']
    action = row['Action Taken']

    if classification == "Hot 🔥":
        notifications.append(f"🚀 An offer was automatically sent to {name} from {company}.")
    elif classification == "Warm ⚡":
        notifications.append(f"🔔 Lead {name} was added to nurture flow.")
    elif classification == "Cold ❄️":
        notifications.append(f"📥 {name} was subscribed to newsletter.")

for note in notifications[:10]:
    st.write(note)

st.markdown("---")

# 🛠️ ACCIONES MANUALES (Simuladas)
st.subheader("🛠️ Manual Actions")

colA, colB, colC = st.columns(3)

# 🔄 Botón para reprocesar leads
if colA.button("🔄 Reprocess Leads"):
    import subprocess
    try:
        subprocess.run(["python", "LeadScoring.py"], check=True)
        st.success("✅ LeadScoring.py re-executed successfully.")
    except Exception as e:
        st.error(f"❌ Failed to run LeadScoring.py: {e}")

# 📩 Botón para enviar email de prueba a un lead Hot
if colB.button("📩 Send Test Email"):
    try:
        hot_leads = df[df['Classification'] == "Hot 🔥"]
        if not hot_leads.empty:
            lead = hot_leads.iloc[0].to_dict()
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            EMAIL_SENDER = os.getenv("GMAIL_EMAIL")
            EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
            EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

            subject = f"[TEST] Simulated offer for {lead['First_Name']} from {lead['Company']}"
            body = f"""
            Hi {lead['First_Name']},

            We noticed your strong interest in {lead['Interested_Product']}.
            Our team would love to assist you further and provide a custom offer.

            Best regards,
            Guillermo
            Sales Automation Team
            """

            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECIPIENT
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

            st.success(f"📩 Test email sent to {EMAIL_RECIPIENT}")
        else:
            st.warning("⚠️ No 'Hot 🔥' leads available.")
    except Exception as e:
        st.error(f"❌ Error sending email: {e}")

# 🔁 Botón para recargar los datos sin recargar la app completa
if colC.button("🔁 Reload Data"):
    try:
        df = pd.read_excel("leads_classified.xlsx")
        st.success("🔁 Data reloaded successfully.")
    except Exception as e:
        st.error(f"❌ Could not reload data: {e}")


if "Conversion Probability (%)" not in df.columns:
    st.warning("⚠️ La columna 'Conversion Probability (%)' no está en el archivo cargado.")
    st.write("📊 Columnas encontradas:", df.columns.tolist())
    st.stop()



'''
📸 PDF Quote Preview (On-Demand)

This block adds a button to preview the latest generated PDF quote from the `pdf_quotes` folder.
When clicked, it converts the first page of the most recent PDF into an image and displays it.

Dependencies:
- pdf2image
- PIL (Pillow)
- Poppler installed (and poppler_path configured)

To remove, delete this entire block safely.
'''

from pdf2image import convert_from_path
from PIL import Image
import glob

st.markdown("---")
st.subheader("🧾 Quote Preview")

if st.button("👁️ Show latest quote preview"):
    poppler_path = r"C:\Users\guill\OneDrive\Documentos\GitHub\Sales-Automation\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    quote_files = glob.glob("pdf_quotes/*.pdf")

    if quote_files:
        latest_pdf = max(quote_files, key=os.path.getctime)

        try:
            images = convert_from_path(
                latest_pdf,
                poppler_path=poppler_path,
                first_page=1,
                last_page=1
            )

            st.image(images[0], caption=os.path.basename(latest_pdf), use_column_width=True)

        except Exception as e:
            st.warning(f"⚠️ Could not generate image from PDF: {e}")
    else:
        st.info("ℹ️ No quote PDF found to preview.")
