FROM python:3.12 AS bet_maker

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
