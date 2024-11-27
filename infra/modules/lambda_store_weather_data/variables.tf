# Variable para almacenar el nombre del evento de EventBridge
variable "event_rule" {
  type    = string
  default = "event_cron"
}


# Variable para almacenar expresión 'cron' para saber cuando se ejecuta
# la Lambda (actualmente cada 2 horas)
variable "schedule_expression" {
  type    = string
  default = "cron(0 */2 * * ? *)"
}


# Variable para configurar el nombre de la Lambda
variable "function_name" {
  type    = string
  default = "get_and_store_weather_data"
}


# Variable para configurar la concurrencia de la Lambda
variable "concurrency_lamba" {
  type    = number
  default = 1
}


# Variable para almacenar el ARN para el rol de la Lambda
variable "role_lambda" {
  type    = string
  default = "arn:aws:iam::637423493436:role/LabRole"
}


# Variable para almacenar la ruta del '.zip' de la Lambda
variable "lamba_path" {
  type    = string
  default = "resources/get_and_store_weather_data.zip"
}


# Variable para almacenar la descripción de la Lambda
variable "lambda_description" {
  type    = string
  default = "Realiza solicitudes GET a OpenWeatherMap y guarda datos en DynamoDB"
}


# Variable para almacenar el 'runtime' de la Lambda
variable "runtime" {
  type    = string
  default = "python3.11"
}


# Variable para almacenar el 'handler' de la Lambda
variable "handler" {
  type    = string
  default = "lambda_function.lambda_handler"
}


# Variable para almacenar el ARN de la 'layer' a usar
variable "layer" {
  type        = string
  description = "ARN de la 'layer' a usar para la Lambda"
}


# Variable para almacenar el 'timeout' en segundos de la Lambda
variable "timeout" {
  type    = number
  default = 30
}


# Variable para recopilar el valor de la API KEY de OpenWeatherMap
variable "api_key" {
  type      = string
  sensitive = true
}
