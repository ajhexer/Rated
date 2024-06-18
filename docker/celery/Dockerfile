FROM python:3.12-alpine

WORKDIR /app

COPY ../.. .


RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-docker-deps \
	gcc libc-dev linux-headers postgresql-dev


RUN pip install --no-cache-dir -r requirements.txt

ENV CELERY_BROKER_URL redis://redis:6379/0

CMD ["celery", "-A", "config", "worker", "-c", "10", "--loglevel=info"]