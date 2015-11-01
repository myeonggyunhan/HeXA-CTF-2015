#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python initialize.py

