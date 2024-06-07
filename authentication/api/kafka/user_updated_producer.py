from kafka import KafkaProducer
import os
from json import dumps


class KafkaUserDeletedProducer:
    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=[os.getenv("KAFKA_BROKER")],
            value_serializer=lambda x: dumps(x).encode("utf-8"),
            retries=20,
        )
        self._topic = "user-deleted"

    def send_message(self, message):
        print(message)
        self._producer.send(self._topic, message)
