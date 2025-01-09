from ..core.database import Database
from ..models.user_model import UserModel
from ..core.security import verify_password
from typing import Optional

class UserRepository:
    def __init__(self, database=None):
        self.db = database or Database.get_db()
        self.collection = self.db["users"]

    async def create(self, user: UserModel) -> str:
        result = await self.collection.insert_one(user.model_dump(exclude={"id"}))
        return str(result.inserted_id)

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        pipeline = [
            {"$match": {"email": email}},
            {"$addFields": {"id": {"$toString": "$_id"}}},
            {"$project": {"_id": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        document = await cursor.to_list(length=1)
        if document:
            return UserModel(**document[0])
        return None