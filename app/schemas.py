from pydantic import BaseModel

from pydantic import BaseModel
from typing import List


class MovieCreate(BaseModel):
    title: str
    description: str
    author: str
    year: str
    genres: List[str]
    actors: List[str]


class MovieResponse(BaseModel):
    title: str
    description: str
    author: str
    year: str
    genres: List[str]
    actors: List[str]

    class Config:
        form_attribute = True


class Genre(BaseModel):
    genre_id: int
    name: str


class GenreCreate(BaseModel):
    name: str


class Actor(BaseModel):
    actor_id: int
    name: str
    gender: str


class ActorCreate(BaseModel):
    name: str
    gender: str
