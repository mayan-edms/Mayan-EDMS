#!/bin/bash

QUEUE_LIST=`MAYAN_WORKER_NAME=$1 su mayan -c "${MAYAN_PYTHON_BIN_DIR}mayan-edms.py platformtemplate worker_queues"`

# Use -A and not --app. Both are the same but behave differently
# -A can be located before the command while --app cannot.
# Pass ${@:2} to allow overriding the defaults arguments
su mayan -c "${MAYAN_PYTHON_BIN_DIR}celery -A mayan worker -Ofair -l ERROR -Q $QUEUE_LIST ${@:2}"
