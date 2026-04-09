import json
import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    window,
    avg,
    stddev,
    to_timestamp
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
)

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "wine.inference.events"
ALERT_TOPIC = "wine.security.alerts"

# WINDOW_DURATION = "5 minutes"
# SLIDE_DURATION = "1 minute"
WINDOW_DURATION = "1 minutes"
SLIDE_DURATION = "30 seconds"

DRIFT_Z_THRESHOLD = 3.0 # Drift clasico
POISON_VARIANCE_RATIO = 0.3 # variance collapse threshold
PSI_THRESHOLD = 0.2

REFERENCE_STATS_PATH = "/app/reference/reference_stats.json"

def compute_psi(expected_mean, expected_std, actual_mean):
    if expected_std == 0:
        return 0.0
    return abs((actual_mean - expected_mean)/expected_std)

spark = (
    SparkSession.builder
    .appName("WineDriftDetector")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

#### Carga de features y estadisticas

with open(REFERENCE_STATS_PATH) as f:
    reference_stats = json.load(f)

FEATURES = list(reference_stats.keys())

##### Esquemas de Kafka

features_schema = StructType([
    StructField(f, DoubleType()) for f in FEATURES
])

schema = StructType([
    StructField("event_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("model_name", StringType()),
    StructField("features", features_schema),
    StructField("prediction", IntegerType()),
])

##### Read stream

raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)

parsed_df = (
    raw_df
    .selectExpr("CAST(value AS STRING) as json")
    .select(from_json(col("json"), schema).alias("data"))
    .select("data.*")
    .withColumn("timestamp", to_timestamp(col("timestamp")))
)

for feature in FEATURES:
    parsed_df = parsed_df.withColumn(feature, col(f"features.{feature}"))

##### Windowed aggregation
aggregations = []

for feature in FEATURES:
    aggregations.append(avg(col(feature)).alias(f"{feature}_mean"))
    aggregations.append(stddev(col(feature)).alias(f"{feature}_std"))

windowed_df = (
    parsed_df
    .groupBy(window(col("timestamp"), WINDOW_DURATION, SLIDE_DURATION))
    .agg(*aggregations)
)

# Alertas de Kafka
def publish_alert(alert: dict):
    spark.createDataFrame([alert]).selectExpr(
        "to_json(struct(*)) AS value"
    ).write.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("topic", ALERT_TOPIC) \
    .save()

# Drift detection per microbatch
def detect_drift(batch_df, batch_id):
    rows = batch_df.collect()
    for row in rows:
        for feature, stats in reference_stats.items():
            psi = compute_psi(
                expected_mean=stats["mean"],
                expected_std=stats["std"],
                actual_mean=row[feature]
            )

            if psi > PSI_THRESHOLD:
                print("="*20)
                print(
                    f"DRIFT DETECTADO:\n\tfeature={feature}\n\tPSI={psi:.3f}"
                )

##### Logica de deteccion de drift o data poisoning
def analyze_batch(df, batch_id):
    rows = df.collect()

    for row in rows:
        for feature in FEATURES:
            ref_mean = reference_stats[feature]["mean"]
            ref_std = reference_stats[feature]["std"]
            obs_mean = row[f"{feature}_mean"]
            obs_std = row[f"{feature}_std"]

            # Deteccion de drift mediante z-score
            if ref_std > 0:
                z = abs(obs_mean - ref_mean)/ref_std
            else:
                z = 0

            # Heuristica para detectar data poisoning
            variance_ratio = (
                obs_std / ref_std if ref_std > 0 and obs_std is not None else 1
            )

            if z > DRIFT_Z_THRESHOLD:
                alert = {
                    "feature": feature,
                    "z_score": z,
                    "variance_ratio": variance_ratio,
                    "window_start": row["window"].start.isoformat(),
                    "window_end": row["window"].end.isoformat()
                }
                if variance_ratio < POISON_VARIANCE_RATIO:
                    alert["alert_type"] = "poisoning"
                    print("POISONING!!!!!")
                    publish_alert(alert=alert)
                else:
                    alert["alert_type"] = "drift"
                    print("Drift!!!!!")
                    publish_alert(alert=alert)

query = (
    windowed_df
    .writeStream
    .foreachBatch(analyze_batch)
    .outputMode("update")
    .start()
)

query.awaitTermination()