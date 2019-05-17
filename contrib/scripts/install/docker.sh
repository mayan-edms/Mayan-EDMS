#!/bin/sh
set -e

# This script is meant for quick & easy install via:
#   $ curl -fsSL get.mayan-edms.com -o get-mayan-edms.sh
#   $ sh get-mayan-edms.sh
#
# NOTE: Make sure to verify the contents of the script
#       you downloaded matches the contents of docker.sh
#       located at https://gitlab.com/mayan-edms/mayan-edms/blob/master/contrib/scripts/install/docker.sh
#       before executing.

: ${VERBOSE:=true}
: ${INSTALL_DOCKER:=false}
: ${DELETE_VOLUMES:=false}
: ${DATABASE_USER:=mayan}
: ${DATABASE_NAME:=mayan}
: ${DATABASE_PASSWORD:=mayanuserpass}
: ${DOCKER_POSTGRES_IMAGE:=postgres:9.6}
: ${DOCKER_POSTGRES_CONTAINER:=mayan-edms-postgres}
: ${DOCKER_POSTGRES_VOLUME:=/docker-volumes/mayan-edms/postgres}
: ${DOCKER_POSTGRES_PORT:=5432}
: ${DOCKER_MAYAN_IMAGE:=mayanedms/mayanedms:latest}
: ${DOCKER_MAYAN_CONTAINER:=mayan-edms}
: ${DOCKER_MAYAN_VOLUME:=/docker-volumes/mayan-edms/media}

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
echo "DATABASE_USER: $DATABASE_USER"
echo "DATABASE_NAME: $DATABASE_NAME"
echo "DATABASE_PASSWORD: $DATABASE_PASSWORD"
echo "DOCKER_POSTGRES_IMAGE: $DOCKER_POSTGRES_IMAGE"
echo "DOCKER_POSTGRES_CONTAINER: $DOCKER_POSTGRES_CONTAINER"
echo "DOCKER_POSTGRES_VOLUME: $DOCKER_POSTGRES_VOLUME"
echo "DOCKER_POSTGRES_PORT: $DOCKER_POSTGRES_PORT"
echo "DOCKER_MAYAN_IMAGE: $DOCKER_MAYAN_IMAGE"
echo "DOCKER_MAYAN_CONTAINER: $DOCKER_MAYAN_CONTAINER"
echo "DOCKER_MAYAN_VOLUME: $DOCKER_MAYAN_VOLUME"
echo "\nStarting in 10 seconds."
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
true || docker stop $DOCKER_MAYAN_CONTAINER >/dev/null 2>&1
true || docker rm $DOCKER_MAYAN_CONTAINER >/dev/null 2>&1
true || docker stop $DOCKER_POSTGRES_CONTAINER >/dev/null 2>&1
true || docker rm $DOCKER_POSTGRES_CONTAINER >/dev/null 2>&1
echo "Done"

if [ "$DELETE_VOLUMES" = true ]; then
echo -n "* Deleting Docker volumes in 5 seconds (warning: this delete all document data)..."
sleep 5
true || rm DOCKER_MAYAN_VOLUME -Rf
true || rm DOCKER_POSTGRES_VOLUME -Rf
echo "Done"
fi

echo -n "* Pulling (downloading) the Mayan EDMS Docker image..."
docker pull $DOCKER_MAYAN_IMAGE >/dev/null
echo "Done"

echo -n "* Pulling (downloading) the PostgreSQL Docker image..."
docker pull $DOCKER_POSTGRES_IMAGE > /dev/null
echo "Done"

echo -n "* Deploying the PostgreSQL container..."
docker run -d \
--name $DOCKER_POSTGRES_CONTAINER \
--restart=always \
-p $DOCKER_POSTGRES_PORT:5432 \
-e POSTGRES_USER=$DATABASE_USER \
-e POSTGRES_DB=$DATABASE_NAME \
-e POSTGRES_PASSWORD=$DATABASE_PASSWORD \
-v $DOCKER_POSTGRES_VOLUME:/var/lib/postgresql/data \
$DOCKER_POSTGRES_IMAGE >/dev/null
echo "Done"

echo -n "* Waiting for the PostgreSQL container to be ready (10 seconds)..."
sleep 10
echo "Done"

echo -n "* Deploying Mayan EDMS container..."
docker run -d \
--name $DOCKER_MAYAN_CONTAINER \
--restart=always \
-p 80:8000 \
-e MAYAN_DATABASE_ENGINE=django.db.backends.postgresql \
-e MAYAN_DATABASE_HOST=172.17.0.1 \
-e MAYAN_DATABASE_NAME=$DATABASE_NAME \
-e MAYAN_DATABASE_PASSWORD=$DATABASE_PASSWORD \
-e MAYAN_DATABASE_USER=$DATABASE_USER \
-e MAYAN_DATABASE_PORT=$DOCKER_POSTGRES_PORT \
-e MAYAN_DATABASE_CONN_MAX_AGE=0 \
-v $DOCKER_MAYAN_VOLUME:/var/lib/mayan \
$DOCKER_MAYAN_IMAGE >/dev/null
echo "Done"

echo -n "* Waiting for the Mayan EDMS container to be ready (might take a few minutes)..."
while ! curl --output /dev/null --silent --head --fail http://localhost:80; do sleep 1 && echo -n .; done;
echo "Done"
