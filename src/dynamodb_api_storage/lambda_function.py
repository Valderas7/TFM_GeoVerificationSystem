# Librerías
import requests
import json
import boto3
import os
from decimal import Decimal

# Función Lambda
def lambda_handler(event, context):

    # Se obtiene la variable de entorno SECRET_NAME (definida en Terraform),
    # que es el nombre del secreto definido en Terraform
    secret_name = os.getenv("SECRET_NAME")

    # Se inicia un cliente para AWS Secrets Manager
    secrets_client = boto3.client('secretsmanager')

    # Se intenta ejecutar el siguiente bloque de código...
    try:

        # Se intenta recuperar el contenido del nombre del secreto con el
        # cliente de boto3
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

    #NOMBRE_TABLA = "MoviesDB"

    # Se hace una consulta 'GET' a la 'API'
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={api_key}")

    # Lista para guardar cada diccionario
    results = []

    # Si el código de respuesta es OK se itera sobre todos los diccionarios (hay uno por película) 
    # del campo 'result' ('array') de la consulta, y a cada uno de ellos se le crea un campo 'rank' 
    # con un valor incremental. Se guarda cada nuevo diccionario en la lista 'results'
    if response.status_code == 200:
        for index, movie in enumerate(response.json()['results']):
            movie['rank'] = index + 1
            results.append(movie)

    # 2.- CONFIGURAD EL RECURSO Y TABLA DE DYNAMO_DB
    dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
    dybamodb_table = dynamodb_resource.Table(NOMBRE_TABLA)

    # 3.- MODIFICAD EL FORMATO DE LOS DATOS OBTENIDOS PARA QUE PUEDAN GUARDARSE EN DYNAMO_DB
    # Se itera sobre cada diccionario de la lista de diccionarios
    for dict in results:

        # Para cada diccionario dentro de la lista 'results', se cambia el tipo de la clave 'id'
        # a 'string' para que concuerde con el tipo especificado en la base de datos para la clave
        # de partición
        dict['id'] = str(dict['id'])

        # Para cada diccionario dentro de la lista 'results', se crea una clave 'y_m' (clave de
        # partición del índice secundario global) con valor 'YYYY_MM'.
        dict['y_m'] = dict['release_date'].split('-')[0] + '_' + dict['release_date'].split('-')[1]

        # Para cada diccionario dentro de la lista 'results', se crea una clave 'val' (clave de
        # ordenación del índice secundario global) con el valor de la clave 'vote_average'
        dict['val'] = dict['vote_average']

    # 4.- GUARDAD UNA ÚNICA ENTRADA EN DYNAMO DB, USANDO EL MÉTODO A CONTINUACIÓN
    single_element = results[0]
    dybamodb_table.put_item(Item=json.loads(json.dumps(single_element), parse_float=Decimal))