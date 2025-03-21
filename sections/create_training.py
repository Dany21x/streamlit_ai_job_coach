import streamlit as st
from auth.decorators import require_auth
from azure.storage.blob import BlobServiceClient
import requests
import os
import uuid

# Azure Storage Account details
azure_storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
azure_storage_account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

# API endpoint para enviar la URL del archivo, training name y description
API_CREATE_TRAINING_URL = "https://beecode.azurewebsites.net/generate_topics"
API_TOPICS_TO_DB = os.getenv("API_TOPICS_TO_DB", "https://ai-jobs-coaches-api-backend.azurewebsites.net/api/trainings")

def send_topics_to_db(topics_data):
    try:
        # Extraer el contenido de "topics_json"
        topics_json = topics_data.get("topics_json", {})

        # Asegurar que "topics" sea una lista, incluso si está vacío
        topics = topics_json.get("topics", [])
        if not isinstance(topics, list):
            topics = []  # Garantizar que sea una lista vacía en caso de error

        # Renombrar las claves según lo esperado por la API
        payload = {
            "training_name": topics_json.get("trainingName"),
            "description": topics_json.get("description"),
            "url": topics_json.get("attachment"),
            "topics": topics  # Ahora garantizamos que sea una lista
        }

        # Validar que la lista de temas no esté vacía
        if not topics:
            st.error("Error: El campo 'topics' está vacío. Verifica la fuente de datos.")
            return

        response = requests.post(API_TOPICS_TO_DB, json=payload)
        if response.status_code == 200:
            st.success("¡Curso registrado!")
        else:
            st.error(f"Error al registrar en base de datos: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error al conectar con la API de registro: {e}")

# Función para subir el archivo a Azure Blob Storage
def upload_to_azure_storage(file):
    file_extension = os.path.splitext(file.name)[1]  # Obtener la extensión del archivo (.pdf, .jpg, etc.)
    unique_blob_name = f"{uuid.uuid4()}{file_extension}"  # Nombre único con UUID y extensión

    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={azure_storage_account_name};"
            f"AccountKey={azure_storage_account_key}"
        )

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_blob_name)
        blob_client.upload_blob(file)

        # Construir la URL del blob
        blob_url = f"https://{azure_storage_account_name}.blob.core.windows.net/{container_name}/{unique_blob_name}"
        return blob_url
    except Exception as e:
        st.error(f"Error al subir el archivo: {e}")
        return None

# Función para enviar los datos a la API
def send_metadata_to_api(training_name, description, file_url):
    payload = {
        "training_name": training_name,
        "description": description,
        "url": file_url
    }

    print(f'"training_name": {training_name}, "description": {description}, "url": {file_url}')

    try:
        response = requests.post(API_CREATE_TRAINING_URL, json=payload)
        if response.status_code == 200:
            st.success("Documento analizado correctamente")
            return response.json().get("topics_json", "Lo siento, intente nuevamente")
        else:
            st.error(f"Error en la API: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error al conectar con la API de análisis: {e}")


@require_auth
def show():
    st.title("📚 Crear Curso")

    # Campos de entrada
    training_name = st.text_input("🏷 Nombre del entrenamiento")
    description = st.text_area("📝 Descripción del curso")

    uploaded_file = st.file_uploader("📂 Selecciona un documento")

    if uploaded_file and training_name and description:
        if st.button("🚀 Cargar documento"):
            file_url = upload_to_azure_storage(uploaded_file)

            if file_url:
                st.success("✅ Archivo subido con éxito")
                #st.markdown(f"[🔗 Ver archivo]({file_url})")

                # Enviar los datos a la API
                analyzer_response = send_metadata_to_api(training_name, description, file_url)
                st.markdown(analyzer_response)

                send_topics_to_db(analyzer_response)

            else:
                st.error("❌ No se pudo obtener la URL del archivo")
