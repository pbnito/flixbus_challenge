#!/bin/sh
echo "Tests"
pytest local_kafka/tests/test_local_kafka.py

echo "Loading Envirnment"
source environment_variables.sh

echo "Starting docker-compose"
docker-compose up -d
echo "docker-compose finished"

sleep 5
source kafka_cli/create_topics.sh
source kafka_cli/ingest_data.sh

docker run -d --env-file local_kafka/local_kafka.env app
sleep 5

echo "Cleaning up"
docker-compose down
docker stop app
docker rm app ##TODO check this

echo "The End"
