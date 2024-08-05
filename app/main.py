# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List, Type
from app import models, schemas, auth
from app.auth import get_db
from app.crud import create_movie, get_movies, get_movie, create_actor, get_actors, get_actor, create_genre, get_genres, \
    get_genre
from app.database import SessionLocal, engine

import os

from app.models import User, Movie

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# auth
app.include_router(auth.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(user_id == User.user_id).first()
    if user is None:
        raise credentials_exception
    return user


def get_movie_by_id(movie_id: int, db: Session) -> Type[Movie] | None:
    return db.query(Movie).filter(movie_id == Movie.movie_id).first()


# auth-end

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/movie/", response_model=schemas.Movie)
async def create_movie_endpoint(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_movies(db, skip=skip, limit=limit)


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


@app.post("/actors/", response_model=schemas.Actor)
def create_actor_endpoint(actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    return create_actor(db=db, actor=actor)


@app.get("/actors/", response_model=List[schemas.Actor])
def read_actors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_actors(db, skip=skip, limit=limit)


@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def read_actor(actor_id: int, db: Session = Depends(get_db)):
    db_actor = get_actor(db, actor_id=actor_id)
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return db_actor


@app.post("/genres/", response_model=schemas.Genre)
def create_genre_endpoint(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    return create_genre(db=db, genre=genre)


@app.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_genres(db, skip=skip, limit=limit)


@app.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = get_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre
