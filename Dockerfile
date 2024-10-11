FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /backend/

ADD backend .
ADD requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV LC_TIME ru_RU.UTF-8
