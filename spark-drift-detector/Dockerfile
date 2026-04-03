FROM spark:3.5.1

USER root

WORKDIR /app

COPY spark-drift-detector/drift_detector.py /app/drift_detector.py

COPY reference/reference_stats.json /app/reference/reference_stats.json

CMD ["/opt/spark/bin/spark-submit", "--master", "local[*]","--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "/app/drift_detector.py"]