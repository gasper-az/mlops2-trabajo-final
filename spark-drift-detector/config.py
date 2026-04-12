import psycopg2
import os

ALERT_TOPIC: str = os.getenv(
    "KAFKA_ALERT_TOPIC", "wine.security.alerts"
)

DRIFT_Z_THRESHOLD: float = float(os.getenv(
    "DRIFT_Z_THRESHOLD", 3.0
))

KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"
)

KAFKA_TOPIC: str = os.getenv(
    "KAFKA_TOPIC", "wine.inference.events"
)

MODEL_NAME:str = os.getenv(
    "MODEL_NAME", "WineClassifier"
)

POISON_VARIANCE_RATIO: float = float(os.getenv(
    "POISON_VARIANCE_RATIO", 0.3 # variance collapse threshold
))

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_JDBC_URL = os.getenv("POSTGRES_JDBC_URL")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")

REFERENCE_STATS_PATH:str = os.getenv(
    "REFERENCE_STATS_PATH", "/opt/app/reference/reference_stats.json"
)

SLIDE_DURATION:str = os.getenv(
    "SLIDE_DURATION", "10 minutes"
)

WINDOW_DURATION:str = os.getenv(
    "WINDOW_DURATION", "1 minutes"
)