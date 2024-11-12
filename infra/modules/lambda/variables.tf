# Variable para configurar la concurrencia de la Lambda
variable "concurrency_lamba" {
  type    = number
  default = 1
}

# Variable para el rol de la Lambda
variable "role_lambda" {
  type    = string
  default = "LabRole"
}