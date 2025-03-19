import openai
import streamlit as st
from auth.decorators import require_auth
from utils.azure_speech import speech_recognize_once_from_mic
import tempfile
import os
from streamlit_extras.stylable_container import stylable_container
from openai import AzureOpenAI

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

    # Inicializar historial de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto
    user_input = st.chat_input("Escribe un mensaje...")

    # 🔥 Mover el audio input al sidebar SOLO en modo chat
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

        response = f'echo: {message_content}'

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        audio_text = None


    session_state = st.session_state.get("selected_item_id", None)
    get_new_explanation = st.session_state.get("get_new_explanation", False)
    print(f'session_state in chat: {session_state}')

    if session_state is not None and get_new_explanation:
        print(f'st.session_state.get(["selected_item_id"], None) is not None')
        st.session_state["get_new_explanation"] = False
        topic = f'{st.session_state.get("item_name", None)} orientado a un curso de {st.session_state.get("training_name", None)}'
        topic_md = get_topic_content(topic)
        # Agregar la explicación inicial al historial del chat
        st.session_state.messages.append({"role": "assistant", "content": topic_md})

        # Mostrar la explicación en la interfaz
        with st.chat_message("assistant"):
            st.markdown(topic_md)

def get_topic_content(topic):
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
