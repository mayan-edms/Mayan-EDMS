#!/bin/bash

echo "mayan-edms: run_all"

rm -rf /var/run/supervisor.sock
exec /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
