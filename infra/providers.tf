# Providers requeridos (solamente AWS en su versión 5.77.0)
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.77.0"
    }
  }
}

# Configuración para el provider de AWS
provider "aws" {
  region = var.aws_region
}