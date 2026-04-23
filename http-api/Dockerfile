FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY http-api/pyproject.toml http-api/poetry.lock* ./

COPY http-api/src/ src/

COPY protogen/python protogen/python

ENV PYTHONPATH="/app/protogen/python:/app/src"

RUN poetry install --without dev --no-interaction --no-ansi

EXPOSE 8080

CMD ["uvicorn", "wine_rest_api.main:app", "--host", "0.0.0.0", "--port", "8080"]