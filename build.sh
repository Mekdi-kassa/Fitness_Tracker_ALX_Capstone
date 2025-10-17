#!/usr/bin/env bash
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Making migrations ==="
python manage.py makemigrations

echo "=== Applying migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear

echo "=== Creating startup script ==="
# Create a simple start script
cat > start.sh << EOF
#!/bin/bash
exec gunicorn fitness_tracker.wsgi:application --bind 0.0.0.0:\${PORT:-10000}
EOF

chmod +x start.sh

echo "=== Build completed ==="