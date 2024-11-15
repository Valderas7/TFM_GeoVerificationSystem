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
  region = var.aws_region
}