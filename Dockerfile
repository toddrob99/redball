FROM python:3.8.3-alpine

LABEL Name=redball Version=0.0.7

WORKDIR /app
ADD . /app

EXPOSE 8087

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev
RUN python3 -m pip install -r requirements.txt
RUN apk del .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev
RUN apk add tzdata

CMD ["python3", "redball.py"]
