import os
import openai
import json
from pc_command import PcCommand
from voz import speech_to_text_live
from weather import Weather
from texto import text_to_speech
import azure.cognitiveservices.speech as speechsdk


openai.api_type = "azure"
openai.api_base = "https://domotica.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv('OPENAI_API_KEY')


orden=speech_to_text_live()
print(orden)

response = openai.ChatCompletion.create(
  engine="asistente",
  messages = [ {"role": "system", "content": "Eres un asistente muy util"},
                {"role": "user", "content": orden},],
  functions=[{
                    "name": "open_brave",
                    "description": "Abrir el explorador Brave en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            }
                        }
                    }
                },
             {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicación, debe ser una ciudad",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "send_email",
                    "description": "Enviar un correo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient": {
                                "type": "string",
                                "description": "La dirección de correo que recibirá el correo electrónico",
                            },
                            "subject": {
                                "type": "string",
                                "description": "El asunto del correo",
                            },
                            "body": {
                                "type": "string",
                                "description": "El texto del cuerpo del correo",
                            }
                        },
                        "required": [],
                    },
                },
             
             ],
  function_call="auto",
 )
#print(response["choices"][0]["message"]["content"])
message = response["choices"][0]["message"]

if message.get("function_call"):
  #Sip
  function_name = message["function_call"]["name"] #Que funcion?
  args = message.to_dict()['function_call']['arguments'] #Con que datos?
  print("Funcion a llamar: " + function_name)
  args = json.loads(args)
  if function_name == "open_brave":
    PcCommand().open_chrome(website=args["website"])
  elif function_name == "get_weather":
    function_response = Weather().get(args["ubicacion"])
    function_response = json.dumps(function_response)
    print(f"Respuesta de la funcion: {function_response}")
else:
    speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv("SPEETCH_API_KEY"), 
    region="eastus"
    )
    message_text = [{"role": "user", "content": orden}]
    completion = openai.ChatCompletion.create(
        engine="asistente",
        messages=[
                {"role": "system", "content": "Eres un asistente muy util"},
                {"role": "user", "content": orden},
                message,
                {
                    "role": "function",
                    "name": "get_weather",
                    "content": "el clima actual es de 20 c° humedad 30%",
                },
            ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    speech_config.speech_synthesis_voice_name = "es-CO-SalomeNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config)
    speech_synthesizer.speak_text(
    completion['choices'][0]['message']['content'])
    #input_text = completion['choices'][0]['message']['content']
    #output_file_path = "output.wav"
    #text_to_speech(input_text, output_file_path)
