terraform {
  required_version = ">= 1.5"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = var.docker_host
}

resource "docker_image" "app" {
  name         = var.image
  keep_locally = true
}

resource "docker_container" "staging" {
  name  = var.container_name
  image = docker_image.app.image_id

  networks_advanced {
    name = var.network
  }

  ports {
    internal = 8000
    external = var.external_port
  }

  healthcheck {
    test     = ["CMD", "python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"]
    interval = "10s"
    timeout  = "5s"
    retries  = 3
  }

  restart = "unless-stopped"
}
