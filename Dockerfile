FROM python:alpine3.7

LABEL Name=redball Version=0.0.4

WORKDIR /app
ADD . /app

EXPOSE 8087

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev
RUN python3 -m pip install -r requirements.txt
RUN apk del .build-deps gcc musl-dev libffi-dev openssl-dev python3-dev
RUN apk add tzdata

CMD ["python3", "redball.py"]
