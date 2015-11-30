#!/bin/bash
set -e

if [[ -z $POSTGRES_PORT_5432_TCP_ADDR ]]; then
  echo "** ERROR: You need to link the Postgres container."
  exit 1
fi

until nc -z $POSTGRES_PORT_5432_TCP_ADDR $POSTGRES_PORT_5432_TCP_PORT; do
    echo "$(date) - waiting for Postgres..."
    sleep 1
done

# Migrate database, create initial admin user
mayan-edms.py initialsetup

exec "$@"
