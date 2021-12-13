ARG PYTHON_VERSION=3.8-slim-buster
FROM python:$PYTHON_VERSION

ENV PYTHONUNBUFFERED=1

ARG ENVIRONMENT=production

ENV JWT_SECRET_KEY=some_random_secret

ENV DB_DRIVER=mysql+pymysql
ENV DB_HOSTNAME=openxeco-db
ENV DB_PORT=3309
ENV DB_NAME=cyberlux
ENV DB_USERNAME=cyberlux
ENV DB_PASSWORD=cyberlux

ENV MAIL_SERVER=127.0.0.1
ENV MAIL_PORT=25
ENV MAIL_USERNAME=openxeco@localhost.localdomain
ENV MAIL_PASSWORD=None
ENV MAIL_USE_TLS=True
ENV MAIL_USE_SSL=True
ENV MAIL_DEFAULT_SENDER=openxeco@localhost.localdomain

ENV IMAGE_FOLDER=/cyberlux_media

VOLUME [ "${IMAGE_FOLDER}" ]

WORKDIR /app

RUN pip install gunicorn[gevent]

COPY routes.py      /app/
COPY app.py         /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY db             /app/db
COPY decorator      /app/decorator
COPY exception      /app/exception
COPY migrations     /app/migrations
COPY resource       /app/resource
COPY template       /app/template
COPY utils          /app/utils

COPY config         /app/config
#COPY docker/entrypoint.dev.sh /entrypoint2.sh

EXPOSE 5000

#RUN flask db upgrade

CMD gunicorn --chdir /app --workers 1 --bind 0.0.0.0:5000 app:app
