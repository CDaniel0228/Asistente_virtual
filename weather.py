import requests
import os
from dotenv import load_dotenv

class Weather():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('WEATHER_API_KEY')
        
    def get(self, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.key}'
        response = requests.get(url)
        # Verifica si la solicitud fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            # Convierte la respuesta a formato JSON
            data = response.json()

            # Extrae la información relevante sobre el clima
            temperatura_actual = data['main']['temp']
            temperatura_actualC = temperatura_actual - 273.15
            descripcion_clima = data['weather'][0]['description']
            humedad = data['main']['humidity']
            traducciones_clima = {
                'Clear': 'Despejado',
                'Clouds': 'Nublado',
                'Rain': 'Lluvia',
                'Snow': 'Nieve',
                'Thunderstorm': 'Tormenta eléctrica',
                'overcast clouds': 'Mayormente nublado'
            # Agrega más traducciones según sea necesario
            }   
            descripcion_en_espanol = traducciones_clima.get(descripcion_clima)

            # Imprime la información
            print(f'Humedad: {humedad}%')
            print(f'Temperatura Actual: {temperatura_actual} K {temperatura_actualC:.2f} C°')
            print(f'Descripción del Clima: {descripcion_en_espanol}')
        else:
            print(f'Error al obtener el clima. Código de respuesta: {response.status_code}')