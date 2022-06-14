#!/bin/sh
exec gunicorn -b 0.0.0.0:5555 --access-logfile - --error-logfile - main:app