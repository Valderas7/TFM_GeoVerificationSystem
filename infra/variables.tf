# Variable para almacenar la región de AWS
variable "aws_region" {
  type    = string
  default = "us-east-1"
}


# Variable para almacenar el nombre del bucket de S3 en el que almacenar el
# backend ('.tfstate')
variable "s3_bucket_name" {
  type    = string
  default = "tfm_bucket"
}


# Variable para indicar el nombre con el que se va a guardar el archivo de
# estado ('.tfstate') en el bucket de S3
variable "tfstate_key_name" {
  type    = string
  default = "terraform.tfstate"
}


# Variable para indicar el nombre de la tabla de DynamoDB que se va utilizar
# para habilitar el bloqueo del archivo de estado (backend)
variable "dynamodb_table_lock_state_name" {
  type    = string
  default = "terraform-state-lock"
}


# Variable para almacenar el valor de la API KEY de OpenWeatherMap. Como
# el valor está en 'terraform.tfvars', se carga automáticamente aquí (ya que
# la variable tiene el mismo nombre que la variable de 'terraform.tfvars')
variable "openweather_api_key" {
  description = "API key para el secreto"
  type        = string
  sensitive   = true
}
