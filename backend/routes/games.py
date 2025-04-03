import re
from typing import Optional

from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from backend.app.database import mongodb
from backend.models.game import Game

# Connect to MongoDB (this assumes MongoDB is running on localhost)
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]  # Use your desired database name
router = APIRouter()
# Use the games collection
collection = db.games




@router.get("/games")
async def get_all_games():
    """
    Retrieve all CPUs from the database.

    :return: List of all games as dictionaries.
    """
    try:
        games_cursor = collection.find()
        games = await games_cursor.to_list(length=None)
        # If games is empty count it as no games found error
        if not games:
            raise HTTPException(status_code=404, detail="No games found")
        return [Game(**game, id=str(game["_id"])) for game in games]
    except HTTPException:
        raise HTTPException(status_code=404, detail="No games found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all games: {str(e)}")

@router.get("/games/category")
async def get_games_by_category(genre, limit: Optional[int] = None):
    """
    Retrieve all games with given genre from the DB.
    :return: List of dictionaries with matching genre.
    """
    try:
        genre_regex = {"$regex": re.compile(genre, re.IGNORECASE)}
        games_cursor = collection.find({ "genres": genre_regex })
        games = await games_cursor.to_list(length=limit)
        if not games:
            raise HTTPException(status_code=404, detail="No games found with this genre")
        return [Game(**game, id=str(game["_id"])) for game in games]
    except HTTPException:
        raise HTTPException(status_code=404, detail="No games found with this genre")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all games: {str(e)}")

# TODO needs more work
# TODO create tests
# @router.get("/games/search", response_model=List[Game])
async def search_games(name: Optional[str] = None, year: Optional[str] = None, publisher: Optional[str] = None):
    """
    Performs a search in the MongoDB database for games that match the provided search criteria.
    E.G: name, release year, and publisher.
    The search is flexible and can handle partial matches for the game name and publisher.

    :param name: (str, optional): The name of the game to search for (case-insensitive).
    :param year: (str, optional): The release year of the game. TODO change to int
    :param publisher: (str, optional): The publisher of the game.
    :return: List[GameResponse]: A list of games that match the search criteria.

    :raises: HTTPException: If no games match the search criteria.
    """
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Case-insensitive search
    if year:
        query["release_date"] = year
    if publisher:
        query["publisher"] = {"$regex": publisher, "$options": "i"}  # Case-insensitive search

    games_collection = mongodb.get_collection("games")
    games = await games_collection.find(query).to_list(None)  # Fetch all matching games

    if not games:
        raise HTTPException(status_code=404, detail="No games found matching the criteria")

    return [Game(**game) for game in games]
