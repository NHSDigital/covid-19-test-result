FROM python:3

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip setuptools poetry && \
  poetry install

EXPOSE 9000
CMD poetry run flask run --host=0.0.0.0 --port=9000
