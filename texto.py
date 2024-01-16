import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from pydub.playback import play
import io


def text_to_speech(text):
    # Coloca aquí tus propias credenciales
    subscription_key = os.getenv('SPEETCH_API_KEY')
    endpoint = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, endpoint=endpoint)
    speech_config.speech_synthesis_voice_name='es-CO-SalomeNeural'
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text(text)
        
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Leyendo...")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

