from pymongo import MongoClient
from datetime import datetime

"""
All function for handling the DB will be here for ease of use and maintainability.
For example: adding new hardware, new games, new settings and more.
"""

# Assuming MongoDB instance running locally
client = MongoClient('mongodb://localhost:27017')
db = client['game_requirements_db']

# TODO add validation (duplications, nulls, empty objects)
def add_gpu(brand, model, fullname):
    """
    Adding a new GPU to the collection.
    :param brand: brand of the GPU. E.G: Nvidia
    :param model: GPU model. E.G RTX 4090
    :param fullname: name of the GPU model. E.G: RTX 4070 TI super
    """
    gpu_id = brand.lower() + "_" + model.lower().replace(' ', '_')
    db.hardware.insert_one(
        {"hardware_id": gpu_id, "brand": brand, "model": model, "fullname": fullname, "type": "gpu_" + brand.lower()})

# TODO add validation (duplications, nulls, empty objects)
def add_cpu(brand, model, fullname):
    """
    Adding a new CPU to the collection.
    :param brand: brand of the CPU. E.G: AMD
    :param model: CPU model without spaces. E.G RYZEN3600
    :param fullname: full name of the CPU model. E.G RYZEN R5 3600
    """
    cpu_id = brand.lower() + "_" + model.lower().replace(' ', '_')
    db.hardware.insert_one(
        {"hardware_id": cpu_id, "brand": brand, "model": model, "fullname": fullname, "type": "cpu_" +brand.lower()})

# Add new game
def create_game(name, publisher, release_date, image_url, additional_info=None):
    """
    Adds a new game to the database.
    :param name: Name of the game
    :param publisher: Publisher of the game
    :param release_date: Release date of the game
    :param image_url: URL for the game image
    :param additional_info: Any other relevant info (optional)
    """
    new_game = {
        "id": name.lower().replace(' ', '_') + "_" + get_year_from_date(release_date),
        "name": name,
        "publisher": publisher,
        "release_date": release_date,
        "image_url": image_url,
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