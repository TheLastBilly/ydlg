FROM alpine:latest

LABEL maintaienr="Jose Ricardo <jtmonegro@gmail.com>"

RUN apk add --no-cahce python3 py3-pip
RUN rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN mkdir /app
COPY ../ydlg /app/
COPY ../initApp.py /app/
COPY ../requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./default.conf /etc/nginx/sites-enabled/default.conf
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

RUN mkdir /downloads/
RUN mkdir /logs/

CMD ./entrypoint.sh