from src.broker.producer import KafkaProducerClient


class SendMessageToKafka: 
    @staticmethod 
    async def send_message_to_kafka(topic: str, message: dict) -> None: 
        async with KafkaProducerClient(topic) as producer: 
            await producer.send_message(message)
