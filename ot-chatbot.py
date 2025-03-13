import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

#  Ruta donde guardaste los PDFs en tu PC
pdf_folder = r"C:\Users\guill\OneDrive\Documentos\GitHub\Sales-Automation\pdfs"

#  Cargar y extraer texto de todos los PDFs en la carpeta
documents = []
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_folder, pdf_file))
        documents.extend(loader.load())

#  Dividir texto en fragmentos más pequeños para mejor búsqueda
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

#  Mostrar algunos fragmentos como prueba
print(f"Se han extraído {len(docs)} fragmentos de texto.")
print("\nEjemplo de fragmento:")
print(docs[0].page_content[:500])  # Muestra los primeros 500 caracteres del primer fragmento


from langchain_community.embeddings import HuggingFaceEmbeddings

# Cargar modelo de embeddings desde Hugging Face
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os


# Ruta donde están los PDFs
PDF_FOLDER = "C:/Users/guill/OneDrive/Documentos/GitHub/Sales-Automation/pdfs"
FAISS_DB_PATH = os.path.join(PDF_FOLDER, "faiss_index")  # Ruta donde guardaremos la base de datos de FAISS

# Cargar documentos PDF
pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
documents = []
for pdf in pdf_files:
    loader = PyPDFLoader(os.path.join(PDF_FOLDER, pdf))
    documents.extend(loader.load())

print(f"Se han cargado {len(documents)} fragmentos de texto de los PDFs.")

# Convertir documentos a embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_index = FAISS.from_documents(documents, embeddings)

# Guardar la base de datos en FAISS
faiss_index.save_local(FAISS_DB_PATH)
print(f"Base de datos FAISS guardada en {FAISS_DB_PATH}")

# Cargar Faiss

import os
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#  Cargar variables de entorno
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError(" ERROR: No se encontró la API Key de Mistral en el archivo .env.")

#  URL de la API de Mistral
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

#  Función para hacer consultas a la API de Mistral
def query_mistral_api(user_input, context=""):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": f"{context}\n{user_input}"}],
        "temperature": 0.7
    }

    response = requests.post(MISTRAL_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f" Error: {response.status_code} - {response.text}"

#  Rutas de los archivos
PDF_FOLDER = "C:/Users/guill/OneDrive/Documentos/GitHub/Sales-Automation/pdfs"
FAISS_DB_PATH = os.path.join(PDF_FOLDER, "faiss_index")

#  Verificar si ya existe FAISS para evitar recalcular embeddings
if not os.path.exists(FAISS_DB_PATH):
    print(" Generando nueva base de datos FAISS...")
    
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    documents = []
    
    for pdf in pdf_files:
        loader = PyPDFLoader(os.path.join(PDF_FOLDER, pdf))
        documents.extend(loader.load())
    
    print(f" Se han cargado {len(documents)} fragmentos de texto de los PDFs.")

    #  Convertir documentos a embeddings y guardarlos en FAISS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.from_documents(documents, embeddings)
    faiss_index.save_local(FAISS_DB_PATH)
    print(f" Base de datos FAISS guardada en {FAISS_DB_PATH}")
else:
    print(" Base de datos FAISS ya existe. Cargando desde disco...")

#  Cargar FAISS desde disco
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_index = FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
print(" FAISS cargado correctamente.")

#  Bucle de preguntas interactivas
print("\n💬 Escribe tu pregunta (o 'salir' para terminar)")
while True:
    query = input("🟢 Tú: ")
    if query.lower() == "salir":
        print("👋 ¡Hasta luego!")
        break

    #  Buscar documentos relevantes en FAISS
    docs = faiss_index.similarity_search(query, k=3)
    print(f"✅ Documentos relevantes encontrados: {len(docs)}")

    #  Concatenar el contexto de los fragmentos
    context = "\n\n".join([doc.page_content for doc in docs])
    print("🟢 Contexto recopilado. Enviando consulta a Mistral...")

    #  Generar la respuesta con Mistral
    response = query_mistral_api(query, context)

    #  Mostrar el resultado
    print("\n🤖 Respuesta de Mistral:")
    print(response)
    print("\n────────────────────────────────────\n")


# Agregamos Streamlit

import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#  Cargar variables de entorno
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key de Mistral en el archivo .env.")

#  URL de la API de Mistral
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

#  Función para hacer consultas a la API de Mistral
def query_mistral_api(user_input, context=""):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": f"{context}\n{user_input}"}],
        "temperature": 0.7
    }

    response = requests.post(MISTRAL_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

#  Configurar Streamlit
st.set_page_config(page_title="Ot AI Sales Compliance Assistant", page_icon="📊")
st.title("📊 OT AI Sales Compliance Assistant")
st.markdown("### 🚀 Optimiza tus ventas con inteligencia artificial")

#  Cargar documentos PDF en FAISS
PDF_FOLDER = "C:/Users/guill/OneDrive/Documentos/GitHub/Sales-Automation/pdfs"
FAISS_DB_PATH = os.path.join(PDF_FOLDER, "faiss_index")

if os.path.exists(FAISS_DB_PATH):
    st.success("✅ Base de datos FAISS ya existe. Cargando desde disco...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
else:
    st.warning("⚠️ No se encontró la base de datos FAISS. Creándola ahora...")
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    documents = []
    for pdf in pdf_files:
        loader = PyPDFLoader(os.path.join(PDF_FOLDER, pdf))
        documents.extend(loader.load())

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.from_documents(documents, embeddings)
    faiss_index.save_local(FAISS_DB_PATH)
    st.success("✅ Base de datos FAISS creada y guardada con éxito.")

#  Input del usuario
user_query = st.text_input("💬 Escribe tu pregunta:")

if st.button("🔍 Buscar"):
    if user_query:
        st.info("🔍 Buscando en la base de datos FAISS...")
        docs = faiss_index.similarity_search(user_query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        st.success("✅ Documentos relevantes encontrados.")

        st.info("🤖 Generando respuesta...")
        response = query_mistral_api(user_query, context)
        st.markdown("### 🤖 Respuesta:")
        st.write(response)
    else:
        st.warning("⚠️ Por favor, introduce una pregunta.")

#  Footer profesional
st.markdown("---")
st.markdown("**Powered by Guillermo Rodríguez Vargas | AI & Compliance Solutions**")
