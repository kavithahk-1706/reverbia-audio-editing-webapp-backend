from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.base import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import Text, Date
from sqlalchemy.orm import Mapped
import uuid


playlist_track=Table(
    "playlist_track",
    Base.metadata,
    Column("playlist_id",ForeignKey("playlists.id"),primary_key=True),
    Column("track_id",ForeignKey("tracks.id"),primary_key=True) 
)

class Track(Base):
    __tablename__="tracks"
    
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,nullable=False)
    artist=Column(String,nullable=True)
    filename=Column(String,nullable=False)
    owner_id=Column(UUID(as_uuid=True),ForeignKey("users.id"))
    
    owner=relationship("User",back_populates="tracks")
    playlists=relationship("Playlist",secondary="playlist_track",back_populates="tracks")
    preset_id=Column(Integer,ForeignKey("presets.id"),nullable=True)
    presets=relationship("Preset",back_populates="tracks")
    
    def __repr__(self):
        return f"<Track id={self.id}, title='{self.title}', artist='{self.artist}'>"
    
    
    
class Playlist(Base):
    __tablename__="playlists"
    
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String,nullable=False)
    owner_id=Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    owner=relationship("User",back_populates="playlists")
    tracks=relationship("Track",secondary=playlist_track,back_populates="playlists")
    
    def __repr__(self):
        return f"<Playlist id={self.id}, name='{self.name}'>"
    
class Preset(Base):
    __tablename__="presets"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(Text,nullable=True)
    owner_id=Column(UUID(as_uuid=True),ForeignKey("users.id"))
    
    owner=relationship("User",back_populates="presets")
    tracks=relationship("Track",back_populates="presets")
    
class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__="oauth_account"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    oauth_name = Column(String, nullable=False)
    account_id = Column(String, nullable=False) 
    account_email=Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    expires_at = Column(Integer, nullable=True)
    refresh_token = Column(String, nullable=True)     
    users: Mapped["User"] = relationship("User", back_populates="oauth_accounts") 

   


class User(SQLAlchemyBaseUserTableUUID,Base):
    __tablename__="users"
    
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    first_name=Column(String,nullable=True)
    last_name=Column(String,nullable=True)
    username=Column(String,unique=True,nullable=True)
    bio=Column(Text,nullable=True)
    profile_pic=Column(Text,nullable=True)
    phone_number=Column(String,nullable=True,unique=True)
    dob=Column(Date, nullable=True)
    country=Column(String, nullable=True)
    
    
    tracks=relationship("Track",back_populates="owner")
    playlists=relationship("Playlist",back_populates="owner")
    presets=relationship("Preset",back_populates="owner")
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", back_populates="users", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User id={self.id}, name={self.first_name} {self.last_name}, username={self.username}>"

