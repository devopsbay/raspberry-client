FROM --platform=${TARGETPLATFORM} python:3.7-alpine

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

RUN apk add gcc musl-dev make linux-headers

COPY . /opt/door-system

RUN python -m venv /opt/door-system/nfc_venv

RUN /opt/door-system/nfc_venv/bin/pip install -r /opt/door-system/requirements.txt
