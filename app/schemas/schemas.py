from fastapi_users import schemas
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID



class UserRead(schemas.BaseUser[UUID]):
    id: UUID | None
    first_name: str | None
    last_name: str | None
    username: str | None
    bio: str | None
    profile_pic: str | None
    phone_number:str | None

class UserCreate(schemas.BaseUserCreate):
    id:UUID | None=None
    first_name: str | None=None
    last_name: str | None=None
    username: str | None
    bio: str | None=None
    profile_pic: str | None=None
    phone_number:str | None=None

class UserUpdate(schemas.BaseUserUpdate):
    id:UUID | None=None
    first_name: str | None=None
    last_name: str | None=None
    username: str | None
    bio: str | None=None
    profile_pic: str | None=None
    phone_number:str | None=None

from pydantic import BaseModel

