FROM python:3.9-alpine

WORKDIR /app

COPY ../.. .

RUN pip install --no-cache-dir -r requirements.txt

ENV CELERY_BROKER_URL redis://redis:6379/0

CMD ["celery", "-A", "config", "worker", "-c", "10", "--loglevel=info"]