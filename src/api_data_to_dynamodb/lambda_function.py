# Librerías
import requests
import json
import boto3
import os
from decimal import Decimal

# Función Lambda
def lambda_handler(event, context):

    # Se obtiene la variable de entorno SECRET_NAME de la Lambda, que es
    # el nombre del secreto definido en Terraform
    secret_name = os.getenv("SECRET_NAME")

    # Se inicia un cliente para AWS Secrets Manager
    secrets_client = boto3.client('secretsmanager')

    # Se intenta ejecutar el siguiente bloque de código...
    try:

        # Se consulta el contenido del nombre del secreto en
        # AWS Secrets Mangaer
        response = secrets_client.get_secret_value(SecretId=secret_name)

        # Se deserializa a un diccionario de Python el campo 'SecretString'
        # (valor desencriptado del secreto) de la respuesta
        secret = json.loads(response['SecretString'])

        # Se extrae el valor de la clave 'api_key' del diccionario, que es
        # donde está el valor de la API KEY de OpenWeatherMap
        api_key = secret['api_key']

    # Si no...
    except Exception as e:

        # Se imprime error
        print(f"Error al obtener el secreto: {e}")
        raise e

    # Se inicia cliente de recursos de DynamoDB
    dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')

    # Se accede con dicho cliente a la tabla "WeatherDB"
    dybamodb_table = dynamodb_resource.Table("WeatherDB")

    # Se hace una consulta 'GET' a la 'API' usando la 'API KEY' almacenada en
    # AWS Secrets Manager
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?"
                            f"q=Madrid,es&APPID={api_key}&units=metric")

    # Lista para guardar cada objeto
    results = []

    # Si el código de respuesta es OK
    if response.status_code == 200:
        print(results)