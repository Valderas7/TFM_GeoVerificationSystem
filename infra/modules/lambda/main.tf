# Función Lambda para consultar la API del Tiempo y almacenar los datos
# en una tabla de DynamoDb
resource "aws_lambda_function" "get_api_data" {
  function_name                  = "get_api_data"
  role                           = var.role_lambda
  reserved_concurrent_executions = var.concurrency_lamba
}