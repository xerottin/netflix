#models.py
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

watch_list = Table(
    'watch_list', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.movie_id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")  # Добавлено
    watch_list = relationship("Movie", secondary=watch_list, back_populates="watchers")


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
    ratings = relationship("Rating", back_populates="movie")  # Добавлено
    watchers = relationship("User", secondary=watch_list, back_populates="watch_list")


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


class Rating(Base):
    __tablename__ = 'ratings'
    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
