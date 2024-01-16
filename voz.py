import os
import azure.cognitiveservices.speech as speechsdk

def speech_to_text_live():
    # Coloca aquí tus propias credenciales
    subscription_key = os.getenv('SPEETCH_API_KEY')
    endpoint = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    language = "es-CO"
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, endpoint=endpoint, speech_recognition_language=language)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Escuchando...")
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No se pudo reconocer el audio."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return "Reconocimiento cancelado: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            return "Error details: {}".format(cancellation_details.error_details)

