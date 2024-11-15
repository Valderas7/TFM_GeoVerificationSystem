# Se crea una 'layer' para usar las librerías necesarias en Lambda
resource "aws_lambda_layer_version" "tfm_layer" {
  layer_name = var.layer_name
  filename   = var.layer_path
}

# Se crea una función Lambda para consultar la API de OpenWeather y almacenar
# los datos en una tabla de DynamoDB. Se especifica la ruta local del '.zip'
# del código de la lambda y el ARN de la 'layer'.
# NOTA: Los argumentos 'runtime' y 'handler' son obligatorios cuando la
# función se añade mediante 'filename'
resource "aws_lambda_function" "lambda_weather_database" {
  function_name                  = var.function_name
  role                           = var.role_lambda
  reserved_concurrent_executions = var.concurrency_lamba
  filename                       = var.lamba_path
  runtime                        = var.runtime
  handler                        = var.handler
  layers                         = [aws_lambda_layer_version.tfm_layer.arn]
  environment {
    variables = {
      API_KEY = var.api_key
    }
  }
}