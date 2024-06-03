#!/bin/bash

python manage.py makemigrations --no-input
python manage.py migrate --no-input

python manage.py loaddata user_fixture.json
python manage.py loaddata tokens.json

python manage.py runserver 0.0.0.0:8000