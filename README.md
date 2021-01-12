# YDLG: Youtube DL GUI

**WARNING: This image/project is NOT production ready. This is a dumb little thing I made over a week end, and it's meant for internal use only. DO NOT put this on a live server, you've been warned.**

## How to use it
While you could use a one-liner with docker to setup this image, I much rather use a docker-compose file.

```yml
version: '2'

services: 
    ydlg:
        image: thelastbilly/ydlg
        ports:
            - "[HOST PORT]:80"                              # You can use any ports you'd like
        volumes:
            - "[PATH TO LOGS FOLDER ON HOST]:/logs"         # Optional, but you know, it's a good idea to also set this one up
            - "[PATH TO DOWNLOADS FOLDER ON HOST]:/downloads"
        environment: 
            - YDLG_USERNAME=[USERNAME FOR UI]               # Username and pass for the login screen
            - YDLG_PASSWORD=[PASSWORD FOR UI]

            - PUID=[USER ID FOR IMAGE]                      # Both are optional-ish since you "can" run the image without them, but you'll run into
            - PGID=[GROUP ID FOR IMAGE]                     # permissions errors with the downloads
```