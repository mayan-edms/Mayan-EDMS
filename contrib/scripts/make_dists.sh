#!/bin/sh

python setup.py sdist
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
