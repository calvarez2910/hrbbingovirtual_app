
#FROM dockerregistry.mvilla.org/alpine-pandas:3.7.9
FROM python:3.7.9


WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uwsgi", "app.ini"]
