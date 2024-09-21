#!/usr/bin/env bash
set -e
host=${1:-"localhost"}

database_name="recon_db"
database_user="recon_user"

echo "Droping database ..."
COMMAND="sudo -u postgres psql -c 'drop database $database_name' || true"
eval $COMMAND || exit 1

echo "Creating user..."
COMMAND="sudo -u postgres psql -c \"CREATE USER $database_user WITH PASSWORD 'recon_pass';\" -h $host || true"
eval $COMMAND || exit 1

echo "Assign user CREATEDB database role..."
COMMAND="sudo -u postgres psql -c \"ALTER USER $database_user WITH CREATEDB;\" -h $host || true"
eval $COMMAND || exit 1

echo "Creating database..."
COMMAND="sudo -u postgres psql -c \"CREATE DATABASE $database_name OWNER $database_user;\" -h $host || true"
eval $COMMAND || exit 1

# Apply any database migrations
COMMAND="python manage.py migrate"
echo "Applying database migrations ($COMMAND)..."
eval $COMMAND || exit 1


