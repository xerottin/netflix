# crud.py
from sqlalchemy.orm import Session

from app import models, schemas
from app.models import Rating
from app.schemas import RatingCreate


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
    )
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


def create_rating(db: Session, rating: RatingCreate, user_id: int):
    db_rating = Rating(**rating.model_dump(), user_id=user_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_movie_average_rating(db: Session, movie_id: int):
    ratings = db.query(Rating).filter(movie_id == Rating.movie_id).all()
    if not ratings:
        return None
    total = sum(r.rating for r in ratings)
    return total / len(ratings)


def add_to_watchlist(db: Session, watchlist: schemas.WatchListCreate):
    db_user = db.query(models.User).filter(watchlist.user_id == models.User.user_id).first()
    db_movie = db.query(models.Movie).filter(watchlist.movie_id == models.Movie.movie_id).first()

    if not db_user or not db_movie:
        return None

    db_user.watch_list.append(db_movie)
    db.commit()
    db.refresh(db_user)

    return db_user
