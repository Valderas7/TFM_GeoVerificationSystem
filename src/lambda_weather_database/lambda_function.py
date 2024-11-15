# Librerías
import requests
import json
import boto3
import os
from decimal import Decimal

# Función Lambda
def lambda_handler(event, context):

    api_key = os.getenv('API_KEY')
    print(api_key)

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