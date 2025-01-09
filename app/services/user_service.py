from fastapi import Depends, HTTPException
from ..repositories.user_repository import UserRepository
from ..models.user_model import UserModel, UserCreate
from ..models.token_model import Token
from ..core.security import get_password_hash, verify_password, create_access_token

class UserService:
    def __init__(self, repository: UserRepository = None):
        self.repository = repository or UserRepository()

    async def register(self, user_data: UserCreate) -> str:
        if await self.repository.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user_data.password)
        user = UserModel(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            province=user_data.province
        )
        return await self.repository.create(user)
    
    async def authenticate(self, email: str, password: str) -> Token:
        user = await self.repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = create_access_token({"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")

    async def get_by_email(self, email: str) -> UserModel:
        return await self.repository.get_by_email(email)
        
def get_user_service():
    return UserService()