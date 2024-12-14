# Bloque de datos que permite el acceso a la lista de zonas de
# disponibilidad que están disponibles dentro de la región configurada
# en el 'provider' de AWS.
data "aws_availability_zones" "available" {
  state = "available"
}


# Recurso para crear una VPC con un CIDR privado en el que 26 bits son
# fijos y se utilizan para identificar la red; y los 6 bits restantes se
# utilizan para identificar dispositivos (64 IPs en total) dentro de la red.
resource "aws_vpc" "web_application_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    "Project" = "TFM"
    "Name"    = "web-application-vpc"
  }
}

# Se crean dos recursos para crear subredes (una subred por recurso) dentro
# de la VPC creada. A cada una de ellas se le aplica la función 'cidrsubnet'
# para aumentar en uno la máscara original y que sea '/27' (es decir, 32 IPs
# por subred para dispositivos). Por otra parte, cada subred estará dentro de
# una zona de disponibilidad distinta de la región.
resource "aws_subnet" "web_application_subnets" {
  count             = var.subnets_count
  vpc_id            = aws_vpc.web_application_vpc.id
  cidr_block        = cidrsubnet(aws_vpc.web_application_vpc.cidr_block, 1, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    "Project" = "TFM"
    "Name"    = "web-application-subnet-${count.index}"
  }
}


# Recurso para crear un 'Grupo de Seguridad' que permite el tráfico entrante
# exclusivamente en el puerto 8501 desde cualquier IP mediante 'TCP'. También
# se permite el tráfico saliente hacia todas las IPs y puertos mediante todos
# los protocolos (TCP, UDP, ICMP...), algo necesario para conectarse a ECR
# y usar una imagen de Docker.
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
    "Name"    = "web_application_security_group"
  }
}


# Recurso para crear una 'Puerta de enlace a Internet' para que la VPC, y
# por tanto, sus subredes, tengan acceso a Internet.
resource "aws_internet_gateway" "web_application_igw" {
  vpc_id = aws_vpc.web_application_vpc.id

  tags = {
    "Project" = "TFM"
    "Name"    = "web_application_igw"
  }
}


# Recurso para crear una tabla de enrutamiento para la VPC de forma
# que se redirija todo el tráfico saliente de ella a la 'Puerta de enlace
# a Internet'. Como consecuencia, las redes asociadas a esta tabla de
# enrutamiento van a ser públicas.
resource "aws_route_table" "web_application_route_table" {
  vpc_id = aws_vpc.web_application_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.web_application_igw.id
  }

  tags = {
    "Project" = "TFM"
    "Name"    = "web-application-route-table"
  }
}


# Se crean dos recursos de asociación (uno para cada subred): cada uno de
# estos recursos asocia la tabla de enrutamiento (que redirije el tráfico
# a la 'Puerta de enlace a Internet') con la subred correspondiente, haciendo
# las subredes públicas.
resource "aws_route_table_association" "web_application_route_table_association" {
  count          = var.subnets_count
  subnet_id      = aws_subnet.web_application_subnets[count.index].id
  route_table_id = aws_route_table.web_application_route_table.id
}
