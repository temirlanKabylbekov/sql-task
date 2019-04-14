FROM python:3.6-alpine

COPY . /app
WORKDIR /app

RUN apk update && apk add bash postgresql-dev gcc python3-dev linux-headers musl-dev
RUN pip install -r requirements.txt

# CMD flake8 && py.test
CMD tail -f /dev/null
