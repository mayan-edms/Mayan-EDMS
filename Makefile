.PHONY: clean-pyc clean-build


help:
	@echo
	@echo "clean-build - Remove build artifacts."
	@echo "clean-pyc - Remove Python artifacts."
	@echo "clean - Remove Python and build artifacts."

	@echo "test MODULE=<python module name> - Run tests for a single App, module or test class."
	@echo "test-all - Run all tests."
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

	@echo "runserver - Run the development server."
	@echo "runserver_plus - Run the Django extension's development server."
	@echo "shell_plus - Run the shell_plus command."

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
	./manage.py runtests --settings=mayan.settings.testing --nomigrations


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

release: clean
	python setup.py sdist bdist_wheel upload

sdist: clean
	python setup.py sdist
	ls -l dist

wheel: clean
	python setup.py bdist_wheel
	ls -l dist


# Dev server

runserver:
	./manage.py runserver

runserver_plus:
	$(BROWSER) http://127.0.0.1:8000
	./manage.py runserver_plus --settings=mayan.settings.development

shell_plus:
	./manage.py shell_plus --settings=mayan.settings.development


# Security

safety_check:
	safety check

