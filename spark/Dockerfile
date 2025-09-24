FROM openjdk:11-jre-slim

ENV SPARK_VERSION=3.4.4
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y curl procps dos2unix && apt-get clean

# Python 설치
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# kafka-python 설치. python과 kafka가 통신하기 위한 라이브러리
RUN pip3 install --no-cache-dir kafka-python

# 로컬에서 다운로드해 놓은 Spark 바이너리 복사
COPY spark-3.4.4-bin-hadoop3 /opt/spark

# Iceberg + Kafka + Hadoop AWS JAR 추가 (2025.09.15 추가) 
ENV ICEBERG_VERSION=1.9.2
RUN curl -L -o /opt/spark/jars/iceberg-spark-runtime-${SPARK_VERSION}_2.12-${ICEBERG_VERSION}.jar \
        https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.4_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-3.4_2.12-${ICEBERG_VERSION}.jar && \
    curl -L -o /opt/spark/jars/spark-sql-kafka-0-10_2.12-${SPARK_VERSION}.jar \
        https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/${SPARK_VERSION}/spark-sql-kafka-0-10_2.12-${SPARK_VERSION}.jar && \
    curl -L -o /opt/spark/jars/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar \
        https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/${SPARK_VERSION}/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar && \
    curl -L -o /opt/spark/jars/kafka-clients-3.4.1.jar \
        https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.1/kafka-clients-3.4.1.jar && \
    curl -L -o /opt/spark/jars/hadoop-aws-3.3.4.jar \
        https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -L -o /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar \
        https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

# 쉘 스크립트 라인 엔딩 변환 + 실행 권한 부여
RUN dos2unix /opt/spark/sbin/*.sh /opt/spark/bin/*.sh && \
    chmod +x /opt/spark/sbin/*.sh /opt/spark/bin/*.sh

ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

WORKDIR /opt/spark

CMD ["/bin/bash"]
