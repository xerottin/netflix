from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Movie, Genre, Actor
from app.schemas import MovieResponse, MovieCreate

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/movies/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    genre_objects = [db.query(Genre).filter(Genre.name == genre).first() for genre in movie.genres]
    actor_objects = [db.query(Actor).filter(Actor.name == actor).first() for actor in movie.actors]

    if any(g is None for g in genre_objects):
        raise HTTPException(status_code=400, detail="Some genres not found")
    if any(a is None for a in actor_objects):
        raise HTTPException(status_code=400, detail="Some actors not found")

    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        author=movie.author,
        year=movie.year,
        genres=genre_objects,
        actors=actor_objects
    )

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie
