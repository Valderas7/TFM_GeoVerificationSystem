# Providers requeridos
terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
    }
  }
}

# Configuración para el provider de AWS
provider "aws" {
    region = "us-east-1"
    access_key = "ASIAZI2LGUE6OIUAZS4I"
    secret_key = "TyLsBvb/NfKpWOts+x0Bqm6eLZx5wxtehAh1rUbp"
    token = "IQoJb3JpZ2luX2VjEOH//////////wEaCXVzLXdlc3QtMiJIMEYCIQC1XfYefGz/b3i6K+6MSiMY88TKtmydUJc/ZfqLA1DyTQIhAKc63YjkoMXusnZmLA0EpA0CFl4MCg1cnzDzoi6aBDTXKqsCCGoQABoMNjM3NDIzNDkzNDM2IgxXxJ2vZ3XIE3Y6QIsqiAIPBOHAj+7FRbSfBin1qeGolz++ZbEY0kBADy9IRakLM/NGs5iCAxVcihg16mpb0t+KtJ83DKzTTMwEasWtFdqY1XsKhMTGvkNEhLfa5zjX6XsWM2wkadHTy3OzRBYcPoI6CluVRhMY1zt4yzyqZ9nZZvOnoKP/B6eifnuattH2vXt/rJW4EYcgjmRSDToaWllxe2TImZrgkFTiOxMPpBtsxx+LZ0Vc3Pp4O82StKA6Jn/1wjzdmPwwErILaShkOOzHUIp/Cbe8la6o1/GFXe/bsDb8UrSuJuTpl1UcXwTVVLTFg7qOcAWYQzVY4kW6PyH2TX/uBkpyq12IwVUqYxCG3LhCZsSjM2gw2em6uQY6nAHoOXcM18sTdzlnjgo+8Vv3zLjvxb8Za/u1mlrvReSmnMuT6tMzy54jsQEYbCuE9F5CtEjNtUrSelgtBpRW7+DncqgEob4Apn3qHIxgPnsOE8lZc8ySqmrI1gFqFC4xES87sL5Qd9tC6GeldU/f64MWP2BS6v4XPmCH8+KbhOSeCemvWIiHOvo82jFIQk4xO6uO+PNDGDTF1MT3C0o="
}