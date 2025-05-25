from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport
from app.models.models import User
from app.auth.user_manager import get_user_manager
from app.schemas.schemas import UserRead, UserCreate, UserUpdate
from uuid import UUID


from app.auth.custom_auth import auth_backend,custom_auth_router

from fastapi import Depends




bearer_transport=BearerTransport(tokenUrl='auth/jwt/login')



fastapi_users=FastAPIUsers[User,UUID](
    get_user_manager,
    [auth_backend],
)

get_current_active_user=fastapi_users.current_user(active=True)

router=APIRouter()





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

@router.get("/users/me", response_model=UserRead)
async def get_me(user: User = Depends(get_current_active_user)):
    return UserRead.model_validate(user, from_attributes=True)


@router.patch("/users/me", response_model=UserRead)
async def patch_me(
    update: UserUpdate,
    user: User = Depends(get_current_active_user),
    user_manager=Depends(get_user_manager),
):
    updated_user = await user_manager.update(update, user)
    return UserRead.model_validate(updated_user, from_attributes=True)


@router.put("/users/me", response_model=UserRead)
async def put_me(
    update: UserUpdate,
    user: User = Depends(get_current_active_user),
    user_manager=Depends(get_user_manager),
):
    updated_user = await user_manager.update(update, user)
    return UserRead.model_validate(updated_user, from_attributes=True)


@router.delete("/users/me")
async def delete_me(
    user: User = Depends(get_current_active_user),
    user_manager=Depends(get_user_manager),
):
    await user_manager.delete(user)
    return {"detail": "User deleted"}


