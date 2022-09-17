FROM python:3.10.6

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

COPY Pipfile Pipfile.lock /usr/src/app/

RUN pipenv install --system --deploy

COPY . /usr/src/app/