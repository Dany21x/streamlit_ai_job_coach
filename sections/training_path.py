import streamlit as st
from auth.decorators import require_auth
import requests
from utils.css_styles import course_card

@require_auth
def show():
    st.title("Ruta de aprendizaje")
    st.write("Bienvenido a la Ruta de aprendizaje.")

    # Aplicar estilos CSS
    local_css()

    # Obtener datos de la API
    trainings = get_trainings(st.session_state.id_user)

    if trainings:
        st.markdown("### Selecciona una ruta de formación para comenzar")

        # Crear filas y columnas para mostrar las tarjetas
        cols = st.columns(2)  # Mostrar 2 cursos por fila

        for idx, training in enumerate(trainings):
            with cols[idx % 2]:
                # Mostrar tarjeta del curso
                st.markdown(render_course_card(training), unsafe_allow_html=True)

    else:
        st.warning("No se pudieron cargar las rutas de formación. Por favor, inténtalo más tarde.")


# Función para renderizar un curso como tarjeta
def render_course_card(course):
    course_id = course.get('trainingID', 'N/A')
    course_name = course.get('trainingName', 'Sin nombre')
    description = course.get('description', 'Sin descripción')

    card_html = f"""
    <div class="course-card" onclick="handleCardClick({course_id})">
        <div class="course-title">{course_name}</div>
        <div class="course-description">{description}</div>
    </div>
    <script>
    function handleCardClick(id) {{
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: id
        }}, '*');
    }}
    </script>
    """
    return card_html

# Función para obtener datos de la API
def get_trainings(id_user):
    api_url = f"https://ai-jobs-coaches-api.azurewebsites.net/api/employees/{id_user}/trainings"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        # Intentar diferentes métodos HTTP
        for method in ["GET", "POST"]:
            try:
                if method == "GET":
                    response = requests.get(api_url, headers=headers)
                else:
                    response = requests.post(api_url, headers=headers)
                print(response.json())
                if response.status_code == 200:

                    return response.json()
            except:
                continue

    except Exception as e:
        st.error(f"Error al procesar datos: {str(e)}")

# Funciones de estilo CSS personalizado
def local_css():
    st.markdown(course_card, unsafe_allow_html=True)