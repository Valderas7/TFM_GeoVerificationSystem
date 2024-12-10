# Recurso para crear un cluster de ECS
resource "aws_ecs_cluster" "web_application_cluster" {
  name = var.cluster_name

  tags = {
    "Project" = "TFM"
  }
}


# Recurso para crear una definición de tarea y así especificar como ejecutar
# un contenedor en ECS. Se va a ejecutar con Fargate con un modo de red
# 'awsvpc', que suele usarse con Fargate
resource "aws_ecs_task_definition" "web_application_task" {
  family                   = var.task_definition_name
  execution_role_arn       = var.role_iam
  task_role_arn            = var.role_iam
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
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