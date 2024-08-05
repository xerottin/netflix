# models.py
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import engine, Base

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


class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(String, index=True)
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies")


class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")


class Actor(Base):
    __tablename__ = 'actors'
    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    gender = Column(String, index=True)
    movies = relationship("Movie", secondary=movie_actors, back_populates="actors")


# user
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String)


Base.metadata.create_all(bind=engine)
