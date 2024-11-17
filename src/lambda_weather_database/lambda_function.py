# Librerías
import requests
import boto3
import os
from botocore.exceptions import ClientError
from utils.spain_geography import get_provinces_and_autonomous_cities


# Función Lambda
def lambda_handler(event: None, context: None):

    # Se obtiene el valor de la 'API KEY' pasado como variable de entorno
    api_key = os.getenv('API_KEY')

    # Se llama a 'get_provinces_and_autonomous_cities' para obtener los
    # nombres de las provincias y ciudades autónomas de España
    spain_provinces_cities_list = get_provinces_and_autonomous_cities()

    # Se inicia cliente de recursos de DynamoDB para gestionar una tabla
    dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb_table = dynamodb_resource.Table("Weather_DB")

    # Para cada una de las provincias y ciudades autónomas...
    for province in spain_provinces_cities_list:

        # Se hace una consulta 'GET' a la 'API' usando la 'API KEY' para
        # la provincia actual
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/"
            f"weather?q={province},es&APPID={api_key}&units=metric")

        # Si la respuesta es satisfactoria...
        if response.status_code == 200:

            # Se obtiene el JSON de la respuesta
            response = response.json()

            # Se almacena el ID único de la provincia
            id = response["id"]

            # Se almacena su nombre
            name = response["name"]

            # Se almacena la situación meteorológica
            weather = response["weather"][0]["main"]

            # Se almacena la temperatura
            temperature = response["main"]["temp"]

            # Se almacena la presión
            pressure = response["main"]["pressure"]

            # Se almacena la humedad
            humidity = response["main"]["humidity"]

            # Se almacena la velocidad del viento
            wind = response["wind"]["speed"]

            # Se almacena la nubosidad
            cloudiness = response["clouds"]["all"]

            # Si la clave "rain" está presente en la respuesta se almacenan
            # las precipitaciones, si no se deja el campo vacío
            rain = response["rain"]["1h"] if "rain" in response else "--"

            # Si la clave "snow" está presente en la respuesta se almacenan
            # las nevadas, si no se deja el campo vacío
            snow = response["snow"]["1h"] if "snow" in response else "--"

            # Latitud y longitud de la provincia o ciudad autónoma
            lat = response["coord"]["lat"]
            lon = response["coord"]["lon"]

        # Si no, la respuesta no es satisfactoria...
        else:

            # Se imprime mensaje de error
            print("Error: No se pudieron obtener los datos. "
                  f"Código de estado {response.status_code}")

        # Se prepara el diccionario para insertar en DynamoDB
        item = {
            'id': id,
            'name': name,
            'weather': weather,
            'temperature': temperature,
            'pressure': pressure,
            'humidity': humidity,
            'wind': wind,
            'cloudiness': cloudiness,
            'rain': rain,
            'snow': snow,
            'latitude': lat,
            'longitude': lon
        }

        # Se intenta insertar el diccionario en la tabla de Dynamo
        try:
            dynamodb_table.put_item(Item=item)
            print(f"Datos guardados en DynamoDB para {name}")

        # Si no, se ejecuta un error
        except ClientError as e:
            print(f"Error al guardar los datos en DynamoDB: "
                  f"{e.response['Error']['Message']}")
