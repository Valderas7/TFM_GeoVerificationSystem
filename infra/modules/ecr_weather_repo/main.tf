# Recurso para crear un repositorio dentro de ECR. Se evita que Terraform
# intente destruir el repositorio
resource "aws_ecr_repository" "weather_repo" {
  name = var.name

  tags = {
    "Project" = "TFM"
  }
}


# Recurso para crear una política de ciclo de vida para el repositorio, de
# forma que se eliminan imágenes antiguas si se sube una nueva al
# repositorio con un 'tag' ya usado anteriormente
resource "aws_ecr_lifecycle_policy" "streamlit_lifecycle_policy" {
  repository = aws_ecr_repository.weather_repo.name
  policy     = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Eliminar imágenes antiguas con el mismo tag",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": [""],
        "countType": "imageCountMoreThan",
        "countNumber": 1
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
  depends_on = [aws_ecr_repository.weather_repo]
}