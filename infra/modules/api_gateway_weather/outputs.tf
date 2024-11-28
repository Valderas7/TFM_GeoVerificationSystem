# Bloque de salida para almacenar el ARN de ejecución de la API Gateway
# que se usa para darle permisos para ejecutar una Lambda
output "api_arn" {
  description = "ARN de ejecución de la API Gateway"
  value = aws_api_gateway_rest_api.clima_api_gateway.execution_arn
}