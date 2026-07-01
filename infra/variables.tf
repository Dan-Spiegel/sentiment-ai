variable "image" {
  type    = string
  default = "ghcr.io/dan-spiegel/sentiment-ai:latest"
}

variable "container_name" {
  type    = string
  default = "sentiment-ai-staging"
}

variable "network" {
  type    = string
  default = "cicd-network"
}

variable "external_port" {
  type    = number
  default = 8001
}

variable "docker_host" {
  # Linux : unix:///var/run/docker.sock  -  Windows : npipe:////./pipe/docker_engine
  type    = string
  default = "unix:///var/run/docker.sock"
}
