#!/bin/bash

# Rodar migrações antes de iniciar
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
