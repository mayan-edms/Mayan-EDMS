#!/bin/sh
set -e

# This script is meant for quick & easy install via:
#   $ curl -fsSL get.mayan-edms.com -o get-mayan-edms.sh
#   $ sh get-mayan-edms.sh
#
# NOTE: Before executing, make sure to verify the contents of the script
#       you downloaded matches the contents of docker.sh
#       located at https://gitlab.com/mayan-edms/mayan-edms/blob/master/contrib/scripts/install/docker.sh

: ${VERBOSE:=true}
: ${INSTALL_DOCKER:=false}
: ${DELETE_VOLUMES:=false}
: ${USE_DOCKER_NETWORK:=true}
: ${DOCKER_NETWORK_NAME:=mayan}
: ${DATABASE_USER:=mayan}
: ${DATABASE_NAME:=mayan}
: ${DATABASE_PASSWORD:=mayanuserpass}
: ${DOCKER_POSTGRES_IMAGE:=postgres:9.6-alpine}
: ${DOCKER_POSTGRES_CONTAINER:=mayan-edms-postgres}
: ${DOCKER_POSTGRES_VOLUME:=/docker-volumes/mayan-edms/postgres}
: ${DOCKER_POSTGRES_PORT:=5432}
: ${DOCKER_POSTGRES_DELAY:=10}
: ${DOCKER_REDIS_IMAGE:=redis:5.0-alpine}
: ${DOCKER_REDIS_CONTAINER:=mayan-edms-redis}
: ${DOCKER_REDIS_PASSWORD:=mayanredispassword}
: ${DOCKER_REDIS_PORT:=6379}
: ${DOCKER_REDIS_VOLUME:=/docker-volumes/mayan-edms/redis}
: ${DOCKER_MAYAN_IMAGE:=mayanedms/mayanedms:latest}
: ${DOCKER_MAYAN_CONTAINER:=mayan-edms}
: ${DOCKER_MAYAN_VOLUME:=/docker-volumes/mayan-edms/media}
: ${DOCKER_MAYAN_PORT:=80}

cat << EOF

███╗   ███╗ █████╗ ██╗   ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║
██╔████╔██║███████║ ╚████╔╝ ███████║██╔██╗ ██║
██║╚██╔╝██║██╔══██║  ╚██╔╝  ██╔══██║██║╚██╗██║
██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
Docker deploy script

NOTE: Make sure to verify the contents of this script
matches the contents of docker.sh located at https://gitlab.com/mayan-edms/mayan-edms/blob/master/contrib/scripts/install/docker.sh before executing.

EOF

if [ "$VERBOSE" = true ]; then
echo "Variable values to be used:"
echo "---------------------------"
echo "INSTALL_DOCKER: $INSTALL_DOCKER"
echo "DELETE_VOLUMES: $DELETE_VOLUMES"
echo "USE_DOCKER_NETWORK: $USE_DOCKER_NETWORK"
echo "DOCKER_NETWORK_NAME: $DOCKER_NETWORK_NAME"
echo "DATABASE_USER: $DATABASE_USER"
echo "DATABASE_NAME: $DATABASE_NAME"
echo "DATABASE_PASSWORD: $DATABASE_PASSWORD"
echo "DOCKER_POSTGRES_IMAGE: $DOCKER_POSTGRES_IMAGE"
echo "DOCKER_POSTGRES_CONTAINER: $DOCKER_POSTGRES_CONTAINER"
echo "DOCKER_POSTGRES_VOLUME: $DOCKER_POSTGRES_VOLUME"
echo "DOCKER_POSTGRES_PORT: $DOCKER_POSTGRES_PORT"
echo "DOCKER_POSTGRES_DELAY: $DOCKER_POSTGRES_DELAY"
echo "DOCKER_REDIS_IMAGE: $DOCKER_REDIS_IMAGE"
echo "DOCKER_REDIS_CONTAINER: $DOCKER_REDIS_CONTAINER"
echo "DOCKER_REDIS_PORT: $DOCKER_REDIS_PORT"
echo "DOCKER_REDIS_PASSWORD: $DOCKER_REDIS_PASSWORD"
echo "DOCKER_REDIS_VOLUME: $DOCKER_REDIS_VOLUME"
echo "DOCKER_MAYAN_IMAGE: $DOCKER_MAYAN_IMAGE"
echo "DOCKER_MAYAN_CONTAINER: $DOCKER_MAYAN_CONTAINER"
echo "DOCKER_MAYAN_VOLUME: $DOCKER_MAYAN_VOLUME"
echo "DOCKER_MAYAN_PORT: $DOCKER_MAYAN_PORT"
echo
echo "Override any of them by setting them before the script. "
echo "Example: INSTALL_DOCKER=true sh get-mayan-edms.sh"

echo "\nStarting in 10 seconds. Press CTRL+C to cancel."
sleep 10
fi

if [ "$INSTALL_DOCKER" = true ]; then
    echo -n "* Installing Docker..."
    curl -fsSL get.docker.com -o get-docker.sh >/dev/null
    sh get-docker.sh >/dev/null 2>&1
    rm get-docker.sh
    echo "Done"
fi

if [ -z `which docker`  ]; then
    echo "Docker is not installed. Rerun this script with the variable INSTALL_DOCKER set to true."
    exit 1
fi

echo -n "* Removing existing Mayan EDMS and PostgreSQL containers (no data will be lost)..."
docker rm -f $DOCKER_REDIS_CONTAINER >/dev/null 2>&1  || true
docker rm -f $DOCKER_POSTGRES_CONTAINER >/dev/null 2>&1  || true
docker rm -f $DOCKER_MAYAN_CONTAINER >/dev/null 2>&1  || true
echo "Done"

if [ "$DELETE_VOLUMES" = true ]; then
echo -n "* Deleting Docker volumes in 5 seconds (warning: this will delete all document data). Press CTRL+C to cancel..."
sleep 5
rm DOCKER_MAYAN_VOLUME -Rf || true
rm DOCKER_POSTGRES_VOLUME -Rf || true
echo "Done"
fi

echo -n "* Pulling (downloading) the Redis Docker image..."
docker pull $DOCKER_REDIS_IMAGE > /dev/null
echo "Done"

echo -n "* Pulling (downloading) the PostgreSQL Docker image..."
docker pull $DOCKER_POSTGRES_IMAGE > /dev/null
echo "Done"

echo -n "* Pulling (downloading) the Mayan EDMS Docker image..."
docker pull $DOCKER_MAYAN_IMAGE >/dev/null
echo "Done"

if [ "$USE_DOCKER_NETWORK" = true ]; then
    echo -n "* Creating Docker network..."
    docker network create $DOCKER_NETWORK_NAME 2> /dev/null || true
    # Ignore error if the network already exists
    echo "Done"
fi

if [ "$USE_DOCKER_NETWORK" = true ]; then
    NETWORK_ARGUMENT="--network=$DOCKER_NETWORK_NAME"
    POSTGRES_PORT_ARGUMENT=""
    REDIS_PORT_ARGUMENT=""
    MAYAN_DATABASE_PORT_ARGUMENT=""
    MAYAN_DATABASE_HOST_ARGUMENT="-e MAYAN_DATABASE_HOST=$DOCKER_POSTGRES_CONTAINER"
    MAYAN_CELERY_BROKER_URL_ARGUMENT="-e MAYAN_CELERY_BROKER_URL=redis://:${DOCKER_REDIS_PASSWORD}@$DOCKER_REDIS_CONTAINER:6379/0"
    MAYAN_CELERY_RESULT_BACKEND_ARGUMENT="-e MAYAN_CELERY_RESULT_BACKEND=redis://:${DOCKER_REDIS_PASSWORD}@$DOCKER_REDIS_CONTAINER:6379/1"
else
    NETWORK_ARGUMENT=""
    POSTGRES_PORT_ARGUMENT="-e $DOCKER_POSTGRES_PORT:5432"
    REDIS_PORT_ARGUMENT="-e $DOCKER_REDIS_PORT:6379"
    MAYAN_DATABASE_PORT_ARGUMENT="-e MAYAN_DATABASE_PORT=$DOCKER_POSTGRES_PORT"
    MAYAN_DATABASE_HOST_ARGUMENT="-e MAYAN_DATABASE_HOST=172.17.0.1"
    MAYAN_CELERY_BROKER_URL_ARGUMENT="-e MAYAN_CELERY_BROKER_URL=redis://:${DOCKER_REDIS_PASSWORD}@172.17.0.1:6379/0"
    MAYAN_CELERY_RESULT_BACKEND_ARGUMENT="-e MAYAN_CELERY_RESULT_BACKEND=redis://:${DOCKER_REDIS_PASSWORD}@172.17.0.1:6379/1"
fi

echo -n "* Deploying the PostgreSQL container..."
docker run -d \
--name $DOCKER_POSTGRES_CONTAINER \
$NETWORK_ARGUMENT \
--restart=always \
$POSTGRES_PORT_ARGUMENT \
-e POSTGRES_USER=$DATABASE_USER \
-e POSTGRES_DB=$DATABASE_NAME \
-e POSTGRES_PASSWORD=$DATABASE_PASSWORD \
-v $DOCKER_POSTGRES_VOLUME:/var/lib/postgresql/data \
$DOCKER_POSTGRES_IMAGE >/dev/null
echo "Done"

echo -n "* Deploying the Redis container..."
docker run -d \
--name $DOCKER_REDIS_CONTAINER \
$NETWORK_ARGUMENT \
--restart=always \
$REDIS_PORT_ARGUMENT \
-v $DOCKER_REDIS_VOLUME:/data \
$DOCKER_REDIS_IMAGE \
redis-server \
--appendonly no \
--databases 2 \
--maxmemory 100mb \
--maxmemory-policy allkeys-lru \
--maxclients 500 \
--save "" \
--tcp-backlog 256 \
--requirepass $DOCKER_REDIS_PASSWORD \
>/dev/null
echo "Done"

echo -n "* Waiting for the PostgreSQL container to be ready (${DOCKER_POSTGRES_DELAY} seconds)..."
sleep $DOCKER_POSTGRES_DELAY
echo "Done"

echo -n "* Deploying Mayan EDMS container..."
docker run -d \
--name $DOCKER_MAYAN_CONTAINER \
$NETWORK_ARGUMENT \
--restart=always \
-p $DOCKER_MAYAN_PORT:8000 \
-e MAYAN_DATABASE_ENGINE=django.db.backends.postgresql \
$MAYAN_DATABASE_HOST_ARGUMENT \
$MAYAN_DATABASE_PORT_ARGUMENT \
-e MAYAN_DATABASE_NAME=$DATABASE_NAME \
-e MAYAN_DATABASE_PASSWORD=$DATABASE_PASSWORD \
-e MAYAN_DATABASE_USER=$DATABASE_USER \
-e MAYAN_DATABASE_CONN_MAX_AGE=0 \
$MAYAN_CELERY_BROKER_URL_ARGUMENT \
$MAYAN_CELERY_RESULT_BACKEND_ARGUMENT \
-v $DOCKER_MAYAN_VOLUME:/var/lib/mayan \
$DOCKER_MAYAN_IMAGE >/dev/null
echo "Done"

echo -n "* Waiting for the Mayan EDMS container to be ready (might take a few minutes)..."
while ! curl --output /dev/null --silent --head --fail http://localhost:$DOCKER_MAYAN_PORT; do sleep 1 && echo -n .; done;
echo "Done"
