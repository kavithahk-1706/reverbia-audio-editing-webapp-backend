from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport
from app.models.models import User
from app.auth.user_manager import get_user_manager
from app.schemas.schemas import UserRead, UserCreate, UserUpdate
from uuid import UUID
bearer_transport=BearerTransport(tokenUrl='auth/jwt/login')
from app.auth.custom_auth import auth_backend,custom_auth_router



fastapi_users=FastAPIUsers[User,UUID](
    get_user_manager,
    [auth_backend],
)

router=APIRouter()

#router.include_router(
#   fastapi_users.get_auth_router(auth_backend),
#   prefix="/auth/jwt",
#   tags=["auth"],
#)

router.include_router(
    custom_auth_router(),
    prefix="/auth/jwt",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead,UserCreate),
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_users_router(UserRead,UserUpdate),
    prefix="/users",
    tags=["users"],
)

