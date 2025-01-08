import re

from bson import ObjectId
from fastapi import FastAPI, Query, APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from backend.routes.cpus import collection
from backend.routes.games import router

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

@router.get("/hardware/gpus")
async def get_all_gpus():
    """
    Retrieve all GPUs from the database.
    :return: List of all GPUs as dictionaries.
    """
    gpu_regex = {"$regex": re.compile("gpu", re.IGNORECASE)}
    gpus_cursor = collection.find({"type": gpu_regex})
    gpus = await gpus_cursor.to_list()
    return gpus


@router.get("/hardware/gpus/brand")
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


@router.get("/hardware/gpus/model")
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






