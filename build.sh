#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

poetry add django
poetry add dj_database_url
poetry add allauth

python manage.py collectstatic --no-input
python manage.py migrate

chmod a+x build.sh

poetry add gunicorn