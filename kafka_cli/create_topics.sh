#!/bin/sh
echo "Begin creating topics"
docker exec kafka kafka-topics.sh --create --if-not-exists --bootstrap-server $KAFKA_BOOTSTRAP_SERVER --partitions 1 --replication-factor 1 --topic $KAFKA_INPUT_TOPIC_NAME
docker exec kafka kafka-topics.sh --create --if-not-exists --bootstrap-server $KAFKA_BOOTSTRAP_SERVER --partitions 1 --replication-factor 1 --topic $KAFKA_OUTPUT_TOPIC_NAME
echo "Done creating topics"