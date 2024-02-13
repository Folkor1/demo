#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

add django

python manage.py collectstatic --no-input
python manage.py migrate

chmod a+x build.sh

poetry add gunicorn