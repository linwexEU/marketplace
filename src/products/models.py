from pydantic import BaseModel 


class Products(BaseModel):
    # Required fields
    name: str 
    price: float
    image: bytes
    
    # Not required fields
    description: str | None = None
    sub_description: str | None = None
