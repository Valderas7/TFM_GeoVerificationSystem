# Recurso para crear un cluster de ECS
resource "aws_ecs_cluster" "web_application_cluster" {
  name = var.cluster_name

  tags = {
    "Project" = "TFM"
  }
}


# Recurso para crear una definición de tarea y así especificar como ejecutar
# un contenedor en ECS. Se va a ejecutar con Fargate con un modo de red
# 'awsvpc' (necesario para Fargate)
resource "aws_ecs_task_definition" "web_application_task" {
  family                   = var.task_definition_name
  execution_role_arn       = var.role_iam
  task_role_arn            = var.role_iam
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory
  container_definitions = jsonencode([
    {
      name      = var.container_name
      image     = "${var.repo_url}${var.repo_tag}"
      cpu       = var.cpu
      memory    = var.memory
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]
    }
  ])
}


# Recurso para crear un servicio ECS en el cluster y con la definición de
# tarea definidas. Se le asigna una IP pública, el grupo de seguridad y las
# subredes creadas en el módulo de 'VPC' para realizar la configuración de
# red del servicio (el grupo de seguridad permite el tráfico entrante solo en
# el puerto 8501 desde cualquier IP mediante 'TCP'; y el tráfico saliente
# hacia todas las IPs y puertos mediante todos los protocolos).
resource "aws_ecs_service" "web_application_service" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.web_application_cluster.arn
  task_definition = "${aws_ecs_task_definition.web_application_task.family}:${aws_ecs_task_definition.web_application_task.revision}"
  desired_count   = var.instances_number
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip = true
    security_groups  = [var.security_group]
    subnets          = var.subnets
  }
}
