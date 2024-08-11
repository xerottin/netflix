from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    ratings = relationship("Rating", back_populates="user")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    score = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer)
    user = relationship("User", back_populates="ratings")
