#!/bin/sh
set -e

MEDIA_ROOT="${MAYAN_MEDIA_ROOT:-/app/mayan/media}"
DB_PATH="$MEDIA_ROOT/db.sqlite3"

# First-run: if database doesn't exist, run migrations and create admin user
if [ ! -f "$DB_PATH" ]; then
    echo ">>> First run detected. Running migrations..."
    python manage.py migrate --settings=mayan.settings.development --noinput

    echo ">>> Creating default admin user (admin / adminpassword)..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print('Admin user created.')
else:
    print('Admin user already exists.')
"
    echo ">>> First-run setup complete."
else
    echo ">>> Existing database found at $DB_PATH. Skipping setup."
fi

# Execute the CMD (default: runserver)
exec "$@"
