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


# Se llama al módulo 'lambda_query_weather_data' para realizar las consultas
# de datos climáticos almacenados en DynamoDB cada vez que se invocan
# recursos de API Gateway
module "lambda_query_weather_data" {
  source = "./modules/lambda_query_weather_data"
}


# Se llama al módulo 'api_gateway_weather' para crear la API y todos sus
# recursos y métodos asociados. Se le pasa el output 'lambda_uri' del módulo
# 'lambda_query_weather_data' a la variable 'lambda_uri_integration' de este
# módulo de API Gateway para que tenga el URI de la Lambda a usar
module "api_gateway_weather" {
  source                 = "./modules/api_gateway_weather"
  lambda_uri_integration = module.lambda_query_weather_data.lambda_uri
}
