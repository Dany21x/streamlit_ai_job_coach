import streamlit as st
from auth.login import login_page, logout
from sections import chat, test, dashboard, training_path

st.sidebar.title("Opciones")
pagina = st.sidebar.selectbox("Selecciona una sección", ["Login", "Ruta de aprendizaje", "Chat de entrenamiento",
                                                         "¡Evalúa mi conocimiento!", "Dashboard progreso"])

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    st.sidebar.button("Cerrar Sesión", on_click=logout)

if pagina == "Login":
    login_page()
elif pagina == "Ruta de aprendizaje":
    training_path.show()
elif pagina == "Chat de entrenamiento":
    chat.show()
elif pagina == "Test":
    test.show()
elif pagina == "Dashboard progreso":
    dashboard.show()
