# Flix Challenge
One Paragraph of project description goes here (to be completed)

## Table of contents
* [Getting Started](#getting-started)
* [Project Structure](#project-structure)

## Getting Started
To run the exercise
````
./ci-job.sh
````

To check the output topic
````
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output_topic  --property print.key=true --from-beginning

````
### Prerequisites

What things you need to install the software and how to install them
## Project Structure

## Extras


````
docker exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --list
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic input_topic  --from-beginning
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output_topic  --property print.key=true --from-beginning
````

````
docker-compose down
docker-compose --env-file docker.env up -d

````
https://github.com/wurstmeister/kafka-docker/wiki/Connectivity

docker exec kafka kafka-console-producer.sh --bootstrap-server kafka:9092 --topic input_topic --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" < data/input.json

docker exec app python app/app.py
docker run --network app-tier python:3.11


kafka-topics.sh --bootstrap-server localhost:9093 --list
kafka-topics.sh --create --if-not-exists --bootstrap-server localhost:9093 --partitions 1 --replication-factor 1 --topic input_topic
kafka-topics.sh --create --if-not-exists --bootstrap-server localhost:9093  --partitions 1 --replication-factor 1 --topic output_topic
kafka-console-producer.sh --bootstrap-server localhost:9093 --topic input_topic --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" < data/input.json


kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic output_topic  --property print.key=true --from-beginning


https://github.com/dpkp/kafka-python/issues/1308?tdsourcetag=s_pctim_aiomsg
