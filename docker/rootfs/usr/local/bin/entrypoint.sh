#!/bin/sh

set -e
echo "mayan: starting entrypoint.sh"
INSTALL_FLAG=/var/lib/mayan/system/SECRET_KEY
CONCURRENCY_ARGUMENT=--concurrency=

DEFAULT_USER_UID=1000
DEFAULT_USER_GUID=1000

export MAYAN_DEFAULT_BROKER_URL=redis://127.0.0.1:6379/0
export MAYAN_DEFAULT_CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

export MAYAN_ALLOWED_HOSTS='["*"]'
export MAYAN_BIN=/opt/mayan-edms/bin/mayan-edms.py
export MAYAN_BROKER_URL=${MAYAN_BROKER_URL:-${MAYAN_DEFAULT_BROKER_URL}}
export MAYAN_CELERY_RESULT_BACKEND=${MAYAN_CELERY_RESULT_BACKEND:-${MAYAN_DEFAULT_CELERY_RESULT_BACKEND}}
export MAYAN_INSTALL_DIR=/opt/mayan-edms
export MAYAN_PYTHON_BIN_DIR=/opt/mayan-edms/bin/
export MAYAN_MEDIA_ROOT=/var/lib/mayan
export MAYAN_SETTINGS_MODULE=${MAYAN_SETTINGS_MODULE:-mayan.settings.production}

export MAYAN_GUNICORN_BIN=${MAYAN_PYTHON_BIN_DIR}gunicorn
export MAYAN_GUNICORN_WORKERS=${MAYAN_GUNICORN_WORKERS:-2}
export MAYAN_GUNICORN_TIMEOUT=${MAYAN_GUNICORN_TIMEOUT:-120}
export MAYAN_PIP_BIN=${MAYAN_PYTHON_BIN_DIR}pip
export MAYAN_STATIC_ROOT=${MAYAN_INSTALL_DIR}/static

MAYAN_WORKER_FAST_CONCURRENCY=${MAYAN_WORKER_FAST_CONCURRENCY:-1}
MAYAN_WORKER_MEDIUM_CONCURRENCY=${MAYAN_WORKER_MEDIUM_CONCURRENCY:-1}
MAYAN_WORKER_SLOW_CONCURRENCY=${MAYAN_WORKER_SLOW_CONCURRENCY:-1}

echo "mayan: changing uid/guid"
usermod mayan -u ${MAYAN_USER_UID:-${DEFAULT_USER_UID}}
groupmod mayan -g ${MAYAN_USER_GUID:-${DEFAULT_USER_GUID}}

if [ "$MAYAN_WORKER_FAST_CONCURRENCY" -eq 0 ]; then
    MAYAN_WORKER_FAST_CONCURRENCY=
else
    MAYAN_WORKER_FAST_CONCURRENCY="${CONCURRENCY_ARGUMENT}${MAYAN_WORKER_FAST_CONCURRENCY}"
fi
export MAYAN_WORKER_FAST_CONCURRENCY

if [ "$MAYAN_WORKER_MEDIUM_CONCURRENCY" -eq 0 ]; then
    MAYAN_WORKER_MEDIUM_CONCURRENCY=
else
    MAYAN_WORKER_MEDIUM_CONCURRENCY="${CONCURRENCY_ARGUMENT}${MAYAN_WORKER_MEDIUM_CONCURRENCY}"
fi
export MAYAN_WORKER_MEDIUM_CONCURRENCY

if [ "$MAYAN_WORKER_SLOW_CONCURRENCY" -eq 0 ]; then
    MAYAN_WORKER_SLOW_CONCURRENCY=
else
    MAYAN_WORKER_SLOW_CONCURRENCY="${CONCURRENCY_ARGUMENT}${MAYAN_WORKER_SLOW_CONCURRENCY}"
fi
export MAYAN_WORKER_SLOW_CONCURRENCY

export CELERY_ALWAYS_EAGER=False
export PYTHONPATH=$PYTHONPATH:$MAYAN_MEDIA_ROOT

chown mayan:mayan /var/lib/mayan -R

apt_get_install() {
    apt-get -q update
    apt-get install -y --force-yes --no-install-recommends --auto-remove "$@"
    apt-get -q clean
    rm -rf /var/lib/apt/lists/*
}

initialize() {
    echo "mayan: initialize()"
    su mayan -c "${MAYAN_BIN} initialsetup --force --no-javascript"
}

os_package_installs() {
    echo "mayan: os_package_installs()"
    if [ "${MAYAN_APT_INSTALLS}" ]; then
        DEBIAN_FRONTEND=noninteractive apt_get_install $MAYAN_APT_INSTALLS
    fi
}

pip_installs() {
    echo "mayan: pip_installs()"
    if [ "${MAYAN_PIP_INSTALLS}" ]; then
        su mayan -c "${MAYAN_PIP_BIN} install $MAYAN_PIP_INSTALLS"
    fi
}

start() {
    echo "mayan: start()"
    rm -rf /var/run/supervisor.sock
    exec /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
}

upgrade() {
    echo "mayan: upgrade()"
    su mayan -c "${MAYAN_BIN} performupgrade --no-javascript"
}

os_package_installs || true
pip_installs || true

case "$1" in

mayan) # Check if this is a new install, otherwise try to upgrade the existing
       # installation on subsequent starts
       if [ ! -f $INSTALL_FLAG ]; then
           initialize
       else
           upgrade
       fi
       start
       ;;

run-tests) # Check if this is a new install, otherwise try to upgrade the existing
           # installation on subsequent starts
           if [ ! -f $INSTALL_FLAG ]; then
               initialize
           else
               upgrade
           fi
           run-tests.sh
           ;;

*) su mayan -c "$@";
   ;;

esac
