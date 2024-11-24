# Recurso para crear una API Gateway de tipo API REST con un alcance regional
resource "aws_api_gateway_rest_api" "weather_api_gateway" {
  name        = var.api_name
  description = var.description

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}


# Se crea un recurso (en este caso la ruta '/weather') a partir del recurso
# raíz ('/') de la API
resource "aws_api_gateway_resource" "weather_resource" {
  rest_api_id = aws_api_gateway_rest_api.weather_api_gateway.id
  parent_id   = aws_api_gateway_rest_api.weather_api_gateway.root_resource_id
  path_part   = var.path_part
}


# Se crea un método GET para el recurso '/weather' de la API
# sin requerir ninguna autorización
resource "aws_api_gateway_method" "weather_resource_get" {
  rest_api_id   = aws_api_gateway_rest_api.weather_api_gateway.id
  resource_id   = aws_api_gateway_resource.weather_resource.id
  http_method   = "GET"
  authorization = "NONE"
}


# Se establece una integración con un backend (una función Lambda). Para ellas
# el método de integración HTTP siempre debe ser 'POST' y el tipo de entrada
# de integración debe ser 'AWS_PROXY'
resource "aws_api_gateway_integration" "integration_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.weather_api_gateway.id
  resource_id             = aws_api_gateway_resource.weather_resource.id
  http_method             = aws_api_gateway_method.weather_resource_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:lambda:us-east-1:"
}


# Deploy a la API para hacerla accesible
resource "aws_api_gateway_deployment" "example_deployment" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  stage_name  = "prod"
  depends_on  = [
    aws_api_gateway_integration.example_integration,
    aws_api_gateway_method.example_method
  ]
}