# Llamada al módulo 'lambda_store_weather_data' pasando el valor de la API KEY
# (que está en 'var.openweather_api_key') a la variable 'api_key' del módulo
# para crear la función Lambda que realiza consultas a la API de
# OpenWeatherMap y guarda los registros en una tabla de DynamoDB
module "lambda_store_weather_data" {
  source  = "./modules/lambda_store_weather_data"
  api_key = var.openweather_api_key
}


# Se llama al módulo 'dynamo_weather_database' para crear la base de datos de
# DynamoDB en la que almacenar los datos de la API de OpenWeatherMap
# consultados con la función Lambda
module "dynamo_weather_database" {
  source = "./modules/dynamodb_weather_database"
}
