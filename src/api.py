from fastapi import APIRouter

from src.products.views import router as products_router
from src.users.views import router as users_router

api_router = APIRouter() 

# Users
api_router.include_router(users_router, prefix="/users", tags=["Users"])


# Products 
api_router.include_router(products_router, prefix="/products", tags=["Products"])
