# Flix Challenge
This project aims to solve the Flix Challenge.

## Table of contents
* [Prerequisites](#prerequisites)
* [Project Structure](#project-structure)
* [Challenge](#challenge)
  * [Run Exercise](#run-exercise)
  * [Challenge Commands Walktrough](#challenge-commands-walkthrough)
    * [Environment Variables](#environment-variables)
    * [Kafka Cluster](#kafka-cluster)
    * [Create Kafka Topics and Populate Input Topic](#create-kafka-topics-and-populate-input-topic) 
    * [Python Transformer Application](#python-transformer-application)
    * [Challenge Output](#challenge-output)
* [Final Remarks](#final-remarks) 

## Prerequisites
One needs to have docker installed.

## Project Structure
````
├── code_challenge
│   ├── coding_challenge_additional_notes.pdf
│   └── coding_challenge_data_engineer.pdf

├── data
│   └── input.json

├── kafka_cli
│   ├── create_topics.sh
│   └── ingest_data.sh

├── local_kafka
│   ├── Dockerfile
│   ├── local_kafka.env
│   ├── requirements
│   ├── app
│   │    ├── __init__.py
│   │    └── app.py
│   └── tests
│        ├── __init__.py
│        └── test_local_kafka.py

├── ci-job.sh
├── docker-compose.yml
├── environment-variables.sh
├── README.md
````

## Challenge
### Run Exercise
To run the exercise:
````
./ci-job.sh
````

To check the output's topic content:
````
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output_topic  --property print.key=true --from-beginning
````

### Challenge Commands Walkthrough

#### Environment Variables 
To enhance reusability and ease of use, each step of the challenge is parameterized. 
Therefore, **please make sure that you define the following parameters before executing the exercise**.

````
export KAFKA_BOOTSTRAP_SERVER=kafka:9092
export KAFKA_INPUT_TOPIC_NAME=input_topic
export KAFKA_OUTPUT_TOPIC_NAME=output_topic
export INPUT_FILE_PATH=data/input.json
````
Or just run:

````
./environment_variables.sh
````

#### Kafka Cluster
To start the Kafka Cluster

````
docker-compose up -d
````

To stop the Kafka Cluster
````
docker-compose down
````
#### Create Kafka Topics and Populate Input Topic
To create the input and output topic:

````
docker exec kafka kafka-topics.sh \
    --create --if-not-exists \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --partitions 1 --replication-factor 1 \
    --topic $KAFKA_INPUT_TOPIC_NAME

docker exec kafka kafka-topics.sh \
    --create --if-not-exists \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --partitions 1 --replication-factor 1 \
    --topic $KAFKA_OUTPUT_TOPIC_NAME
````
Alternatively, one can run:
````
./kafka_cli/create_topics.sh
````

To populate the input topic:
````
docker exec -i kafka kafka-console-producer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_INPUT_TOPIC_NAME \
    --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" \
    < $INPUT_FILE_PATH
````
Or run:
````
./kafka_cli/ingest_data.sh
````

#### Python Transformer Application
To run the python application that consumes all the messages from
"input_topic" and write the corrected messages to "output_topic:
````
docker run -d --env-file local_kafka/local_kafka.env app
````

To stop the app:
````
docker stop app
docker rm app
````

#### Challenge Output:
To check if the messages were correctly writen to the output topic:
````
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output_topic  --property print.key=true --from-beginning
````

### Challenge Explained






## Final Remarks
