# SentimentAI

Petite API REST en FastAPI qui analyse le sentiment d'un texte.
Projet du TP DevOps : pipeline CI/CD complet avec Docker, Jenkins, SonarQube,
Trivy, Terraform et un monitoring Prometheus + Grafana.

## Endpoints

- `GET /health` : renvoie `{"status":"ok"}`
- `POST /predict` : analyse un texte et renvoie positive / negative / neutral
- `GET /metrics` : metriques pour Prometheus
- `GET /docs` : Swagger

Exemple :

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this"}'
```

## Lancer en local

```bash
make install
make test
make run
```

Avec Docker :

```bash
docker network create cicd-network
make build
make up
```

## Monitoring

```bash
cd monitoring
docker compose up -d
```

Prometheus : http://localhost:9090 - Grafana : http://localhost:3000 (admin / admin).

## Pipeline (9 stages)

Le Jenkinsfile est a la racine. Les stages :

1. Checkout
2. Lint (flake8)
3. Build & Test (pytest + coverage)
4. SonarQube
5. Quality Gate
6. Security Scan (Trivy)
7. Push de l'image sur ghcr.io
8. Terraform (deploiement staging)
9. Smoke Test (curl /health)

## Config Jenkins

- credential `ghcr-credentials` : user GitHub + token avec le scope write:packages
- credential `sonar-token` et serveur SonarQube nomme `SonarQube`
- outil `sonar-scanner` dans Manage Jenkins > Tools
- webhook SonarQube vers http://jenkins:8080/sonarqube-webhook/
- conteneur jenkins sur le reseau cicd-network avec le socket Docker monte
