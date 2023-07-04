FROM alpine:3.18
RUN apk add --no-cache py3-pip
RUN apk add --no-cache py3-hatchling
RUN apk add --no-cache py3-pytest
RUN apk add --no-cache git