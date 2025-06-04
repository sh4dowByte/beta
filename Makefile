# Jalankan Dev
dev-up:
	docker compose -f docker-compose.dev.yaml up --build --remove-orphans

dev-down:
	docker compose -f docker-compose.yaml down

dev-bash:
	docker exec -it beta_dev bash

# Jalankan Prod
up:
	docker compose up -d

down:
	docker compose down

bash:
	docker exec -it beta bash

# Build image manual
build:
	docker build -t sh4dowbyte/beta:latest .

# Push ke Docker Hub
push:
	docker push sh4dowbyte/beta:latest
