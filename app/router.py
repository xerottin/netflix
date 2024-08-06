# router.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import models
from app.dependencies import get_current_user, get_db
from app.models import User, Movie
from app.schemas import CommentCreate, Comment

router = APIRouter()


@router.post("/movies/{movie_id}/comments", response_model=Comment)
def add_comment(
        movie_id: int,
        comment: CommentCreate,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(movie_id == Movie.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    new_comment = models.Comment(
        movie_id=movie_id,
        user_id=user.user_id,
        content=comment.content
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment
