from pydantic import BaseModel
from typing import List, Optional


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    genre_id: Optional[int]

    class Config:
        orm_mode = True


class ActorBase(BaseModel):
    name: str
    gender: Optional[str]


class ActorCreate(ActorBase):
    pass


class Actor(ActorBase):
    actor_id: Optional[int]

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str
    description: Optional[str]
    author: Optional[str]
    year: Optional[str]


class MovieCreate(MovieBase):
    genres: List[GenreCreate] = []
    actors: List[ActorCreate] = []


class Movie(MovieBase):
    movie_id: Optional[int]
    genres: List[Genre] = []
    actors: List[Actor] = []

    class Config:
        orm_mode = True
