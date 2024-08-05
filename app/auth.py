import os
from datetime import timedelta, datetime
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
import jwt
from app.database import SessionLocal
from app.models import Users

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# schemas
class User(BaseModel):
    id: int
    username: str


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    try:
        create_user_model = Users(
            username=create_user_request.username,
            hashed_password=bcrypt_context.hash(create_user_request.password),
        )

        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)
        return User(id=create_user_model.user_id, username=create_user_model.username)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверное имя пользователя или пароль")
    token = create_access_token(user.username, user.user_id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db: Session) -> Union[Users, None]:
    user = db.query(Users).filter(Users.username == username).first()

    if user and bcrypt_context.verify(password, user.hashed_password):
        return user
    return None


def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)