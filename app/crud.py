from sqlalchemy.orm import Session

from app.models import Rating
from app.schemas import RatingCreate


def create_rating(db: Session, rating: RatingCreate, id: int):
    db_rating = Rating(**rating.model_dump(), user_id=id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating
