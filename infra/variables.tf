variable "aws_session" {
  type = map(string)
  default = {
    region     = "us-east-1"
    access_key = "your_access_key_value"
    secret_key = "your_secret_key_value"
    token      = "your_token_value"
  }
}
