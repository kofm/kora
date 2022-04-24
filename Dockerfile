# syntax=docker/dockerfile:1
FROM python:3
ARG secretkey
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=${secretkey}
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
# Collect static files
RUN python manage.py collectstatic --noinput
