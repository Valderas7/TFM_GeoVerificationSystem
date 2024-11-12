# Librerías
import requests
import json
import boto3    
from decimal import Decimal

# Función para obtener el secreto
def get_secret():

    # Se inicia cliente de AWS Secrets Manager
    client = boto3.client('secretsmanager')

    # Se obtiene el valor del secreto llamado 'api_key_open_weather_map'
    response = client.get_secret_value(SecretId="api_key_open_weather_map")

    # Se convierte a un objeto de Python la clave 'SecretString' de la
    # respuesta del cliente de Boto3
    secret = json.loads(response['SecretString'])

    # La función retorna el valor de la API KEY
    return secret['api_key']

# Se llama a la función 'get_secret' para obtener el valor de la API KEY de
# OpenWeatherMap
api_key = get_secret()

NOMBRE_TABLA = "MoviesDB"

# Clave de mi cuenta para acceder a la API de TMDB
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