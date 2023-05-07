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
  * [Challenge Explained](#challenge-explained)
    * [Kafka Cluster and App](#1-kafka-cluster-and-app)
    * [Create Input and Output Topic](#2-create-input-and-output-topic)
    * [Populate Input Topic](#3-populate-input-topic)
    * [Python Transformer Application](#4-python-transformer-application)
      * [Application Tests](#application-tests)
    * [Parameterization](#5-parameterization)

## Prerequisites
One needs to have docker installed.

## Project Structure
````css
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
├── env-variables.sh
├── README.md
````

## Challenge
### Run Exercise
To run the exercise:
````shell
./ci-job.sh
````

To check the output's topic content:
````shell
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output_topic  --property print.key=true --from-beginning
````
Clean up:
````shell
docker-compose down
````

### Challenge Commands Walkthrough

#### Environment Variables 
To enhance reusability and ease of use, each step of the challenge is parameterized. 
Therefore, **please make sure that you define the following parameters before executing the exercise**.

````shell
export KAFKA_BOOTSTRAP_SERVER=kafka:9092
export KAFKA_INPUT_TOPIC_NAME=input_topic
export KAFKA_OUTPUT_TOPIC_NAME=output_topic
export INPUT_FILE_PATH=data/input.json
````
Or just run:

````shell
./env_variables.sh
````

#### Kafka Cluster
To start the Kafka Cluster

````shell
docker-compose up -d
````

To stop the Kafka Cluster
````shell
docker-compose down
````
#### Create Kafka Topics and Populate Input Topic
To create the input and output topic:

````shell
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
````shell
./kafka_cli/create_topics.sh
````

To populate the input topic:
````shell
docker exec -i kafka kafka-console-producer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_INPUT_TOPIC_NAME \
    --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" \
    < $INPUT_FILE_PATH
````
Or run:
````shell
./kafka_cli/ingest_data.sh
````

#### Python Transformer Application
Alternatively, one can start the Kafka Cluster without the app:
````shell
docker-compose up -d zookeeper kafka
````
And then start the python application:

````shell
docker-compose up --no-deps app 
````

#### Challenge Output:
To check if the messages were correctly writen to the output topic:
````shell
docker exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic output_topic  --property print.key=true --from-beginning
````

### Challenge Explained
### 1. Kafka Cluster and App

File: [docker-compose.yml](docker-compose.yml)

To provided example was used to setup the local kafka cluster using docker-compose.
To "Dockerize your application, so it can be run with Docker" a container, named app, was added.
This way one can start all containers with docker-compose.

```` dockerfile
app:
  build:
    context: ./local_kafka
    dockerfile: Dockerfile
  container_name: app
  env_file:
    - local_kafka/local_kafka.env
  depends_on:
    - kafka
  networks:
    - app-tier
````
The application was "dockerized" by leveraging the following Dockerfile:
```` dockerfile
FROM python:3.11-alpine

WORKDIR /home

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/app.py"]
````
### 2. Create Input and Output Topic
To create topics, kafka-cli commands were used. To automate the creation process one can also run
the **create_topics.sh** under the local_kafka folder.
File: [create_topics.sh](kafka_cli/create_topics.sh)

Example:
````shell
docker exec kafka kafka-topics.sh \
    --create --if-not-exists \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --partitions 1 --replication-factor 1 \
    --topic $KAFKA_INPUT_TOPIC_NAME
````
### 3. Populate Input Topic
The input data can be found in the **input.json** file under the data folder.
The data is passed to the kafka consumer using the respective kafka-cli command.
File: [ingest_data.sh](kafka_cli/ingest_data.sh)

Example:
````shell
docker exec -i kafka kafka-console-producer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_INPUT_TOPIC_NAME \
    --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" \
    < $INPUT_FILE_PATH
````
### 4. Python Transformer Application

The python application that consume all the messages from
"input_topic", converts the timestamp to UTC and writes the corrected messages to "output_topic".
File: [app.py](local_kafka/app/app.py)

The "handler" is structured as shown in the code block and it: 
* Creates the **app object** that gets and stores the Kafka configurations.
* Creates the Kafka consumer and producer, with the **setup method**.
* Applies the topology (business logic), that is, converts the timestamp to utc, and writes the records to the output topic - **topology method**
* "Closes" all consumers and producers. 
````python
def main():
  """
  Initializes an instance of the App class, sets up the Kafka consumer and producer, and starts the message processing.

  :return: None
  """

  app = App()
  app.setup()
  try:
    app.topology()
  finally:
    app.consumer.close()
    app.producer.close()
    app.producer.flush()

if __name__ == "__main__":
  main()
````
The  _ _ init _ _  method gets and stores the Kafka configurations.

````python
class App:
  """
  Consume and produce messages to/from Kafka topics while converting the timestamp value to UTC timezone.
  """

  def __init__(self):
    """
    Initializes the class instance with the configuration options for Kafka.

    :return: None
    """
    self.config = {
      "BOOTSTRAP_SERVER": os.environ.get("KAFKA_BOOTSTRAP_SERVER", "kafka:9092"),
      "INPUT_TOPIC_NAME": os.environ.get("INPUT_TOPIC_NAME", "input_topic"),
      "OUTPUT_TOPIC_NAME": os.environ.get("OUTPUT_TOPIC_NAME", "output_topic"),
      "AUTO_OFFSET_RESET": os.environ.get("AUTO_OFFSET_RESET", "earliest"),
      "GROUP_ID": os.environ.get("GROUP_ID", "local_kafka_test"),
    }
````
The **setup method** creates the Kafka consumer and producer with the received configurations. 

**Note**: While these objects could have been separated into their own classes for improved reusability, 
it was decided to keep them in the same Python file due to the nature of the exercise.
````python
def setup(self):
  """
  Sets up the Kafka consumer and producer instances with the configuration options.

  :return: None
  """

  self.consumer = KafkaConsumer(
    self.config.get("INPUT_TOPIC_NAME"),
    bootstrap_servers=self.config.get("BOOTSTRAP_SERVER"),
    auto_offset_reset=self.config.get("AUTO_OFFSET_RESET"),
    group_id=self.config.get("GROUP_ID"),
    value_deserializer=lambda m: m.decode("utf-8"),
    api_version=(2, 0, 2),
  )
  """
  When you set api_version the client will not attempt
  to probe brokers for version information."""

  self.producer = KafkaProducer(
    bootstrap_servers=self.config.get("BOOTSTRAP_SERVER"),
    key_serializer=str.encode,
    value_serializer=lambda x: dumps(x).encode("utf-8"),
    api_version=(2, 0, 2),
  )
````
The topology represents the business logic/quality constrains of the exercise.
Topology:
* Read the consumer's records.
* Convert the timestamp from Europe/Berlin to UTC.
* Write the records to the output topic.

**Note**: The writing part (to the output topic) could have separated from the topology. 
Nonetheless, given the exercise's nature the decision was write the records in this method, for simplicity.

````python
def convert_datetime_to_utc(self, timestamp, format="%Y-%m-%dT%H:%M:%S%z"):
  """
  Converts a given timestamp string to a UTC datetime object.

  :param timestamp: A timestamp string in the given format".
  :return: A string representation of the given timestamp in UTC format if the conversion was successful,
           an empty string otherwise.
  """
  try:
    dt_timestamp = datetime.datetime.strptime(timestamp, format)
  except:
    print(f"Found Timestamp with Invalid Format: {timestamp}")
    return ""

  return dt_timestamp.astimezone(pytz_utc).isoformat()

def topology(self):
  """
  Performs the processing of messages from the input Kafka topic, converting the timestamps to UTC format,
  and producing them to the output Kafka topic.

  :return: None
  """

  print("Starting Topology Processing")
  for msg in self.consumer:
    record = loads(msg.value)
    if "myTimestamp" in record:
      timestamp = record.get("myTimestamp")

      if timestamp:
        utc_timestamp = self.convert_datetime_to_utc(timestamp)
        if utc_timestamp:
          record["myTimestamp"] = utc_timestamp
        else:
          print(f"Missed record: Key:{record.get('myKey')} Value: {record}")
          continue

    """
    Assuming that messages with empty timestamps are not filtered out
    One could have decoupled the send part from the topology
    """
    print(f"Sending record: Key:{record.get('myKey')} Value: {record}")
    self.producer.send(
      self.config["OUTPUT_TOPIC_NAME"], key=str(record.get("myKey")), value=record
    )
  print("Finished Topology Processing")
````

#### Application Tests
The application's tests can be found here: [test_local_kafka.py](local_kafka/tests/test_local_kafka.py)


### 5. Parameterization
One can change the following configurations without having to change the docker files and applications.

[env_variables.sh](env_variables.sh)
* KAFKA_BOOTSTRAP_SERVER (ex: kafka:9092)
* KAFKA_INPUT_TOPIC_NAME  (ex: input_topic)
* KAFKA_OUTPUT_TOPIC_NAME (ex: output_topic)
* INPUT_FILE_PATH (ex: data/input.json)

[local_kafka.env](local_kafka/local_kafka.env)
* AUTO_OFFSET_RESET (ex: earliest)
* GROUP_ID (ex: local_kafka)