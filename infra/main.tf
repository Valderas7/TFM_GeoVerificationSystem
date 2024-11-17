# Se llama al módulo 'lambda_weather_database' pasando el valor de la API KEY
# (que está en 'var.openweather_api_key') a la variable 'api_key' del módulo
module "lambda_weather_database" {
  source  = "./modules/lambda_weather_database"
  api_key = var.openweather_api_key
}

# Se llama al módulo '' pasando el valor de la API KEY
# (que está en 'var.openweather_api_key') a la variable 'api_key' del módulo
module "dynamo_weather_database" {
  source  = "./modules/dynamodb_weather_database"
}