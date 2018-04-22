
APT_PROXY ?= `/sbin/ip route|awk '/docker0/ { print $$9 }'`:3142
VERSION ?= `cat version`

help:
	@echo
	@echo "readme-render - Generate a new README.md from README.md.tmpl."
	@echo "release - Push code to trigger and publish a new version build."
	@echo "build - Build a new image locally."
	@echo "build-with-proxy - Build a new image locally using an APT proxy."
	@echo "test-container - Build and run a test container."
	@echo "test-cleanup - Delete the test container and the test volume."
	@echo "test-all - Build, run a test container, and executed the test suite."

readme-render:
	@export VERSION=$(VERSION); \
	envsubst < README.md.tmpl > README.md

release:
	git push origin
	git push --tags origin || true
	git push --tags bitbucket || true
	git push bitbucket

build:
	@export DIRECTORY=`pwd`; \
	export PARENT_DIRECTORY=`dirname "$$DIRECTORY"`; \
	docker build -t mayanedms/mayanedms:$(VERSION) -f $$PARENT_DIRECTORY

build-with-proxy:
	docker build -t mayanedms/mayanedms:$(VERSION) --build-arg APT_PROXY=$(APT_PROXY) .

test-launch-container: build-with-proxy test-cleanup
	docker run -d --name test-mayan-edms -p 80:80 -v test-mayan_data:/var/lib/mayan mayanedms/mayanedms:$(VERSION)

test-cleanup:
	@docker rm -f test-mayan-edms || true
	@docker volume rm test-mayan_data || true

test-all: test-launch-container
	docker exec -ti test-mayan-edms sh -c "apt-get update && apt-get install -y tesseract-ocr-deu"
	docker exec -ti test-mayan-edms sh -c "mayan-edms.py test --mayan-apps"
