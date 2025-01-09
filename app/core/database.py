from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if not cls.client:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        return cls.client

    @classmethod
    def get_db(cls):
        return cls.get_client()[settings.DATABASE_NAME]