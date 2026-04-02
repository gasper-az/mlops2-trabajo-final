# Use a stable Python 3.10 slim base
FROM python:3.11-slim

# Set the MLflow version
ARG MLFLOW_VERSION=3.10.1

# Install system dependencies and clean up to keep image small
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install MLflow and common storage/database drivers
RUN pip install --no-cache-dir \
    mlflow==${MLFLOW_VERSION} \
    psycopg2-binary \
    boto3 \
    google-cloud-storage \
    azure-storage-blob

# Expose the default MLflow port
EXPOSE 5000
