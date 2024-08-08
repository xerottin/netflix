# routers/actors.py
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.models import Actor
from app.schemas import ActorCreate, ActorOut

router = APIRouter()

@router.post("/", response_model=ActorOut)
async def create_actor(actor: ActorCreate, db: Database = Depends(get_db)):
    actor_dict = actor.model_dump()
    actor_id = db["actors"].insert_one(actor_dict).inserted_id
    actor_out = db["actors"].find_one({"_id": actor_id})
    return actor_out

@router.get("/{actor_id}", response_model=ActorOut)
async def get_actor(actor_id: str, db: Database = Depends(get_db)):
    actor = db["actors"].find_one({"_id": ObjectId(actor_id)})
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor
