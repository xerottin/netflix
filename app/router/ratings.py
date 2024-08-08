# routers/ratings.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.models import Rating
from app.schemas import RatingCreate, RatingOut

router = APIRouter()

@router.post("/", response_model=RatingOut)
async def create_rating(rating: RatingCreate, db: Database = Depends(get_db)):
    rating_dict = rating.model_dump()
    rating_id = db["ratings"].insert_one(rating_dict).inserted_id
    rating_out = db["ratings"].find_one({"_id": rating_id})
    return rating_out

@router.get("/{rating_id}", response_model=RatingOut)
async def get_rating(rating_id: str, db: Database = Depends(get_db)):
    rating = db["ratings"].find_one({"_id": ObjectId(rating_id)})
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating
