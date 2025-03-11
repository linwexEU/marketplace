from fastapi import APIRouter 
from fastapi_utils.cbv import cbv
import logging

from src.auth.utils import get_password_hash
from src.users.models import Users
from src.users.schemas import RegisterUser, RegisterUserPayload
from src.users.service import UserServiceDep

router = APIRouter() 
log = logging.getLogger(__name__)


@cbv(router) 
class UsersAPI: 
    @router.post("/register/", response_model=RegisterUserPayload)
    async def register_user(self, user_data: RegisterUser, users_service: UserServiceDep) -> RegisterUserPayload: 
        try:
            hashed_password = get_password_hash(user_data.password)
            await users_service.create(
                Users(username=user_data.username, hashed_password=hashed_password, 
                      email=user_data.email, bio=user_data.bio, age=user_data.age)
            )
        except Exception as ex: 
            log.error("%s" % ex)
            return RegisterUserPayload(UserHasBeenCreated=False)
        return RegisterUserPayload(UserHasBeenCreated=True)
