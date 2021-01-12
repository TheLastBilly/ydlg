#!/bin/sh

python3 initApp.py

usermod -u $PUID nginx
groupmod -g $PGID www-data

su - nginx

chown -R nginx:www-data /downloads
chown -R nginx:www-data /logs

nginx -g 'daemon off;' &
gunicorn --workers 3 --access-logfile /logs/gunicorn.log --error-logfile /logs/app.log --bind unix:/tmp/ydlg.sock -m 007 wsgi -u nginx --capture-output