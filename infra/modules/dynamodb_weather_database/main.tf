# Se crea una tabla de DynamoDB para ir recopilando la información del clima
# consultada en la API de OpenWeatherMap. Solo es necesario declarar la clave
# de partición y la clave de ordenación (no todas las columnas) tanto en las
# 'key' como en los 'attribute'
resource "aws_dynamodb_table" "weather_db" {
  name         = var.table_name
  billing_mode = var.billing_mode
  hash_key     = var.partition_key
  range_key    = var.sort_key

  attribute {
    name = var.partition_key
    type = "S"
  }

  attribute {
    name = var.sort_key
    type = "N"
  }

  tags = {
    Project = "TFM"
  }
}
