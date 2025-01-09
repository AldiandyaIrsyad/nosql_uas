from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserModel(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    username: str = Field(min_length=3)
    hashed_password: str
    is_authenticated: bool = True
    province: str

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    province: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AnonymousUser(BaseModel):
    is_authenticated: bool = False