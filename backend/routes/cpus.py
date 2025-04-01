import asyncio
import re

from bson import ObjectId
from fastapi import FastAPI, Query, APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

"""
All function for handling the CPUs in the DB will be here for ease of use and maintainability.
For example: adding new hardware, fetching hardware, and more.
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
        # If cpus is empty count it as no games found error
        if not cpus:
            raise HTTPException(status_code=404, detail="No CPUs found")
        return [Cpu(**cpu, id=str(cpu["_id"])) for cpu in cpus]
    except HTTPException:
        raise HTTPException(status_code=404, detail="No CPUs found")
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
        # If cpus is empty count it as no games found error
        if not cpus:
            raise HTTPException(status_code=404, detail="No CPUs found")
        return [Cpu(**cpu, id=str(cpu["_id"])) for cpu in cpus]
    except HTTPException:
        raise HTTPException(status_code=404, detail="No CPUs found")
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
        if not cpus:
            raise HTTPException(status_code=404, detail="No CPUs found")
        return [Cpu(**cpu, id=str(cpu["_id"])) for cpu in cpus]
    except HTTPException:
        raise HTTPException(status_code=404, detail="No CPUs found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CPUs by model: {str(e)}")
