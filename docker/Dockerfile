FROM alpine:latest

LABEL maintaienr="Jose Ricardo <jtmonegro@gmail.com>"

RUN apk add --no-cache python3 py3-pip nginx
RUN rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN mkdir /app
ADD ./ydlg /app/ydlg
COPY ./initApp.py /app/
COPY ./wsgi.py /app/
COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./docker/default.conf /etc/nginx/conf.d/default.conf
COPY ./docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

RUN mkdir /downloads/
RUN mkdir /logs/

RUN mkdir -p /run/nginx

CMD ./entrypoint.sh