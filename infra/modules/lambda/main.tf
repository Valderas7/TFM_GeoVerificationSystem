# Se crea una función Lambda para consultar la API del Tiempo y almacenar
# los datos en una tabla de DynamoDb. Se especifica la ruta local del .zip
# donde está el código de la Lambda
# Los argumentos 'runtime' y 'handler' son obligatorios cuando la función
# se añade mediante 'filename'
# También se pasa como variable de entorno la clave del secreto creado
# en el módulo 'secrets_manager'
resource "aws_lambda_function" "get_api_data_store_dynamodb" {
  function_name                  = "get_api_data_store_dynamodb"
  role                           = var.role_lambda
  reserved_concurrent_executions = var.concurrency_lamba
  filename                       = var.lamba_path
  runtime                        = var.runtime
  handler                        = var.handler
  environment {
    variables = {
      SECRET_NAME = aws_secretsmanager_secret.api_key_secret.name
    }
  }
}