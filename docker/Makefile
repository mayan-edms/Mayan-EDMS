APT_PROXY ?= `/sbin/ip route|awk '/docker0/ { print $$9 }'`:3142
CONSOLE_COLUMNS ?= `echo $$(tput cols)`
CONSOLE_LINES ?= `echo $$(tput lines)`
IMAGE_VERSION ?= `cat docker/rootfs/version`

docker-build: ## Build a new image locally.
	docker build -t mayanedms/mayanedms:$(IMAGE_VERSION) -f docker/Dockerfile .

docker-build-with-proxy: ## Build a new image locally using an APT proxy as APT_PROXY.
	docker build -t mayanedms/mayanedms:$(IMAGE_VERSION) -f docker/Dockerfile --build-arg APT_PROXY=$(APT_PROXY) .

docker-shell: ## Launch a bash instance inside a running container. Pass the container name via DOCKER_CONTAINER.
	docker exec -e TERM=$(TERM) -e "COLUMNS=$(CONSOLE_COLUMNS)" -e "LINES=$(CONSOLE_LINES)" -it $(DOCKER_CONTAINER) /bin/bash

docker-runtest-container: ## Run a test container.
docker-runtest-container: docker-test-cleanup
	docker run -d \
	--name test-mayan-edms \
	-p 80:8000 \
	-v test-mayan_data:/var/lib/mayan \
	mayanedms/mayanedms:$(IMAGE_VERSION)

docker-runtest-cleanup: ## Delete the test container and the test volume.
	@docker rm -f test-mayan-edms || true
	@docker volume rm test-mayan_data || true

docker-runtest-all: ## Executed the test suite in a test container.
	docker run --rm run-tests

docker-compose-build:
	docker-compose -f docker/docker-compose.yml -p mayan-edms build

docker-compose-build-with-proxy:
	docker-compose -f docker/docker-compose.yml -p mayan-edms build --build-arg APT_PROXY=$(APT_PROXY)

docker-compose-up:
	docker-compose -f docker/docker-compose.yml -p mayan-edms up

docker-staging-network-create:
	@docker network rm mayan-staging || true
	docker network create mayan-staging

docker-staging-container-postgresql-start:
	docker run -d \
    --name mayan-staging-postgres \
    --network=mayan-staging \
    -e POSTGRES_USER=mayan \
    -e POSTGRES_DB=mayan \
    -e POSTGRES_PASSWORD=mayanuserpass \
    -v mayan-staging-postgres:/var/lib/postgresql/data \
    postgres:9.6-alpine

docker-staging-container-redis-start:
	docker run -d \
    --name mayan-staging-redis \
    --network=mayan-staging \
    redis:5.0-alpine \
    redis-server \
    --databases \
    "2" \
    --maxmemory-policy \
    allkeys-lru \
    --save \
    ""

docker-staging-container-mayan-start:
	docker run -d \
    --name mayan-staging-app \
    --network=mayan-staging \
    -p 80:8000 \
    -e MAYAN_DATABASE_ENGINE=django.db.backends.postgresql \
    -e MAYAN_DATABASE_HOST=mayan-staging-postgres \
    -e MAYAN_DATABASE_NAME=mayan \
    -e MAYAN_DATABASE_PASSWORD=mayanuserpass \
    -e MAYAN_DATABASE_USER=mayan \
    -e MAYAN_BROKER_URL="redis://mayan-staging-redis:6379/0" \
    -e MAYAN_CELERY_RESULT_BACKEND="redis://mayan-staging-redis:6379/1" \
    -v mayan-staging-app:/var/lib/mayan \
    mayanedms/mayanedms:$(IMAGE_VERSION)

docker-staging-start: docker-staging-network-create docker-staging-container-postgresql-start docker-staging-container-redis-start docker-staging-container-mayan-start
	docker logs -f mayan-staging-app

docker-staging-cleanup: ## Delete the test container and the test volume.
	@docker rm -f mayan-staging-app || true
	@docker rm -f mayan-staging-redis || true
	@docker rm -f mayan-staging-postgres || true
	@docker volume rm mayan-staging-app || true
	@docker volume rm mayan-staging-postgres || true
	@docker network rm mayan-staging || true
