#!/bin/sh
set -e

echo "Waiting for database to be ready..."
/code/wait_for_db.sh

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

exec "$@"
