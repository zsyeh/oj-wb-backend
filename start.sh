#!/bin/bash
lsof -i :8000
source ~/django_venv/bin/activate

gunicorn --workers 3 leave_management.wsgi:application &

