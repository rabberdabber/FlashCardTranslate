#!/bin/sh
source venv/bin/activate
exec gunicorn -b 0.0.0.0:8000 -w 4 --access-logfile - --error-logfile - main:app