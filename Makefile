.PHONY: clean-pyc clean-build

DOCKER_MYSQL_IMAGE = mysql:8.0
DOCKER_ORACLE_IMAGE = wnameless/oracle-xe-11g
DOCKER_POSTGRES_IMAGE = postgres:9.6-alpine
DOCKER_REDIS_IMAGE = redis:5.0-alpine

PYTHON_MYSQL_VERSION = 1.4.4
PYTHON_PSYCOPG2_VERSION = 2.8.3
PYTHON_RABBITMQ_VERSION = 2.0.0
PYTHON_REDIS_VERSION = 3.2.1

help:
	@echo "Usage: make <target>\n"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?## / { printf "  * %-40s -%s\n", $$1, $$2 }' $(MAKEFILE_LIST)|sort

# Cleaning

clean: ## Remove Python and build artifacts.
clean: clean-build clean-pyc

clean-build: ## Remove build artifacts.
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## Remove Python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -R -f {} +

# Testing

test: clean-pyc
test: ## MODULE=<python module name> - Run tests for a single app, module or test class.
	./manage.py test $(MODULE) --settings=mayan.settings.testing.development --nomigrations $(ARGUMENTS)

test-all: ## Run all tests.
test-all: clean-pyc
	./manage.py test --mayan-apps --settings=mayan.settings.testing.development --nomigrations $(ARGUMENTS)

test-launch-postgres:
	@docker rm -f test-postgres || true
	@docker volume rm test-postgres || true
	docker run -d --name test-postgres -p 5432:5432 -v test-postgres:/var/lib/postgresql/data $(DOCKER_POSTGRES_IMAGE)
	sudo apt-get install -q libpq-dev
	pip install psycopg2==$(PYTHON_PSYCOPG2_VERSION)
	while ! nc -z 127.0.0.1 5432; do sleep 1; done

test-with-postgres: ## MODULE=<python module name> - Run tests for a single app, module or test class against a Postgres database container.
test-with-postgres: test-launch-postgres
	./manage.py test $(MODULE) --settings=mayan.settings.testing.docker.db_postgres --nomigrations
	@docker rm -f test-postgres || true
	@docker volume rm test-postgres || true

test-with-postgres-all: ## Run all tests against a Postgres database container.
test-with-postgres-all: test-launch-postgres
	./manage.py test --mayan-apps --settings=mayan.settings.testing.docker.db_postgres --nomigrations
	@docker rm -f test-postgres || true
	@docker volume rm test-postgres || true

test-launch-mysql:
	@docker rm -f test-mysql || true
	@docker volume rm test-mysql || true
	docker run -d --name test-mysql -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=True -e MYSQL_DATABASE=mayan -v test-mysql:/var/lib/mysql $(DOCKER_MYSQL_IMAGE)
	sudo apt-get install -q libmysqlclient-dev mysql-client
	pip install mysqlclient==$(PYTHON_MYSQL_VERSION)
	while ! nc -z 127.0.0.1 3306; do sleep 1; done
	mysql -h 127.0.0.1 -P 3306 -uroot  -e "set global character_set_server=utf8mb4;"

test-with-mysql: ## MODULE=<python module name> - Run tests for a single app, module or test class against a MySQL database container.
test-with-mysql: test-launch-mysql
	./manage.py test $(MODULE) --settings=mayan.settings.testing.docker.db_mysql --nomigrations
	@docker rm -f test-mysql || true
	@docker volume rm test-mysql || true


test-with-mysql-all: ## Run all tests against a MySQL database container.
test-with-mysql-all: test-launch-mysql
	./manage.py test --mayan-apps --settings=mayan.settings.testing.docker.db_mysql --nomigrations
	@docker rm -f test-mysql || true
	@docker volume rm test-mysql || true

test-launch-oracle:
	@docker rm -f test-oracle || true
	@docker volume rm test-oracle || true
	docker run -d --name test-oracle -p 49160:22 -p 49161:1521 -e ORACLE_ALLOW_REMOTE=true -v test-oracle:/u01/app/oracle $(DOCKER_ORACLE_IMAGE)
	# https://gist.github.com/kimus/10012910
	pip install cx_Oracle
	while ! nc -z 127.0.0.1 49161; do sleep 1; done
	sleep 10

test-with-oracle: ## MODULE=<python module name> - Run tests for a single app, module or test class against a Oracle database container.
test-with-oracle: test-launch-oracle
	./manage.py test $(MODULE) --settings=mayan.settings.testing.docker.db_oracle --nomigrations
	@docker rm -f test-oracle || true
	@docker volume rm test-oracle || true

test-with-oracle-all: ## Run all tests against a Oracle database container.
test-with-oracle-all: test-launch-oracle
	./manage.py test --mayan-apps --settings=mayan.settings.testing.docker.db_oracle --nomigrations
	@docker rm -f test-oracle || true
	@docker volume rm test-oracle || true

# Documentation

docs-serve: ## Run the livehtml documentation generator.
	cd docs;make livehtml

docs-spellcheck: ## Spellcheck the documentation.
	sphinx-build -b spelling -d docs/_build/ docs docs/_build/spelling

# Translations

translations-make: ## Refresh all translation files.
	contrib/scripts/process_messages.py -m

translations-compile: ## Compile all translation files.
	contrib/scripts/process_messages.py -c

translations-push: ## Upload all translation files to Transifex.
	tx push -s

translations-pull: ## Download all translation files from Transifex.
	tx pull -f

# Releases

increase-version: ## Increase the version number of the entire project's files.
	@VERSION=`grep "__version__ =" mayan/__init__.py| cut -d\' -f 2|./increase_version.py - $(PART)`; \
	BUILD=`echo $$VERSION|awk '{split($$VERSION,a,"."); printf("0x%02d%02d%02d\n", a[1],a[2], a[3])}'`; \
	sed -i -e "s/__build__ = 0x[0-9]*/__build__ = $${BUILD}/g" mayan/__init__.py; \
	sed -i -e "s/__version__ = '[0-9\.]*'/__version__ = '$${VERSION}'/g" mayan/__init__.py; \
	echo $$VERSION > docker/rootfs/version
	make generate-setup

python-test-release: ## Package (sdist and wheel) and upload to the PyPI test server.
python-test-release: clean wheel
	twine upload dist/* -r testpypi
	@echo "Test with: pip install -i https://testpypi.python.org/pypi mayan-edms"

python-release: ## Package (sdist and wheel) and upload a release.
python-release: clean python-wheel
	twine upload dist/* -r pypi

python-sdist: ## Build the source distribution package.
python-sdist: clean
	python setup.py sdist
	ls -l dist

python-wheel: ## Build the wheel distribution package.
python-wheel: clean python-sdist
	pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
	ls -l dist

python-release-test-via-docker-ubuntu: ## Package (sdist and wheel) and upload to the PyPI test server using an Ubuntu Docker builder.
	docker run --rm --name mayan_release -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "\
	echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/default/locale && \
	locale-gen en_US.UTF-8 && \
	update-locale LANG=en_US.UTF-8 && \
	export LC_ALL=en_US.UTF-8 && \
	cp -r /host_source/* . && \
	apt-get update && \
	apt-get install make python-pip -y && \
	pip install -r requirements/build.txt && \
	cp -r /host_home/.pypirc ~/.pypirc && \
	make test-release"

python-release-via-docker-ubuntu: ## Package (sdist and wheel) and upload to PyPI using an Ubuntu Docker builder.
	docker run --rm --name mayan_release -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "\
	apt-get update && \
	apt-get -y install locales && \
	echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/default/locale && \
	locale-gen en_US.UTF-8 && \
	update-locale LANG=en_US.UTF-8 && \
	export LC_ALL=en_US.UTF-8 && \
	cp -r /host_source/* . && \
	apt-get install make python-pip -y && \
	pip install -r requirements/build.txt && \
	cp -r /host_home/.pypirc ~/.pypirc && \
	make release"

test-sdist-via-docker-ubuntu: ## Make an sdist package and test it using an Ubuntu Docker container.
	docker run --rm --name mayan_sdist_test -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "\
	cp -r /host_source/* . && \
	echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/default/locale && \
	locale-gen en_US.UTF-8 && \
	update-locale LANG=en_US.UTF-8 && \
	export LC_ALL=en_US.UTF-8 && \
	apt-get update && \
	apt-get install make python-pip libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils -y && \
	pip install -r requirements/development.txt && \
	make sdist-test-suit \
	"

test-wheel-via-docker-ubuntu: ## Make a wheel package and test it using an Ubuntu Docker container.
	docker run --rm --name mayan_wheel_test -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source ubuntu:16.04 /bin/bash -c "\
	cp -r /host_source/* . && \
	echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/default/locale && \
	locale-gen en_US.UTF-8 && \
	update-locale LANG=en_US.UTF-8 && \
	export LC_ALL=en_US.UTF-8 && \
	apt-get update && \
	apt-get install make python-pip libreoffice tesseract-ocr tesseract-ocr-deu poppler-utils -y && \
	pip install -r requirements/development.txt && \
	make wheel-test-suit \
	"

python-sdist-test-suit: sdist
	rm -f -R _virtualenv
	virtualenv _virtualenv
	sh -c '\
	. _virtualenv/bin/activate; \
	pip install `ls dist/*.gz`; \
	_virtualenv/bin/mayan-edms.py initialsetup; \
	pip install mock==2.0.0; \
	_virtualenv/bin/mayan-edms.py test --mayan-apps \
	'

python-wheel-test-suit: wheel
	rm -f -R _virtualenv
	virtualenv _virtualenv
	sh -c '\
	. _virtualenv/bin/activate; \
	pip install `ls dist/*.whl`; \
	_virtualenv/bin/mayan-edms.py initialsetup; \
	pip install mock==2.0.0; \
	_virtualenv/bin/mayan-edms.py test --mayan-apps \
	'

generate-setup: ## Create and update the setup.py file.
generate-setup: generate-requirements
	@./generate_setup.py
	@echo "Complete."

generate-requirements: ## Generate all requirements files from the project depedency declarations.
	@./manage.py generaterequirements build > requirements/build.txt
	@./manage.py generaterequirements development > requirements/development.txt
	@./manage.py generaterequirements testing > requirements/testing-base.txt
	@./manage.py generaterequirements production --exclude=django > requirements/base.txt
	@./manage.py generaterequirements production --only=django > requirements/common.txt

# Dev server

runserver: ## Run the development server.
	./manage.py runserver --nothreading --settings=mayan.settings.development $(ADDRPORT)

runserver_plus: ## Run the Django extension's development server.
	./manage.py runserver_plus --nothreading --settings=mayan.settings.development $(ADDRPORT)

shell_plus: ## Run the shell_plus command.
	./manage.py shell_plus --settings=mayan.settings.development

test-with-docker-services-on: ## Launch and initialize production-like services using Docker (Postgres and Redis).
	docker run -d --name redis -p 6379:6379 $(DOCKER_REDIS_IMAGE)
	docker run -d --name postgres -p 5432:5432 $(DOCKER_POSTGRES_IMAGE)
	while ! nc -z 127.0.0.1 6379; do sleep 1; done
	while ! nc -z 127.0.0.1 5432; do sleep 1; done
	sleep 4
	pip install psycopg2==$(PYTHON_PSYCOPG2_VERSION) redis==$(PYTHON_REDIS_VERSION)
	./manage.py initialsetup --settings=mayan.settings.staging.docker

test-with-docker-services-off: ## Stop and delete the Docker production-like services.
	docker stop postgres redis
	docker rm postgres redis

test-with-docker-frontend: ## Launch a front end instance that uses the production-like services.
	./manage.py runserver --settings=mayan.settings.staging.docker

test-with-docker-worker: ## Launch a worker instance that uses the production-like services.
	DJANGO_SETTINGS_MODULE=mayan.settings.staging.docker ./manage.py celery worker -A mayan -B -l INFO -O fair

docker-mysql-on: ## Launch and initialize a MySQL Docker container.
	docker run -d --name mysql -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=True -e MYSQL_DATABASE=mayan_edms $(DOCKER_MYSQL_IMAGE)
	while ! nc -z 127.0.0.1 3306; do sleep 1; done

docker-mysql-off: ## Stop and delete the MySQL Docker container.
	docker stop mysql
	docker rm mysql

docker-postgres-on: ## Launch and initialize a PostgreSQL Docker container.
	docker run -d --name postgres -p 5432:5432 $(DOCKER_POSTGRES_IMAGE)
	while ! nc -z 127.0.0.1 5432; do sleep 1; done

docker-postgres-off: ## Stop and delete the PostgreSQL Docker container.
	docker stop postgres
	docker rm postgres


# Security

safety-check: ## Run a package safety check.
	safety check


# Other
find-gitignores: ## Find stray .gitignore files.
	@export FIND_GITIGNORES=`find -name '.gitignore'| wc -l`; \
	if [ $${FIND_GITIGNORES} -gt 1 ] ;then echo "More than one .gitignore found."; fi

python-build:
	docker rm -f mayan-edms-build || true && \
	docker run --rm --name mayan-edms-build -v $(HOME):/host_home:ro -v `pwd`:/host_source -w /source python:2-slim sh -c "\
	rm /host_source/dist -R || true && \
	mkdir /host_source/dist || true && \
	export LC_ALL=C.UTF-8 && \
	cp -r /host_source/* . && \
	apt-get update && \
	apt-get install -y make && \
	pip install -r requirements/build.txt && \
	make wheel && \
	cp dist/* /host_source/dist/"

check-readme: ## Checks validity of the README.rst file for PyPI publication.
	python setup.py check -r -s

check-missing-migrations: ## Make sure all models have proper migrations.
	./manage.py makemigrations --dry-run --noinput --check

setup-dev-environment: ## Bootstrap a virtualenv by install all dependencies to start developing.
	pip install -r requirements.txt -r requirements/development.txt -r requirements/testing-base.txt -r requirements/documentation.txt -r requirements/build.txt

-include docker/Makefile
