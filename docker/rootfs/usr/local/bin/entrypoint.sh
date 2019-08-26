#!/bin/bash

# Use bash and not sh to support argument slicing "${@:2}"
# sh defaults to dash instead of bash.

set -e
echo "mayan: starting entrypoint.sh"
INSTALL_FLAG=/var/lib/mayan/system/SECRET_KEY
CONCURRENCY_ARGUMENT=--concurrency=

DEFAULT_USER_UID=1000
DEFAULT_USER_GID=1000

MAYAN_USER_UID=${MAYAN_USER_UID:-${DEFAULT_USER_UID}}
MAYAN_USER_GID=${MAYAN_USER_GID:-${DEFAULT_USER_GID}}

export MAYAN_ALLOWED_HOSTS='["*"]'
export MAYAN_BIN=/opt/mayan-edms/bin/mayan-edms.py
export MAYAN_INSTALL_DIR=/opt/mayan-edms
export MAYAN_PYTHON_BIN_DIR=/opt/mayan-edms/bin/
export MAYAN_MEDIA_ROOT=/var/lib/mayan
export MAYAN_SETTINGS_MODULE=${MAYAN_SETTINGS_MODULE:-mayan.settings.production}
export DJANGO_SETTINGS_MODULE=${MAYAN_SETTINGS_MODULE}

export MAYAN_GUNICORN_BIN=${MAYAN_PYTHON_BIN_DIR}gunicorn
export MAYAN_GUNICORN_WORKERS=${MAYAN_GUNICORN_WORKERS:-2}
export MAYAN_GUNICORN_TIMEOUT=${MAYAN_GUNICORN_TIMEOUT:-120}
export MAYAN_PIP_BIN=${MAYAN_PYTHON_BIN_DIR}pip
export MAYAN_STATIC_ROOT=${MAYAN_INSTALL_DIR}/static

MAYAN_WORKER_FAST_CONCURRENCY=${MAYAN_WORKER_FAST_CONCURRENCY:-0}
MAYAN_WORKER_MEDIUM_CONCURRENCY=${MAYAN_WORKER_MEDIUM_CONCURRENCY:-0}
MAYAN_WORKER_SLOW_CONCURRENCY=${MAYAN_WORKER_SLOW_CONCURRENCY:-0}

update_uid_gid() {
    echo "mayan: update_uid_gid()"
    groupmod mayan -g ${MAYAN_USER_GID} 2>/dev/null || true
    usermod mayan -u ${MAYAN_USER_UID} -g ${MAYAN_USER_GID} 2>/dev/null

    if [ ${MAYAN_USER_UID} -ne ${DEFAULT_USER_UID} ] || [ ${MAYAN_USER_GID} -ne ${DEFAULT_USER_GID} ]; then
        echo "mayan: Updating file ownership. This might take a while if there are many documents."
        chown mayan:mayan ${MAYAN_INSTALL_DIR} ${MAYAN_STATIC_ROOT} ${MAYAN_MEDIA_ROOT}
    fi
}

update_uid_gid

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

# Allow importing of user setting modules
export PYTHONPATH=$PYTHONPATH:$MAYAN_MEDIA_ROOT

apt_get_install() {
    apt-get -q update
    apt-get install -y --force-yes --no-install-recommends --auto-remove "$@"
    apt-get -q clean
    rm -rf /var/lib/apt/lists/*
}

initialsetup() {
    echo "mayan: initialsetup()"
    su mayan -c "${MAYAN_BIN} initialsetup --force --no-dependencies"
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

run_all() {
    echo "mayan: start()"
    rm -rf /var/run/supervisor.sock
    exec /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
}

performupgrade() {
    echo "mayan: performupgrade()"
    su mayan -c "${MAYAN_BIN} performupgrade --no-dependencies"
}

make_ready() {
    # Check if this is a new install, otherwise try to upgrade the existing
    # installation on subsequent starts
    if [ ! -f $INSTALL_FLAG ]; then
        initialsetup
    else
        performupgrade
    fi
}

set_uid_guid() {
    echo "mayan: changing uid/guid"
    usermod mayan -u ${MAYAN_USER_UID:-${DEFAULT_USER_UID}}
    groupmod mayan -g ${MAYAN_USER_GID:-${DEFAULT_USER_GID}}
}

os_package_installs || true
pip_installs || true
chown mayan:mayan /var/lib/mayan -R

case "$1" in

run_initialsetup)
    initialsetup
    ;;

run_performupgrade)
    performupgrade
    ;;

run_all)
    make_ready
    run_all
    ;;

run_celery)
    run_celery.sh "${@:2}"
    ;;

run_frontend)
    run_frontend.sh
    ;;

run_tests)
    make_ready
    run_tests.sh
    ;;

run_worker)
    run_worker.sh "${@:2}"
    ;;

*)
    su mayan -c "$@"
    ;;

esac
