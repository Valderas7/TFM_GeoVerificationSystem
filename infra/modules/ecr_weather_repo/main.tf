# Recurso para crear un repositorio dentro de ECR
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
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1 # Prioridad de la regla
        description  = "Eliminar Imágenes Antiguas con el mismo Tag"
        action = {
          type = "expire" # Acción cuando se cumpla la regla (eliminar imágenes)
        }
        filter = {
          tagStatus     = "tagged" # Aplica a imágenes etiquetadas
          tagPrefixList = []       # Aplica a imágenes con cualquier 'tag'
        }
        imageCountMoreThan = 1 # Mantiene una imagen con el mismo tag, eliminando las anteriores
      }
    ]
  })
}
