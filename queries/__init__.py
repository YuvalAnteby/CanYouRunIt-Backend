"""
Queries module: Contains MongoDB query functions for the DB.

Modules:
- games_queries: Functions for handling game-related database operations.
- hardware_queries: Functions for handling hardware-related database operations.
"""

from motor.motor_asyncio import AsyncIOMotorClient

# Import specific functions or classes to expose them at the package level
from .game_queries import create_game, get_all_games, add_hardware_to_requirement, add_requirement_to_game
from .hardware_queries import add_cpu, add_gpu

# TODO remove after finishing editing DB

# Connect to MongoDB (this assumes MongoDB is running on localhost)
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]  # Use your desired database name