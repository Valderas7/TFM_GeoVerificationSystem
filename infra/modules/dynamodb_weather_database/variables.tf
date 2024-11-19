# Variable para el nombre de la tabla de DynamoDB
variable "table_name" {
    type = string
    default = "Weather_DB"
}


# Variable para el método de facturación
variable "billing_mode" {
    type = string
    default = "PAY_PER_REQUEST"
}
