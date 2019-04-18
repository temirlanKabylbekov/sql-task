FROM python:3.6-alpine

ARG DB_HOST
ARG DB_PORT
ARG DB_WAIT_TIMEOUT

COPY . /app
WORKDIR /app

RUN apk update && apk add bash postgresql-dev gcc python3-dev linux-headers musl-dev
RUN pip install -r requirements.txt

ENV DOCKERIZE_VERSION v0.6.1
RUN wget http://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# stay container runnable (tail -f)
CMD dockerize -wait tcp://${DB_HOST}:${DB_PORT} -timeout ${DB_WAIT_TIMEOUT} flake8 && py.test && tail -f /dev/null
