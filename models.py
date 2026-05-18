from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
    account = relationship("Account", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True)
    balance = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    
    user_id = Column(String, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="account")

class Song(Base):
    __tablename__ = 'songs'
    song_id = Column(String, primary_key=True)
    title = Column(String)
    price = Column(Float)
    artist = Column(String)
    genre = Column(String)