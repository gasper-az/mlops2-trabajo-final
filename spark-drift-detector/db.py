import psycopg2
import os

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_JDBC_URL = os.getenv("POSTGRES_JDBC_URL")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")

def ensure_alerts_table():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS security_alerts (
                            id SERIAL PRIMARY KEY,
                            timestamp TIMESTAMPTZ NOT NULL,
                            alert_type TEXT NOT NULL,
                            feature TEXT NOT NULL,
                            z_score DOUBLE PRECISION NOT NULL,
                            variance_ratio DOUBLE PRECISION NOT NULL,
                            window_start TIMESTAMPTZ,
                            window_end TIMESTAMPTZ,
                            model_name TEXT NOT NULL,
                            schema_version INTEGER NOT NULL
                        );

                        CREATE INDEX IF NOT EXISTS idx_alert_time
                            on security_alerts(timestamp);
                        
                        CREATE INDEX IF NOT EXISTS idx_alerts_type
                            on security_alerts(alert_type);
                        """)