FROM python:alpine3.9

RUN apk add --no-cache curl jq && \
    pip install aiven-client
ADD . /acorn

ENTRYPOINT [ "/acorn/scripts/render.sh" ]