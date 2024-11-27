# Se crea una función Lambda para integrar la API Gateway. Se especifica la
# ruta local del '.zip' del código de la lambda y el ARN de la 'layer'.
# NOTA: Los argumentos 'runtime' y 'handler' son obligatorios cuando la
# función se añade mediante 'filename'
resource "aws_lambda_function" "query_weather_data" {
  function_name                  = var.function_name
  role                           = var.role_lambda
  reserved_concurrent_executions = var.concurrency_lamba
  filename                       = var.lamba_path
  source_code_hash               = filebase64sha256(var.lamba_path)
  description                    = var.lambda_description
  runtime                        = var.runtime
  handler                        = var.handler
  layers                         = [var.layer]
  timeout                        = var.timeout

  tags = {
    "Project" = "TFM"
  }
}
