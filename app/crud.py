# crud.py
from sqlalchemy.orm import Session
from app import models, schemas


def get_genre(db: Session, genre_id: int):
    return db.query(models.Genre).filter(genre_id == models.Genre.genre_id).first()


def get_genres(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Genre).offset(skip).limit(limit).all()


def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(movie_id == models.Movie.movie_id).first()


def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        author=movie.author,
        year=movie.year
    )
    if movie.genres:
        db_movie.genres = db.query(models.Genre).filter(models.Genre.genre_id.in_(movie.genres)).all()
    if movie.actors:
        db_movie.actors = db.query(models.Actor).filter(models.Actor.actor_id.in_(movie.actors)).all()
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def get_actor(db: Session, actor_id: int):
    return db.query(models.Actor).filter(actor_id == models.Actor.actor_id).first()


def get_actors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Actor).offset(skip).limit(limit).all()


def create_actor(db: Session, actor: schemas.ActorCreate):
    db_actor = models.Actor(
        name=actor.name,
        gender=actor.gender
    )
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor




