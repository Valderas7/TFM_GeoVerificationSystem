# Recurso para crear un repositorio dentro de ECR. Se evita que Terraform
# intente destruir el repositorio
resource "aws_ecr_repository" "weather_repo" {
  name = var.name

  tags = {
    "Project" = "TFM"
  }
}
