# routers/movies.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.models import Movie
from app.schemas import MovieCreate, MovieOut

router = APIRouter()


@router.post("/", response_model=MovieOut)
async def create_movie(movie: MovieCreate, db: Database = Depends(get_db)):
    movie_dict = movie.model_dump()
    movie_id = db["movies"].insert_one(movie_dict).inserted_id
    movie_out = db["movies"].find_one({"_id": movie_id})
    return movie_out


@router.get("/{movie_id}", response_model=MovieOut)
async def get_movie(movie_id: str, db: Database = Depends(get_db)):
    movie = db["movies"].find_one({"_id": ObjectId(movie_id)})
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
