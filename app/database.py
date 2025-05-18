from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.models import User
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL as DB_URL
from fastapi import Depends
from sqlalchemy import select,or_


DATABASE_URL=DB_URL

async def get_user_by_identifier(session:AsyncSession,identifier:str):
    result=await session.execute(
        select(User).where(
            or_(
                User.email==identifier,
                User.username==identifier,
                User.phone_number==identifier,
            )
        )
    )
    return result.scalar_one_or_none()


engine=create_async_engine(DATABASE_URL,echo=True)
AsyncSessionLocal=sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_db(session:AsyncSession=Depends(get_db)):
    yield SQLAlchemyUserDatabase(session,User)