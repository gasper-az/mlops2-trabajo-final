# gRPC server

## local run

```bash
poetry install
poetry run python -m src.server
```

## Docker run

```bash
docker build -t grpc-server .
docker run -p 50051:50051 grpc-server
```
