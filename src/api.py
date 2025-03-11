from fastapi import APIRouter

from src.users.views import router as users_router

api_router = APIRouter() 

# Users
api_router.include_router(users_router, prefix="/users", tags=["Users"])
