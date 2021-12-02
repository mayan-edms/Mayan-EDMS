#!/bin/sh

export DEBIAN_FRONTEND=noninteractive
TEST_ARGUMENT=${@:-"--mayan-apps --no-exclude"}

apt-get update
apt-get install -y --no-install-recommends gcc python3-dev tesseract-ocr-deu

su mayan --command "${MAYAN_PIP_BIN} install --requirement ${MAYAN_INSTALL_DIR}/testing-base.txt"

su mayan --command "MAYAN_TESTS_SELENIUM_SKIP=true ${MAYAN_BIN} test ${TEST_ARGUMENT} --settings=mayan.settings.testing"
