import asyncio
import json 
import logging
import sys 

from aiokafka import AIOKafkaConsumer 

from src.config import settings
from src.products.service import ProductSevice
from src.redis.redis_client import RedisClient

log = logging.getLogger(__name__)


class KafkaConsumerClient: 
    def __init__(self, topic: str): 
        self.topic = topic 
        self.consumer = AIOKafkaConsumer(
            self.topic, 
            bootstrap_servers="localhost:9092", 
            auto_offset_reset="latest",
            enable_auto_commit=True, 
            value_deserializer=self.json_deserializer
        )

        self.product_service = ProductSevice()

    def json_deserializer(self, message: bytes): 
        return json.loads(message.decode("utf-8")) 

    async def consume_message(self): 
        await self.consumer.start() 
        log.info("[KAFKA] Start consuming...")
        try:
            async for message in self.consumer: 
                match self.topic: 
                    case settings.UPDATE_DB_TOPIC: 
                        log.info(f"[KAFKA] Consume message for {settings.UPDATE_DB_TOPIC}")
                        query = message.value["query"] 
                        updated_data = {"$set": message.value["updated_data"]}
                        try:
                            await self.product_service.update(query, updated_data)
                        except Exception as ex: 
                            log.error("[KAFKA] Error while updating db: %s" % ex) 
                        log.info("[KAFKA] Updated product in db")
                    case settings.UPDATE_CACHE_TOPIC: 
                        log.info(f"[KAFKA] Consume message for {settings.UPDATE_CACHE_TOPIC}")
                        uuid = message.value["uuid"]
                        updated_product = message.value["updated_product"]

                        try:
                            async with RedisClient() as redis_client: 
                                await redis_client.set(uuid, json.dumps(updated_product))
                        except Exception as ex: 
                            log.error("[KAFKA] Error while updating cache: %s" % ex) 
                        log.info("[KAFKA] Updated product in cache")
        finally: 
            await self.consumer.stop()

    async def __aenter__(self) -> "KafkaConsumerClient": 
        return self 
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: 
        await self.consumer.stop() 


async def run_consumer() -> None: 
    topic = sys.argv[1:][0]
    async with KafkaConsumerClient(topic) as consumer: 
        await consumer.consume_message() 


if __name__ == "__main__": 
    asyncio.run(run_consumer()) 
