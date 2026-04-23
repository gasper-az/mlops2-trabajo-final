FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY graphql-api/pyproject.toml graphql-api/poetry.lock* ./

COPY graphql-api/src/ src/

ENV PYTHONPATH="/app/src"

RUN poetry install --without dev --no-interaction --no-ansi

EXPOSE 8090

CMD ["uvicorn", "wine_graphql_api.main:app", "--host", "0.0.0.0", "--port", "8090"]
