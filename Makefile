.PHONY: clean-pyc clean-build

define BROWSER_PYSCRIPT
import sys, webbrowser
webbrowser.open(sys.argv[1])
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


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
	python -Wall ./manage.py test $(MODULE) --settings=mayan.settings.testing --nomigrations

test-all:
	python -Wall ./manage.py runtests --settings=mayan.settings.testing --nomigrations


# Documentation

docs_serve:
	$(BROWSER) http://127.0.0.1:8000
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
	$(BROWSER) http://127.0.0.1:8000
	./manage.py runserver
