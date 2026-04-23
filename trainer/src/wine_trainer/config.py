import os

MLFLOW_TRACKING_URI: str = os.getenv(
    "MLFLOW_TRACKING_URI", "http://localhost:5000"
)

EXPERIMENT_NAME: str = os.getenv(
    "MLFLOW_EXPERIMENT_NAME", "wine-classification"
)

MODEL_NAME: str = os.getenv(
    "MODEL_NAME", "WineClassifier"
)

RANDOM_STATE: int = int(os.getenv("RANDOM_STATE", 42))
TEST_SIZE: float = float(os.getenv("TEST_SIZE", 0.2))

OOD_STATS_PATH: str = os.getenv(
    "OOD_STATS_PATH", "/opt/reference/ood_reference_stats.npz"
)