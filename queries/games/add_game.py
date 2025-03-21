import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]
collection = db.games
#TODO add OS supported

# Add new game
async def add_one_game(name,
                       publisher,
                       developer,
                       release_date,
                       genres,
                       desc,
                       is_ssd_required,
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
    :param is_ssd_required: True if the player should install the game on an SSD. otherwise, false.
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
        "isSsdRequired": is_ssd_required,
        "upscaleSupport": upscale_support,
        "apiSupport": api_support,
        "trailer_url": trailer_url,
        "portrait_url": port_url,
        "landscape_url": land_url,
        "buy_links": buy_links,
    })
    print(f"Game '{name}' added to the database.")


async def main():
    name = "Kingdom Come Deliverance 1"

    publisher = "Deep Silver"

    developer = "Warhorse Studios"

    release_date = 2018

    genres = ["Action", "Adventure", "RPG"]

    desc = ("Story-driven open-world RPG that immerses you in an epic adventure in the Holy Roman Empire. Avenge "
            "your parents' death as you battle invading forces, go on game-changing quests, and make influential "
            "choices. Explore castles, forests, villages and other realistic settings in medieval Bohemia!")

    is_ssd_required = False

    upscale_support = []

    api_support = ["DX11"]

    trailer = "https://www.youtube.com/watch?v=_D48PCFshHg"

    portrait = "https://imgur.com/q1aVXnw"

    landscape = "https://imgur.com/DgbCcxa"

    buy_links = []

    await add_one_game(name,
                       publisher,
                       developer,
                       release_date,
                       genres,
                       desc,
                       is_ssd_required,
                       upscale_support,
                       api_support,
                       trailer,
                       portrait,
                       landscape,
                       buy_links)


# Run the script
asyncio.run(main())
