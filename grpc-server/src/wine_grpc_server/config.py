import os

MLFLOW_TRACKING_URI: str = os.getenv(
    "MLFLOW_TRACKING_URI", "http://localhost:5000"
)

MODEL_NAME:str = os.getenv(
    "MODEL_NAME", "WineClassifier"
)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))