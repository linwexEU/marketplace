import uuid
from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import StreamingResponse
from fastapi_utils.cbv import cbv 
import io

import json
from redis_utils.redis_client import RedisClient
from auth.views import CurrentUser
from products.models import Products
from products.schemas import CreateProductResponse, GetProducts, UpdateProduct, UpdateProductResponse, DeleteProductResponse
from products.service import ProductSeviceDep 
import logging 
from logger import configure_logging
from config import settings
from utils import SendMessageToKafka 

router = APIRouter()

log = logging.getLogger(__name__)
configure_logging()

@cbv(router) 
class ProductApi: 
    @router.get("/", response_model=list[GetProducts])
    async def get_products(self, product_service: ProductSeviceDep) -> list[GetProducts]: 
        # Get cached uuids 
        async with RedisClient() as redis_client: 
            cached_uuids_json = await redis_client.get(settings.CACHED_UUIDS_KEY)
            if cached_uuids_json: 
                cached_uuids = json.loads(cached_uuids_json) 
            else: 
                cached_uuids = [] 
        
        count_products = await product_service.count()
        products = []

        # Get cached products
        if cached_uuids and len(cached_uuids) == count_products: 
            async with RedisClient() as redis_client:
                cached_products = await redis_client.mget(cached_uuids)
                products = [json.loads(product) for product in cached_products]
        else: 
            # Cache and get products
            products = await product_service.select(projection={"image": 0, "_id": 0})
            cached_uuids = [product["uuid"] for product in products] 

            async with RedisClient() as redis_client: 
                pipeline = redis_client.pipeline() 
                for product in products: 
                    pipeline.set(product["uuid"], json.dumps(product)) 
                pipeline.set(settings.CACHED_UUIDS_KEY, json.dumps(cached_uuids))
                await pipeline.execute() 

        return GetProducts.from_orm(products)
    
    @router.get("/image/{uuid}")
    async def get_product_image(self, uuid: str, product_service: ProductSeviceDep): 
        product = await product_service.select_one({"uuid": uuid})
        return StreamingResponse(io.BytesIO(product["image"]), media_type="image/jpg")

    @router.post("/create", response_model=CreateProductResponse)
    async def create_product(
        self, 
        name: str, 
        price: float,  
        image: UploadFile, 
        product_service: ProductSeviceDep, 
        current_user: CurrentUser,
        description: str | None = None, 
        sub_description: str | None = None,
    ) -> CreateProductResponse: 
        try:
            create_model = Products(name=name, price=price, uuid=str(uuid.uuid4()), image=image.file.read(), description=description, sub_description=sub_description)
            await product_service.create(create_model)
            return CreateProductResponse(ProductHasBeenCreated=True)
        except Exception as ex: 
            log.error("%s" % ex) 
            return CreateProductResponse(ProductHasBeenCreated=False)
    
    @router.put("/{uuid}", response_model=UpdateProductResponse)
    async def update_product(
        self, 
        uuid: str,
        data: UpdateProduct, 
        current_user: CurrentUser, 
        product_service: ProductSeviceDep
    ) -> UpdateProductResponse: 
        try: 
            data_to_dict = data.model_dump(exclude_none=True)

            # Update in db 
            message = {"query": {"uuid": uuid}, "updated_data": {k: v for k, v in data_to_dict.items()}}
            await SendMessageToKafka.send_message_to_kafka(settings.UPDATE_DB_TOPIC, message)
            
            # Update in cache 
            updated_product = await product_service.select_one({"uuid": uuid}, {"image": 0, "_id": 0})
            message = {"uuid": uuid, "updated_product": updated_product}
            await SendMessageToKafka.send_message_to_kafka(settings.UPDATE_CACHE_TOPIC, message)

            return UpdateProductResponse(ProductHasBeenUpdated=True)
        except Exception as ex: 
            log.error("%s" % ex) 
            return UpdateProductResponse(ProductHasBeenUpdated=False)
    
    @router.delete("/{uuid}", response_model=DeleteProductResponse)
    async def delete_product(
        self, 
        uuid: str, 
        current_user: CurrentUser, 
        product_service: ProductSeviceDep
    ) -> DeleteProductResponse: 
        try:
            await product_service.delete({"uuid": uuid})
            return DeleteProductResponse(ProductHasBeenDeleted=True)
        except Exception as ex: 
            log.error("%s"% ex)
            return DeleteProductResponse(ProductHasBeenDeleted=False)
