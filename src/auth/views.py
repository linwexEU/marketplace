from typing import Annotated

from fastapi import HTTPException, status, Depends 
from fastapi.security import HTTPBasicCredentials, HTTPBasic 

from src.auth.utils import verify_password
from src.users.service import UserServiceDep
from src.users.models import Users

security = HTTPBasic()


async def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)], users_service: UserServiceDep): 
    # Get info from credentials
    username = credentials.username 
    password = credentials.password

    # Get user's hashed_password
    user = await users_service.select_one({"username": username})

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Basic"}
        )

    # Check password 
    if not verify_password(password, user["hashed_password"]): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Basic"}
        )
    
    return Users(**user)


CurrentUser = Annotated[Users, Depends(get_current_user)]
