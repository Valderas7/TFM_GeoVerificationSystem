# Variable para declarar el valor de la API KEY sin valor por defecto (se
# cogerá de 'terraform.tfvars')
variable "openweather_api_key" {
  description = "API key para el secreto"
  type        = string
  sensitive   = true
}
