# Providers requeridos (solamente AWS)
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.74.0"
    }
  }
  required_version = ">= 1.5.0"
}

# Configuración para el provider de AWS
provider "aws" {
  region = var.aws_region
}