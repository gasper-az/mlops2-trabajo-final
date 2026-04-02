import mlflow.pyfunc
from wine_grpc_server.config import (
    MLFLOW_TRACKING_URI,
    MODEL_NAME
)

def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = f"models:/{MODEL_NAME}/latest"
    model = mlflow.pyfunc.load_model(model_uri)

    return model