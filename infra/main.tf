# Se llama al módulo 'iam'
module "iam" {
  source = "./modules/iam"
}

# Se llama al módulo 'secrets_manager' pasando la variable de la API KEY
module "secrets" {
  source              = "./modules/secrets_manager"
  openweather_api_key = var.openweather_api_key
}

# Se llama al módulo Lambda
module "lambda" {
  source = "./modules/lambda"
}