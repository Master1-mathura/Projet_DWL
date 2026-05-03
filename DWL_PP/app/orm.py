from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(255),nullable=False, unique=True)
    mdp = Column(String(255),nullable=False)
    watchlist = relationship("Watchlist", back_populates="user",cascade="all, delete")
    settings = relationship("UserSettings", back_populates="user", cascade="all, delete", uselist=False)

class Watchlist(Base):
    __tablename__ = "watchlist"
    imdb_id = Column(String(50),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete = "CASCADE"),primary_key=True)
    film_name = Column(String(150),nullable=False)
    poster = Column(String(255),nullable=False)
    background = Column(String(255),nullable=False)
    etat = Column(String(20),nullable=False)
    user = relationship("User", back_populates="watchlist")

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),unique=True)
    theme = Column(String(20),nullable=False,default="dark")
    blur_effect = Column(String(20),nullable=False,default="off")
    user = relationship("User", back_populates="settings")