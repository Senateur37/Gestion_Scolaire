#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python G_Scolaire/manage.py collectstatic --no-input
python G_Scolaire/manage.py migrate
