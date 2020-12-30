FROM python:3.8.5

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./require.txt /app/require.txt

RUN pip install -r require.txt

RUN pip install --upgrade pip

COPY . /app


