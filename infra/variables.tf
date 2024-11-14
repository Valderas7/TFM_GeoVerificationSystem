# Variable para almacenar la región de AWS
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

# Variable ya usada en el modulo 'secrets_manager'. Como en el módulo no
# tiene valor por defecto, también se declara en el 'variables.tf' de la
# raíz del proyecto de Terraform
variable "openweather_api_key" {
  description = "API key para el secreto"
  type        = string
  sensitive   = true
}