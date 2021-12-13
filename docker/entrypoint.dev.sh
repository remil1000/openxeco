#!/bin/bash

exec gunicorn --chdir /app --workers 1 --bind 0.0.0.0:5000 app:app
exec python -m smtpd -n -c DebuggingServer 0.0.0.0:25