from fastapi import Depends
from db.base import BaseService 
from motor.motor_asyncio import AsyncIOMotorClient 
from config import settings 
from typing import Annotated
from db.base import BaseService


class UsersService(BaseService): 
    client = AsyncIOMotorClient(settings.MONGO_DB_URL) 
    db = client.database 
    collection = db.users 


UserServiceDep = Annotated[BaseService, Depends(UsersService)]
