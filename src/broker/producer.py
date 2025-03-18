import json
import logging

from aiokafka import AIOKafkaProducer 

log = logging.getLogger(__name__) 


class KafkaProducerClient: 
    def __init__(self, topic: str): 
        self.producer = AIOKafkaProducer(
            bootstrap_servers="localhost:9092", 
            value_serializer=self.json_serializer, 
            enable_idempotence=True
        )
        self.topic=topic

    def json_serializer(self, message: dict) -> bytes: 
        return json.dumps(message).encode("utf-8")

    async def send_message(self, message: dict): 
        await self.producer.start() 
        try:
            await self.producer.send(self.topic, message) 
            log.info("[KAFKA] Message was send to Kafka")
        finally: 
            await self.producer.stop() 

    async def __aenter__(self) -> "KafkaProducerClient": 
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None: 
        return await self.producer.stop() 
