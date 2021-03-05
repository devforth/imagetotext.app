FROM python:3.8

WORKDIR /code/

ENV PYTHONUNBUFFERED 1
RUN apt update -y && apt install -y libicu-dev pkg-config tesseract-ocr libtesseract-dev libleptonica-dev
RUN pip install --upgrade pip &&\
pip install pipenv

COPY Pipfile /code/
COPY Pipfile.lock /code/

RUN pipenv sync

COPY . /code/

