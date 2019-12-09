#!make
include config.env

HOST_IP = `/sbin/ip route|awk '/docker0/ { print $$9 }'`
APT_PROXY ?= $(HOST_IP):3142
CONSOLE_COLUMNS ?= `echo $$(tput cols)`
CONSOLE_LINES ?= `echo $$(tput lines)`
IMAGE_VERSION ?= `cat docker/rootfs/version`
PIP_INDEX_URL ?= http://$(HOST_IP):3141/root/pypi/+simple/
PIP_TRUSTED_HOST ?= $(HOST_IP)

docker-build: ## Build a new image locally.
	docker build -t mayanedms/mayanedms:$(IMAGE_VERSION) -f docker/Dockerfile .

docker-build-with-proxy: ## Build a new image locally using an APT proxy as APT_PROXY.
docker-build-with-proxy: devpi-start
	docker build -t mayanedms/mayanedms:$(IMAGE_VERSION) -f docker/Dockerfile --build-arg APT_PROXY=$(APT_PROXY) --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) --build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) --build-arg HTTP_PROXY=$(HTTP_PROXY) --build-arg HTTPS_PROXY=$(HTTPS_PROXY) .
	$(MAKE) devpi-stop

docker-shell: ## Launch a bash instance inside a running container. Pass the container name via DOCKER_CONTAINER.
	docker exec -e TERM=$(TERM) -e "COLUMNS=$(CONSOLE_COLUMNS)" -e "LINES=$(CONSOLE_LINES)" -it $(DOCKER_CONTAINER) /bin/bash

docker-runtest-container: ## Run a test container.
docker-runtest-container: docker-test-cleanup
	docker run \
	-d \
	--name test-mayan-edms \
	-p 80:8000 \
	-v test-mayan_data:/var/lib/mayan \
	mayanedms/mayanedms:$(IMAGE_VERSION)

docker-runtest-cleanup: ## Delete the test container and the test volume.
	@docker rm -f test-mayan-edms || true
	@docker volume rm test-mayan_data || true

docker-runtest-all: ## Executed the test suite in a test container.
	docker run --rm mayanedms/mayanedms:$(IMAGE_VERSION) run_tests

docker-compose-build:
	docker-compose -f docker/docker-compose.yml -p mayan-edms build

docker-compose-build-with-proxy: devpi-start
	docker-compose -f docker/docker-compose.yml -p mayan-edms build --build-arg APT_PROXY=$(APT_PROXY) --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) --build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) --build-arg HTTP_PROXY=$(HTTP_PROXY) --build-arg HTTPS_PROXY=$(HTTPS_PROXY)
	$(MAKE) devpi-stop

docker-compose-up:
	docker-compose -f docker/docker-compose.yml -p mayan-edms up

docker-staging-network-create:
	@docker network rm mayan-staging || true
	docker network create mayan-staging

docker-staging-container-postgresql-start:
	docker run \
	-d \
	--name mayan-staging-postgres \
	--network=mayan-staging \
	-e POSTGRES_USER=mayan \
	-e POSTGRES_DB=mayan \
	-e POSTGRES_PASSWORD=mayanuserpass \
	-v mayan-staging-postgres:/var/lib/postgresql/data \
	$(DOCKER_POSTGRES_IMAGE_VERSION)

docker-staging-container-redis-start:
	docker run \
	-d \
	--name mayan-staging-redis \
	--network=mayan-staging \
	-v mayan-staging-redis:/data \
	$(DOCKER_REDIS_IMAGE_VERSION) \
	redis-server \
	--databases \
	"2" \
	--maxmemory-policy \
	allkeys-lru \
	--save \
	""

docker-staging-container-rabbitmq-start:
	docker run \
	-d \
	--name mayan-staging-rabbitmq \
	--network=mayan-staging \
	-v mayan-staging-rabbitmq:/var/lib/rabbitmq \
	$(DOCKER_RABBITMQ_IMAGE_VERSION) \

docker-staging-container-mayan-start:
	sleep 5 && docker run \
	-d \
	--name mayan-staging-app \
	--network=mayan-staging \
	-p 80:8000 \
	-e MAYAN_DATABASE_ENGINE=django.db.backends.postgresql \
	-e MAYAN_DATABASE_HOST=mayan-staging-postgres \
	-e MAYAN_DATABASE_NAME=mayan \
	-e MAYAN_DATABASE_PASSWORD=mayanuserpass \
	-e MAYAN_DATABASE_USER=mayan \
	-e MAYAN_CELERY_BROKER_URL=$(MAYAN_CELERY_BROKER_URL) \
	-e MAYAN_CELERY_RESULT_BACKEND="redis://mayan-staging-redis:6379/1" \
	-v mayan-staging-app:/var/lib/mayan \
	mayanedms/mayanedms:$(IMAGE_VERSION)

docker-staging-start-with-rabbitmq: MAYAN_CELERY_BROKER_URL="amqp://guest:guest@mayan-staging-rabbitmq:5672/"
docker-staging-start-with-rabbitmq: docker-staging-start

docker-staging-start-with-redis: MAYAN_CELERY_BROKER_URL="redis://mayan-staging-redis:6379/0"
docker-staging-start-with-redis: docker-staging-start

docker-staging-start: docker-staging-cleanup docker-staging-network-create docker-staging-container-postgresql-start docker-staging-container-rabbitmq-start docker-staging-container-redis-start docker-staging-container-mayan-start
	docker logs -f mayan-staging-app

docker-staging-cleanup: ## Delete the test container and the test volume.
	@docker rm -f mayan-staging-app || true
	@docker rm -f mayan-staging-redis || true
	@docker rm -f mayan-staging-rabbitmq || true
	@docker rm -f mayan-staging-postgres || true
	@docker volume rm mayan-staging-app || true
	@docker volume rm mayan-staging-postgres || true
	@docker volume rm mayan-staging-rabbitmq || true
	@docker volume rm mayan-staging-redis || true
	@docker network rm mayan-staging || true

devpi-init:
	devpi-server --init || true

devpi-start: devpi-init
	devpi-server --start --host=0.0.0.0 || true

devpi-stop:
	devpi-server --stop || true
