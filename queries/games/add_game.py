import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]
collection = db.games


# Add new game
async def add_one_game(name,
                       publisher,
                       developer,
                       release_date,
                       genres,
                       desc,
                       is_ssd_recommended,
                       upscale_support,
                       api_support,
                       trailer_url,
                       port_url,
                       land_url,
                       buy_links):
    """
    Adds a new game to the database.

    :param name: Name of the game
    :param publisher: Publisher of the game
    :param developer: Developer of the game
    :param release_date: Release date of the game
    :param genres: array of strings of genres
    :param desc: description of the game
    :param is_ssd_recommended: True if the player should install the game on an SSD. otherwise, false.
    :param upscale_support: array of upscalers supported by the game. (E.G DLSS)
    :param api_support: array of APIs supported by the game. (E.G DX12 and Vulkan)
    :param trailer_url: URL of the trailer in YouTube
    :param port_url: URL for the portrait image
    :param land_url: URL for the landscape image
    :param buy_links: array of links of places you can buy the game on
    """
    game_id = name.lower().replace(' ', '_') + "_" + str(release_date)
    await db.games.insert_one({
        "game_id": game_id,
        "name": name,
        "publisher": publisher,
        "developer": developer,
        "release_date": release_date,
        "genres": genres,
        "desc": desc,
        "isSsdRecommended": is_ssd_recommended,
        "upscaleSupport": upscale_support,
        "apiSupport": api_support,
        "trailer_url": trailer_url,
        "portrait_url": port_url,
        "landscape_url": land_url,
        "buy_links": buy_links,
    })
    print(f"Game '{name}' added to the database.")


async def main():
    name = "God of War Ragnarok"

    publisher = "Sony Interactive Entertainment"

    developer = "Santa Monica Studio"

    release_date = 2022

    genres = ["Action", "Adventure", "RPG"]

    desc = "Kratos and Atreus embark on a mythic journey for answers before Ragnarök arrives "

    is_ssd_recommended = True

    upscale_support = ["NVIDIA DLSS 3.7", "AMD FSR 3.1", "Intel XeSS 1.3"]

    api_support = ["DX12"]

    trailer = "https://www.youtube.com/watch?v=EE-4GvjKcfs"

    portrait = "https://imgur.com/CyHn5T3"

    landscape = "https://imgur.com/Ds1R60w"

    buy_links = []

    await add_one_game(name,
                       publisher,
                       developer,
                       release_date,
                       genres,
                       desc,
                       is_ssd_recommended,
                       upscale_support,
                       api_support,
                       trailer,
                       portrait,
                       landscape,
                       buy_links)


# Run the script
asyncio.run(main())
