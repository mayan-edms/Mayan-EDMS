#!make
include config.env

HOST_IP = `/sbin/ip route|awk '/docker0/ { print $$9 }'`
APT_PROXY ?= $(HOST_IP):3142
CONSOLE_COLUMNS ?= `echo $$(tput cols)`
CONSOLE_LINES ?= `echo $$(tput lines)`
IMAGE_VERSION ?= `cat docker/rootfs/version`
PIP_INDEX_URL ?= http://$(HOST_IP):3141/root/pypi/+simple/
PIP_TRUSTED_HOST ?= $(HOST_IP)
DOCKER_HOST_REGISTRY_NAME ?= $(DOCKER_HOST_REGISTRY_NAME)
DOCKER_HOST_REGISTRY_PORT ?= $(DOCKER_HOST_REGISTRY_PORT)
DOCKER_IMAGE_MAYAN_NAME ?= $(DOCKER_IMAGE_MAYAN_NAME)

docker-build: ## Build a new image locally.
docker-build: docker-dockerfile-update
	docker build --file docker/Dockerfile --tag $(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION) .

docker-build-with-proxy: ## Build a new image locally using an APT proxy as APT_PROXY.
docker-build-with-proxy: docker-dockerfile-update devpi-start
	docker build --build-arg APT_PROXY=$(APT_PROXY) --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) --build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) --build-arg HTTP_PROXY=$(HTTP_PROXY) --build-arg HTTPS_PROXY=$(HTTPS_PROXY) --file docker/Dockerfile --tag $(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION) .
	$(MAKE) devpi-stop

docker-build-with-proxy-push: ## Build an image with an APT proxy and push to the test registry.
docker-build-with-proxy-push: docker-build-with-proxy docker-registry-push

docker-registry-push: ## Push a built image to the test Docker registry.
	docker tag $(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION) $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION)
	docker push $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION)
	# /etc/docker/daemon.json {"insecure-registries" : ["docker-registry.local:5000"]}
	# /etc/hosts <ip address>  docker-registry.local

docker-registry-pull: ## Pull an image from the test Docker registry.
	docker pull $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION)
	docker tag $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION) $(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION)

docker-registry-catalog: ## Show the test Docker registry catalog.
	curl http://$(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/v2/_catalog

docker-registry-tags: ## Show the tags for the image in the test Docker registry.
	curl http://$(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/v2/$(DOCKER_IMAGE_MAYAN_NAME)/tags/list

docker-registry-run: # Launch a test Docker registry.
	docker run --detach --name registry --publish 5000:5000 registry:2

docker-shell: ## Launch a bash instance inside a running container. Pass the container name via DOCKER_CONTAINER.
	docker exec --env TERM=$(TERM) --env "COLUMNS=$(CONSOLE_COLUMNS)" --env "LINES=$(CONSOLE_LINES)" --interactive --tty $(DOCKER_CONTAINER) /bin/bash

docker-runtest-container: ## Run a test container.
docker-runtest-container: docker-test-cleanup
	docker run \
	--detach \
	--name test-mayan-edms \
	--publish 80:8000 \
	--volume test-mayan_data:/var/lib/mayan \
	$(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION)

docker-runtest-cleanup: ## Delete the test container and the test volume.
	@docker rm --file test-mayan-edms || true
	@docker volume rm test-mayan_data || true

docker-runtest-all: ## Executed the test suite in a test container.
	docker run --rm $(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION) run_tests

docker-compose-build:
	docker-compose --file docker/docker-compose.yml --project-name mayan-edms build

docker-compose-build-with-proxy: devpi-start
	docker-compose --file docker/docker-compose.yml --project-name mayan-edms build --build-arg APT_PROXY=$(APT_PROXY) --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) --build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) --build-arg HTTP_PROXY=$(HTTP_PROXY) --build-arg HTTPS_PROXY=$(HTTPS_PROXY)
	$(MAKE) devpi-stop

docker-compose-up:
	docker-compose --file docker/docker-compose.yml --project-name mayan-edms up

docker-staging-network-create:
	@docker network rm mayan-staging || true
	docker network create mayan-staging

docker-staging-container-postgresql-start:
	docker run \
	--detach \
	--name mayan-staging-postgres \
	--network=mayan-staging \
	--env POSTGRES_USER=($DEFAULT_DATABASE_USER) \
	--env POSTGRES_DB=$(DEFAULT_DATABASE_NAME) \
	--env POSTGRES_PASSWORD=$(DEFAULT_DATABASE_PASSWORD) \
	--volume mayan-staging-postgres:/var/lib/postgresql/data \
	$(DOCKER_POSTGRES_IMAGE_VERSION)

docker-staging-container-redis-start:
	docker run \
	--detach \
	--name mayan-staging-redis \
	--network=mayan-staging \
	--volume mayan-staging-redis:/data \
	$(DOCKER_REDIS_IMAGE_VERSION) \
	redis-server \
	--databases \
	"2" \
	--maxmemory-policy \
	allkeys-lru \
	--save \
	"" \
	--requirepass mayanredispassword

docker-staging-container-rabbitmq-start:
	docker run \
	--detach \
	--name mayan-staging-rabbitmq \
	--network=mayan-staging \
	--volume mayan-staging-rabbitmq:/var/lib/rabbitmq \
	$(DOCKER_RABBITMQ_IMAGE_VERSION) \

docker-staging-container-mayan-start:
	sleep 5 && docker run \
	--detach \
	--name mayan-staging-app \
	--network=mayan-staging \
	--publish 80:8000 \
	--env MAYAN_DATABASE_ENGINE=django.db.backends.postgresql \
	--env MAYAN_DATABASE_HOST=mayan-staging-postgres \
	--env MAYAN_DATABASE_NAME=$(DEFAULT_DATABASE_NAME) \
	--env MAYAN_DATABASE_PASSWORD=($DEFAULT_DATABASE_PASSWORD) \
	--env MAYAN_DATABASE_USER=mayan \
	--env MAYAN_CELERY_BROKER_URL=$(MAYAN_CELERY_BROKER_URL) \
	--env MAYAN_CELERY_RESULT_BACKEND="redis://:mayanredispassword@mayan-staging-redis:6379/1" \
	--volume mayan-staging-app:/var/lib/mayan \
	$(DOCKER_IMAGE_MAYAN_NAME):$(IMAGE_VERSION)

docker-staging-start-with-rabbitmq: MAYAN_CELERY_BROKER_URL="amqp://guest:guest@mayan-staging-rabbitmq:5672/"
docker-staging-start-with-rabbitmq: docker-staging-start

docker-staging-start-with-redis: MAYAN_CELERY_BROKER_URL="redis://:mayanredispassword@mayan-staging-redis:6379/0"
docker-staging-start-with-redis: docker-staging-start

docker-staging-start: docker-staging-cleanup docker-staging-network-create docker-staging-container-postgresql-start docker-staging-container-rabbitmq-start docker-staging-container-redis-start docker-staging-container-mayan-start
	docker logs --file mayan-staging-app

docker-staging-cleanup: ## Delete the test container and the test volume.
	@docker rm --file mayan-staging-app || true
	@docker rm --file mayan-staging-redis || true
	@docker rm --file mayan-staging-rabbitmq || true
	@docker rm --file mayan-staging-postgres || true
	@docker volume rm mayan-staging-app || true
	@docker volume rm mayan-staging-postgres || true
	@docker volume rm mayan-staging-rabbitmq || true
	@docker volume rm mayan-staging-redis || true
	@docker network rm mayan-staging || true

docker-development-container-redis-start:
	docker run \
	--detach \
	--name mayan-development-redis \
	--publish 6379:6379 \
	--volume mayan-development-redis:/data \
	$(DOCKER_REDIS_IMAGE_VERSION) \
	redis-server \
	--databases \
	"2" \
	--maxmemory-policy \
	allkeys-lru \
	--save \
	"" \

docker-development-container-rabbitmq-start:
	docker run \
	--detach \
	--name mayan-development-rabbitmq \
	--publish 5672:5672 \
	--volume mayan-development-rabbitmq:/var/lib/rabbitmq \
	$(DOCKER_RABBITMQ_IMAGE_VERSION) \

docker-development-container-postgresql-start:
	docker run \
	--detach \
	--name mayan-development-postgres \
	--publish 5432:5432 \
	--env POSTGRES_PASSWORD=postgres \
	--volume mayan-development-postgres:/var/lib/postgresql/data \
	$(DOCKER_POSTGRES_IMAGE_VERSION)

docker-development-cleanup: ## Delete the test container and the test volume.
	@docker rm --file mayan-development-postgres || true
	@docker rm --file mayan-development-rabbitmq || true
	@docker rm --file mayan-development-redis || true
	@docker volume rm mayan-development-postgres || true
	@docker volume rm mayan-development-rabbitmq || true
	@docker volume rm mayan-development-redis || true
