import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]
collection = db.games
# TODO test script

# Add new game
async def add_one_game(name,
                       publisher,
                       release_date,
                       #genres,
                       #desc,
                       #trailer_url,
                       port_url,
                       land_url#,
                       #buy_links
                       ):
    """
    Adds a new game to the database.

    :param name: Name of the game
    :param publisher: Publisher of the game
    :param release_date: Release date of the game
    :param genres: array of strings of genres
    :param desc: description of the game
    :param trailer_url: URL of the trailer in YouTube
    :param port_url: URL for the portrait image
    :param land_url: URL for the landscape image
    :param buy_links: array of links of places you can buy the game on
    """
    game_id = name.lower().replace(' ', '_') + "_" + str(release_date)
    await db.games.insert_one({
        "id": game_id,
        "name": name,
        "publisher": publisher,
        "release_date": release_date,
        #"genres": genres,
        #"desc": desc,
        #"trailer_url": trailer_url,
        "portrait_url": port_url,
        "landscape_url": land_url,
        #"buy_links": buy_links,
        "requirements": {},  # Initialize the requirements as an empty dictionary
    })
    print(f"Game '{name}' added to the database.")

async def main():
    await add_one_game()


# Run the script
asyncio.run(main())