import os

GRPC_SERVER_HOST = os.getenv("GRPC_SERVER_HOST", "grpc-server")
GRPC_SERVER_PORT = os.getenv("GRPC_SERVER_PORT", "50051")