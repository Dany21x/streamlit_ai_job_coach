import streamlit as st
from auth.decorators import require_auth
from azure.storage.blob import BlobServiceClient
from datetime import datetime

# Azure Storage Account details
azure_storage_account_name = "your_storage_account_name"
azure_storage_account_key = "your_storage_account_key"
container_name = "your_container_name"

# Function to upload file to Azure Storage
def upload_to_azure_storage(file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_blob_name = f"{timestamp}_{file.name}"

    blob_service_client = BlobServiceClient.from_connection_string(f"DefaultEndpointsProtocol=https;"
                                                                   f"AccountName={azure_storage_account_name};"
                                                                   f"AccountKey={azure_storage_account_key}")
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_blob_name)
    blob_client.upload_blob(file)

    return blob_client.url

@require_auth
def show():
    st.title("Crear curso")

    uploaded_file = st.file_uploader("Selecciona un documento")
    if uploaded_file is not None:
        # Upload the file to Azure Storage on button click
        if st.button("Cargar documento"):
            upload_to_azure_storage(uploaded_file)
            st.success("File uploaded to Azure Storage!")
