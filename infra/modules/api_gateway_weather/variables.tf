# Variable para el nombre de la API REST
variable "api_name" {
  type    = string
  default = "clima_api_gateway"
}


# Variable para la descripción de la API REST
variable "description" {
  type    = string
  default = "API REST para consultar el clima de provincias y ciudades autónomas de España"
}


# Variable para indicar un 'path' de un recurso de la API
variable "path_part" {
  type    = string
  default = "clima"
}


# Variable para indicar un 'subpath' del un recurso de la API
variable "subpath_part" {
  type    = string
  default = "{provincia}"
}


# Variable para pasar el URI de la Lambda definida en otro módulo
variable "lambda_uri_integration" {
  description = "URI de la función Lambda a usar en API Gateway"
  type        = string
}


# Variable para indicar el 'stage' del despliegue de la API
variable "stage" {
  type    = string
  default = "prod"
}
