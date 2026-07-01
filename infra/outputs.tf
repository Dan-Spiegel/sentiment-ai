output "staging_url" {
  value = "http://localhost:${var.external_port}/health"
}

output "staging_container" {
  value = docker_container.staging.name
}
