# Librerías
import boto3
import decimal
import json
import urllib.parse
import logging
from utils.get_unique_keys_utils import (get_provinces_and_autonomous_cities,
                                         translate_province_list)

# AWS ya tiene un manejador de 'logging' por defecto, por lo que se selecciona
# y se establece su nivel a INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Se inicia cliente de recursos de DynamoDB para gestionar una tabla
dynamo_resource = boto3.resource('dynamodb', region_name='us-east-1')
dynamo_table = dynamo_resource.Table("weather")


# Se crea una clase para manejar los tipos de datos 'Decimal' y poder
# serializarlos en el JSON
class DecimalEncoder(json.JSONEncoder):

    # Método 'default' que recibe un parámetro 'o'
    def default(self, o):

        # Si 'o' es de tipo 'Decimal'...
        if isinstance(o, decimal.Decimal):

            # Se convierte de 'Decimal' a 'string'
            return str(o)

        # Llama a la implementación base para otros tipos
        return super(DecimalEncoder, self).default(o)


# Función Lambda
def lambda_handler(event, context):

    # Se intenta ejecutar el bloque de código
    try:

        # Se verifica si el evento contiene un parámetro de ruta 'provincia'.
        # Si lo hay, obtiene su valor; y si no lo hay, la variable vale 'None'
        place = (
            event.get('pathParameters', {}).get('provincia', None)
            if event.get('pathParameters') else None
        )

        # Si el parámetro de ruta 'provincia' existe, el método es
        # 'GET /clima/{provincia}'
        if place:

            # Mensaje de 'logging' de información
            logger.info("Se proporcionó una provincia. Recurso 'GET "
                        "/clima/provincia'")

            # Se decodifica el parámetro de la provincia para convertirlo
            # a su formato original ('Cádiz', 'La Coruña', 'Málaga', etc),
            # ya que en las URLs están transformadas a sus versiones sin
            # acentos, 'ñ' ni espacios
            place = urllib.parse.unquote(place)

            # Se intenta ejecutar el siguiente bloque de código
            try:

                # Se realiza una consulta a la tabla de DynamoDB cuya clave
                # primaria ('Nombre') es igual a la variable 'place',
                # obteniendo los doce registros (12 * 2 = 24h) más recientes
                # que hay (ordenados por la clave de partición) con dicha
                # clave primaria
                response = dynamo_table.query(
                    KeyConditionExpression="Nombre = :nombre",
                    ExpressionAttributeValues={':nombre': place},
                    ScanIndexForward=False,
                    Limit=12
                )

            # Si no se puede consultar la tabla de DynamoDB...
            except Exception as e:

                # Mensaje de 'logging' de error
                logger.error(f"Error al consultar DynamoDB: {str(e)}")

                # Se retorna un HTTP 500 con un diccionario indicando
                # que hay error en el servidor
                return {
                    "statusCode": 500,
                    "body": json.dumps({"error": "Error interno en "
                                        "DynamoDB"}),
                    "headers": {"Content-Type": "application/json"}
                }

            # Después de realizar la consulta, se verifica el campo 'Items'
            # del diccionario obtenido como respuesta a la consulta (debe ser
            # una lista de diccionarios)
            items = response.get('Items', None)

            # Si el campo 'Items' es una lista vacía (en Python las listas
            # vacías son 'False' en condición booleana) no se han encontrado
            # registros...
            if not items:

                # Mensaje de 'logging' de error
                logger.error(f"No se encontró '{place}' en la base de datos "
                             "de DynamoDB.")

                # Se retorna un HTTP 404 con un diccionario indicando que hay
                # un recurso no encontrado
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": f"Clave primaria '{place}' "
                                        "no encontrada en DynamoDB"}),
                    "headers": {"Content-Type": "application/json"}
                }

            # Mensaje 'logging' de información
            logger.info(f"Clave de partición '{place}' encontrada en "
                        "DynamoDB.")

            # Se devuelve un HTTP 200 con la lista de diccionarios, sin
            # escapar los caracteres no ASCII (tildes, etc) y que se muestren
            # tal y como son
            return {
                'statusCode': 200,
                'body': json.dumps(items, cls=DecimalEncoder,
                                   ensure_ascii=False)
            }

        # Si en cambio es None, el método es 'GET /clima'
        else:

            # Mensaje de 'logging' de información
            logger.info("No se proporcionó provincia. Recurso 'GET /clima'")

            # Se crea una lista para ir almacenando los registros más recientes
            # de cada clave de partición
            recent_items_list = []

            # Se llama a 'get_provinces_and_autonomous_cities' para obtener
            # los nombres de las provincias y ciudades autónomas de España, y
            # posteriormente 'translate_province_list' para transformar cada
            # una de ellas a la nomenclatura que tienen en DynamoDB, teniendo
            # así una lista con todas las claves de partición únicas
            unique_partition_keys_list = (
                translate_province_list(
                    get_provinces_and_autonomous_cities()
                )
            )

            # Para cada clave de partición...
            for partition_key in unique_partition_keys_list:

                # Se realiza una consulta a la tabla de DynamoDB indicando
                # la clave de partición a buscar, ordenando los resultados en
                # orden descendente según la clave de ordenación, y limitando
                # los resultados a solo un registro (el más reciente)
                response = dynamo_table.query(
                    KeyConditionExpression="Nombre = :nombre",
                    ExpressionAttributeValues={':nombre': partition_key},
                    ScanIndexForward=False,
                    Limit=1
                )

                # Si hay una clave 'Items' en la respuesta y la longitud de
                # la lista de dicha clave es mayor que cero (se ha encontrado
                # registro)...
                if 'Items' in response and len(response['Items']) > 0:

                    # Se almacena el primer (y único) elemento de la lista de
                    # la clave 'Items', que es el registro encontrado
                    item = response['Items'][0]

                    # Mensaje de 'logging' de información
                    logger.info(f"Encontrado registro para {item['Nombre']} "
                                f"con tiempo Unix {item['Marca_Temporal']}")

                    # Se añade el registro (un diccionario) a la lista
                    # 'recent_items_list'
                    recent_items_list.append(item)

                # Si no se encuentra registro tras la consulta...
                else:

                    # Mensaje de 'logging' de error
                    logger.error(f"No se encontró registro para "
                                 f"{partition_key}")

            # Se devuelve un HTTP 200 con un diccionario con clave 'data' que
            # tiene como valor la lista 'recent_items_list' que almacena todos
            # los registros más recientes para cada provincia o ciudad
            # autónoma (clave de partición)
            return {
                "statusCode": 200,
                "body": json.dumps({"data": recent_items_list},
                                   cls=DecimalEncoder)
            }

    # Si no se puede ejecutar el bloque de código anterior se lanza una
    # excepción
    except Exception as e:

        # Mensaje de 'logging' crítico
        logger.critical(f"Error en la función Lambda: {str(e)}")

        # Se devuelve un HTTP 500 con un diccionario que indica que hay error
        # en el servidor
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
