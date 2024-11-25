# Variable para configurar el nombre de la Lambda
variable "function_name" {
  type    = string
  default = "query_weather_data"
}


# Variable para configurar la concurrencia de la Lambda
variable "concurrency_lamba" {
  type    = number
  default = 1
}


# Variable para almacenar el ARN para el rol de la Lambda ('LabRole')
variable "role_lambda" {
  type    = string
  default = "arn:aws:iam::637423493436:role/LabRole"
}


# Variable para almacenar la ruta del '.zip' de la Lambda
variable "lamba_path" {
  type    = string
  default = "resources/.zip"
}


# Variable para almacenar la descripción de la Lambda
variable "lambda_description" {
  type    = string
  default = "Consulta datos climáticos de OpenWeatherMap almacenados en DynamoDB ante eventos de API Gateway"
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


# Variable para almacenar el 'timeout' en segundos de la Lambda
variable "timeout" {
  type    = number
  default = 30
}