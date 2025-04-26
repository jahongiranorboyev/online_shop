#!/bin/sh

HOST=${POSTGRES_HOST}
PORT=${POSTGRES_PORT}

echo "Waiting for database at $HOST:$PORT..."

while ! nc -z $HOST $PORT; do
  sleep 0.1
done

echo "Database is up!"
exec "$@"
