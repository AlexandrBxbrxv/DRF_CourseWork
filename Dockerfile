FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
