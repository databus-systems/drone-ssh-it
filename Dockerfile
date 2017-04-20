FROM python:3.5-alpine

LABEL maintainer "Costin Bleotu <costin.bleotu@databus.systems>"

RUN set -ex \
        && apk add --no-cache \
            ca-certificates \
            libffi \
            openssl \
        \
        && apk add --no-cache --virtual .build-dependencies \
            python3-dev\
            gcc \
            musl-dev \
            libffi-dev \
            openssl-dev \
        \
        && pip install --no-cache-dir --upgrade \
            paramiko \
        \
        && apk del .build-dependencies

ADD run_ssh.py /usr/bin/

CMD ["python3", "/usr/bin/run_ssh.py"]