from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi import Depends, Request, HTTPException, status
from typing import Optional
from uuid import UUID
from app.models.models import User
from app.database import get_user_db,get_user_by_identifier
from app.config import SECRET
from fastapi_users.manager import BaseUserManager, UUIDIDMixin



from fastapi_users.manager import BaseUserManager
from fastapi_users.password import PasswordHelper

class CustomUserManager(BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    password_helper = PasswordHelper()

    async def authenticate(self, credentials: dict[str, str]):
        identifier = credentials.username
        password = credentials.password

        user = await get_user_by_identifier(self.user_db.session, identifier)
        if user is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid credentials")

        verified, _ = self.password_helper.verify_and_update(password, user.hashed_password)
        if not verified:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid credentials")
        return user

        
async def get_user_manager(user_db=Depends(get_user_db)):
    yield CustomUserManager(user_db)
    
    