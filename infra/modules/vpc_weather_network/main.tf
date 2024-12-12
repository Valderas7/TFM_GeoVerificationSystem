# Bloque de datos que permite el acceso a la lista de zonas de
# disponibilidad que pueden ser accedidas por la cuenta AWS dentro de la
# región configurada en el 'provider' de AWS
data "aws_availability_zones" "available" {
  state = "available"
}


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
  availability_zone       = data.aws_availability_zones.available.names[count.index]

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


# Recurso para crear una puerta de enlace de internet para que las subredes
# públicas de la VPC definida tengan acceso a Internet, y por tanto, las
# instancias o tareas del móulo ECS
resource "aws_internet_gateway" "web_application_igw" {
  vpc_id = aws_vpc.web_application_vpc.id

  tags = {
    "Project" = "TFM"
  }
}


# Recurso para crear una tabla de enrutamiento para la VPC definida de forma
# que se redirija el tráfico externo a la puerta de enlace de internet
resource "aws_route_table" "web_application_route_table" {
  vpc_id = aws_vpc.web_application_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.web_application_igw.id
  }

  tags = {
    "Project" = "TFM"
  }
}


# Se crean dos recursos de asociación: cada uno de ellos servirá para
# asociar la tabla de enrutamiento con la subred correspondiente
resource "aws_route_table_association" "web_application_route_table_association" {
  count          = 2
  subnet_id      = aws_subnet.web_application_subnets[count.index].id
  route_table_id = aws_route_table.web_application_route_table.id
}
