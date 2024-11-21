# Librerías
import requests
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
from utils.spain_geography import get_provinces_and_autonomous_cities

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
                    'Id': data["id"],
                    'Name': data["name"],
                    'Weather': data["weather"][0]["main"],
                    'Temperature': data["main"]["temp"],
                    'Pressure': data["main"]["pressure"],
                    'Humidity': data["main"]["humidity"],
                    'Wind': data["wind"]["speed"],
                    'Cloudiness': data["clouds"]["all"],
                    'Rain': data["rain"]["1h"] if "rain" in data else None,
                    'Snow': data["snow"]["1h"] if "snow" in data else None,
                    'Latitude': data["coord"]["lat"],
                    'Longitude': data["coord"]["lon"]
                }

                # Se intenta insertar el diccionario en la tabla de Dynamo
                try:

                    # Se comprueba si en la tabla ya hay un registro con la
                    # clave de de partición ('Id') de la provincia actual
                    response = dynamodb_table.get_item(
                        Key={'Id': item["Id"]}
                    )

                    # Si no hay un registro en la tabla con esa clave de
                    # partición...
                    if 'Item' not in response:

                        # Se añade el diccionario a la tabla de DynamoDB
                        # (convirtiéndolo a 'string' para convertir los
                        # 'floats' en 'Decimal'; y después convirtiéndolos de
                        # vuelta a diccionario)
                        dynamodb_table.put_item(
                            Item=json.loads(
                                json.dumps(item),
                                parse_float=Decimal
                            ),
                            ConditionExpression='attribute_not_exists(Id)'
                        )

                    # Si ya hay registro con esa clave...
                    else:

                        # Se actualizan los campos
                        dynamodb_table.update_item(
                            Key={'Id': item["Id"]},
                            ConditionExpression='attribute_exists(Id)',
                            UpdateExpression=(
                                "SET Weather = :val1, "
                                "Temperature = :val2, "
                                "Pressure = :val3, "
                                "Humidity = :val4, "
                                "Wind = :val5, "
                                "Cloudiness = :val6, "
                                "Rain = :val7, "
                                "Snow = :val8"
                            ),
                            ExpressionAttributeValues={
                                ':val1': json.loads(
                                    json.dumps(item['weather']),
                                    parse_float=Decimal
                                ),
                                ':val2': json.loads(
                                    json.dumps(item['temperature']),
                                    parse_float=Decimal
                                ),
                                ':val3': json.loads(
                                    json.dumps(item['pressure']),
                                    parse_float=Decimal
                                ),
                                ':val4': json.loads(
                                    json.dumps(item['humidity']),
                                    parse_float=Decimal
                                ),
                                ':val5': json.loads(json.dumps(item['wind']),
                                                    parse_float=Decimal),
                                ':val6': json.loads(
                                    json.dumps(item['cloudiness']),
                                    parse_float=Decimal
                                ),
                                ':val7': json.loads(json.dumps(item['rain']),
                                                    parse_float=Decimal),
                                ':val8': json.loads(json.dumps(item['snow']),
                                                    parse_float=Decimal)
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
