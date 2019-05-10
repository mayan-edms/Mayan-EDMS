APT_PROXY ?= `/sbin/ip route|awk '/docker0/ { print $$9 }'`:3142
IMAGE_VERSION ?= `cat docker/rootfs/version`
CONSOLE_COLUMNS ?= `echo $$(tput cols)`
CONSOLE_LINES ?= `echo $$(tput lines)`

docker-build: ## Build a new image locally.
	docker build -t mayanedms/mayanedms:$(IMAGE_VERSION) -f docker/Dockerfile .

docker-build-with-proxy: ## Build a new image locally using an APT proxy as APT_PROXY.
	docker build -t mayanedms/mayanedms:$(IMAGE_VERSION) -f docker/Dockerfile --build-arg APT_PROXY=$(APT_PROXY) .

docker-shell: ## Launch a bash instance inside a running container. Pass the container name via DOCKER_CONTAINER.
	docker exec -e TERM=$(TERM) -e "COLUMNS=$(CONSOLE_COLUMNS)" -e "LINES=$(CONSOLE_LINES)" -it $(DOCKER_CONTAINER) /bin/bash

docker-test-container: ## Build and run a test container.
docker-test-container: docker-build-with-proxy docker-test-cleanup
	docker run -d --name test-mayan-edms -p 80:8000 -v test-mayan_data:/var/lib/mayan mayanedms/mayanedms:$(DOCKER_VERSION)

docker-test-cleanup: ## Delete the test container and the test volume.
	@docker rm -f test-mayan-edms || true
	@docker volume rm test-mayan_data || true

docker-test-all: ## Build and executed the test suite in a test container.
docker-test-all: docker-build-with-proxy
	docker run --rm run-tests
