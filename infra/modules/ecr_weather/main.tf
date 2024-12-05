# Recurso para crear un repositorio dentro de ECR
resource "aws_ecr_repository" "weather_repo" {
  name = var.name

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    "Project" = "TFM"
  }
}