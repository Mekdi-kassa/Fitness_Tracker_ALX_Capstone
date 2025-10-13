#!/usr/bin/env bash
# build.sh - Emergency fix for auth conflict
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Resetting migration issues ==="
# Delete problematic migration files in auth app
find . -path "*/auth/migrations/*.py" -not -name "__init__.py" -delete

echo "=== Creating fresh migrations ==="
python manage.py makemigrations auth --empty
python manage.py makemigrations

echo "=== Applying migrations with fake initial ==="
python manage.py migrate --fake-initial

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear

echo "=== Build completed ==="