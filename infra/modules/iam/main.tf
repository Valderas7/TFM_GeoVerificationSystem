# Se asigna una política administrada de AWS para proporcionarle permisos de
# lectura y escritura de AWS Secrets Manager al rol "LabRole"
resource "aws_iam_role_policy_attachment" "lambda_secret_policy_attachment" {
  role       = "LabRole"
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}
