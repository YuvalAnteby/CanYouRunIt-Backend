import asyncio
import re

from bson import ObjectId
from fastapi import FastAPI, Query, APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

"""
All function for handling the GPUs in the DB will be here for ease of use and maintainability.
For example: adding new hardware, fetching hardware, and more.
"""
# Connect to MongoDB (this assumes MongoDB is running on localhost)
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]  # Use your desired database name
router = APIRouter()
# Use the hardware collection
collection = db.hardware


class Gpu(BaseModel):
    hardware_id: str
    brand: str
    model: str
    fullname: str
    type: str

    # Convert ObjectId to string
    id: str

    class Config:
        json_encoders = {
            ObjectId: str  # This will convert ObjectId to a string automatically
        }


@router.get("/gpus")
async def get_all_gpus():
    """
    Retrieve all GPUs from the database.

    :return: List of all GPUs as dictionaries.
    """
    gpu_regex = {"$regex": re.compile("gpu", re.IGNORECASE)}
    try:
        print("Querying all GPUs from the database...")
        gpus_cursor = collection.find({"type": gpu_regex})
        gpus = await gpus_cursor.to_list(length=None)
        print(f"Found GPUs: {gpus}")  # Print the fetched data
        return [Gpu(**gpu, id=str(gpu["_id"])) for gpu in gpus]
    except Exception as e:
        print(f"Error fetching GPUs: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching GPUs: {str(e)}")


@router.get("/gpus/brand")
async def get_gpu_by_brand(brand: str):
    """
    Retrieve GPUs with the given brand from the database.

    :param brand: string of brand of the GPU. E.G: Nvidia. (Not case-sensitive)
    :return: list of GPUs of the given brand.
    """
    brand_regex = {"$regex": re.compile(brand, re.IGNORECASE)}
    gpu_regex = {"$regex": re.compile("gpu", re.IGNORECASE)}
    gpus_cursor = collection.find({"brand": brand_regex, "type": gpu_regex})
    gpus = await gpus_cursor.to_list(length=None)
    return [Gpu(**gpu, id=str(gpu["_id"])) for gpu in gpus]


@router.get("/gpus/model")
async def get_gpu_by_model(model: str):
    """
    Performs a search in the MongoDB collection for GPUs using regex of the model.

    :param model: string of GPU model, E.G: RTX4090 (Not case-sensitive)
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
    return [Gpu(**gpu, id=str(gpu["_id"])) for gpu in gpus]
