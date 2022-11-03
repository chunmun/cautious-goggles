FROM python:latest

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000