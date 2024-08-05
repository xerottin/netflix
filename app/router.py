from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.auth import get_db, User
from app.main import get_current_user
from app.main import get_movie_by_id
from app.schemas import Comment

router = APIRouter()


@router.post("/movies/{movie_id}/comments")
def add_comment(movie_id: str, comment: Comment,  user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    movie = get_movie_by_id
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    new_comment = Comment(
        id=int(uuid4()),
        movie_id=movie_id,
        user_id=user.id,
        content=comment.content,
        created_at=datetime.utcnow()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment
