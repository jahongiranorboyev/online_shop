#!/bin/sh

HOST=${POSTGRES_HOST:-db}
PORT=${POSTGRES_PORT:-5432}

echo "Waiting for database at $HOST:$PORT..."

while ! nc -z $HOST $PORT; do
  sleep 0.1
done

echo "Database is up!"
exec "$@"
