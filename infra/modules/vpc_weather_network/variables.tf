# Variable para almacenar el bloque CIDR de la VPC
variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/26"
}

# Variable para indicar el número de subredes a crear
variable "subnets_count" {
  type    = number
  default = 2
}