# Salida para referenciarla en otros módulos
output "secret_name" {
  value = aws_secretsmanager_secret.api_key_secret.name
}