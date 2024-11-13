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
  default = "./"
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