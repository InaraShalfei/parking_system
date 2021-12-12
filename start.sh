#!/bin/bash

python manage.py makemigrations users
python manage.py migrate users
python manage.py makemigrations parking_systems
python manage.py migrate parking_systems
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000