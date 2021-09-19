FROM python:3.9-alpine

LABEL Name=redball Version=1.0.0

WORKDIR /app
ADD . /app

EXPOSE 8087

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev rust cargo
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN apk del .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev rust cargo
RUN apk add tzdata

CMD ["python3", "redball.py"]
