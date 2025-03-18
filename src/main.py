from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.api import api_router
from src.logging import configure_logging
from src.redis.redis_client import RedisClient


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
