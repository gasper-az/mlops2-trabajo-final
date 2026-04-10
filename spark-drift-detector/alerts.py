from dataclasses import dataclass
from datetime import datetime, timezone

ALERT_SCHEMA_VERSION = 1

@dataclass
class Alert:
    timestamp: str
    alert_type: str
    feature: str
    z_score: float
    variance_ratio: float
    window_start: str
    window_end: str
    model_name: str
    schema_version: int = ALERT_SCHEMA_VERSION

    @staticmethod
    def now_iso():
        return datetime.now(timezone.utc)