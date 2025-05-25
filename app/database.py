from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.models import User, OAuthAccount
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL 
from fastapi import Depends
from sqlalchemy import select,or_
from uuid import uuid4

class CustomUserDatabase(SQLAlchemyUserDatabase):
    def __init__(self, session: AsyncSession):
        self.session=session
        super().__init__(session, User, OAuthAccount)
        self.model = User
    async def get_by_oauth_account(self, oauth: str, account_id: str):
        query = select(self.model).join(User.oauth_accounts).where(
            (OAuthAccount.oauth_name == oauth) & (OAuthAccount.account_id == account_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def add_oauth_account(self, user: User, oauth_account: OAuthAccount):
        try:
            oauth_account=OAuthAccount(**oauth_account)
            self.session.add(oauth_account)
            await self.session.commit()
            await self.session.refresh(oauth_account)
            print(f"YAY ADDED ACCOUNT")
            return user
        except Exception as e:
            await self.session.rollback()
            print(f"Error adding OAuth Account: {e}")
            raise

# Step 2: Engine & Session Setup (unchanged)


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
    return result.unique().scalar_one_or_none()

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Step 3: Updated get_user_db using CustomUserDatabase
async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield CustomUserDatabase(session)



