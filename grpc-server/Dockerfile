FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY grpc-server/pyproject.toml grpc-server/poetry.lock* ./

COPY grpc-server/src/ src/

COPY protogen/python /app/protogen/python

ENV PYTHONPATH="/app/protogen/python:/app/src"

RUN poetry install --without dev --no-interaction --no-ansi

ENTRYPOINT ["python", "-m", "wine_grpc_server.main"]