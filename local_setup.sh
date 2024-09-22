#!/usr/bin/env bash
set -e
host=${1:-"localhost"}

database_name="recon_db"
database_user="recon_user"

echo "Droping database ..."
COMMAND="psql -U postgres  -c 'drop database $database_name' || true"
eval $COMMAND || exit 1

echo "Creating user..."
psql -U postgres  -c "CREATE USER $database_user WITH PASSWORD 'recon_pass';" -h $host || true

echo "Assign user CREATEDB database role..."
psql -U postgres  -c "ALTER USER $database_user WITH CREATEDB;" -h $host || true

echo "Creating database ..."
COMMAND="psql -U postgres  -c 'create database $database_name owner $database_user;' -h $host"
eval $COMMAND || exit 1

# Apply any database migrations
COMMAND="python manage.py migrate"
echo "Applying database migrations ($COMMAND)..."
eval $COMMAND || exit 1
