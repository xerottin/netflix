# routers/genres.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.models import Genre
from app.schemas import GenreCreate, GenreOut

router = APIRouter()


@router.post("/", response_model=GenreOut)
async def create_genre(genre: GenreCreate, db: Database = Depends(get_db)):
    genre_dict = genre.model_dump()
    genre_id = db["genres"].insert_one(genre_dict).inserted_id
    genre_out = db["genres"].find_one({"_id": genre_id})
    return genre_out


@router.get("/{genre_id}", response_model=GenreOut)
async def get_genre(genre_id: str, db: Database = Depends(get_db)):
    genre = db["genres"].find_one({"_id": ObjectId(genre_id)})
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre
