# Variable para el nombre del cluster
variable "cluster_name" {
  type    = string
  default = "weather_web_application_cluster"
}

# Variable para el nombre de la definición de la tarea
variable "task_definition_name" {
  type    = string
  default = "weather_web_application_task_definition"
}


# Variable para almacenar el ARN para el rol de la tarea de ECS
variable "role_iam" {
  type    = string
  default = "arn:aws:iam::637423493436:role/LabRole"
}


# Variable para pasar la URL del repositorio de ECR en la definición de
# la tarea
variable "repo_url" {
  type = string
}


# Variable para pasar el 'tag' de la URL del repositorio de ECR en la
# definición de la tarea
variable "repo_tag" {
  type    = string
  default = ":1.0"
}


# Variable para indicar la CPU que va a usar la definición de tarea
variable "cpu" {
  type    = number
  default = 1024 # 1 vCPU
}


# Variable para indicar la memoria que va a usar la definición de tarea
variable "memory" {
  type    = number
  default = 2048 # 2 GB RAM
}


# Variable para el puerto del contenedor
variable "container_name" {
  type    = string
  default = "weather_web_application_container"
}


# Variable para el puerto del contenedor
variable "container_port" {
  type    = number
  default = 8501
}


# Variable para el nombre del servicio
variable "service_name" {
  type    = string
  default = "web_application_service"
}


# Variable para el número de instancias de contenedor de ECS
variable "instances_number" {
  type    = number
  default = 2
}


# Variable para las subredes de la VPC definida en el
# módulo 'vpc_weather_network'
variable "subnets" {
  type = string
}


# Variable para el 'Security Group' de la VPC definida en el
# módulo 'vpc_weather_network'
variable "security_group" {
  type = string
}
