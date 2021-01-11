FROM python:3.7-buster

LABEL maintaienr="Jose Ricardo <jtmonegro@gmail.com>"

RUN apt update -y && apt install nginx -y
RUN pip install uwsgi

COPY . ./app
WORKDIR ./app

RUN pip install -r requirements.txt
RUN python init_db.py

COPY ./ydlg.nginx /etc/nginx/sites-enabled/default

CMD gunicorn --workers 3 --access-logfile ydlg.log --bind unix:/tmp/ydlg.sock -m 007 wsgi -u www-data -g www-data