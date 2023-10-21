FROM python:3.11.6-alpine3.18
WORKDIR /events
RUN apk update && apk add bash postgresql-dev gcc python3-dev musl-dev postgresql-client libpq-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "./entrypoint.sh"]
