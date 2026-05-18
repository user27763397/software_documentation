from sqlalchemy import Column, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'
    
    song_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre = Column(String)
    price = Column(Float)