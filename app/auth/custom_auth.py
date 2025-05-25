from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.config import SECRET
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from app.database import get_db, get_user_by_identifier
from fastapi.security import HTTPBearer
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend
from app.schemas.schemas import LoginRequest


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

router = APIRouter()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend=AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)



security = HTTPBearer()

ALGORITHM = "HS256"

from uuid import UUID

from pydantic import BaseModel



@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    identifier = data.identifier
    password = data.password

    user = await get_user_by_identifier(db, identifier)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    ph = PasswordHasher()
    try:
        ph.verify(user.hashed_password, password)
    except VerifyMismatchError:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    strategy = auth_backend.get_strategy()
    access_token = await strategy.write_token(user)
   
    return JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})


def custom_auth_router() -> APIRouter:
    return router
