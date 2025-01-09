from fastapi import Depends, HTTPException, status, Cookie
from typing import Optional, Union
from ..services.user_service import UserService, get_user_service
from ..models.user_model import UserModel, AnonymousUser
from ..core.security import verify_token


async def get_token_from_cookie(
    access_token: Optional[str] = Cookie(None)
) -> Optional[str]:
    if access_token and access_token.startswith('Bearer '):
        return access_token.split(' ')[1]
    return None

async def get_current_user(
    token: str = Depends(get_token_from_cookie),
    service: UserService = Depends(get_user_service)
) -> Union[UserModel, AnonymousUser]:
    if not token:
        return AnonymousUser()
        
    payload = verify_token(token)
    if payload is None:
        return AnonymousUser()
        
    email: str = payload.get("sub")
    if email is None:
        return AnonymousUser()
    
    user = await service.get_by_email(email)
    if user is None:
        return AnonymousUser()
        
    return user