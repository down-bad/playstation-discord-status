FROM python:alpine

WORKDIR /app
COPY requirements.txt ./
RUN pip install -y -r requirements.txt
COPY ./src/* /app
