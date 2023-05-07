# -*- coding: utf-8 -*-
import os
import datetime
from pytz import utc as pytz_utc
from json import loads, dumps
from kafka import KafkaConsumer, KafkaProducer


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
            "BOOTSTRAP_SERVER": os.environ.get("BOOTSTRAP_SERVER", "kafka:9092"),
            "INPUT_TOPIC_NAME": os.environ.get("INPUT_TOPIC_NAME", "input_topic"),
            "OUTPUT_TOPIC_NAME": os.environ.get("OUTPUT_TOPIC_NAME", "output_topic"),
            "AUTO_OFFSET_RESET": os.environ.get("AUTO_OFFSET_RESET", "earliest"),
            "GROUP_ID": os.environ.get("GROUP_ID", "local_kafka_test"),
        }
        print("Broker: ", self.config.get("BOOTSTRAP_SERVER"))

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
