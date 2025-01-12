# Librerías
import requests
import boto3
import os
import json
import time
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
from utils.geography_utils import get_provinces_and_autonomous_cities
from utils.translate_dict_utils import translate_weather_dict

# AWS ya tiene un manejador de 'logging' por defecto, por lo que se selecciona
# y se establece su nivel a INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Se inicia cliente de recursos de DynamoDB para gestionar una tabla
dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
dynamodb_table = dynamodb_resource.Table("weather")


# Función Lambda
def lambda_handler(event: None, context: None):

    # Se intenta ejecutar el siguiente bloque de código
    try:

        # Se obtiene el valor de la 'API KEY' pasado como variable de entorno
        api_key = os.getenv('API_KEY')
        logger.info("API_KEY cargada correctamente.")

        # Se llama a 'get_provinces_and_autonomous_cities' para obtener los
        # nombres de las provincias y ciudades autónomas de España
        spain_provinces_cities_list = get_provinces_and_autonomous_cities()

        # Se obtiene el 'timestamp' numérico en segundos para comprobar
        # cuando se ejecuta la Lambda
        timestamp = int(time.time())

        # Para cada una de las provincias y ciudades autónomas...
        for province in spain_provinces_cities_list:

            # Se intenta ejecutar el siguiente bloque de código
            try:

                # Se hace una consulta 'GET' a la 'API' usando la 'API KEY'
                # para la provincia actual con un timeout de 10s
                response = requests.get(
                    "https://api.openweathermap.org/data/2.5/"
                    f"weather?q={province},es&APPID={api_key}&units=metric",
                    timeout=10
                )

                # Se lanza excepción si la respuesta no es un HTTP 200
                response.raise_for_status()

                # Se obtiene el JSON de la respuesta y se almacena
                data = response.json()

                # Se crea el diccionario para insertar en DynamoDB con el ID
                # de la provincia o ciudad (clave de partición), el
                # 'timestamp' (clave de ordenación), el nombre, la situación
                # meteorológica, temperatura, presión, humedad, viento,
                # nubosidad, y en caso de que las hubiese, lluvias y nevadas.
                # Además se almacena la longitud y latitud de cada lugar.
                item = {
                    'Nombre': data["name"],
                    'Marca_Temporal': timestamp,
                    'Clima': data["weather"][0]["main"],
                    'Temperatura': data["main"]["temp"],
                    'Presion_Atmosferica': data["main"]["pressure"],
                    'Humedad': data["main"]["humidity"],
                    'Velocidad_Viento': data["wind"]["speed"],
                    'Nubosidad': data["clouds"]["all"],
                    'Precipitaciones': (
                        data["rain"]["1h"] if "rain" in data else 0
                    ),
                    'Nevadas': data["snow"]["1h"] if "snow" in data else 0,
                    'Latitud': data["coord"]["lat"],
                    'Longitud': data["coord"]["lon"]
                }

                # Se llama a 'translate_weather_dict' para transformar los
                # valores de la clave 'Clima' a español
                item = translate_weather_dict(item)

                # Se almacena el nombre actualizado de la provincia para
                # usarlo simplemente en los mensajes de 'logging'
                province_updated = item["Nombre"]
                logger.info(f"Datos obtenidos para {province_updated}.")

                # Se convierte a 'string' el diccionario para convertir los
                # 'float' a 'Decimal'. Tras esto, se vuelve a convertir el
                # 'string' de vuelta a un diccionario
                item = json.loads(json.dumps(item), parse_float=Decimal)

                # Se intenta insertar el diccionario en la tabla de Dynamo
                try:

                    # Se añade el diccionario a la tabla de DynamoDB solo si
                    # la 'Marca_Temporal' no existe previamente para esa
                    # provincia en concreto (la condición solo se aplica al
                    # 'timestamp' dentro del contexto de cada provincia
                    # individual, y no en todas las provincias).
                    dynamodb_table.put_item(
                        Item=item,
                        ConditionExpression=(
                            'attribute_not_exists(Marca_Temporal)')
                    )
                    logger.info("Registro insertado en DynamoDB para "
                                f"{province_updated} con la época "
                                f"{timestamp}.")

                # Si hay alguna excepción con la inserción en DynamoDB
                except ClientError as e:

                    # Mensaje de logging de error
                    logger.error(
                        f"Error al introducir el registro en DynamoDB para "
                        f"{province_updated}: {str(e)}"
                    )

            # Si hay alguna excepción con la petición a la API...
            except requests.exceptions.RequestException as e:

                # Mensaje de logging de error
                logger.error(f"Error en la API para {province}: {str(e)}")

    # Si no se entra en la función Lambda el error es crítico
    except Exception as e:

        # Mensaje de logging de error crítico
        logger.critical(f"Error crítico en la función Lambda: {str(e)}")
