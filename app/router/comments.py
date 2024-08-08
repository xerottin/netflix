# routers/comments.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.models import Comment
from app.schemas import CommentCreate, CommentOut

router = APIRouter()

@router.post("/", response_model=CommentOut)
async def create_comment(comment: CommentCreate, db: Database = Depends(get_db)):
    comment_dict = comment.model_dump()
    comment_id = db["comments"].insert_one(comment_dict).inserted_id
    comment_out = db["comments"].find_one({"_id": comment_id})
    return comment_out

@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(comment_id: str, db: Database = Depends(get_db)):
    comment = db["comments"].find_one({"_id": ObjectId(comment_id)})
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
