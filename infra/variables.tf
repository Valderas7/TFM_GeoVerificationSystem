variable "aws_session" {
  type = map(string)
  default = {
    region     = "us-east-1"
    access_key = "ASIAZI2LGUE6DTKFUZQP"
    secret_key = "1R9ZWOfJYEVfPknNL+SMWSCl1LgEZi8WinEFWkpZ"
    token      = "IQoJb3JpZ2luX2VjED0aCXVzLXdlc3QtMiJIMEYCIQCnM1YICyPtUQ32X40ISTO2CZQ9Z/B1HR4a/H37Y1JFqwIhAPuYXfwhR2BUP3deZpbvY1pkYNeTW0PxByPfe77knDNEKrQCCMb//////////wEQABoMNjM3NDIzNDkzNDM2Igwu033zmQ5xngixq1kqiAI2HOUAVeBTf9fUlnYPHTzesKk5D6so9PlNFZwV6PhS8oy33fRBgTt+r+heHCgNNYSzrt5jnCQ1wNKOmCWTMZq3vszkT6rn+JJxI8FcKBYtbVlfPpoMIu8FaKbwFstWHo5quhBIvQpflYbgCM+Okpg7EB3r4bsiPuRqdXSoNA57DuHTIB5FyX0loMdp0xL2Gs7nb0SdBRbzdQyhttXMUxnggkXoWoIBBgvsulMCDjcYygwLpWby7C9TruZpo9VKjBS/G8ZJ4bMNhh8enw7hS5m60F3TeZDkmQEofQwt7d87ZcFNY7zzHym9oq/PGxeKRBDBQl0cAwkNum9z4lDB8X1+AlOt5RWYvNQwj/rOuQY6nAHXa3nGdWBAYZ/t8SPC/qpUPSIvepet7AU2RCJ8lxpHBS2V+HSOgH3kW4RhwvVTpjPi5SkcQC3mpGhXsSbGegDaI7QKfHCrfRjVRlpHTfw0tTvIV7ZCaw3Kp7wb+zlDA+2Yno3mhF6MeEaW+ck3EViAsTaa7lgdx9Np14wFRrSQ5dlI3nVEAz6gwXxdch4EpsakotwNOeO+EK0rpgw="
  }
}

# Variable ya usada en el modulo 'secrets_manager'. Como en el módulo no
# tiene valor por defecto, también se declara en el 'variables.tf' de la
# raíz del proyecto de Terraform
variable "openweather_api_key" {
  description = "API key para el secreto"
  type        = string
  sensitive   = true
}