# Se crea un secreto de AWS Secrets Manager
resource "aws_secretsmanager_secret" "api_key_secret" {
  name = "api_key_open_weather_map"
}

# Valor del secreto para el recurso creado arriba. Se almacena mediante un
# JSON stringificado con clave 'api_key' y con el valor de la API KEY
resource "aws_secretsmanager_secret_version" "api_key_secret_version" {
  secret_id     = aws_secretsmanager_secret.api_key_secret.id
  secret_string = jsonencode({ api_key = var.openweather_api_key })
}
