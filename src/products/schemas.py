from pydantic import BaseModel 


class CreateProductResponse(BaseModel): 
    ProductHasBeenCreated: bool 


class GetProducts(BaseModel): 
    name: str 
    uuid: str
    price: float 
    description: str | None = None
    sub_description: str | None = None

    @staticmethod 
    def from_orm(products) -> "list[GetProducts]":
        result = [] 
        for item in products: 
            result.append(
                GetProducts(
                    name=item.get("name"), 
                    uuid=item.get("uuid"), 
                    price=item.get("price"), 
                    description=item.get("description"), 
                    sub_description=item.get("sub_description")
                )
            )
        return result 


class UpdateProduct(BaseModel): 
    name: str | None = None
    price: str | None = None
    description: str | None = None
    sub_description: str | None = None 


class UpdateProductResponse(BaseModel): 
    ProductHasBeenUpdated: bool 


class DeleteProductResponse(BaseModel): 
    ProductHasBeenDeleted: bool 
