from fastapi import Depends
from ..repositories.item_repository import ItemRepository
from ..models.item_model import ItemModel
from typing import List

class ItemService:
    def __init__(self, repository: ItemRepository = None):
        self.repository = repository or ItemRepository()

    async def create_item(self, item: ItemModel) -> str:
        return await self.repository.create(item)

    async def get_items(self) -> List[ItemModel]:
        return await self.repository.get_all()

def get_item_service():
    return ItemService()