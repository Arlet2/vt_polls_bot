FROM python:3.11.6-alpine3.17

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt
RUN mkdir bingo_img

ENTRYPOINT python -u main.py