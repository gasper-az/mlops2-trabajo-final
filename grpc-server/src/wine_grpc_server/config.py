import os

FEATURE_ORDER = [
    "alcohol", "malic_acid", "ash",
    "alcalinity_of_ash", "magnesium",
    "total_phenols", "flavanoids",
    "nonflavanoid_phenols","proanthocyanins",
    "color_intensity", "hue", "od280_od315",
    "proline"
]

GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))

KAFKA_ALERT_TOPIC: str = os.getenv(
    "KAFKA_ALERT_TOPIC", "wine.security.alerts"
)

KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"
)

KAFKA_TOPIC: str = os.getenv(
    "KAFKA_TOPIC", "wine.inference.events"
)

MLFLOW_TRACKING_URI: str = os.getenv(
    "MLFLOW_TRACKING_URI", "http://localhost:5000"
)

MODEL_NAME:str = os.getenv(
    "MODEL_NAME", "WineClassifier"
)

OOD_HIGH: float = float(os.getenv(
    "OOD_HIGH", 25.0
))

OOD_LOW: float = float(os.getenv(
    "OOD_LOW", 10.0
))

OOD_STATS_PATH: str = os.getenv(
    "OOD_STATS_PATH", "/opt/app/reference/ood_reference_stats.npz"
)