# Variable para el nombre de la tabla de DynamoDB
variable "table_name" {
  type    = string
  default = "weather"
}


# Variable para el método de facturación
variable "billing_mode" {
  type    = string
  default = "PAY_PER_REQUEST"
}


# Variable para la clave de partición
variable "partition_key" {
  type    = string
  default = "Nombre"
}

# Variable para la clave de ordenación
variable "sort_key" {
  type    = string
  default = "Marca_Temporal"
}
