FROM --platform=$BUILDPLATFORM python:3.7-alpine

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /github/workspace/log

RUN apk add gcc musl-dev make linux-headers

COPY . /opt/raspberry-client

RUN python -m venv /opt/raspberry-client/nfc_env

RUN /opt/raspberry-client/nfc_env/bin/pip install -r /opt/raspberry-client/requirements.txt
