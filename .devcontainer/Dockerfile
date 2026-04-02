FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

RUN pip install --no-cache-dir grpcio grpcio-tools protobuf==6.33.6

SHELL ["/bin/bash", "-c"]