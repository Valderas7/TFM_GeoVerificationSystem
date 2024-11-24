# Variable para el nombre de la API REST
variable "api_name" {
  type    = string
  default = "weather_api_gateway"
}


# Variable para la descripción de la API REST
variable "description" {
  type    = string
  default = "API REST para consultar el clima de provincias y ciudades autónomas de España"
}


# Variable para indicar el 'path' del recurso
variable "path_part" {
  type    = string
  default = "weather"
}
