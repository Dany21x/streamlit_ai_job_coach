import streamlit as st
import requests
import os

API_URL = os.getenv("API_LOGIN_URL", "https://ai-jobs-coaches-api-backend.azurewebsites.net/api/accounts/login")


def authenticate(username, password):
    """Autentica al usuario llamando a la API y obtiene su rol."""
    response = requests.post(API_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        user_data = response.json()
        if user_data["isSuccess"]:
            st.session_state["authenticated"] = True
            st.session_state["user"] = user_data
            st.session_state["id_user"] = user_data["data"]["employeeID"]
            st.session_state["roleID"] = user_data["data"]["employee"]["roleID"]  # Guardar el rol
            return True
    return False


def login_page():
    """Interfaz del login centrado visualmente."""
    st.title("Iniciar Sesión")

    # Crear columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:  # El formulario está en la columna del centro
        st.markdown("### Accede con tus credenciales")
        
        username = st.text_input("Usuario", key="username", help="Ingresa tu nombre de usuario")
        password = st.text_input("Contraseña", type="password", key="password", help="Ingresa tu contraseña")

        login_btn = st.button("Ingresar", use_container_width=True)

        if login_btn:
            if authenticate(username, password):
                st.success("¡Login exitoso!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")


def logout():
    """Cierra la sesión del usuario."""
    st.session_state.clear()
    