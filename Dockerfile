FROM selenium/chrome-standalone:latest

WORKDIR /mnt/src
ADD ["/src",  "."]

