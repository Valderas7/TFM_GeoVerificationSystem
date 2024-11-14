# Variable para configurar el nombre de la Lambda
variable "function_name" {
  type    = string
  default = "api_data_to_dynamodb"
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
  default = "src/api_data_to_dynamodb/lambda_function.zip"
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

# Variable para almacenar el nombre del secreto almacenado
# en AWS Secrets Manager (proviene del 'outputs.tf' del módulo 
# 'secrets_manager')
variable "nombre_secreto" {
  type = string
}