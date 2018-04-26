#!/bin/sh

set -e
echo "* start"
INSTALL_FLAG=/var/lib/mayan/media/system/SECRET_KEY

export MAYAN_MEDIA_ROOT=/var/lib/mayan
export MAYAN_GUNICORN_WORKERS=${MAYAN_GUNICORN_WORKERS:-3}
export MAYAN_ALLOWED_HOSTS=*

chown mayan:mayan /var/lib/mayan -R

initialize() {
    echo "* initialize"
    su mayan -c "mayan-edms.py initialsetup --force"
    su mayan -c "mayan-edms.py collectstatic --noinput --clear"
}

upgrade() {
    echo "* upgrade"
    su mayan -c "mayan-edms.py performupgrade"
    su mayan -c "mayan-edms.py collectstatic --noinput --clear"
}

start() {
    rm -rf /var/run/supervisor.sock
    exec /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
}

os_package_installs() {
    echo "* os_package_installs"
    if [ "${MAYAN_APT_INSTALLS}" ]; then
        apt-get-install $MAYAN_APT_INSTALLS
    fi
}

pip_installs() {
    echo "* pip_installs"
    if [ "${MAYAN_PIP_INSTALLS}" ]; then
        pip install $MAYAN_PIP_INSTALLS
    fi
}

os_package_installs || true
pip_installs || true

if [ "$1" = 'mayan' ]; then
    # Check if this is a new install, otherwise try to upgrade the existing
    # installation on subsequent starts
    if [ ! -f $INSTALL_FLAG ]; then
        initialize
    else
        upgrade
    fi
    start
else
    su mayan -c "mayan-edms.py $@";
fi
