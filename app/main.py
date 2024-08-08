from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth, router
from app.database import engine, get_db
from app.crud import create_movie, get_movies, get_movie, create_actor, get_actors, get_actor, create_genre, get_genres, \
    get_genre, create_rating, get_movie_average_rating
from app.dependencies import get_current_user
from app.models import User, Movie

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Authentication
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include your router for other endpoints
app.include_router(router.router)


@app.post("/movies/", response_model=schemas.Movie)
async def create_movie_endpoint(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_movies(db, skip=skip, limit=limit)


@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    average_rating = get_movie_average_rating(db, movie_id)
    return schemas.MovieResponse(
        movie_id=db_movie.id,
        title=db_movie.title,
        description=db_movie.description,
        author=db_movie.author,
        year=db_movie.year,
        average_rating=average_rating
    )


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


@app.post("/ratings/", response_model=schemas.RatingResponse)
def create_movie_rating(
        rating: schemas.RatingCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_movie = db.query(Movie).filter(rating.movie_id == Movie.id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db_rating = create_rating(db, rating, current_user.id)
    return db_rating


@app.post("/movies/{movie_id}/comments", response_model=schemas.Comment)
def add_comment(
        movie_id: str,
        comment: schemas.CommentCreate,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(movie_id == Movie.id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    new_comment = models.Comment(
        movie_id=movie_id,
        user_id=user.id,
        content=comment.content
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment
