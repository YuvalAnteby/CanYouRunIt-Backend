import re

from motor.motor_asyncio import AsyncIOMotorClient

"""
All function for handling the hardware in the DB will be here for ease of use and maintainability.
For example: adding new hardware, fetching hardware, and more.
"""

# Assuming MongoDB instance running locally
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client['game_db']
collection = db.hardware


def add_gpu(brand, model, fullname):
    """
    Adding a new GPU to the collection.
    :param brand: brand of the GPU. E.G: Nvidia
    :param model: GPU model. E.G RTX 4090
    :param fullname: name of the GPU model. E.G: RTX 4070 TI super
    """
    # Make sure the input isn't empty
    if brand.empty() or model.empty() or fullname.empty():
        return
    # Standardize ids for the GPUs
    gpu_id = brand.lower() + "_" + model.lower().replace(' ', '_')
    # Check if the GPU already exists to avoid duplicates
    existing_gpu = db.hardware.find_one({"hardware_id": gpu_id, "type": "gpu"})
    if existing_gpu:
        print(f"GPU '{fullname}' already exists in the database.")
        return
    # Insert the new GPU to the DB
    db.hardware.insert_one(
        {"hardware_id": gpu_id, "brand": brand, "model": model, "fullname": fullname, "type": "gpu_" + brand.lower()})


def add_cpu(brand, model, fullname):
    """
    Adding a new CPU to the collection.
    :param brand: brand of the CPU. E.G: AMD
    :param model: CPU model without spaces. E.G RYZEN3600
    :param fullname: full name of the CPU model. E.G RYZEN R5 3600
    """
    # Make sure the input isn't empty
    if brand.strip() == "" or model.strip() == "" or fullname.strip() == "":
        return
    # Standardize ids for the CPUs
    cpu_id = brand.lower() + "_" + model.lower().replace(' ', '_')
    # Check if the CPU already exists to avoid duplicates
    existing_cpu = db.hardware.find_one({"hardware_id": cpu_id, "type": "cpu"})
    if existing_cpu:
        print(f"CPU '{fullname}' already exists in the database.")
        return
    # Insert the new CPU to the DB
    db.hardware.insert_one(
        {"hardware_id": cpu_id, "brand": brand, "model": model, "fullname": fullname, "type": "cpu_" + brand.lower()})


async def get_all_gpus():
    """
    Retrieve all GPUs from the database.
    :return: List of all GPUs as dictionaries.
    """
    gpu_regex = {"$regex": re.compile("gpu", re.IGNORECASE)}
    gpus_cursor = collection.find({"type": gpu_regex})
    gpus = await gpus_cursor.to_list()
    return gpus


async def get_gpu_by_brand(brand: str):
    """
    Retrieve GPUs with the given brand from the database.

    :param brand: string of brand of the GPU. E.G: Nvidia.
    :return: list of GPUs of the given brand.
    """
    brand_regex = {"$regex": re.compile(brand, re.IGNORECASE)}
    gpu_regex = {"$regex": re.compile("gpu", re.IGNORECASE)}
    gpus_cursor = collection.find({"brand": brand_regex, "type": gpu_regex})
    gpus = await gpus_cursor.to_list()
    return gpus


async def get_gpu_by_model(model: str):
    """
    Performs a search in the MongoDB collection for GPUs using regex of the model.
    :param model: string of GPU model, E.G: RTX4090
    :return: list of GPUS with matching fullname or model
    """
    model_regex = {"$regex": re.compile(model, re.IGNORECASE)}
    gpu_regex = {"$regex": re.compile("gpu", re.IGNORECASE)}
    search_query = {
        "$and": [
            {"type": gpu_regex},  # Ensure the hardware is a CPU
            {
                "$or": [  # Match the input's regex with the full name or the shorten model name.
                    {"model": model_regex},
                    {"fullname": model_regex}
                ]
            }
        ]
    }
    gpus_cursor = collection.find(search_query)
    gpus = await gpus_cursor.to_list()
    return gpus


async def get_all_cpus():
    """
    Retrieve all CPUs from the database.

    :return: List of all CPUs as dictionaries.
    """
    cpu_regex = {"$regex": re.compile("cpu", re.IGNORECASE)}
    cpus_cursor = collection.find({"type": cpu_regex})
    cpus = await cpus_cursor.to_list()
    return cpus


async def get_cpu_by_brand(brand: str):
    """
    Retrieve CPUs with the given brand from the database.

    :param brand: string of brand of the CPU. E.G: AMD and Intel.
    :return: list of CPUs of the given brand.
    """
    brand_regex = {"$regex": re.compile(brand, re.IGNORECASE)}
    cpu_regex = {"$regex": re.compile("cpu", re.IGNORECASE)}
    cpus_cursor = collection.find({"brand": brand_regex, "type": cpu_regex})
    cpus = await cpus_cursor.to_list()
    return cpus


async def get_cpu_by_model(model: str):
    """
    Retrieve CPUs with the given model from the database.

    :param model: string of CPU model. E.G: RYZEN3600
    :return:
    """
    model_regex = {"$regex": re.compile(model, re.IGNORECASE)}
    cpu_regex = {"$regex": re.compile("cpu", re.IGNORECASE)}
    search_query = {
        "$and": [
            {"type": cpu_regex},  # Ensure the hardware is a CPU
            {
                "$or": [  # Match the input's regex with the full name or the shorten model name.
                    {"model": model_regex},
                    {"fullname": model_regex}
                ]
            }
        ]
    }
    cpus_cursor = collection.find(search_query)
    cpus = await cpus_cursor.to_list()
    return cpus
