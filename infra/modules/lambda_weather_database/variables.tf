# Variable para almacenar el nombre de la layer
variable "layer_name" {
  type    = string
  default = "tfm_layer"
}

# Variable para almacenar la ruta del '.zip' de la layer
variable "layer_path" {
  type    = string
  default = "resources/tfm_layer.zip"
}

# Variable para almacenar el nombre del evento de EventBridge
variable "event_rule" {
  type    = string
  default = "event_cron"
}

# Variable para almacenar la ruta del '.zip' de la layer
variable "schedule_expression" {
  type    = string
  default = "cron(0 * * * ? *)"

}

# Variable para configurar el nombre de la Lambda
variable "function_name" {
  type    = string
  default = "lambda_weather_database"
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
  default = "resources/weather_dynamo_lambda.zip"
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

# Variable para recopilar el valor de la API KEY de OpenWeatherMap
variable "api_key" {
  type      = string
  sensitive = true
}