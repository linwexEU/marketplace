import logging
from typing import Any 
from redis.asyncio import Redis as AsyncRedis
import asyncio 

log = logging.getLogger(__name__) 


class RedisClient: 
    def __init__(self): 
        self.client: AsyncRedis | None = None 

    async def connect(self) -> None: 
        log.info("Conecting to Redis...")
        await self._connect_async_redis() 
        log.info("Redis connected!")

    async def _connect_async_redis(self) -> None: 
        self.client = AsyncRedis.from_url("redis://localhost:6379")

        tries_count = 1 
        while True: 
            tries_count += 1 
            try: 
                await self.client.ping() 
                break 
            except Exception as ex: 
                log.warning("Can't connecto to Redis: %s" % ex)

            if tries_count >= 5: 
                raise Exception("Can't connecto to Redis")
            await asyncio.sleep(1) 

    async def disconnet(self) -> None: 
        if self.client: 
            await self.client.aclose() 
            log.warning("Redis disconnected!")

    async def __aenter__(self) -> "RedisClient": 
        await self.connect() 
        return self.client 
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: 
        await self.disconnet() 
