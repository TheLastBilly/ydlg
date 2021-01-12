#!/bin/sh

python3 initApp.py

nginx -g 'daemon off;' &
gunicorn --workers 3 --access-logfile /logs/gunicorn.log --bind unix:/tmp/ydlg.sock -m 007 wsgi -u nginx