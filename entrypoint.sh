#!/bin/bash
# Apply any database migrations
COMMAND="python manage.py migrate"
echo "Applying database migrations ($COMMAND)..."
eval $COMMAND || exit 1

# Adding initial default industries data
COMMAND="python manage.py industrysetup"
echo "Adding initial default data ($COMMAND)..."
eval $COMMAND || exit 1

COMMAND="python manage.py collectstatic --no-input"
echo "Collecting statifiles ($COMMAND)..."
eval $COMMAND || exit 1

# Default to port 8000 if PORT is not set
: "${PORT:=8000}"
# Running server
echo "Running server..."
exec gunicorn --bind :$PORT --workers 2 src.config.wsgi  --access-logfile - --error-logfile - --log-level info
