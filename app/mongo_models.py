from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class Genre(BaseModel):
    name: str


class Actor(BaseModel):
    name: str


class Comment(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    text: str
    movie_id: Optional[str] = None  # Используем строку для идентификатора

    def to_mongo(self):
        return {
            "_id": ObjectId(self.id) if self.id else None,
            "text": self.text,
            "movie_id": ObjectId(self.movie_id) if self.movie_id else None,
        }

    class Config:
        arbitrary_types_allowed = True


class Movie(BaseModel):
    title: str
    description: str
    genres: List[Genre]
    actors: List[Actor]
    comments: List[Comment] = []

    class Config:
        arbitrary_types_allowed = True
