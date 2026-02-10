#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser (if not exists)..."
python manage.py customcreatesuperuser || true


echo "Starting server..."
exec "$@"
