#!/bin/sh

export $(egrep -v '^#' config.env | xargs)

export DEBIAN_FRONTEND=noninteractive

if [ "${APT_PROXY}" ]; \
    then echo "Acquire::http { Proxy \"${APT_PROXY}\"; };" | sudo tee /etc/apt/apt.conf.d/01proxy \
; fi \

# User settings: Update these
BINARY_MAYAN=${DEFAULT_DIRECTORY_INSTALLATION}bin/mayan-edms.py
BINARY_PIP=${DEFAULT_DIRECTORY_INSTALLATION}bin/pip
MAYAN_DATABASE_HOST=127.0.0.1
REDIS_HOST=127.0.0.1
MAYAN_VERSION="mayan-edms>=4.1<4.2"

if [ -d ${DEFAULT_DIRECTORY_INSTALLATION} ]; then
    echo "Mayan EDMS already installed.\n"
    exit 0
fi

echo -e "i. Running apt-get update \n"
sudo apt-get update

echo -e "1. Install binary dependencies \n"
sudo apt-get install --yes \
exiftool g++ gcc coreutils ghostscript gnupg1 graphviz \
libfuse2 libjpeg-dev libmagic1 libpq-dev libpng-dev libreoffice \
libtiff-dev poppler-utils postgresql python3-dev python3-venv \
redis-server sane-utils supervisor tesseract-ocr zlib1g-dev

echo -e "2. Create the user account for the installation \n"
sudo adduser mayan --disabled-password --disabled-login --gecos ""

echo -e "3. Create the parent directory where the project will be deployed \n"
sudo mkdir --parent /opt

echo -e "4. Create the Python virtual environment \n"
sudo python3 -m venv ${DEFAULT_DIRECTORY_INSTALLATION}

echo -e "5. Make the mayan user the owner of the installation directory \n"
sudo chown mayan:mayan ${DEFAULT_DIRECTORY_INSTALLATION} -R

echo -e "6. Upgrade to the latest pip version \n"
sudo -E -u mayan ${BINARY_PIP} install -U pip

echo -e "7. Install Mayan EDMS from PyPI \n"
sudo -E -u mayan ${BINARY_PIP} install ${MAYAN_VERSION}

echo -e "8. Install the Python client for PostgreSQL and Redis \n"
sudo -E -u mayan ${BINARY_PIP} install psycopg2==${PYTHON_PSYCOPG2_VERSION} redis==${PYTHON_REDIS_VERSION}

echo -e "9. Create the database for the installation \n"
sudo -u postgres psql -c "CREATE USER ${DEFAULT_DATABASE_USER} WITH password '${DEFAULT_DATABASE_PASSWORD}';"
sudo -u postgres createdb -O ${DEFAULT_DATABASE_USER} ${DEFAULT_DATABASE_NAME}

echo -e "10. Configure Redis \n"
echo "maxmemory-policy allkeys-lru" | sudo tee -a /etc/redis/redis.conf
echo "save \"\"" | sudo tee -a /etc/redis/redis.conf
echo "databases 3" | sudo tee -a /etc/redis/redis.conf
echo "requirepass ${DEFAULT_REDIS_PASSWORD}" | sudo tee -a /etc/redis/redis.conf
sudo systemctl restart redis

echo -e "11. Initialize the project \n"
sudo -u mayan \
MAYAN_CELERY_BROKER_URL="redis://:${DEFAULT_REDIS_PASSWORD}@${REDIS_HOST}:6379/0" \
MAYAN_CELERY_RESULT_BACKEND="redis://:${DEFAULT_REDIS_PASSWORD}@${REDIS_HOST}:6379/1" \
MAYAN_DATABASES="{'default':{'ENGINE':'django.db.backends.postgresql','NAME':'${DEFAULT_DATABASE_USER}','PASSWORD':'${DEFAULT_DATABASE_PASSWORD}','USER':'${MAYAN_DATABASE_USER}','HOST':'${MAYAN_DATABASE_HOST}'}}" \
MAYAN_LOCK_MANAGER_BACKEND="mayan.apps.lock_manager.backends.redis_lock.RedisLock" \
MAYAN_LOCK_MANAGER_BACKEND_ARGUMENTS="{'redis_url':'redis://:${DEFAULT_REDIS_PASSWORD}@${REDIS_HOST}:6379/2'}" \
DEFAULT_DIRECTORY_MEDIA_ROOT="${DEFAULT_DIRECTORY_MEDIA_ROOT}" \
${BINARY_MAYAN} initialsetup

echo -e "12. Create the Supervisord file at /etc/supervisor/conf.d/mayan-edms.conf \n"
sudo -u mayan DEFAULT_DIRECTORY_MEDIA_ROOT="${DEFAULT_DIRECTORY_MEDIA_ROOT}" ${DEFAULT_DIRECTORY_INSTALLATION}bin/mayan-edms.py platformtemplate supervisord | sudo sh -c "cat > /etc/supervisor/conf.d/mayan-edms.conf"

echo -e "13. Enable and restart the services \n"
sudo systemctl enable supervisor
sudo systemctl restart supervisor

echo -e "13-1. Upgrade Supervisord \n"
sudo systemctl stop supervisor
wget -c http://ftp.us.debian.org/debian/pool/main/s/supervisor/supervisor_4.2.2-2_all.deb
sudo dpkg --install supervisor_4.2.2-2_all.deb
sudo systemctl restart supervisor

echo -e "14. Cleaning up \n"
sudo apt-get remove --purge --yes libjpeg-dev libpq-dev libpng-dev libtiff-dev zlib1g-dev
