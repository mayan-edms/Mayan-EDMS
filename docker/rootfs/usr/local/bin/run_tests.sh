#!/bin/sh

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y --no-install-recommends gcc python-dev tesseract-ocr-deu

su mayan -c "$MAYAN_PIP_BIN install -r ${MAYAN_INSTALL_DIR}/testing-base.txt"

su mayan -c "$MAYAN_BIN test --mayan-apps --settings=mayan.settings.testing"
