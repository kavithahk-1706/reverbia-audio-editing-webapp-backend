from fastapi_users import BaseUserManager
from fastapi import Depends, HTTPException, status
from uuid import UUID
from app.database import get_user_db,get_user_by_identifier
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi_users.password import PasswordHelper
from app.models.models import User

from fastapi_users import BaseUserManager

from fastapi_users.password import PasswordHelper
from uuid import UUID, uuid4


from app.models.models import User
from app.database import get_user_db, get_user_by_identifier
from app.config import SECRET


class CustomUserManager(BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    password_helper = PasswordHelper()

    def parse_id(self, user_id: str) -> UUID:
        return UUID(user_id)

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
    

    async def oauth_callback(
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[datetime] = None,
        refresh_token: Optional[str] = None,
        account_data: Optional[dict] = None,
        *,
        is_verified_by_default: bool = False,
        associate_by_email: bool = True,
    ) -> User:
       try:
           print(f"account id: {account_id}")
           print(f"account email: {account_email}")
           user = await super().oauth_callback(
               oauth_name,
               access_token,
               account_id,
               account_email,
               expires_at,
               refresh_token,
               account_data,
            )

           return user
       except Exception as e:
           print(f"OAuth callback error: {repr(e)}")
           raise


    

    async def on_after_oauth_login(self, user: User, oauth_account):
        '''
        Called after a successful OAuth login (whether user is created or already exists).
        Update extra fields here.
        '''
        updated = False

        first_name = oauth_account.account.get("given_name", "user")
        last_name = oauth_account.account.get("family_name", "anon")

        # If it's a newly created user, update their name and generate a username
        if not user.first_name:
            user.first_name = first_name
            updated = True

        if not user.last_name:
            user.last_name = last_name
            updated = True

        if not user.username:
            user.username = f"{first_name}.{last_name}_{uuid4().hex[:6]}"
            updated = True

        if updated:
            await self.user_db.update(user)


# Dependency to use in routers
async def get_user_manager(user_db=Depends(get_user_db)):
    yield CustomUserManager(user_db)

    
    