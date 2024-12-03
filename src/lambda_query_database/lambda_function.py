# Librerías
import boto3
import decimal
import json
import urllib.parse
import logging

# Configuración básica del 'logging'
logging.basicConfig(level=logging.INFO)

# Se inicia cliente de recursos de DynamoDB para gestionar una tabla
dynamo_resource = boto3.resource('dynamodb', region_name='us-east-1')
dynamo_table = dynamo_resource.Table("Weather_DB")


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

            # Se decodifica el parámetro de la provincia para convertirlo
            # a su formato original ('Cádiz', 'La Coruña', 'Málaga', etc),
            # ya que en las URLs se transforman a palabras sin acentos ni
            # eñes ni espacios
            place = urllib.parse.unquote(place)

            # Se realiza la consulta a la tabla de DynamoDB cuya clave
            # primaria ('Nombre') es igual a la variable 'place'
            response = dynamo_table.get_item(Key={'Nombre': place})
            logging.info(f"Parámetro 'provincia' recibido: {place}")

            # Después de realizar la consulta, se verifica el campo 'Item' del
            # diccionario obtenido como respuesta a la consulta
            item = response.get('Item', None)

            # Si la clave consultada no existe...
            if not item:

                # Se devuelve diccionario de error
                logging.warning(f"No se encontró la provincia '{place}' en "
                                "la base de datos.")
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "Provincia no encontrada"}),
                    "headers": {"Content-Type": "application/json"}
                }

            # Se devuelve un diccionario con el código de estado HTTP 200 y
            # el JSON, sin escapar los caracteres no ASCII (tildes, etc)
            logging.info(f"Provincia '{place}' encontrada en DynamoDB. "
                         "Retornando datos.")
            return {
                'statusCode': 200,
                'body': json.dumps(item, cls=DecimalEncoder,
                                   ensure_ascii=False)
            }

        # Si en cambio es None, el método es 'GET /clima'
        else:

            # Se realiza un escaneo de la tabla de Dynamo
            response = dynamo_table.scan()
            logging.info("No se proporcionó una provincia. Realizando un "
                         "escaneo de todos los registros.")

            # Después de realizar el escaneo, se verifica el campo 'Items'
            # del diccionario obtenido como respuesta al escaneo
            items = response.get('Items', None)

            # Se devuelve un diccionario con el código de estado y el JSON
            logging.info(f"Se encontraron {len(items)} registros en la "
                         "base de datos.")
            return {
                "statusCode": 200,
                "body": json.dumps({"data": items}, cls=DecimalEncoder)
            }

    # Si no se puede ejecutar el bloque de código anterior se lanza una
    # excepción
    except Exception as e:

        # Se devuelve un diccionario con un error HTTP 500 y el error que ha
        # ocurrido
        logging.error(f"Error en la función lambda_handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
