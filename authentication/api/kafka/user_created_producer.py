from kafka import KafkaProducer
import os
from json import dumps


class KafkaUserCreatedProducer:
    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=[os.getenv("KAFKA_BROKER")],
            value_serializer=lambda x: dumps(x).encode("utf-8"),
            retries=20,
        )
        self._topic = "user-created"

    def send_message(self, message):
        print(message)
        self._producer.send(self._topic, message)


# Run your test suite
