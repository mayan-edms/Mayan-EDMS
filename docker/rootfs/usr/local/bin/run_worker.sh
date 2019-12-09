#!/bin/bash

export MAYAN_WORKER_NAME=${MAYAN_WORKER_NAME:-$1}

QUEUE_LIST_DEFAULT=`su mayan -c "${MAYAN_PYTHON_BIN_DIR}mayan-edms.py platformtemplate worker_queues"`

MAYAN_QUEUE_LIST=${MAYAN_QUEUE_LIST:-${QUEUE_LIST_DEFAULT}}

# Use -A and not --app. Both are the same but behave differently
# -A can be located before the command while --app cannot.
# Pass ${@:2} to allow overriding the defaults arguments
su mayan -c "${MAYAN_PYTHON_BIN_DIR}celery -A mayan worker -Ofair -l ERROR -Q ${MAYAN_QUEUE_LIST} ${@:2}"
