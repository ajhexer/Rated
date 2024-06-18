FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-docker-deps \
	gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# Remove dependencies
RUN apk del .tmp-docker-deps


WORKDIR /app
COPY ../.. .
