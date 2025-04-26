#!/bin/bash
set -e

# PostgreSQLni kutish
echo "Waiting for database to be ready..."
./wait_for_db.sh

# Django migratsiyalar
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Kerakli komandani bajarish
exec "$@"
