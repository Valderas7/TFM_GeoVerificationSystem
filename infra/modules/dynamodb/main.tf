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
  attribute {
    name = "Nombre"
    type = "S"
  }
  attribute {
    name = "Situación_meteorológica"
    type = "S"
  }
  attribute {
    name = "Temperatura"
    type = "N"
  }
  attribute {
    name = "Presión"
    type = "N"
  }
  attribute {
    name = "Humedad"
    type = "N"
  }
  attribute {
    name = "Velocidad_viento"
    type = "N"
  }
  attribute {
    name = "Nubosidad"
    type = "N"
  }
  attribute {
    name = "Precipitaciones"
    type = "N"
  }
  attribute {
    name = "Nevada"
    type = "N"
  }
  attribute {
    name = "Latitud"
    type = "N"
  }
  attribute {
    name = "Longitud"
    type = "N"
  }
  tags = {
    Project = "TFM"
  }
}