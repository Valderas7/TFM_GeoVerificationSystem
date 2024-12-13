# 'Output' para almacenar los IDs de las subredes del módulo
output "subnets" {
  value = aws_subnet.web_application_subnets.*.id
}


# 'Output' para almacenar el ID del 'Grupo de Seguridad' del módulo
output "security_group" {
  value = aws_security_group.web_application_security_group.id
}