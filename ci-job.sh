#!/bin/sh
echo "Tests"
pytest local_kafka/tests/test_local_kafka.py

echo "Loading Envirnment"
source env_variables.sh

echo "Starting Kafka Cluster and Application"
docker-compose down
docker-compose up -d
echo "Started Kafka Cluster and Application"

sleep 5
source kafka_cli/create_topics.sh
source kafka_cli/ingest_data.sh