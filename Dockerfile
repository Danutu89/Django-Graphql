FROM python:3.6-slim

RUN mkdir /api
WORKDIR /api

ADD . /api/

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev 

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE ${PORT}

CMD python manange.py runserver 0.0.0.0:${PORT}