FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY http-api/pyproject.toml http-api/poetry.lock http-api/README.md ./
COPY http-api/src ./src
COPY generated ./generated

RUN poetry install --without dev --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "http_api.main:app", "--host", "0.0.0.0", "--port", "8000"]