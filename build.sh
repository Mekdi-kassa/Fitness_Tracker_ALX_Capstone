#!/usr/bin/env bash
# Exit if any command fails
set -o errexit

# 1. Install all required packages
pip install -r requirements.txt

# 2. Update database structure
python manage.py migrate

# 3. Prepare CSS/JS/image files
python manage.py collectstatic --no-input