# Variable para almacenar el nombre del bucket de S3 en el que almacenar
# el backend (archivo '.tfstate')
variable "backend_bucket" {
  type    = string
  default = "tfm_bucket"
}


# Variable para almacenar el nombre de la tabla de DynamoDB en la que
# habilitar el bloqueo de estado ('state locking') para evitar que múltiples
# ejecuciones de Terraform modifiquen el estado ('tfstate') simultáneamente
variable "backend_table" {
  type    = string
  default = "terraform-state-lock"
}
