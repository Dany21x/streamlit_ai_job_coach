import streamlit as st
from auth.login import login_page, logout
from sections import chat, test, dashboard, training_path, home

# Inicializar estado de sesión si no existe
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"  # Página por defecto después del login

# Si el usuario no está autenticado, mostrar solo el login
if not st.session_state["authenticated"]:
    login_page()
    st.stop()  # 🔥 Evita que se ejecute el resto del código si el usuario no ha iniciado sesión

# Sidebar de navegación
st.sidebar.title("Opciones")
pagina = st.sidebar.selectbox("Selecciona una sección", ["Home", "Ruta de aprendizaje", "Chat de entrenamiento",
                                                         "¡Evalúa mi conocimiento!", "Dashboard progreso"])

st.sidebar.button("Cerrar Sesión", on_click=logout)

# Mostrar solo la página seleccionada
if pagina == "Ruta de aprendizaje":
    training_path.show()
elif pagina == "Home":
    home.show()
elif pagina == "Chat de entrenamiento":
    chat.show()
elif pagina == "¡Evalúa mi conocimiento!":
    test.show()
elif pagina == "Dashboard progreso":
    dashboard.show()
