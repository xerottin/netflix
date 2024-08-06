from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Промежуточные таблицы для связи многие-ко-многим
movie_genres = Table(
    'movie_genres', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.movie_id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.genre_id'), primary_key=True)
)

movie_actors = Table(
    'movie_actors', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.movie_id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.actor_id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    comments = relationship("Comment", back_populates="user")


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)
    author = Column(String)
    year = Column(Integer)
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies")
    comments = relationship("Comment", back_populates="movie")


class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    birth_year = Column(Integer)
    country = Column(String)
    movies = relationship("Movie", secondary=movie_actors, back_populates="actors")


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(String, nullable=False)

    movie = relationship("Movie", back_populates="comments")
    user = relationship("User", back_populates="comments")

