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










