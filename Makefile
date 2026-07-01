.PHONY: install lint test run build up down

install:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	flake8 app tests

test:
	pytest --cov=app --cov-report=xml --cov-report=term

run:
	uvicorn app.main:app --reload

build:
	docker build --target runtime -t ghcr.io/dan-spiegel/sentiment-ai:latest .

up:
	docker compose up -d

down:
	docker compose down
