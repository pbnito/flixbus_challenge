echo "Ingesting Data"
docker exec -i kafka kafka-console-producer.sh --bootstrap-server $KAFKA_BOOTSTRAP_SERVER --topic input_topic --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" < $INPUT_FILE_PATH
echo "Ingested Data"
