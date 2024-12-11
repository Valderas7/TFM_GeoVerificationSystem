# Recurso para crear una VPC con un CIDR privado en el que hay
# un total de 256 direcciones IP
resource "aws_vpc" "web_application_vpc" {
  cidr_block = "10.0.0.0/24"

  tags = {
    "Project" = "TFM"
  }
}

# Recurso para crear subredes
resource "aws_subnet" "web_application_subnets" {
  count                   = 2
  vpc_id                  = aws_vpc.web_application_vpc.id
  cidr_block              = cidrsubnet(aws_vpc.web_application_vpc.cidr_block, 4, count.index)
  map_public_ip_on_launch = true

  tags = {
    "Project" = "TFM"
  }
}


# Recurso para crear un 'SG' que permite el tráfico entrante en el
# puerto 8501 desde cualquier IP mediante protocolo 'TCP'. También se
# permite el tráfico saliente hacia todas las IPs y puertos
resource "aws_security_group" "web_application_security_group" {
  vpc_id = aws_vpc.web_application_vpc.id

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Project" = "TFM"
  }

}
