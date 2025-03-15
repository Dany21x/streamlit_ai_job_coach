import streamlit as st
from auth.decorators import require_auth
from utils.azure_speech import speech_recognize_once_from_mic
import tempfile
from streamlit_extras.stylable_container import stylable_container

@require_auth
def show():
    st.title("Chat de entrenamiento")
    st.write("Bienvenido al chat de entrenamiento.")

    # Initialize chat history as an empty list
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto
    user_input = st.chat_input("Escribe un mensaje...")

    with stylable_container(
            key="bottom_content",
            css_styles="""
                {
                    position: fixed;
                    bottom: 120px;
                }
                """,
    ):
        audio_value = st.audio_input("Graba un mensaje de voz")

    audio_text = None
    if audio_value:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_value.getvalue())  # Guardar audio en un archivo temporal
            temp_audio_path = temp_audio.name

        audio_text = speech_recognize_once_from_mic(temp_audio_path)  # Convertir audio a texto
        #st.success(f"Texto detectado: {audio_text}")

    # Procesar entrada (texto o audio convertido)
    if user_input or audio_text:
        message_content = user_input if user_input else audio_text

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(message_content)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": message_content})

        response = f'echo: {message_content}'

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        audio_text = None
