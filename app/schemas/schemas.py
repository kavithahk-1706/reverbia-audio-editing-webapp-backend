from fastapi_users import schemas
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date
from typing import Dict

#oauth schemas

class OAuthAccountInfo(BaseModel):
    account_id: str
    account_email: str
    oauth_name: str
    account: Dict[str, str]  
    access_token: str | None = None
    refresh_token: str | None = None
    expires_at: int | None = None



class OAuthAccountBase(BaseModel):
    oauth_name: str
    account_email: str
    account_id: str
    access_token: Optional[str] = None
    expires_at: Optional[int] = None
    refresh_token: Optional[str] = None

class OAuthAccountCreate(OAuthAccountBase):
    pass

class OAuthAccountRead(OAuthAccountBase):
    id: UUID

    class Config:
        orm_mode = True


#custom schemas

class UserRead(schemas.BaseUser[UUID]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    username: Optional[str]=None
    profile_pic: Optional[str] = None
    phone_number: Optional[str] = None
    dob: Optional[date]=None
    country: Optional[str]=None



class UserCreate(schemas.BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    phone_number: Optional[str] = None
    dob: Optional[date]=None
    country: Optional[str]=None
  


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    username: Optional[str]=None
    profile_pic: Optional[str] = None
    phone_number: Optional[str] = None
    dob: Optional[date]=None
    country: Optional[str]=None


class LoginRequest(BaseModel):
    identifier: str
    password: str