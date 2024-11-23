# Librerías
import requests
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
from utils.geography_utils import get_provinces_and_autonomous_cities
from utils.translate_dict_utils import translate_weather_dict

# Configuración básica del 'logging'
logging.basicConfig(level=logging.INFO)


# Función Lambda
def lambda_handler(event: None, context: None):

    # Se intenta ejecutar el siguiente bloque de código
    try:

        # Se obtiene el valor de la 'API KEY' pasado como variable de entorno
        api_key = os.getenv('API_KEY')
        logging.info("API_KEY cargada correctamente.")

        # Se llama a 'get_provinces_and_autonomous_cities' para obtener los
        # nombres de las provincias y ciudades autónomas de España
        spain_provinces_cities_list = get_provinces_and_autonomous_cities()

        # Se inicia cliente de recursos de DynamoDB para gestionar una tabla
        dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
        dynamodb_table = dynamodb_resource.Table("Weather_DB")

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

                # Se obtiene el JSON de la respuesta para ver los datos
                data = response.json()
                logging.info(f"Datos obtenidos para {province}")

                # Se crea el diccionario para insertar en DynamoDB con el ID
                # de la provincia o ciudad (clave de partición), el nombre,
                # la situación meteorológica, temperatura, presión, humedad,
                # viento, nubosidad, y en caso de que las hubiese, lluvias
                # y nevadas.
                # Además se almacena la longitud y latitud de cada sitio
                item = {
                    'Nombre': data["name"],
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

                # Se convierte a 'string' el diccionario para convertir los
                # 'float' a 'Decimal'. Tras esto, se vuelve a convertir el
                # 'string' de vuelta a un diccionario
                item = json.loads(json.dumps(item), parse_float=Decimal)

                # Se intenta insertar el diccionario en la tabla de Dynamo
                try:

                    # Se comprueba si en la tabla ya hay un registro con la
                    # clave de de partición ('Nombre') de la provincia actual
                    response = dynamodb_table.get_item(
                        Key={'Nombre': item["Nombre"]}
                    )

                    # Si no hay un registro en la tabla con esa clave de
                    # partición...
                    if 'Item' not in response:

                        # Se añade el diccionario a la tabla de DynamoDB
                        dynamodb_table.put_item(
                            Item=item,
                            ConditionExpression='attribute_not_exists(Nombre)'
                        )

                    # Si no, ya hay registro con esa clave...
                    else:

                        # Por tanto, se actualizan los registros con los
                        # nuevos valores
                        dynamodb_table.update_item(
                            Key={'Nombre': item["Nombre"]},
                            ConditionExpression='attribute_exists(Nombre)',
                            UpdateExpression=(
                                "SET Clima = :val1, "
                                "Temperatura = :val2, "
                                "Presion_Atmosferica = :val3, "
                                "Humedad = :val4, "
                                "Velocidad_Viento = :val5, "
                                "Nubosidad = :val6, "
                                "Precipitaciones = :val7, "
                                "Nevadas = :val8"
                            ),
                            ExpressionAttributeValues={
                                ':val1': item['Clima'],
                                ':val2': item['Temperatura'],
                                ':val3': item['Presion_Atmosferica'],
                                ':val4': item['Humedad'],
                                ':val5': item['Velocidad_Viento'],
                                ':val6': item['Nubosidad'],
                                ':val7': item['Precipitaciones'],
                                ':val8': item['Nevadas']
                            }
                        )

                # Si hay alguna excepción con la inserción en DynamoDB
                except ClientError as e:

                    # Mensaje de logging de error
                    logging.error(
                        f"Error en DynamoDB con la provincia {province}: "
                        f"{str(e)}"
                    )

            # Si hay alguna excepción con la petición a la API...
            except requests.exceptions.RequestException as e:

                # Mensaje de logging de error
                logging.error(
                    f"Error en la API para la provincia {province}: {str(e)}"
                )

    # Si no se entra en la función Lambda el error es crítico
    except Exception as e:

        # Mensaje de logging de error crítico
        logging.critical(f"Error crítico en la función Lambda: {str(e)}")
