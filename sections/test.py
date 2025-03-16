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
def submit_responses(employee_id, training_id, topic_id, responses):
    """Envía las respuestas del usuario a la API en el formato requerido."""
    data = {
        "EmployeeID": employee_id,
        "TrainingID": training_id,
        "TopicID": topic_id,
        "Responses": responses,
        "ResponseDate": datetime.datetime.utcnow().isoformat() + "Z"
    }
    print(f"data response: {data}")
    try:
        response = requests.post(API_RESPONSES_URL, json=data)
        if response.status_code == 200:
            st.success("¡Respuestas enviadas con éxito!")
        else:
            st.error(f"Error al enviar respuestas: {response.status_code}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# Mostrar formulario de evaluación
def display_form(data, employee_id=1, training_id=1, topic_id=1):
    """Genera dinámicamente el formulario de evaluación con las preguntas obtenidas."""
    if not data or "questions" not in data:
        st.warning("No hay preguntas disponibles.")
        return

    st.header("Evaluación de Conocimientos")
    user_responses = []

    for question in data["questions"]:
        question_id = str(question["id"])
        key = f"question_{question_id}"
        selected_option = st.radio(
            f"**{question['question']}**", 
            question["options"], 
            key=key
        )
        
        # Determinar si la respuesta es correcta
        correct_option = question["options"][question["correct_answer"]]
        is_correct = selected_option == correct_option
        
        # Guardar respuesta en el formato requerido
        user_responses.append({
            "QuestionID": question_id,
            "SelectedOptionID": str(question["options"].index(selected_option)),  # ID de la opción seleccionada
            "IsCorrect": is_correct
        })

        st.write("---")

    if st.button("Enviar Evaluación"):
        submit_responses(employee_id, training_id, topic_id, user_responses)

def get_dummy_data():
    # Datos de ejemplo para simular la respuesta de la API
    return {
        "questions": [
            {
            "id": 1,
            "question": "¿Cuál es la diferencia entre listas, tuplas y diccionarios en Python?",
            "options": [
                "Las listas y tuplas son mutables, pero los diccionarios no.",
                "Las listas son mutables, las tuplas son inmutables y los diccionarios almacenan pares clave-valor.",
                "Las tuplas pueden cambiar de tamaño, pero las listas no.",
                "Los diccionarios solo pueden almacenar datos numéricos."
            ],
            "correct_answer": 1
            },
            {
            "id": 2,
            "question": "¿Cómo funcionan las funciones en Python y cuál es la diferencia entre args y **kwargs?",
            "options": [
                "args permite recibir un número variable de argumentos posicionales, mientras que kwargs recibe un número variable de argumentos con nombre.",
                "*args solo acepta listas y kwargs solo acepta diccionarios.",
                "args y **kwargs siempre deben usarse juntos en una función.",
                "args y *kwargs son formas de definir variables dentro de una función."
            ],
            "correct_answer": 0
            },
            {
            "id": 3,
            "question": "¿Cuál de las siguientes opciones es una expresión válida en Python?",
            "options": [
                "x = if y > 10 then 'Alto' else 'Bajo'",
                "resultado = (10 + 5) 2",
                "for i in range(5): i * 2",
                "def my_function: return x + y"
            ],
            "correct_answer": 1
            }
        ]
    }

# Función principal
@require_auth
def show():
    """Muestra el módulo de evaluación y maneja la interacción del usuario."""
    st.title("Módulo de Evaluación")
    st.sidebar.header("Opciones")
    
    if st.sidebar.button("Actualizar Preguntas"):
        st.experimental_rerun()

    data = get_data()
    print(data)
    if data is None:
        data= get_dummy_data()
    print(data)
    if data:
        display_form(data)
    else:
        st.warning("No se pudieron cargar las preguntas.")

if __name__ == "__main__":
    show()