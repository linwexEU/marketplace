from pydantic import BaseModel


class BaseService: 
    client = None
    db = None 
    collection = None

    async def select(self, query: dict | None = None, projection: dict | None = None, limit: int = 20):
        if query: 
            if projection:
                return await self.collection.find(query, projection).limit(limit).to_list() 
            return await self.collection.find(query).limit(limit).to_list()

        if projection:
            return await self.collection.find({}, projection).limit(limit).to_list()
        return await self.collection.find().limit(limit).to_list()
    
    def select_one(self, query: dict | None = None, projection: dict | None = None): 
        if query: 
            if projection:
                return self.collection.find_one(query, projection)
            return self.collection.find_one(query)

        if projection:
            return self.collection.find_one({}, projection)
        return self.collection.find_one()

    async def create(self, document: BaseModel) -> None: 
        doc_to_dict = document.model_dump(exclude_none=True)
        self.collection.insert_one(doc_to_dict)

    async def update(self, query: dict, data: dict, one: bool = True) -> None:
        if one: 
            return self.collection.update_one(query, data)
        return self.collection.update_many(query, data) 
    
    async def delete(self, query: dict, one: bool = True) -> None: 
        if one: 
            return self.collection.delete_one(query) 
        return self.collection.delete_many(query)

    async def count(self, query: dict = {}) -> int: 
        return await self.collection.count_documents(query) 
