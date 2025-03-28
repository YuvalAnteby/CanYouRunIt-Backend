from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from backend.app.database import mongodb

# Connect to MongoDB (this assumes MongoDB is running on localhost)
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]  # Use your desired database name
router = APIRouter()
# Use the games collection
collection = db.games

#####
# TODO change as needed
####
class Game(BaseModel):
    """TODO add the new info to the model
    Schema for creating a new game with the relevant attributes
    """
    game_id: str
    name: str
    publisher: str
    developer: str
    release_date: int
    genres: List[str]
    desc: str
    trailer_url: str
    portrait_url: str
    landscape_s: str
    landscape_m: str
    landscape_l: str
    landscape_xl: str
    buy_links: List[str]
    available_resolutions: List[str]
    supported_settings: List[str]

    # Convert ObjectId to string
    id: str

    class Config:
        json_encoders = {
            ObjectId: str  # This will convert ObjectId to a string automatically
        }


@router.get("/games")
async def get_all_games():
    """
    Retrieve all CPUs from the database.

    :return: List of all games as dictionaries.
    """
    try:
        games_cursor = collection.find()
        games = await games_cursor.to_list(length=None)
        return [Game(**game, id=str(game["_id"])) for game in games]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching all games: {str(e)}")

#TODO needs more work and testing
#@router.get("/games/search", response_model=List[Game])
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

# TODO move to scripts
#@router.put("/games/{game_id}", response_model=Game)
async def update_game(game_id: str, game: Game):
    games_collection = mongodb.get_collection("games")
    updated_game = {
        "name": game.name,
        "release_date": game.release_date,
        "requirements": game.requirements
    }
    result = await games_collection.update_one(
        {"_id": ObjectId(game_id)}, {"$set": updated_game}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return {**updated_game, "id": game_id}
