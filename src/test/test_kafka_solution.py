import asyncio
import random
import uuid

import aiohttp 

from src.config import settings
from src.products.models import Products
from src.products.service import ProductSevice

product_service = ProductSevice()

async def create_many_product():
    for num_of_product in range(10000):
        await product_service.create(
            Products(
                name=f"product_{num_of_product + random.randint(999, 9999)}", 
                uuid=str(uuid.uuid4()), 
                price=random.uniform(11.5, 77.9), 
                image="image".encode()
            )
        )


async def update_many_product(): 
    products = await product_service.select(projection={"image": 0, "_id": 0}, limit=10000)
    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(settings.USERNAME, settings.PASSWORD) 
        data_to_update = {"description": "Updated description"}
        for num, product in enumerate(products): 
            async with session.put(f"http://127.0.0.1:8000/products/{product['uuid']}", json=data_to_update, auth=auth) as response: 
                status_code = response.status
                print(f"Request result: {status_code}. Count: {num + 1}")
                assert status_code == 200


if __name__ == "__main__": 
    asyncio.run(update_many_product())
