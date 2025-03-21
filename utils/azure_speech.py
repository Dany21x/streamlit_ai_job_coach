import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import tempfile

load_dotenv()

speech_key = os.environ.get("SPEECH_KEY")
service_region = os.environ.get("SPEECH_REGION")

def speech_recognize_once_from_mic(audio_path, lang_code='es-ES'):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = lang_code
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        return f"Speech Recognition canceled: {result.cancellation_details.reason}"
    return "Unknown error"

def text_to_speech(text, lang_code="es-CO", voice_name="es-PE-AlexNeural"):
    """Convierte texto a audio usando Azure TTS con un idioma y voz específicos"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Establecer idioma y voz
    speech_config.speech_synthesis_language = lang_code
    speech_config.speech_synthesis_voice_name = voice_name

    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

    audio_config = speechsdk.AudioConfig(filename=temp_audio_file.name)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted and result.audio_data:
        return temp_audio_file.name  # Devolver la ruta del archivo de audio
    else:
        #st.error(f"Error en la síntesis: {result.reason}")
        return None

def text_to_speech_beta(text, lang_code='es-ES-AlvaroNeural'):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_language = lang_code
        audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config,
                                                         audio_output_config=audio_output_config)

        result = speech_synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Synthesized Speech !")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled due to ⚠{}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
    except Exception as e:
        print(f"An error occurred: {e}")