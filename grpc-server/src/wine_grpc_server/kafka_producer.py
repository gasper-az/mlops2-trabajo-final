import json
import uuid
from wine_grpc_server.config  import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC
)
from datetime import datetime, timezone
from kafka import KafkaProducer

def serialize_json(obj):
    return json.dumps(obj).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=serialize_json,
    api_version=(3, 6, 1)
)

def publish_inference_event(
        *,
        model_name: str,
        features: dict,
        prediction: int,
) -> None:
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_name": model_name,
        "features": features,
        "prediction": prediction
    }

    producer.send(KAFKA_TOPIC, event)