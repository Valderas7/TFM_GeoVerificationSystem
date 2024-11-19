# Se establece que el 'backend' (el '.tfstate') se va a almacenar en remoto en
# un bucket de S3 con bloqueo de estado para evitar escribir simulatáneamente
terraform {
  backend "s3" {
    bucket         = "tfm_bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
  }
}
