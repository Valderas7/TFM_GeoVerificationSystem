# Bloque de salida para recopilar el URI de la Lambda creada
output "lambda_uri" {
  description = "URI de la Lambda utilizada para consultar datos climáticos"
  value       = aws_lambda_function.dynamodb_weather_query.invoke_arn
}
