import json
import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    window,
    avg,
    to_timestamp
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
    TimestampType,
)

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "wine.inference.events"

WINDOW_DURATION = "5 minutes"
SLIDE_DURATION = "1 minute"

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

with open(REFERENCE_STATS_PATH) as f:
    reference_stats = json.load(f)

features_schema = StructType([
    StructField("alcohol", DoubleType()),
    StructField("malic_acid", DoubleType()),
    StructField("ash", DoubleType()),
    StructField("alcalinity_of_ash", DoubleType()),
    StructField("magnesium", DoubleType()),
    StructField("total_phenols", DoubleType()),
    StructField("flavanoids", DoubleType()),
    StructField("nonflavanoid_phenols", DoubleType()),
    StructField("proanthocyanins", DoubleType()),
    StructField("color_intensity", DoubleType()),
    StructField("hue", DoubleType()),
    StructField("od280_od315", DoubleType()),
    StructField("proline", DoubleType()),
])

schema = StructType([
    StructField("event_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("model_name", StringType()),
    StructField("features", features_schema),
    StructField("prediction", IntegerType()),
])

raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)

# parsed_df = (
#     raw_df
#     .selectExpr("CAST(value AS STRING) as json")
#     .select(from_json(col("json"), schema).alias("data"))
#     .select("data.*")
#     .withColumn("timestamp", col("timestamp").cast(TimestampType))
# )

parsed_df = (
    raw_df
    .selectExpr("CAST(value AS STRING) as json")
    .select(from_json(col("json"), schema).alias("data"))
    .select("data.*")
    .withColumn("timestamp", to_timestamp(col("timestamp")))
)

# Flatten de features
for feature in reference_stats.keys():
    parsed_df = parsed_df.withColumn(feature, col(f"features.{feature}"))

# Windowed aggregation
agg_exprs = [
    avg(col(feature)).alias(feature)
    for feature in reference_stats.keys()
]

windowed_df = (
    parsed_df
    .groupBy(window(col("timestamp"), WINDOW_DURATION, SLIDE_DURATION))
    .agg(*agg_exprs)
)

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

query = (
    windowed_df
    .writeStream
    .foreachBatch(detect_drift)
    .outputMode("update")
    .start()
)

query.awaitTermination()