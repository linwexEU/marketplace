from fastapi import APIRouter

from products.views import router as products_router
from users.views import router as users_router

api_router = APIRouter() 

# Users
api_router.include_router(users_router, prefix="/users", tags=["Users"])


# Products 
api_router.include_router(products_router, prefix="/products", tags=["Products"])
