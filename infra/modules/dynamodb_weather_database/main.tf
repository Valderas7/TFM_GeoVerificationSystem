# Se crea una tabla de DynamoDB para ir recopilando la información del clima
# consultada en la API de OpenWeatherMap
resource "aws_dynamodb_table" "weather_db" {
  name           = var.table_name
  billing_mode   = var.billing_mode
  hash_key       = "Id"
  attribute {
    name = "Id"
    type = "N"
  }
  tags = {
    Project = "TFM"
  }
}