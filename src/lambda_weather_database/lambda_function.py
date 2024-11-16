# Librerías
import requests
import boto3
import os

# Función Lambda
def lambda_handler(event, context):

    # Se obtiene el valor de la 'API KEY' pasado como variable de entorno
    api_key = "fd8c832d3847abbe1f5846f583d84ff3"

    # Se inicia cliente de recursos de DynamoDB
    dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')

    # Se hace una consulta 'GET' a la 'API' usando la 'API KEY' almacenada en
    # AWS Secrets Manager
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/" \
            f"weather?q=Madrid,es&APPID={api_key}&units=metric")

    if response.status_code == 200:
        print(response.json())

lambda_handler(None, None)