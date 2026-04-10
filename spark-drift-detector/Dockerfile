FROM apache/spark:3.5.1

USER root
WORKDIR /opt/app

RUN curl -L -o /opt/spark/jars/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

RUN pip install psycopg2-binary

COPY spark-drift-detector /opt/app/spark-drift-detector

CMD ["/opt/spark/bin/spark-submit", "--master", "local[*]","--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "/opt/app/spark-drift-detector/drift_detector.py"]