import streamlit as st
from auth.login import login_page, logout
from sections import chat, test, dashboard, training_path, home, create_training
from utils.css_styles import load_all_styles

# Cargar estilos
load_all_styles()

# Inicializar estado de sesión si no existe
def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Home"
    if "navigation" not in st.session_state:
        st.session_state["navigation"] = "Home"
    if "roleID" not in st.session_state:
        st.session_state["roleID"] = None

init_session_state()

# Si el usuario no está autenticado, mostrar la página de login y detener ejecución
if not st.session_state["authenticated"]:
    login_page()
    st.stop()

# Obtener el rol del usuario
role_id = st.session_state["roleID"]

# Definir opciones de menú según el rol
menu = ["Home", "Ruta de aprendizaje", "Chat de entrenamiento", "¡Evalúa mi conocimiento!"]
if role_id == 1:  # Coach: Accede a todo
    menu.extend(["Dashboard progreso", "Crear curso"])


# ----- SIDEBAR -----
def render_sidebar():
    with st.sidebar:
        st.image("assets/logo.png", width=125)  # Agrega el logo
        st.title("Opciones")

        prev_navigation = st.session_state["navigation"]

        pagina = st.selectbox(
            "Selecciona una sección",
            menu,
            index=menu.index(st.session_state["navigation"]),
            key="pagina_selector"
        )

        if pagina != prev_navigation:
            st.session_state["navigation"] = pagina
            st.rerun()

        contrast_mode = st.toggle("Modo alto contraste")
        if contrast_mode:
            from utils.css_styles import toggle_contrast_mode
            toggle_contrast_mode(True)

        st.button("Cerrar Sesión", on_click=logout)

        return pagina


# Renderizar sidebar y actualizar la navegación
render_sidebar()

# ----- NAVEGACIÓN -----
def show_page():
    page_mapping = {
        "Home": home.show,
        "Ruta de aprendizaje": training_path.show,
        "Chat de entrenamiento": chat.show,
        "¡Evalúa mi conocimiento!": test.show,
        "Dashboard progreso": dashboard.show if role_id == 1 else None,
        "Crear curso": create_training.show if role_id == 1 else None
    }

    page_function = page_mapping.get(st.session_state["navigation"])
    if page_function:
        page_function()

show_page()

