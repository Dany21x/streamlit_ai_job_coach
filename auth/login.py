import streamlit as st
import requests

API_URL = "https://ai-jobs-coaches-api.azurewebsites.net/api/accounts/login"

def authenticate(username, password):
    """Autentica al usuario llamando a la API."""
    response = requests.post(API_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()  # Retorna el token u otros datos
    return None

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
            user_data = authenticate(username, password)
            if user_data:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user_data
                st.session_state["id_user"] = user_data["data"]["employeeID"]
                st.success("¡Login exitoso!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    """Cierra la sesión del usuario."""
    st.session_state.clear()
    