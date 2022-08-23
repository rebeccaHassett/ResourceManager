# syntax=docker/dockerfile:1

FROM python:3.9-slim

EXPOSE 8000

WORKDIR .
COPY .. .
RUN pip install -r requirements.txt

CMD ["strawberry", "server", "Schema"]