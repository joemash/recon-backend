#!/bin/bash

set -e
# Wait for the database to be available
until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER"; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Start the backend service
COMMAND="python manage.py migrate"
echo "Applying database migrations ($COMMAND)..."
eval $COMMAND || exit 1

COMMAND="python manage.py collectstatic --no-input"
echo "Collecting statifiles ($COMMAND)..."
eval $COMMAND || exit 1

# Default to port 8080 if PORT is not set
: "${PORT:=8080}"
# Running server
echo "Running server..."
exec gunicorn --bind :$PORT --workers 2 src.config.wsgi  --access-logfile - --error-logfile - --log-level info

exec "$@"
