#!/bin/sh
source venv/bin/activate
exec gunicorn -b 0.0.0.0:5555 -w 4 --access-logfile - --error-logfile - main:app