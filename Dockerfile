FROM docker:18.09.2-dind

RUN apk add --update python3 py3-pip make git

RUN pip3 install pika

WORKDIR /work

COPY .make .make
COPY Makefile Makefile
COPY Dockerfile.NODE_11_9_0_ALPINE Dockerfile.NODE_11_9_0_ALPINE
COPY worker.py worker.py

ENTRYPOINT [ "python3", "worker.py" ]
