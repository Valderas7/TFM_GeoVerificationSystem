# 'Output' para recopilar la URL del repositorio en la forma
# 'aws_account_id.dkr.ecr.region.amazonaws.com/repositoryName'
output "repo_url" {
  value = aws_ecr_repository.weather_repo.repository_url
}