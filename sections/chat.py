import openai
import streamlit as st
from auth.decorators import require_auth
from utils.azure_speech import speech_recognize_once_from_mic, text_to_speech
import tempfile
import os
from streamlit_extras.stylable_container import stylable_container
from openai import AzureOpenAI
import requests

# Configuración de la API de Azure OpenAI
client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),
  api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

@require_auth
def show():
    if st.button("🔙 Volver a la Ruta de Aprendizaje"):
        st.session_state["navigation"] = "Ruta de aprendizaje"
        st.session_state["current_section"] = None
        st.rerun()

    if st.sidebar.button("¡Evalúame!"):
        st.session_state["navigation"] = "¡Evalúa mi conocimiento!"
        st.rerun()

    st.title("Chat de entrenamiento")

    topic = f'{st.session_state.get("item_name", None)} orientado a un curso de {st.session_state.get("training_name", None)}'
    st.session_state['topic'] = topic

    # Inicializar historial de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de chat
    for message in st.session_state.messages:
        if message["role"] == "assistant" and message.get("type") == "resources":
            st.subheader("📚 Recursos adicionales para profundizar en el tema")
            cols = st.columns(len(message["content"]))
            for i, resource in enumerate(message["content"]):
                with cols[i]:
                    st.markdown(f"#### {resource['title']}", unsafe_allow_html=True)
                    st.markdown(f"👨‍🏫 *Instructor:* {resource['instructor']}")
                    st.markdown(f"⭐ *Calificación:* {resource['rating']} / 5")
                    st.markdown(f"[🔗 Ver curso]({resource['url']})", unsafe_allow_html=True)
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                # 🔊 Si el mensaje es del asistente, generar y mostrar audio
                if message["role"] == "assistant" and "audio" in message:
                    st.audio(message["audio"], format="audio/wav")

    # Entrada de texto
    user_input = st.chat_input("Escribe un mensaje...")

    # Entrada de audio
    with st.sidebar:
        st.subheader("Entrada de voz")
        audio_value = st.audio_input("Graba un mensaje de voz")

    audio_text = None
    if audio_value:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_value.getvalue())
            temp_audio_path = temp_audio.name
        audio_text = speech_recognize_once_from_mic(temp_audio_path)

    # Procesar entrada (texto o audio convertido)
    if user_input or audio_text:
        message_content = user_input if user_input else audio_text

        with st.chat_message("user"):
            st.markdown(message_content)

        st.session_state.messages.append({"role": "user", "content": message_content})

        response = get_llm_answer(topic, message_content)

        with st.chat_message("assistant"):
            st.markdown(response)

        # 🔊 Generar audio de la respuesta
        audio_path = text_to_speech(response)

        # ✅ Agregar mensaje del asistente con o sin audio, pero solo una vez
        assistant_message = {"role": "assistant", "content": response}
        if audio_path:
            assistant_message["audio"] = audio_path

        st.session_state.messages.append(assistant_message)

        # 🔄 Forzar recarga de la interfaz para que el audio aparezca inmediatamente
        st.rerun()

    session_state = st.session_state.get("selected_item_id", None)
    get_new_explanation = st.session_state.get("get_new_explanation", False)

    if session_state is not None and get_new_explanation:
        st.session_state["get_new_explanation"] = False

        # Obtener la primera explicación del LLM
        topic_md = get_llm_answer(topic)
        st.session_state.messages.append({"role": "assistant", "content": topic_md})

        with st.chat_message("assistant"):
            st.markdown(topic_md)

        # 🔥 Obtener recursos inmediatamente después de la primera respuesta del LLM
        if not any(msg.get("type") == "resources" for msg in st.session_state.messages):
            resources = get_additional_resources(st.session_state["training_id"])
            if resources:
                st.session_state.messages.append({"role": "assistant", "type": "resources", "content": resources})

                # 🔥 Mostrar los recursos inmediatamente después de la explicación
                st.subheader("📚 Recursos adicionales para profundizar en el tema")
                cols = st.columns(len(resources))
                for i, resource in enumerate(resources):
                    with cols[i]:
                        st.markdown(f"#### {resource['title']}", unsafe_allow_html=True)
                        st.markdown(f"👨‍🏫 *Instructor:* {resource['instructor']}")
                        st.markdown(f"⭐ *Calificación:* {resource['rating']} / 5")
                        st.markdown(f"[🔗 Ver curso]({resource['url']})", unsafe_allow_html=True)


def get_llm_answer(topic, question=None):
    api_url = f"https://beecode.azurewebsites.net/chat"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if question:
        payload = {
            "topic": topic,  # Parámetro enviado en el body
            "question": question,
            "id_user": str(st.session_state.get("id_user"))
        }

        print(f'LLM Payload: {payload}')

    else:
        payload = {
            "topic": topic,  # Parámetro enviado en el body
            "id_user": str(st.session_state.get("id_user"))
        }

    print(api_url)
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        print(response.json())
        if response.status_code == 200:
            print(response.json())
            return response.json().get("response", "Lo siento, intente nuevamente")
    except Exception as e:
        st.error(f"Error al obtener subtemas: {str(e)}")


def get_additional_resources(id_training):
    api_url = f"https://ai-jobs-coaches-api-backend.azurewebsites.net/api/trainings/{id_training}/courses"
    print(f'{api_url}')
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

def get_topic_content_openai(topic):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # model = "deployment_name".
        messages=[
            {"role": "system", "content": "Eres un asistente experto en empleo con apoyo, dispuesto a dar explicaciones"
                                          "dinámicas de diversos temas. Principalmente enfocados en tecnologìa y programación."},
            {"role": "user", "content": generate_prompt(topic)}
        ]
    )
    return response.choices[0].message.content

def generate_prompt(topic):
    return f"""
    Explica el tema "{topic}" en un formato Markdown que pueda ser renderizado en Streamlit. 
    La explicación debe ser clara y estructurada con secciones, títulos y ejemplos de código cuando sea relevante.

    Formato esperado:
    - Usa encabezados con `##` o `###` para dividir las secciones.
    - Si el tema incluye código, usa bloques con triple comilla invertida (` ```python ... ``` `).
    - Usa listas, negritas y cursivas cuando sea útil para mejorar la comprensión.

    Ejemplo de salida esperada para "Decoradores en Python":

    ```
    ## 👉 Qué son los Decoradores en Python
    Los **decoradores** son funciones que modifican el comportamiento de otras funciones o métodos sin alterar su código fuente. Se usan para agregar funcionalidades como logging, control de acceso, validación de datos, etc.

    ---

    ## 👉 Ejemplo Básico
    ```python
    def mi_decorador(func):
        def envoltura():
            print("Antes de ejecutar la función")
            func()
            print("Después de ejecutar la función")
        return envoltura

    @mi_decorador
    def saludar():
        print("Hola!")

    saludar()
    ```
    **Salida:**
    ```
    Antes de ejecutar la función
    Hola!
    Después de ejecutar la función
    ```
    ```

    Devuelve solo el texto en formato Markdown sin explicaciones adicionales.
    """
