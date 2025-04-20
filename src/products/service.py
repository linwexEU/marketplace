from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient 

from config import settings
from db.base import BaseService


class ProductSevice(BaseService): 
    client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    db = client.database  
    collection = db.products


ProductSeviceDep = Annotated[BaseService, Depends(ProductSevice)]
