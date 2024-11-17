# Se crea una 'layer' para usar las librerías necesarias en Lambda
resource "aws_lambda_layer_version" "tfm_layer" {
  layer_name = var.layer_name
  filename   = var.layer_path
}

# Se crea un evento de 'EventBridge' que se ejecuta cada X tiempo
resource "aws_cloudwatch_event_rule" "event_cron" {
  name = var.event_rule
  schedule_expression = var.schedule_expression
  tags = {
    "Project" = "TFM"
  }
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
  tags = {
    "Project" = "TFM"
  }
}

# Se enlaza el evento de EventBridge con la función Lambda creada arriba (es
# decir, el 'trigger')
resource "aws_cloudwatch_event_target" "trigger" {
  rule      = aws_cloudwatch_event_rule.event_cron.name
  arn       = aws_lambda_function.lambda_weather_database.arn
}

# Una vez se crea el 'trigger' se crea un permiso para que EventBridge tenga
# los permisos necesarios para ejecutar la función Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_weather_database.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.event_cron.arn
}