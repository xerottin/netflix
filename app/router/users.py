from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from bson import ObjectId
from models import User
from schemas import UserCreate, UserOut
from main import get_db
from utils import hash_password

router = APIRouter()

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: Database = Depends(get_db)):
    user_dict = user.dict()
    user_dict["hashed_password"] = hash_password(user.password)
    del user_dict["password"]
    user_id = db["users"].insert_one(user_dict).inserted_id
    user_out = db["users"].find_one({"_id": ObjectId(user_id)})
    return user_out

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db: Database = Depends(get_db)):
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
