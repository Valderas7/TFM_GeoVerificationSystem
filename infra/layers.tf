# Se crea una 'layer' para usar las librerías necesarias en Lambda
resource "aws_lambda_layer_version" "tfm_layer" {
  layer_name          = var.layer_name
  filename            = var.layer_path
  source_code_hash    = filebase64sha256(var.layer_path)
  compatible_runtimes = ["python3.11"]
}