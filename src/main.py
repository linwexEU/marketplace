from fastapi import FastAPI

from contextlib import asynccontextmanager

from api import api_router
from logging import configure_logging
from redis.redis_client import RedisClient


@asynccontextmanager 
async def lifespan(app: FastAPI):
    redis_client = RedisClient() 
    redis_client.connect() 
    yield 
    redis_client.disconnet() 


def create_app() -> FastAPI: 
    app = FastAPI(lifespan=lifespan) 
    return app 


app = FastAPI()

# configure the logging format
configure_logging()

# add all API routers
app.include_router(api_router)
