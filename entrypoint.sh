#!/bin/bash

# xatoliklarda to'xtat
set -e

# PostgreSQLni kutish
./wait_for_db.sh

# Django migratsiyalar
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Kerakli komandani bajar
exec "$@"
