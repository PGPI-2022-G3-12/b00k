# syntax=docker/dockerfile:1
FROM python:3.10-alpine

ENV SECRET_KEY=django-insecure-2#fh+bnx%)ump)9@^979y&_!*+myh%*dz-1iaa)*&*o$f&dt7n
ENV DB_NAME=b00k_db
ENV DB_USER=b00k
ENV DB_PASSWORD=b00k
ENV DB_HOST=localhost
ENV DB_PORT=5432

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone https://github.com/PGPI-2022-G3-12/b00k.git .
RUN pip install -r requirements.txt

WORKDIR /app/b00k

# local settings.py
ADD docker-settings.py /app/b00k/local_settings.py

RUN ./manage.py collectstatic --noinput

#CMD ["gunicorn", "-w 5", "b00k.wsgi", "--timeout=500", "-b 0.0.0.0:5000"]
