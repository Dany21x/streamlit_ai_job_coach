import streamlit as st
import requests
from auth.decorators import require_auth
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Sistema de Evaluación", layout="wide")

# URLs de la API
API_QUESTIONS_URL = os.getenv("API_QUESTIONS_URL")
API_RESPONSES_FEEDBACK_URL = os.getenv("API_RESPONSES_FEEDBACK_URL")
API_RESPONSES_DATABASE_URL = os.getenv("API_RESPONSES_DATABASE_URL")

# Obtener preguntas desde la API
def get_data():
    """Obtiene las preguntas de la API solo si no están en session_state o si cambia el tema."""

    # Si no hay preguntas o cambió el tema, vuelve a hacer la consulta
    if (
            "quiz_questions" not in st.session_state or
            st.session_state.get("last_topic") != st.session_state.get("topic") or
            st.session_state.get("last_selected_item") != st.session_state.get("selected_item_id")
    ):
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            payload = {
                "text": st.session_state['topic'],
                "training_id": str(st.session_state["training_id"]),
                "topic_id": str(st.session_state["selected_topic_id"])
            }

            response = requests.post(API_QUESTIONS_URL, headers=headers, json=payload)

            if response.status_code == 200:
                st.session_state.quiz_questions = response.json()
                # Guardamos el último tema seleccionado para detectar cambios
                st.session_state.last_topic = st.session_state["topic"]
                st.session_state.last_selected_item = st.session_state["selected_item_id"]
            else:
                st.error(f"Error al obtener preguntas: {response.status_code}")
                st.session_state.quiz_questions = None
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            st.session_state.quiz_questions = None

    return st.session_state.quiz_questions


# Enviar respuestas a la API
def submit_responses(quiz_id, employee_id, training_id, topic_id, responses, user_name):
    """Envía las respuestas del usuario a la API en los dos formatos requeridos."""
    data1 = {
        "quizID": quiz_id,
        "employeeID": employee_id,
        "trainingID": training_id,
        "topicID": topic_id,
        "quizResponses": responses,
        "ResponseDate": datetime.datetime.utcnow().isoformat() + "Z"
    }

    print(f"data1 response: {data1}")

    # '''
    try:

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(API_RESPONSES_DATABASE_URL, headers=headers, json=data1)
        if response.status_code == 200:
            st.success("¡Respuestas enviadas con éxito!")
        else:
            st.error(f"Error al enviar respuestas: {response.status_code}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    # '''
    return data1  # Retornar el segundo JSON


# Mostrar formulario de evaluación
def display_form(data, employee_id=1, training_id=1, topic_id=1, user_name="Usuario"):
    """Genera dinámicamente el formulario de evaluación con las preguntas obtenidas."""
    if not data or "questions" not in data or "Questions" not in data["questions"]:
        st.warning("No hay preguntas disponibles.")
        return

    st.header("Evaluación de Conocimientos")
    user_responses = []

    quiz_id = data["questions"]["id"]
    training_id = data["questions"]["TrainingID"]
    topic_id = data["questions"]["TopicID"]

    for question in data["questions"]["Questions"]:
        question_id = str(question["QuestionID"])
        key = f"question_{question_id}"

        selected_option = st.radio(
            f"**{question['Question']}**",
            question["Options"],
            key=key
        )

        # Obtener la opción correcta
        correct_option = question["Options"][question["CorrectAnswer"]]

        # Guardar respuesta en el formato requerido
        user_responses.append({
            "question": question['Question'],
            "selectedOption": selected_option,  # Opción seleccionada
            "correctOption": correct_option,  # Opción correcta
            "isCorrect": True if correct_option == selected_option else False
        })

        st.write("---")

    if st.button("Enviar Evaluación"):
        json_result = submit_responses(quiz_id, employee_id, training_id, topic_id, user_responses, user_name)
        st.json(json_result)  # Mostrar el segundo JSON en pantalla


# Datos de prueba si la API no responde
def get_dummy_data():
    """Retorna datos de prueba en la misma estructura que la API."""
    return {
        "status": "result",
        "questions": {
            "id": "dummy-id",
            "TrainingID": "1",
            "TopicID": "1",
            "Questions": [
                {
                    "QuestionID": 1,
                    "Question": "¿Qué es una lambda en Python?",
                    "Options": [
                        "Una función anónima",
                        "Una clase especial de variables",
                        "Un módulo de Python",
                        "Un tipo de bucle"
                    ],
                    "CorrectAnswer": 0
                },
                {
                    "QuestionID": 2,
                    "Question": "¿Cuál es la sintaxis básica de una lambda en Python?",
                    "Options": [
                        "lambda x: x*2",
                        "def x: x*2",
                        "class x: x*2",
                        "for x in range(2): x*2"
                    ],
                    "CorrectAnswer": 0
                }
            ]
        }
    }


# Función principal
@require_auth
def show():
    """Muestra el módulo de evaluación sin recargar las preguntas innecesariamente."""
    st.title("Módulo de Evaluación")

    user_name = st.session_state.get("user", {}).get("data", {}).get("employee", {}).get("firstName", "Usuario")

    if st.session_state.get("selected_item_id") and st.session_state.get("topic"):

        st.write(f"Ruta: {st.session_state['training_name']}")

        # Obtener preguntas (solo si es necesario)
        data = get_data()

        if data:
            display_form(data, user_name=user_name)
        else:
            st.warning("No se pudieron cargar las preguntas.")

    else:
        st.warning("No se pudieron cargar las preguntas.")
        st.write(":warning: ¡Primero debes seleccionar un tema en la ruta de aprendizaje! :warning:")

        if st.button("Llévame a la Ruta de Aprendizaje 🚀"):
            st.session_state["navigation"] = "Ruta de aprendizaje"
            st.rerun()

if __name__ == "__main__":
    show()