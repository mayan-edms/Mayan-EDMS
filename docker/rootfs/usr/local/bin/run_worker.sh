#!/bin/sh

export MAYAN_WORKER_NAME=${MAYAN_WORKER_NAME:-$1}
export MAYAN_WORKER_NICE_LEVEL=${MAYAN_WORKER_NICE_LEVEL:-0}

if [ ! "${MAYAN_QUEUE_LIST}" ]; then
    if [ ! "$MAYAN_WORKER_NAME" ]; then
        echo "Must specify either MAYAN_QUEUE_LIST or MAYAN_WORKER_NAME."
        exit 1
    else
        MAYAN_QUEUE_LIST=`su mayan --command "${MAYAN_PYTHON_BIN_DIR}mayan-edms.py platformtemplate worker_queues"`
    fi
fi

# Use -A and not --app. Both are the same but behave differently.
# -A can be located before the command while --app cannot.
shift
su mayan --command "nice -n ${MAYAN_WORKER_NICE_LEVEL} ${MAYAN_PYTHON_BIN_DIR}celery -A mayan worker --loglevel=ERROR -Ofair --queues=${MAYAN_QUEUE_LIST} --without-gossip --without-heartbeat ${@}"
