from ..core.database import Database
from ..models.item_model import ItemModel
from bson import ObjectId
from typing import List

class ItemRepository:
    def __init__(self, database=None):
        self.db = database or Database.get_db()
        self.collection = self.db["items"]

    async def create(self, item: ItemModel) -> str:
        result = await self.collection.insert_one(item.model_dump(exclude={"id"}))
        return str(result.inserted_id)

    async def get_all(self) -> List[ItemModel]:
        pipeline = [
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        documents = await cursor.to_list(length=None)
        return [ItemModel(**doc) for doc in documents]