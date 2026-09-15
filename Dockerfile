# syntax=docker/dockerfile:1

FROM python:3.14-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-u", "main.py"]