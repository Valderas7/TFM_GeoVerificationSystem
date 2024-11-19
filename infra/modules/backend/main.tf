# Recurso para crear una tabla de DynamoDB para habilitar el bloqueo de estado
# ('state locking') del backend para evitar que múltiples ejecuciones de
# Terraform modifiquen el estado simultáneamente
resource "aws_dynamodb_table" "terraform_lock" {
  name         = var.backend_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


# Recurso para crear un bucket de S3 donde almacenar en remoto el backend
resource "aws_s3_bucket" "terraform_backend" {
  bucket = var.backend_bucket
}
