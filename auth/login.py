import streamlit as st
import requests

API_URL = "https://ai-jobs-coaches-api.azurewebsites.net/api/accounts/login"

def authenticate(username, password):
    """Autentica al usuario llamando a la API."""
    response = requests.post(API_URL, json={"username": username, "password": password})
    print(username, password)
    print(response, response.status_code)
    if response.status_code == 200:
        return response.json()  # Retorna el token u otros datos
    return None

def login_page():
    """Interfaz del login."""
    st.title("Iniciar Sesión")

    username = st.text_input("Usuario", key="username")
    password = st.text_input("Contraseña", type="password", key="password")
    login_btn = st.button("Ingresar")

    if login_btn:
        user_data = authenticate(username, password)
        if user_data:
            print(user_data)
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
    #st.rerun()
