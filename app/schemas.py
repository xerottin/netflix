# schemas.py
from typing import List, Optional
from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreInMovie(GenreBase):
    genre_id: int

    class Config:
        from_attributes = True


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    year: Optional[str] = None


class MovieCreate(MovieBase):
    genres: Optional[List[int]] = None
    actors: Optional[List[int]] = None


class MovieInGenre(MovieBase):
    movie_id: int

    class Config:
        from_attributes = True


class Movie(MovieBase):
    movie_id: int
    genres: List[GenreInMovie] = []
    actors: List['Actor'] = []

    class Config:
        from_attributes = True


class Genre(GenreBase):
    genre_id: int
    movies: List[MovieInGenre] = []

    class Config:
        from_attributes = True


class ActorBase(BaseModel):
    name: str
    gender: Optional[str] = None


class ActorCreate(ActorBase):
    pass


class Actor(ActorBase):
    actor_id: int

    class Config:
        from_attributes = True
