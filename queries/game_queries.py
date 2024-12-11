from pymongo import MongoClient
from datetime import datetime
from pymongo import MongoClient

"""
All function for handling the games in the DB will be here for ease of use and maintainability.
For example: adding new game, adding new hardware requirements, and more.
"""

# Assuming MongoDB instance running locally
client = MongoClient('mongodb://localhost:27017')
db = client['game_db']

# Add new game
def create_game(name, publisher, release_date, portrait_url, landscape_url, additional_info=None):
    """
    Adds a new game to the database.
    :param name: Name of the game
    :param publisher: Publisher of the game
    :param release_date: Release date of the game
    :param portrait_url: URL for the portrait image
    :param landscape_url: URL for the landscape image
    :param additional_info: Any other relevant info (optional)
    """
    game_id = name.lower().replace(' ', '_') + "_" + str(get_year_from_date(release_date))
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

    db.games.insert_one(new_game)
    print(f"Game '{name}' added to the database.")

def get_year_from_date(date_string):
    """
    Get the year from a date string.
    :param date_string: string of a date of the format YYYY-MM-DD
    :return: year of a date
    """
    try:
        release_date = datetime.strptime(date_string, "%Y-%m-%d")
        return release_date.year
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD'.")
        return None

# Add a new requirement setting for a game
def add_requirement_to_game(game_id, setting_id, hardware_requirements):
    """
    Add a new setting with required hardware to the game.
    E.G:
        new_setting = {
        "cpu_intel": ["intel_i7_9700k"],
        "gpu_nvidia": ["nvidia_rtx_3080"],
        "ram": 16
        }
        add_requirement_to_game("God of War", "4k_high_60fps", new_setting)

    :param game_id: id of the required game. E.G: RTX 4090
    :param setting_id: name of the required setting. E.G: 1080p_high_60fps
    :param hardware_requirements: list of hardware requirements
    """
    game = db.games.find_one({"id": game_id})
    if game:
        db.games.update_one(
            {"id": game_id},
            {"$set": {f"requirements.{setting_id}": hardware_requirements}}
        )
        print(f"Added requirement '{setting_id}' to game '{game_id}'.")
    else:
        print(f"Game '{game_id}' not found.")

# Add hardware to an existing requirement setting for a game
def add_hardware_to_requirement(game_id, setting_name, hardware_type, hardware_id):
    """
    Add new hardware to an existing setting in a game
    E.G:
        add_hardware_to_requirement("God of War", "4k_high_60fps", "gpu_nvidia", "nvidia_rtx_3090")
    :param game_id: id of the required game. E.G: RTX 4090
    :param setting_name: name of the required setting. E.G: 1080p_high_60fps
    :param hardware_type: type of the hardware. E.G: gpu_nvidia
    :param hardware_id: id of the hardware. E.G: nvidia_rtx_3080
    :return:
    """
    game = db.games.find_one({"id": game_id})
    if game:
        if setting_name in game["requirements"]:
            db.games.update_one(
                {"id": game_id},
                {"$push": {f"requirements.{setting_name}.{hardware_type}": hardware_id}}
            )
            print(f"Added hardware '{hardware_id}' to setting '{setting_name}' for game '{game_id}'.")
        else:
            print(f"Setting '{setting_name}' not found for game '{game_id}'.")
    else:
        print(f"Game '{game_id}' not found.")

async def get_all_games():
    """
    Retrieve all games from the database.
    :return: List of all games as dictionaries.
    """
    return list(db.games.find({}))
