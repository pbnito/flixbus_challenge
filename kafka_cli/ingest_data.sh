echo "Ingesting Data"
kafka-console-producer.sh --bootstrap-server $BOOTSTRAP_SERVER --topic input_topic --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" < $INPUT_FILE_PATH
echo "Ingested Data"
