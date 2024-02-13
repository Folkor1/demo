#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

poetry add django
poetry add dj_database_url
poetry add django-allauth
poetry add django_filter
poetry add cloudinary
poetry add django-crispy-forms
poetry add psycopg2

python manage.py collectstatic --no-input
python manage.py migrate

chmod a+x build.sh

poetry add gunicorn