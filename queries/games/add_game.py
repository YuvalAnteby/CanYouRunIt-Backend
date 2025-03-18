import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]
collection = db.games
# TODO test script

# Add new game
async def create_game(name, publisher, release_date, portrait_url, landscape_url, additional_info=None):
    """
    Adds a new game to the database.
    :param name: Name of the game
    :param publisher: Publisher of the game
    :param release_date: Release date of the game
    :param portrait_url: URL for the portrait image
    :param landscape_url: URL for the landscape image
    :param additional_info: Any other relevant info (optional)
    """
    game_id = name.lower().replace(' ', '_') + "_" + str(release_date)
    new_game = {
        "id": game_id,
        "name": name,
        "publisher": publisher,
        "release_date": release_date,
        "portrait_url": portrait_url,
        "landscape_url": landscape_url,
        "requirements": {},  # Initialize the requirements as an empty dictionary
    }
    if additional_info:
        new_game["additional_info"] = additional_info

    await db.games.insert_one(new_game)
    print(f"Game '{name}' added to the database.")

async def main():
    await create_game("name",
                      "publisher",
                      "release_date",
                      "portrait_url",
                      "landscape_url",
                      "additional_info")


# Run the script
asyncio.run(main())