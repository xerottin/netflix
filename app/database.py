from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.movies_db

users_collection = database.get_collection("users")
movies_collection = database.get_collection("movies")
genres_collection = database.get_collection("genres")
actors_collection = database.get_collection("actors")
comments_collection = database.get_collection("comments")
ratings_collection = database.get_collection("ratings")
