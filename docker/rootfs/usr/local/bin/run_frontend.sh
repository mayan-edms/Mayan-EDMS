#!/bin/sh

su mayan --command "${MAYAN_PYTHON_BIN_DIR}gunicorn --bind 0.0.0.0:8000 --limit-request-line ${MAYAN_GUNICORN_LIMIT_REQUEST_LINE} --max-requests ${MAYAN_GUNICORN_MAX_REQUESTS} --max-requests-jitter ${MAYAN_GUNICORN_REQUESTS_JITTER} ${MAYAN_GUNICORN_TEMPORARY_DIRECTORY} --timeout ${MAYAN_GUNICORN_TIMEOUT} --worker-class ${MAYAN_GUNICORN_WORKER_CLASS} --workers ${MAYAN_GUNICORN_WORKERS} mayan.wsgi"
