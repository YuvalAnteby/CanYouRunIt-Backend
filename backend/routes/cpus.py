import asyncio
import re
from typing import Optional

from bson import ObjectId
from fastapi import FastAPI, Query, APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

"""
All functions for handling the CPUs in the DB will be here for ease of use and maintainability.
For example: fetching all CPUs, fetch CPUs by brand, etc.
"""
# Connect to MongoDB (this assumes MongoDB is running on localhost)
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]  # Use your desired database name
router = APIRouter()
# Use the hardware collection
collection = db.hardware


class Cpu(BaseModel):
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


@router.get("/cpus")
async def get_all_cpus():
    """
    Retrieve all CPUs from the database.

    :return: List of all CPUs as dictionaries.
    """
    cpu_regex = {"$regex": re.compile("cpu", re.IGNORECASE)}
    try:
        cpus_cursor = collection.find({"type": cpu_regex})
        cpus = await cpus_cursor.to_list(length=None)
        validate_cpus_list(cpus)
        return [Cpu(**cpu, id=str(cpu["_id"])) for cpu in cpus]
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print(f"Error fetching CPUs: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching CPUs: {str(e)}")


@router.get("/cpus/brand")
async def get_cpu_by_brand(brand: str):
    """
    Retrieve CPUs with the given brand from the database.

    :param brand: string of brand of the CPU. E.G: AMD and Intel. (Not case-sensitive)
    :return: list of CPUs of the given brand.
    """
    try:
        brand_regex = {"$regex": re.compile(brand, re.IGNORECASE)}
        cpu_regex = {"$regex": re.compile("cpu", re.IGNORECASE)}
        cpus_cursor = collection.find({"brand": brand_regex, "type": cpu_regex})
        cpus = await cpus_cursor.to_list(length=None)
        validate_cpus_list(cpus, brand=brand)
        return [Cpu(**cpu, id=str(cpu["_id"])) for cpu in cpus]
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CPUs by model: {str(e)}")


@router.get("/cpus/model")
async def get_cpu_by_model(model: str):
    """
    Retrieve CPUs with the given model from the database.

    :param model: string of CPU model. E.G: RYZEN3600. (Not case-sensitive)
    :return: list of CPUs of the given model's regex.
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
    try:
        cpus_cursor = collection.find(search_query)
        cpus = await cpus_cursor.to_list()
        # If cpus is empty count it as no games found error
        validate_cpus_list(cpus, model=model)
        return [Cpu(**cpu, id=str(cpu["_id"])) for cpu in cpus]
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CPUs by model: {str(e)}")


def validate_cpus_list(cpus: list, brand: Optional[str] = None, model: Optional[str] = None):
    """
    Validates the list of CPUs fetched from the database.

    - Raises 404 if the list is empty.
    - Raises 500 if any item is included in the list that wasn't supposed to according to filtering. (e.g. brand/ type)

    :param cpus: List of CPU dictionaries from the DB.
    :param brand: Optional brand filter to validate against.
    :param model: Optional model regex to validate against.
    """
    # If cpus is empty count it as no games found error
    if not cpus:
        raise HTTPException(status_code=404, detail="No CPUs found")
    # Ensure only relevant CPUs have been fetched from DB
    model_pattern = re.compile(model, re.IGNORECASE) if model else None
    for cpu in cpus:
        # Check no GPUs were fetched
        if cpu.get("type", "").lower() != "cpu":
            raise HTTPException(status_code=500, detail="Non-CPU hardware found in CPU route")
        # Ensure only relevant brand's CPUs have been fetched
        if brand and cpu.get("brand", "").lower() != brand.lower():
            raise HTTPException(status_code=500, detail="Wrong brand found in CPUs fetched")
        # Ensure only relevant CPU models have been fetched
        if model_pattern:
            if not (
                    model_pattern.search(cpu.get("model", "")) or
                    model_pattern.search(cpu.get("fullname", ""))
            ):
                raise HTTPException(status_code=500, detail="Wrong model regex found in CPUs fetched")
