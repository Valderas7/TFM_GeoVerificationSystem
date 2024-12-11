# Llamada al módulo 'lambda_store_weather_data' pasando el valor de la API KEY
# a la variable 'api_key' del módulo; y el valor del ARN de la 'layer' a la
# variable 'layer' del módulo, para así crear la función Lambda que realiza
# consultas a la API de OpenWeatherMap y guarda los registros en una tabla de
# DynamoDB
module "lambda_store_weather_data" {
  source  = "./modules/lambda_store_weather_data"
  layer   = aws_lambda_layer_version.tfm_layer.arn
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
# recursos de API Gateway pasando el valor del ARN de la 'layer' a la variable
# 'layer' del módulo y también el output 'api_arn' del módulo
# 'api_gateway_weather' a la variable 'api_arn' del módulo para que tenga el
# URI de ejecución de la API Gateway
module "lambda_query_weather_data" {
  source  = "./modules/lambda_query_weather_data"
  layer   = aws_lambda_layer_version.tfm_layer.arn
  api_arn = module.api_gateway_weather.api_arn
}


# Se llama al módulo 'api_gateway_weather' para crear la API y todos sus
# recursos y métodos asociados. Se le pasa el output 'lambda_uri' del módulo
# 'lambda_query_weather_data' a la variable 'lambda_uri_integration' de este
# módulo de API Gateway para que tenga el URI de la Lambda a usar
module "api_gateway_weather" {
  source                 = "./modules/api_gateway_weather"
  lambda_uri_integration = module.lambda_query_weather_data.lambda_uri
}


# Se llama al módulo 'ecr_weather_repo' para crear un repositorio dentro de ECR
# para almacenar imágenes de Docker
module "ecr_weather_repo" {
  source = "./modules/ecr_weather_repo"
}


# Se llama al módulo 'ecs_weather_cluster' para crear un cluster de ECS
# pasando la URL del repositorio de ECR definida como 'output' en el
# módulo 'ecr_weather_repo', además de una definición de tarea para lanzar
# el contenedor
module "ecs_weather_cluster" {
  source         = "./modules/ecs_weather_cluster"
  repo_url       = module.ecr_weather_repo.repo_url
  subnets        = module.vpc_weather_network.subnets
  security_group = module.vpc_weather_network.security_group
}


# Se llama al módulo 'vpc_weather_network' para crear los recursos de red
# que se van a usar para el servicio de ECS
module "vpc_weather_network" {
  source = "./modules/vpc_weather_network"
}
