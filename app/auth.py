import os
from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status
import jwt
from bson import ObjectId
from app.database import users_collection
from app.models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")  # Значение по умолчанию
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(create_user_request: UserCreate):
    existing_user = await users_collection.find_one({"username": create_user_request.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    user = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    new_user = await users_collection.insert_one(user.dict())
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return UserResponse(**created_user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    token = create_access_token(user.username, str(user.id), timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}

async def authenticate_user(username: str, password: str) -> Union[User, None]:
    user = await users_collection.find_one({"username": username})
    if user and bcrypt_context.verify(password, user['hashed_password']):
        return User(**user)
    return None

def create_access_token(username: str, user_id: str, expires_delta: timedelta) -> str:
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
 ##