FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY grpc-server/pyproject.toml grpc-server/poetry.lock grpc-server/README.md ./
COPY grpc-server/src ./src
COPY generated ./generated

RUN poetry install --without dev --no-interaction --no-ansi

EXPOSE 50051

CMD ["python", "-m", "grpc_server.server"]