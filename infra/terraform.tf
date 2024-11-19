# Se establece que el 'backend' ('.tfstate') se va a almacenar en remoto en un
# bucket de S3 con bloqueo de estado para evitar escribir a la vez en él
# Pre-requisitos: El 'bucket' y la tabla deben ser creados previamente
terraform {
  backend "s3" {
    bucket         = "valderas-tfm-bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }
}