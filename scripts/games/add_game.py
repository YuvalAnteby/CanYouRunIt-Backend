import asyncio
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]
collection = db.games


# TODO add OS_support

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
                       land_s,
                       land_m,
                       land_l,
                       land_xl,
                       buy_links,
                       creation_date,
                       supported_settings,
                       available_resolutions):
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
    :param land_s: URL for the landscape image (small size for mobile)
    :param land_m: URL for the landscape image (medium size for tablets)
    :param land_l: URL for the landscape image (large size for most pcs)
    :param land_xl: URL for the landscape image (X large size for high-res pcs)
    :param buy_links: array of links of places you can buy the game on
    :param creation_date: time when added to DB
    :param supported_settings: list of names of graphical settings in game
    :param available_resolutions: array of available resolutions in game
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
        "is_ssd_required": is_ssd_required,
        "upscale_support": upscale_support,
        "api_support": api_support,
        "trailer_url": trailer_url,
        "portrait_url": port_url,
        "landscape_s": land_s,
        "landscape_m": land_m,
        "landscape_l": land_l,
        "landscape_xl": land_xl,
        "buy_links": buy_links,
        "created_at": creation_date,
        "supported_settings": supported_settings,
        "available_resolutions": available_resolutions,
    })
    print(f"Game '{name}' added to the database.")


async def main():
    name = "Red Dead Redemption 2"

    publisher = "Rockstar Games"

    developer = "Rockstar Games"

    release_date = 2019

    genres = ["Action", "Adventure", "Western"]

    desc = "America, 1899. The end of the Wild West era has begun. After a robbery goes badly wrong in the western town of Blackwater, Arthur Morgan and the Van der Linde gang are forced to flee. With federal agents and the best bounty hunters in the nation massing on their heels, the gang must rob, steal and fight their way across the rugged heartland of America in order to survive. As deepening internal divisions threaten to tear the gang apart, Arthur must make a choice between his own ideals and loyalty to the gang who raised him."

    is_ssd_required = False

    upscale_support = ["Nvidia DLSS", "AMD FSR"]

    api_support = ["Vulkan", "DX12"]

    trailer = "https://www.youtube.com/embed/HVRzx17WHVk?si=Pm8sns1kqPSPollI"

    portrait = "https://imgur.com/wNcAUoN"

    landscape_s = ""
    landscape_m = ""
    landscape_l = ""
    landscape_xl = ""

    buy_links = []

    creation_date = datetime.now(timezone.utc)

    supported_settings = []

    available_resolutions = []

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
                       landscape_s,
                       landscape_m,
                       landscape_l,
                       landscape_xl,
                       buy_links,
                       creation_date,
                       supported_settings,
                       available_resolutions)


# Run the script
asyncio.run(main())
