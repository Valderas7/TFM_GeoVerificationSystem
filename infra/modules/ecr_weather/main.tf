# Recurso para crear un repositorio dentro de ECR
resource "aws_ecr_repository" "weather_repo" {
  name = var.name

  tags = {
    "Project" = "TFM"
  }
}