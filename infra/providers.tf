# Providers requeridos (solamente AWS)
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

# Configuración para el provider de AWS
provider "aws" {
  region     = var.aws_session["region"]
  access_key = var.aws_session["access_key"]
  secret_key = var.aws_session["secret_key"]
  token      = var.aws_session["token"]
}