import json
import os
from alerts import Alert
from datetime import timezone
from config import (
    ALERT_TOPIC,
    DRIFT_Z_THRESHOLD,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    MODEL_NAME,
    POISON_VARIANCE_RATIO,
    POSTGRES_JDBC_URL,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    REFERENCE_STATS_PATH,
    SLIDE_DURATION,
    WINDOW_DURATION
)
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    from_json,
    stddev,
    to_timestamp,
    to_json,
    struct,
    window,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
)

spark = (
    SparkSession.builder
    .appName("WineDriftAndPoisoningDetector")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

#### Carga de features y estadisticas
with open(REFERENCE_STATS_PATH, "r") as f:
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

windowed_stats_df = (
    parsed_df
    .groupBy(window(col("timestamp"), WINDOW_DURATION, SLIDE_DURATION))
    .agg(*aggregations)
)

def publish_alert_to_kafka_topic(alerts):
    if not alerts:
        return
    
    df = spark.createDataFrame(alerts)

    df \
        .select(to_json(struct(*df.columns)).alias("value")) \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("topic", ALERT_TOPIC) \
        .save()

def write_alerts_to_postgres(alerts):
    if not alerts:
        return
    
    df = spark.createDataFrame(alerts)

    df.write \
        .format("jdbc") \
        .option("url", POSTGRES_JDBC_URL) \
        .option("dbtable", "security_alerts") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .option("batchsize", "1000") \
        .option("isolationLevel", "READ_COMMITTED") \
        .option("truncate", "false") \
        .mode("append") \
        .save()

def generate_alerts_and_persist(batch_df, batch_id):
    if batch_df.rdd.isEmpty():
        return
    
    rows = batch_df.collect()
    alerts = []

    for row in rows:
        for feature in FEATURES:
            mean = row[f"{feature}_mean"]
            std = row[f"{feature}_std"]
            w_start = row.window.start.replace(tzinfo=timezone.utc)
            w_end = row.window.end.replace(tzinfo=timezone.utc)

            reference = reference_stats.get(feature)

            if not reference:
                continue

            reference_mean = reference["mean"]
            reference_std = reference["std"]

            if reference_std <= 0:
                continue

            # Detector de Data Drifting
            z = abs(mean - reference_mean)/reference_std

            # Heuristica para detectar data poisoning
            variance_ratio = (
                std / reference_std if reference_std > 0 and std is not None else 1
            )

            if z > DRIFT_Z_THRESHOLD:
                alert = Alert(
                    timestamp=Alert.now_iso(),
                    alert_type="drift",
                    feature=feature,
                    z_score=float(z),
                    variance_ratio=variance_ratio,
                    window_start=w_start,
                    window_end=w_end,
                    model_name=MODEL_NAME
                )

                print("="*80)
                print(f"Alerta: {alert}")
                print("="*80)
                
                if variance_ratio < POISON_VARIANCE_RATIO:
                    alert.alert_type = "poisoning"

                alerts.append(alert)
        
    if not alerts:
        return
    
    write_alerts_to_postgres(alerts=alerts)
    publish_alert_to_kafka_topic(alerts=alerts)

query = (
    windowed_stats_df
    .writeStream
    .foreachBatch(generate_alerts_and_persist)
    .outputMode("update")
    .start()
)

query.awaitTermination()