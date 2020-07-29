FROM tiangolo/uvicorn-gunicorn:python3.7

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir cloudant

COPY ./taketwo-webapi /app