FROM python:3.11-slim-buster

LABEL Name=redball Version=1.0.0

WORKDIR /app
ADD . /app

EXPOSE 8087

ARG DEBIAN_FRONTEND=noninteractive

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN apt-get install -y tzdata

CMD ["python3", "redball.py"]
