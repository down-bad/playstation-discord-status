FROM python:3-alpine

RUN mkdir /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app
