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


# Variable para almacenar la región de AWS
variable "aws_region" {
  type    = string
  default = "us-east-1"
}


# Variable para almacenar el valor de la API KEY de OpenWeatherMap. Como
# el valor está en 'terraform.tfvars', se carga automáticamente aquí (ya que
# la variable tiene el mismo nombre que la variable de 'terraform.tfvars')
variable "openweather_api_key" {
  description = "API key para el secreto"
  type        = string
  sensitive   = true
}
