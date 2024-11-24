# Librerías
import boto3
import decimal
import json

# Se inicia cliente de recursos de DynamoDB para gestionar una tabla
dynamo_resource = boto3.resource('dynamodb', region_name='us-east-1')
dynamo_table = dynamo_resource.Table("Weather_DB")


# Se crea una clase para manejar los tipos de datos 'Decimal'
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# Función Lambda
def lambda_handler(event, context):

    # Se almacena el parámetro 'Nombre' del evento
    province = event['pathParameters']['Nombre']

    # Se realiza la consulta a la tabla de DynamoDB cuya clave primaria
    # ('Nombre') es igual a la variable 'movie_id'
    item = dynamo_table.get_item(Key={'Nombre': province})

    # Después de realizar la consulta, se devuelve ésta y también algunos
    # campos extra. Por tanto, se selecciona el campo 'Item', que es el
    # diccionario de la consulta
    item = item['Item']

    # Se devuelve un diccionario con el código de estado y el JSON
    return {
        'statusCode': 200,
        'body': json.dumps(item, cls=DecimalEncoder)
    }
