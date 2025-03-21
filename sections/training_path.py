import streamlit as st
from auth.decorators import require_auth
import requests
from utils.css_styles import course_card
import sections

if "current_section" not in st.session_state:
    st.session_state["current_section"] = None

if "get_new_explanation" not in st.session_state:
    st.session_state["get_new_explanation"] = None

@require_auth
def show():
    # Si hay una sección seleccionada, cargarla y salir de esta función
    if st.session_state.get("current_section"):
        section_to_load = getattr(sections, st.session_state["current_section"], None)
        if section_to_load:
            section_to_load.show()
            return  # Importante: salir de la función show() para no mostrar el contenido principal

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
                # Crear un botón para cada curso
                if st.button(training["trainingName"], key=training["trainingID"]):
                    st.session_state["training_name"] = training["trainingName"]
                    st.session_state["training_id"] = training["trainingID"]
                    st.session_state["get_new_explanation"] = True
                    # Si el curso ya está seleccionado, deseleccionarlo
                    if st.session_state.get("selected_course") == training["trainingID"]:
                        st.session_state.selected_course = None
                    else:
                        st.session_state.selected_course = training["trainingID"]

    else:
        st.warning("No tienes rutas de formación asociadas en el momento.")

    # Si se ha seleccionado un curso, obtener y mostrar los subtemas
    if st.session_state.get("selected_course"):
        show_topics(st.session_state.selected_course)

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
    api_url = f"https://ai-jobs-coaches-api-backend.azurewebsites.net/api/employees/{id_user}/trainings"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(api_url)
    try:
        response = requests.get(api_url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            return response.json().get('data')
    except Exception as e:
        st.error(f"Error al obtener subtemas: {str(e)}")

# Nueva función para obtener subtemas de un curso
def get_topics(course_id):

    print(f'course_id: {course_id}')
    api_url = f"https://ai-jobs-coaches-api-backend.azurewebsites.net/api/trainings/{course_id}/topics"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers)
        print(f'response: {response}')
        if response.status_code == 200:
            return response.json().get("data")
    except Exception as e:
        st.error(f"Error al obtener temas: {str(e)}")

    return []

# Función para mostrar los subtemas con hipervínculos
def show_topics(course_id):
    topics = get_topics(course_id)

    if topics:
        st.markdown("### Temas:")
        for topic in topics:
            topic_name = topic.get("topicName", "No asignado")
            topic_id = topic.get("topicID", "")
            items = topic.get("items", [])

            if st.button(topic_name, key=f"topic_{topic_id}"):
                st.session_state["current_section"] = 'topic_content'  # Guardamos la sección activa
                st.session_state["selected_topic_id"] = topic_id
                st.session_state["topic_name"] = topic_name
                print(f'current_section changed 1: {st.session_state['current_section']}, {topic_name}')
                st.session_state["selected_topic_items"] = items
                # Redirigir a la sección correspondiente
                st.rerun()

    else:
        st.warning("No se encontraron subtemas para este curso.")


# Funciones de estilo CSS personalizado
def local_css():
    st.markdown(course_card, unsafe_allow_html=True)


# Si el usuario ha seleccionado una sección, mostrarla
if st.session_state.get("current_section"):
    print(f'current_section changed 2: {st.session_state["current_section"]}')

    section_to_load = getattr(sections, st.session_state["current_section"], None)
    #st.session_state["current_section"] = None
    if section_to_load:
        section_to_load.show()