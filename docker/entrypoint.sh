#!/bin/sh

python initApp.py

nginx
gunicorn --workers 3 --access-logfile /logs/gunicorn.log --bind unix:/tmp/ydlg.sock -m 007 wsgi -u www-data -g www-data