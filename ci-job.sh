#!/bin/sh
echo "Tests"
pytest local_kafka/tests/test_local_file.py

echo "Loading Envirnment"
export BOOTSTRAP_SERVER=localhost:9093
export KAFKA_BOOTSTRAP_SERVER=kafka:9092
export KAFKA_INPUT_TOPIC_NAME=input_topic
export KAFKA_OUTPUT_TOPIC_NAME=output_topic
export INPUT_FILE_PATH=data/input.json

echo "Starting docker-compose"
docker-compose down
docker-compose up -d
echo "docker-compose finished"

sleep 5
source kafka_cli/create_topics.sh
source kafka_cli/ingest_data.sh

docker run -d --env-file local_kafka/local_kafka.env app
sleep 5
docker stop app
echo "The End"
