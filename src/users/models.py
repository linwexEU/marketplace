from pydantic import BaseModel, EmailStr 


class Users(BaseModel): 
    # Required fields
    username: str 
    uuid: str
    hashed_password: str 

    # Not required fields 
    email: EmailStr | None = None 
    bio: str | None = None 
    age: int | None = None
