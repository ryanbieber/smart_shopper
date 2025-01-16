# Makefile for Docker Compose with logging, restarting, and cleaning up old builds

# Variables
DOCKER_COMPOSE = docker-compose
LOG_FILE = docker-compose.log

.PHONY: up down restart logs clean

# Start the Docker Compose services
up:
	$(DOCKER_COMPOSE) up -d

# Stop the Docker Compose services
down:
	$(DOCKER_COMPOSE) down

# Restart the Docker Compose services
restart: down up

# Tail the logs of the Docker Compose services
logs:
	$(DOCKER_COMPOSE) logs -f > $(LOG_FILE)

# Clean up old Docker images and containers
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	docker system prune -f