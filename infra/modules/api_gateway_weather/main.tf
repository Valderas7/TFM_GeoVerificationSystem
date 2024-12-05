# Recurso para crear una API Gateway de tipo API REST con un alcance regional
resource "aws_api_gateway_rest_api" "clima_api_gateway" {
  name        = var.api_name
  description = var.description

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    "Project" = "TFM"
  }
}


# Se crea un recurso (en este caso la ruta '/clima') a partir del ID del
# recurso raíz ('/') de la API
resource "aws_api_gateway_resource" "clima" {
  rest_api_id = aws_api_gateway_rest_api.clima_api_gateway.id
  parent_id   = aws_api_gateway_rest_api.clima_api_gateway.root_resource_id
  path_part   = var.path_part
}


# Se crea un recurso (en este caso la ruta '/clima/{provincia}') a partir del
# 'ID' del recurso ('/clima') de la API
resource "aws_api_gateway_resource" "clima_provincia" {
  rest_api_id = aws_api_gateway_rest_api.clima_api_gateway.id
  parent_id   = aws_api_gateway_resource.clima.id
  path_part   = var.subpath_part
}


# Se crea un método GET para el recurso '/clima' de la API sin requerir
# ninguna autorización
resource "aws_api_gateway_method" "clima_get" {
  rest_api_id   = aws_api_gateway_rest_api.clima_api_gateway.id
  resource_id   = aws_api_gateway_resource.clima.id
  http_method   = "GET"
  authorization = "NONE"
}


# Se crea un método GET para el recurso '/clima/{provincia}' de la API
# sin requerir ninguna autorización. Se pasa a la función de integración
# el parámetro '{provincia}' de la ruta, ya que la requiere la función
# Lambda de integración
resource "aws_api_gateway_method" "clima_provincia_get" {
  rest_api_id   = aws_api_gateway_rest_api.clima_api_gateway.id
  resource_id   = aws_api_gateway_resource.clima_provincia.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.provincia" = true
  }
}


# Se establece una integración del recurso '/clima' con un backend (una
# función Lambda). Para las Lambdas el método de integración HTTP siempre debe
# ser 'POST' y el tipo de entrada de integración debe ser 'AWS_PROXY'
resource "aws_api_gateway_integration" "clima_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.clima_api_gateway.id
  resource_id             = aws_api_gateway_resource.clima.id
  http_method             = aws_api_gateway_method.clima_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_uri_integration
}


# Se establece una integración del recurso '/clima/{provincia}' con un backend
# (una función Lambda). Para las Lambdas el método de integración HTTP siempre
# debe ser 'POST' y el tipo de entrada de integración debe ser 'AWS_PROXY'. Se
# pasa al respondedor de la función de integración el parámetro '{provincia}'
# de la ruta
resource "aws_api_gateway_integration" "clima_provincia_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.clima_api_gateway.id
  resource_id             = aws_api_gateway_resource.clima_provincia.id
  http_method             = aws_api_gateway_method.clima_provincia_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_uri_integration

  request_parameters = {
    "integration.request.path.provincia" = "method.request.path.provincia"
  }
}


# Se hace el despliegue de la API REST indicando el ID de la API. Se declaran
# dependencias explícitas con las dos integraciones API Gateway - Lambda
# declaradas en este archivo
resource "aws_api_gateway_deployment" "clima_api_gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.clima_api_gateway.id
  depends_on = [
    aws_api_gateway_integration.clima_get_integration,
    aws_api_gateway_integration.clima_provincia_get_integration
  ]
}


# Se configura un 'stage' para realizar el despliegue de la API
resource "aws_api_gateway_stage" "stage" {
  rest_api_id   = aws_api_gateway_rest_api.clima_api_gateway.id
  stage_name    = var.stage
  deployment_id = aws_api_gateway_deployment.clima_api_gateway_deployment.id
}
