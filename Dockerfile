FROM python:3.11.6-alpine3.17

RUN pip install aiogram

WORKDIR /app

COPY main.py ./

ENTRYPOINT python -u main.py