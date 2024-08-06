from typing import List, Optional
from pydantic import BaseModel, Field


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreInMovie(GenreBase):
    genre_id: int

    class Config:
        from_attributes = True  # Используйте orm_mode вместо from_attributes для pydantic моделей


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    year: int


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
    year: int

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


# schemas.py

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    comment_id: int
    movie_id: int
    user_id: int

    class Config:
        orm_mode = True


class RatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    movie_id: int


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    rating_id: int
    user_id: int

    class Config:
        orm_mode = True


class MovieResponse(BaseModel):
    id: int
    title: str
    average_rating: float

    class Config:
        orm_mode = True
