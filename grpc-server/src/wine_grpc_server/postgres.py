import psycopg2
import os

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_JDBC_URL = os.getenv("POSTGRES_JDBC_URL")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")

def ensure_tables():
    ensure_alerts_table()
    ensure_ood_alerts_table()

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

def ensure_ood_alerts_table():
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
                        CREATE TABLE IF NOT EXISTS ood_alerts (
                            id SERIAL PRIMARY KEY,
                            timestamp TIMESTAMPTZ NOT NULL,
                            score DOUBLE PRECISION NOT NULL,
                            model_name TEXT NOT NULL,
                            severity TEXT NOT NULL,
                            schema_version INTEGER NOT NULL
                        );

                        CREATE INDEX IF NOT EXISTS idx_alert_time
                            on ood_alerts(timestamp);
                        
                        CREATE INDEX IF NOT EXISTS idx_alerts_type
                            on ood_alerts(severity);
                        """)

def persist_ood_alert(score: float, severity: str, model_name: str):
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
                        INSERT INTO ood_alerts
                        (
                            timestamp,
                            score,
                            model_name,
                            severity,
                            schema_version
                        )
                        VALUES (
                            NOW(),
                            %s,
                            %s,
                            %s,
                            1
                        );
                        """,
                        (score, model_name, severity)
                    )
            cur.execute("""
                        INSERT INTO security_alerts
                        (
                            timestamp, alert_type, feature, z_score,
                            variance_ratio, window_start, window_end,
                            model_name, schema_version
                        )
                        VALUES (
                            NOW(), 'ood', 'ALL_FEATURES', %s,
                            0, NULL, NULL,
                            %s, 1
                        );
                        """,
                        (score, model_name)
                    )