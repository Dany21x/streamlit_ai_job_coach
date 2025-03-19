import streamlit as st
import requests
from auth.decorators import require_auth
import datetime

# Configuración de la página
st.set_page_config(page_title="Sistema de Evaluación", layout="wide")

# URLs de la API
API_QUESTIONS_URL = "https://your-api.com/evaluation/questions"
API_RESPONSES_URL = "https://your-api.com/evaluation/responses"

# Obtener preguntas desde la API
def get_data():
    """Obtiene las preguntas de la API y devuelve un diccionario con los datos."""
    try:
        response = requests.get(API_QUESTIONS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener preguntas: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# Enviar respuestas a la API
def submit_responses(employee_id, training_id, topic_id, responses, user_name):
    """Envía las respuestas del usuario a la API en los dos formatos requeridos."""
    data1 = {
        "EmployeeID": employee_id,
        "TrainingID": training_id,
        "TopicID": topic_id,
        "Responses": responses,
        "ResponseDate": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    data2 = {
        "usuario": user_name,
        "respuestas": [
            {"id_pregunta": res["QuestionID"], "respuesta_usuario": res["SelectedOptionID"]}
            for res in responses
        ]
    }
    
    print(f"data1 response: {data1}")
    print(f"data2 response: {data2}")
    try:
        response = requests.post(API_RESPONSES_URL, json=data1)
        if response.status_code == 200:
            st.success("¡Respuestas enviadas con éxito!")
        else:
            st.error(f"Error al enviar respuestas: {response.status_code}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    
    return data2  # Retornar el segundo JSON

# Mostrar formulario de evaluación
def display_form(data, employee_id=1, training_id=1, topic_id=1, user_name="Usuario"): 
    """Genera dinámicamente el formulario de evaluación con las preguntas obtenidas."""
    if not data or "questions" not in data or "Questions" not in data["questions"]:
        st.warning("No hay preguntas disponibles.")
        return

    st.header("Evaluación de Conocimientos")
    user_responses = []

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
        
        # Determinar si la respuesta es correcta
        correct_option = question["Options"][question["CorrectAnswer"]]
        is_correct = selected_option == correct_option
        
        # Guardar respuesta en el formato requerido
        user_responses.append({
            "QuestionID": question_id,
            "SelectedOptionID": selected_option,  # Guardamos la opción seleccionada
            "IsCorrect": is_correct
        })

        st.write("---")

    if st.button("Enviar Evaluación"):
        json_result = submit_responses(employee_id, training_id, topic_id, user_responses, user_name)
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
    """Muestra el módulo de evaluación y maneja la interacción del usuario."""
    st.title("Módulo de Evaluación")
    
    user_name = st.session_state.get("user", {}).get("data", {}).get("employee", {}).get("firstName", "Usuario")
    
    data = get_data()
    if data is None:
        data = get_dummy_data()
    
    if data:
        display_form(data, user_name=user_name)
    else:
        st.warning("No se pudieron cargar las preguntas.")

if __name__ == "__main__":
    show()
