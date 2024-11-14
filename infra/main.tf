# Se llama al módulo 'iam'
module "iam" {
  source = "./modules/iam"
}

# Se llama al módulo 'secrets_manager' pasando la variable de la API KEY
module "secrets" {
  source              = "./modules/secrets_manager"
  openweather_api_key = var.openweather_api_key
}

# Se llama al módulo Lambda pasando el parámetro requerido 'nombre_secreto'
# que referencia a 'secret_name' dentro del módulo 'secrets'
module "lambda_store_dynamodb" {
  source         = "./modules/lambda_store_dynamodb"
  nombre_secreto = module.secrets.secret_name
}