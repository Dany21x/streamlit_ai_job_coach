import streamlit as st
from auth.login import login_page, logout
from sections import chat, test, dashboard, training_path, home, create_training

# Inicializar estado de sesión si no existe
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Home"  # Página por defecto después del login
if "navigation" not in st.session_state:
    st.session_state["navigation"] = "Home"
if "roleID" not in st.session_state:
    st.session_state["roleID"] = None  # Asegurar que el rol está en la sesión

# Si el usuario no está autenticado, mostrar solo el login
if not st.session_state["authenticated"]:
    login_page()
    st.stop()  # 🔥 Evita que se ejecute el resto del código si el usuario no ha iniciado sesión

# Obtener el rol del usuario
role_id = st.session_state["roleID"]

# Definir opciones de menú según el rol
menu = ["Home", "Ruta de aprendizaje", "Chat de entrenamiento", "¡Evalúa mi conocimiento!"]
if role_id == 1:  # Coach: Accede a todo
    menu.append("Dashboard progreso")
    menu.append("Crear curso")
# Sidebar de navegación
st.sidebar.title("Opciones")
pagina = st.sidebar.selectbox("Selecciona una sección", menu,
                              index=menu.index(st.session_state["navigation"]),
                              key="pagina_selector")

# Actualizar la navegación
if pagina != st.session_state["navigation"]:
    st.session_state["navigation"] = pagina
    st.rerun()  # 🔄 Volver a renderizar la página para aplicar el cambio

st.sidebar.button("Cerrar Sesión", on_click=logout)

# Mostrar solo la página seleccionada
if st.session_state["navigation"] == "Ruta de aprendizaje":
    training_path.show()
elif st.session_state["navigation"] == "Home":
    home.show()
elif st.session_state["navigation"] == "Chat de entrenamiento":
    chat.show()
elif st.session_state["navigation"] == "¡Evalúa mi conocimiento!":
    test.show()
elif st.session_state["navigation"] == "Dashboard progreso" and role_id == 1:
    dashboard.show()  # Solo Coach accede
elif st.session_state["navigation"] == "Crear curso" and role_id == 1:
    create_training.show()