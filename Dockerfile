FROM --platform=${TARGETPLATFORM} python:3.7-alpine AS builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

RUN apk add gcc musl-dev make linux-headers

COPY . /opt/raspberry-client

RUN python -m venv /opt/raspberry-client/nfc_env

RUN /opt/raspberry-client/nfc_env/bin/pip install -r /opt/raspberry-client/requirements.txt

FROM --platform=${BUILDPLATFORM} buildpack-deps:buster AS builder

COPY --from=builder /opt/raspberry-client /opt/test
