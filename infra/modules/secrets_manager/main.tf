# Define un secreto
resource "aws_secretsmanager_secret" "api_key_secret" {
  name = "api_key_open_weather_map"
}

# Valor del secreto
resource "aws_secretsmanager_secret_version" "api_key_secret_version" {
  secret_id     = aws_secretsmanager_secret.api_key_secret.id
  secret_string = jsonencode({ api_key = var.api_key })
}

# Otorga permiso a la Lambda que consulta a la API y almacena los datos en
# DynamoDB para acceder a AWS Secrets Manager
resource "aws_lambda_permission" "lambda_access_to_secret" {
  statement_id  = "AllowLambdaToAccessSecretsManager"
  action        = "secretsmanager:GetSecretValue"
  principal     = "lambda.amazonaws.com"
  function_name = aws_lambda_function.get_api_data
}
