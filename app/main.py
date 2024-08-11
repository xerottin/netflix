from bson import ObjectId
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient

from app import auth
from app.auth import get_db
from app.crud import create_rating
from app.dependencies import get_current_user
from app.models import User
from app.mongo_models import Movie, Comment
from app.schemas import RatingResponse, RatingCreate

app = FastAPI()

app.include_router(auth.router)

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydatabase


@app.post("/")
async def root():
    return {"Hello": "World"}


@app.post("/ratings/", response_model=RatingResponse)
def create_movie_rating(
        rating: RatingCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_rating = create_rating(db, rating, current_user.id)
    return db_rating


@app.post("/movies/")
async def add_movie(movie: Movie):
    result = await db.movies.insert_one(movie.dict())
    return {"id": str(result.inserted_id)}


@app.get("/movies/")
async def get_movies():
    movies = await db.movies.find().to_list(100)
    return movies


@app.post("/comments/")
async def add_comment(movie_id: str, comment: Comment):
    # Преобразование комментария в формат MongoDB
    mongo_comment = comment.to_mongo()
    result = await db.movies.update_one(
        {"_id": ObjectId(movie_id)},
        {"$push": {"comments": mongo_comment}}
    )
    return {"modified_count": result.modified_count}
