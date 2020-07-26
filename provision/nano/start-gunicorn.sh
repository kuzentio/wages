#!/bin/bash
cd "~/wages"
gunicorn --bind 127.0.0.1:8000 -w 4 --access-logfile - --error-logfile - wages.wsgi
