from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from backend.app.database import mongodb
from bson import ObjectId
from typing import List, Optional

router = APIRouter()

class GameCreate(BaseModel):
    """TODO
    Schema for creating a new game with the relevant attributes
    """
    name: str
    publisher: str
    release_date: str
    portrait_url: str
    landscape_url: str
    requirements: dict


# adds mongoDB's built in id to the GameCreate objects
class GameResponse(GameCreate):
    id: str  # MongoDB's ObjectId will be converted to string

    class Config:
        # Convert MongoDB ObjectId to string when returning the response
        json_encoders = {
            ObjectId: str
        }


@router.post("/games/", response_model=GameResponse)
async def create_game(game: GameCreate):
    """
    TODO
    :param game:
    :return:
    """
    games_collection = mongodb.get_collection("games")  # Get the "games" collection
    new_game = {
        "name": game.name,
        "publisher": game.publisher,
        "release_date": game.release_date,
        "portrait_url": game.portrait_url,
        "landscape_url": game.landscape_url,
        "requirements": game.requirements
    }
    # Insert into MongoDB
    result = await games_collection.insert_one(new_game)
    # Get the inserted document's ID
    game_id = result.inserted_id
    # Return the game data along with its MongoDB ID
    return {**new_game, "id": str(game_id)}

@router.get("/games/search", response_model=List[GameResponse])
async def search_games(name: Optional[str] = None, year: Optional[str] = None, publisher: Optional[str] = None):
    """
    Performs a search in the MongoDB database for games that match the provided search criteria.
    E.G: name, release year, and publisher.
    The search is flexible and can handle partial matches for the game name and publisher.

    :param name: (str, optional): The name of the game to search for (case-insensitive).
    :param year: (str, optional): The release year of the game.
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

    return [GameResponse(**game) for game in games]

# TODO test
@router.put("/games/{game_id}", response_model=GameResponse)
async def update_game(game_id: str, game: GameCreate):
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
