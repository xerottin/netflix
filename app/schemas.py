from pydantic import BaseModel, Field


class RatingBase(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    movie_id: int


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    rating_id: int
    user_id: int

    class Config:
        from_attributes = True
