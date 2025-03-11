from pydantic import BaseModel, EmailStr 


class RegisterUserPayload(BaseModel): 
    UserHasBeenCreated: bool 


class RegisterUser(BaseModel): 
    username: str 
    password: str 
    email: EmailStr | None = None 
    bio: str | None = None 
    age: int | None = None
