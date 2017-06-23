.PHONY: clean-pyc clean-build


help:
	@echo
	@echo "clean-build - Remove build artifacts."
	@echo "clean-pyc - Remove Python artifacts."
	@echo "clean - Remove Python and build artifacts."

	@echo "test-all - Run all tests."
	@echo "test MODULE=<python module name> - Run tests for a single App, module or test class."
	@echo "docs_serve - Run the livehtml documentation generator."

	@echo "translations_make - Refresh all translation files."
	@echo "translations_compile - Compile all translation files."
	@echo "translations_push - Upload all translation files to Transifex."
	@echo "translations_pull - Download all translation files from Transifex."

	@echo "requirements_dev - Install development requirements."
	@echo "requirements_docs - Install documentation requirements."
	@echo "requirements_testing - Install testing requirements."

	@echo "sdist - Build the source distribution package."
	@echo "wheel - Build the wheel distribution package."
	@echo "release - Package (sdist and wheel) and upload a release."
	@echo "test_release - Package (sdist and wheel) and upload to the PyPI test server."
	@echo "release_test_via_docker_ubuntu - Package (sdist and wheel) and upload to the PyPI test server using an Ubuntu Docker builder."
	@echo "release_test_via_docker_alpine - Package (sdist and wheel) and upload to the PyPI test server using an Alpine Docker builder."
	@echo "release_via_docker_ubuntu - Package (sdist and wheel) and upload to PyPI using an Ubuntu Docker builder."
	@echo "release_via_docker_alpine - Package (sdist and wheel) and upload to PyPI using an Alpine Docker builder."
	@echo "test_sdist_via_docker_ubuntu - Make an sdist packange and test it using an Ubuntu Docker container."
	@echo "test_wheel_via_docker_ubuntu - Make a wheel package and test it using an Ubuntu Docker container."

	@echo "runserver - Run the development server."
	@echo "runserver_plus - Run the Django extension's development server."
	@echo "shell_plus - Run the shell_plus command."

	@echo "docker_services_on - Launch and initialize production-like services using Docker (Postgres and Redis)."
	@echo "docker_services_off - Stop and delete the Docker production-like services."
	@echo "docker_services_frontend - Launch a front end instance that uses the production-like services."
	@echo "docker_services_worker - Launch a worker instance that uses the production-like services."
	@echo "docker_service_mysql_on - Launch and initialize a MySQL Docker container."
	@echo "docker_service_mysql_off - Stop and delete the MySQL Docker container."

	@echo "safety_check - Run a package safety check."


# Cleaning

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


# Testing

test:
	./manage.py test $(MODULE) --settings=mayan.settings.testing --nomigrations

test-all:
	./manage.py test --mayan-apps --settings=mayan.settings.testing --nomigrations


# Documentation

docs_serve:
	cd docs;make livehtml


# Translations

translations_make:
	contrib/scripts/process_messages.py -m

translations_compile:
	contrib/scripts/process_messages.py -c

translations_push:
	tx push -s

translations_pull:
	tx pull


# Requirements

requirements_dev:
	pip install -r requirements/development.txt

requirements_docs:
	pip install -r requirements/documentation.txt

requirements_testing:
	pip install -r requirements/testing.txt


# Releases


test_release: clean wheel
	twine upload dist/* -r testpypi
	@echo "Test with: pip install -i https://testpypi.python.org/pypi mayan-edms"

release: clean wheel
	twine upload dist/* -r pypi

sdist: clean
	python setup.py sdist
	ls -l dist

wheel: clean sdist
	pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
	ls -l dist

release_test_via_docker_ubuntu:
	docker run --rm --name mayan_release -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "cp -r /host_source/* . && apt-get update && apt-get install make python-pip -y && pip install -r requirements/build.txt && cp -r /host_home/.pypirc ~/.pypirc && make test_release"

release_via_docker_ubuntu:
	docker run --rm --name mayan_release -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "cp -r /host_source/* . && apt-get update && apt-get install make python-pip -y && pip install -r requirements/build.txt && cp -r /host_home/.pypirc ~/.pypirc && make release"

release_test_via_docker_alpine:
	docker run --rm --name mayan_release -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source alpine /bin/busybox sh -c "cp -r /host_source/* . && apk update && apk add python2 py2-pip make && pip install -r requirements/build.txt && cp -r /host_home/.pypirc ~/.pypirc && make test_release"

release_via_docker_alpine:
	docker run --rm --name mayan_release -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source alpine /bin/busybox sh -c "cp -r /host_source/* . && apk update && apk add python2 py2-pip make && pip install -r requirements/build.txt && cp -r /host_home/.pypirc ~/.pypirc && make release"

test_sdist_via_docker_ubuntu:
	docker run --rm --name mayan_sdist_test -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "cp -r /host_source/* . && apt-get update && apt-get install make python-pip libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils -y && pip install -r requirements/development.txt && make sdist_test_suit"

test_wheel_via_docker_ubuntu:
	docker run --rm --name mayan_wheel_test -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "cp -r /host_source/* . && apt-get update && apt-get install make python-pip libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils -y && pip install -r requirements/development.txt && make wheel_test_suit"

sdist_test_suit: sdist
	rm -f -R _virtualenv
	virtualenv _virtualenv
	sh -c '\
	. _virtualenv/bin/activate; \
	pip install `ls dist/*.gz`; \
	_virtualenv/bin/mayan-edms.py initialsetup; \
	pip install mock==2.0.0; \
	_virtualenv/bin/mayan-edms.py test --mayan-apps \
	'

wheel_test_suit: wheel
	rm -f -R _virtualenv
	virtualenv _virtualenv
	sh -c '\
	. _virtualenv/bin/activate; \
	pip install `ls dist/*.whl`; \
	_virtualenv/bin/mayan-edms.py initialsetup; \
	pip install mock==2.0.0; \
	_virtualenv/bin/mayan-edms.py test --mayan-apps \
	'

# Dev server

runserver:
	./manage.py runserver --settings=mayan.settings.development

runserver_plus:
	./manage.py runserver_plus --settings=mayan.settings.development

shell_plus:
	./manage.py shell_plus --settings=mayan.settings.development

docker_services_on:
	docker run -d --name redis -p 6379:6379 redis
	docker run -d --name postgres -p 5432:5432 postgres
	while ! nc -z 127.0.0.1 6379; do sleep 1; done
	while ! nc -z 127.0.0.1 5432; do sleep 1; done
	sleep 1
	./manage.py initialsetup --settings=mayan.settings.testing.docker

docker_services_off:
	docker stop postgres redis
	docker rm postgres redis

docker_services_frontend:
	./manage.py runserver --settings=mayan.settings.testing.docker

docker_services_worker:
	./manage.py celery worker --settings=mayan.settings.testing.docker -B -l INFO -O fair

docker_service_mysql_on:
	docker run -d --name mysql -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=True -e MYSQL_DATABASE=mayan_edms mysql
	while ! nc -z 127.0.0.1 3306; do sleep 1; done

docker_service_mysql_off:
	docker stop mysql
	docker rm mysql

# Security

safety_check:
	safety check
