FROM alpine:latest

LABEL maintaienr="Jose Ricardo <jtmonegro@gmail.com>"

ENV YDLG_DOWNLOAD_FOLDER="/downloads"

ENV YDLG_USERNAME="admin"
ENV YDLG_PASSWORD="admin"

ENV PUID="1001"
ENV PGID="1001"

RUN apk add --no-cache python3 py3-pip nginx shadow
RUN rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN mkdir /app
ADD ./ydlg /app/ydlg
COPY ./initApp.py /app/
COPY ./wsgi.py /app/
COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

RUN mkdir /downloads/
RUN mkdir /logs/

RUN mkdir -p /run/nginx

CMD ./entrypoint.sh