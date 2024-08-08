from bson import ObjectId
from app.database import genres_collection, movies_collection, actors_collection, ratings_collection, users_collection
from app.models import Genre, Movie, Actor, Rating

async def get_genre(genre_id: str):
    return await genres_collection.find_one({"_id": ObjectId(genre_id)})

async def get_genres(skip: int = 0, limit: int = 10):
    genres_cursor = genres_collection.find().skip(skip).limit(limit)
    return await genres_cursor.to_list(length=limit)

async def create_genre(genre: Genre):
    genre_dict = genre.dict()
    new_genre = await genres_collection.insert_one(genre_dict)
    created_genre = await genres_collection.find_one({"_id": new_genre.inserted_id})
    return created_genre

async def get_movie(movie_id: str):
    return await movies_collection.find_one({"_id": ObjectId(movie_id)})

async def get_movies(skip: int = 0, limit: int = 10):
    movies_cursor = movies_collection.find().skip(skip).limit(limit)
    return await movies_cursor.to_list(length=limit)

async def create_movie(movie: Movie):
    movie_dict = movie.dict()
    if movie.genres:
        movie_dict['genres'] = [ObjectId(genre_id) for genre_id in movie.genres]
    if movie.actors:
        movie_dict['actors'] = [ObjectId(actor_id) for actor_id in movie.actors]
    new_movie = await movies_collection.insert_one(movie_dict)
    created_movie = await movies_collection.find_one({"_id": new_movie.inserted_id})
    return created_movie

async def get_actor(actor_id: str):
    return await actors_collection.find_one({"_id": ObjectId(actor_id)})

async def get_actors(skip: int = 0, limit: int = 10):
    actors_cursor = actors_collection.find().skip(skip).limit(limit)
    return await actors_cursor.to_list(length=limit)

async def create_actor(actor: Actor):
    actor_dict = actor.dict()
    new_actor = await actors_collection.insert_one(actor_dict)
    created_actor = await actors_collection.find_one({"_id": new_actor.inserted_id})
    return created_actor

async def create_rating(rating: Rating):
    rating_dict = rating.dict()
    new_rating = await ratings_collection.insert_one(rating_dict)
    created_rating = await ratings_collection.find_one({"_id": new_rating.inserted_id})
    return created_rating
