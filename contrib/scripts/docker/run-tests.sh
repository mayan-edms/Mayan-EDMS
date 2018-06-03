#!/bin/sh

apt-get update
apt-get install -y --no-install-recommends tesseract-ocr-deu

pip install -r $DOCKER_ROOT/requirements-testing.txt

mayan-edms.py test --mayan-apps --settings=mayan.settings.testing
