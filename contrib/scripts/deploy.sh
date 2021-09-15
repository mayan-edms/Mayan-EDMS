#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive
MAYAN_VERSION=">=4.0"
PYTHON_PIP_VERSION=21.1.1
PYTHON_PSYCOPG2_VERSION=2.8.6
PYTHON_REDIS_VERSION=3.5.3

# User settings. Update these.
MAYAN_DATABASE_HOST=127.0.0.1
MAYAN_DATABASE_NAME=mayan
MAYAN_DATABASE_PASSWORD=mayanuserpass
MAYAN_DATABASE_USERNAME=mayan
MAYAN_INSTALLATION_FOLDER=/opt/mayan-edms/
MAYAN_MEDIA_ROOT=/opt/mayan-edms/media/
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=mayanredispassword

if [ -d ${MAYAN_INSTALLATION_FOLDER} ]; then
    echo "Mayan EDMS already installed.\n"
    exit 0
fi

echo -e "i. Running apt-get update \n"
sudo apt-get update 

echo -e "1. Install binary dependencies \n"
sudo apt-get install --yes \
exiftool g++ gcc coreutils ghostscript gnupg1 graphviz \
libfuse2 libjpeg-dev libmagic1 libpq-dev libpng-dev libreoffice \
libtiff-dev poppler-utils postgresql python3-dev python3-virtualenv \
redis-server sane-utils supervisor tesseract-ocr zlib1g-dev

echo -e "2. Create the user account for the installation \n"
sudo adduser mayan --disabled-password --disabled-login --gecos ""

echo -e "3. Create the parent directory where the project will be deployed \n"
sudo mkdir --parent /opt

echo -e "4. Create the Python virtual environment \n"
sudo virtualenv ${MAYAN_INSTALLATION_FOLDER} -p /usr/bin/python3

echo -e "5. Make the mayan user the owner of the installation directory \n"
sudo chown mayan:mayan ${MAYAN_INSTALLATION_FOLDER} -R

echo -e "6. Upgrade to the latest pip version \n"
sudo -u mayan /opt/mayan-edms/bin/pip install -U pip

echo -e "7. Install Mayan EDMS from PyPI \n"
sudo -u mayan /opt/mayan-edms/bin/pip install mayan-edms${MAYAN_VERSION}

echo -e "8. Install the Python client for PostgreSQL and Redis \n"
sudo -u mayan /opt/mayan-edms/bin/pip install psycopg2==${PYTHON_PSYCOPG2_VERSION} redis==${PYTHON_REDIS_VERSION}

echo -e "9. Create the database for the installation \n"
sudo -u postgres psql -c "CREATE USER ${MAYAN_DATABASE_USERNAME} WITH password '${MAYAN_DATABASE_PASSWORD}';"
sudo -u postgres createdb -O ${MAYAN_DATABASE_USERNAME} ${MAYAN_DATABASE_NAME}

echo -e "10. Configure Redis \n"
echo "maxmemory-policy allkeys-lru" | sudo tee -a /etc/redis/redis.conf
echo "save \"\"" | sudo tee -a /etc/redis/redis.conf
echo "databases 3" | sudo tee -a /etc/redis/redis.conf
echo "requirepass ${REDIS_PASSWORD}" | sudo tee -a /etc/redis/redis.conf
sudo systemctl restart redis

echo -e "11. Initialize the project \n"
sudo -u mayan \
MAYAN_CELERY_BROKER_URL="redis://:${REDIS_PASSWORD}@${REDIS_HOST}:6379/0" \
MAYAN_CELERY_RESULT_BACKEND="redis://:${REDIS_PASSWORD}@${REDIS_HOST}:6379/1" \
MAYAN_DATABASES="{'default':{'ENGINE':'django.db.backends.postgresql','NAME':'${MAYAN_DATABASE_USERNAME}','PASSWORD':'${MAYAN_DATABASE_PASSWORD}','USER':'${MAYAN_DATABASE_USER}','HOST':'${MAYAN_DATABASE_HOST}'}}" \
MAYAN_LOCK_MANAGER_BACKEND="mayan.apps.lock_manager.backends.redis_lock.RedisLock" \
MAYAN_LOCK_MANAGER_BACKEND_ARGUMENTS="{'redis_url':'redis://:${REDIS_PASSWORD}@${REDIS_HOST}:6379/2'}" \
MAYAN_MEDIA_ROOT="${MAYAN_MEDIA_ROOT}" \
${MAYAN_INSTALLATION_FOLDER}bin/mayan-edms.py initialsetup

echo -e "12. Create the supervisor file at /etc/supervisor/conf.d/mayan-edms.conf \n"
sudo -u mayan MAYAN_MEDIA_ROOT="${MAYAN_MEDIA_ROOT}" ${MAYAN_INSTALLATION_FOLDER}bin/mayan-edms.py platformtemplate supervisord | sudo sh -c "cat > /etc/supervisor/conf.d/mayan-edms.conf"

echo -e "13. Enable and restart the services \n"
sudo systemctl enable supervisor
sudo systemctl restart supervisor

echo -e "14. Cleaning up \n"
sudo apt-get remove --purge --yes libjpeg-dev libpq-dev libpng-dev libtiff-dev zlib1g-dev
