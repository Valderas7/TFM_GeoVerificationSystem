# Se establece que el 'backend' (el '.tfstate') se va a almacenar en remoto en
# un bucket de S3
terraform {
  backend "s3" {
    bucket         = "tfm_bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }
}


# Recurso para crear una tabla de DynamoDB para habilitar el bloqueo de estado
# ('state locking') del backend para evitar que múltiples ejecuciones de
# Terraform modifiquen el estado simultáneamente
resource "aws_dynamodb_table" "terraform_lock" {
  name           = "terraform-state-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


# Se llama al módulo 'lambda_weather_database' pasando el valor de la API KEY
# (que está en 'var.openweather_api_key') a la variable 'api_key' del módulo
module "lambda_weather_database" {
  source  = "./modules/lambda_weather_database"
  api_key = var.openweather_api_key
}


# Se llama al módulo 'dynamo_weather_database'
module "dynamo_weather_database" {
  source  = "./modules/dynamodb_weather_database"
}
