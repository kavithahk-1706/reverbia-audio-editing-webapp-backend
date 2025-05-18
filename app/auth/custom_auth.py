from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.config import SECRET
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy, BearerTransport
from app.database import get_db, get_user_by_identifier
router = APIRouter()

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

cookie_transport=CookieTransport(cookie_name="auth",cookie_max_age=3600)

auth_backend=AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)

print("YOOOOOO SERVER STARTED BITCHES")

@router.post("/login")
async def login(identifier: str, password: str, db: AsyncSession = Depends(get_db)):
    print("Login route hit with identifier:", identifier)
    # Check if user exists with username/email/phone
    user = await get_user_by_identifier(db, identifier)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    

    ph = PasswordHasher()
    try:
        ph.verify(user.hashed_password, password)
    except VerifyMismatchError:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # Generate JWT token
    strategy = auth_backend.get_strategy()
    access_token = await strategy.write_token(user)
    print("Returning 200 OK with token 🚀")
    return JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})


def custom_auth_router() -> APIRouter:
    return router
