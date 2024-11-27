# Bloque de salida para recopilar el URI de la Lambda creada
output "lambda_uri" {
  description = "URI de la Lambda utilizada para consultar datos climáticos"
  value       = aws_lambda_function.query_weather_data.invoke_arn
}
