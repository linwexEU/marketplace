from pydantic import BaseModel


class BaseService: 
    client = None
    db = None 
    collection = None

    async def select(self, query: dict | None = None):
        if query: 
            return await self.collection.find(query).to_list() 
        return await self.collection.find().to_list()
    
    def select_one(self, query: dict | None = None): 
        if query:
                return self.collection.find_one(query)
        return self.collection.find_one() 

    async def create(self, document: BaseModel) -> None: 
        doc_to_dict = document.model_dump(exclude_none=True)
        self.collection.insert_one(doc_to_dict)

    async def update(self, query: dict, one: bool = True) -> None:
        if one: 
            return self.collection.update_one(query)
        return self.collection.update_many(query) 
    
    async def delete(self, query: dict, one: bool = True) -> None: 
        if one: 
            return self.collection.delete_one(query) 
        return self.collection.delete_many(query)
