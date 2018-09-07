#!/bin/sh

apt-get update
apt-get install -y --no-install-recommends tesseract-ocr-deu

$MAYAN_PIP_BIN install -r $DOCKER_ROOT/requirements-testing.txt

$MAYAN_BIN test --mayan-apps --settings=mayan.settings.testing
