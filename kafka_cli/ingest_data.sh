echo "Ingesting Data"

docker exec -i kafka kafka-console-producer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_INPUT_TOPIC_NAME \
    --property "value.serializer=org.apache.kafka.common.serialization.StringSerializer" \
    < $INPUT_FILE_PATH
echo "Ingested Data"
