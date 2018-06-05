#!/bin/sh

set -e
echo "mayan: starting entrypoint.sh"
INSTALL_FLAG=/var/lib/mayan/media/system/SECRET_KEY
export DOCKER_ROOT=/root

export MAYAN_DEFAULT_BROKER_URL=redis://127.0.0.1:6379/0
export MAYAN_DEFAULT_CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

export MAYAN_ALLOWED_HOSTS=*
export MAYAN_BIN=/usr/local/lib/python2.7/dist-packages/mayan/bin/mayan-edms.py
export MAYAN_BROKER_URL=${MAYAN_BROKER_URL:-${MAYAN_DEFAULT_BROKER_URL}}
export MAYAN_CELERY_RESULT_BACKEND=${MAYAN_CELERY_RESULT_BACKEND:-${MAYAN_DEFAULT_CELERY_RESULT_BACKEND}}
export MAYAN_GUNICORN_WORKERS=${MAYAN_GUNICORN_WORKERS:-2}
export MAYAN_INSTALL_DIR=/usr/local/lib/python2.7/dist-packages/mayan
export MAYAN_PYTHON_DIR=/usr/local/bin
export MAYAN_MEDIA_ROOT=/var/lib/mayan
export MAYAN_SETTINGS_MODULE=${MAYAN_SETTINGS_MODULE:-mayan.settings.production}

export CELERY_ALWAYS_EAGER=False
export PYTHONPATH=$PYTHONPATH:$MAYAN_MEDIA_ROOT

chown mayan:mayan /var/lib/mayan -R

initialize() {
    echo "mayan: initialize()"
    su mayan -c "mayan-edms.py initialsetup --force"
    su mayan -c "mayan-edms.py collectstatic --noinput --clear"
}

upgrade() {
    echo "mayan: upgrade()"
    su mayan -c "mayan-edms.py performupgrade"
    su mayan -c "mayan-edms.py collectstatic --noinput --clear"
}

start() {
    echo "mayan: start()"
    rm -rf /var/run/supervisor.sock
    exec /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
}

os_package_installs() {
    echo "mayan: os_package_installs()"
    if [ "${MAYAN_APT_INSTALLS}" ]; then
        apt-get-install $MAYAN_APT_INSTALLS
    fi
}

pip_installs() {
    echo "mayan: pip_installs()"
    if [ "${MAYAN_PIP_INSTALLS}" ]; then
        pip install $MAYAN_PIP_INSTALLS
    fi
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
           $DOCKER_ROOT/run-tests.sh
           ;;

*) su mayan -c "$@";
   ;;

esac
