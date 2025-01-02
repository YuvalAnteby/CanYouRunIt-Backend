from fastapi import FastAPI
from backend.routes import games
import asyncio

from queries import get_all_games
from queries.game_queries import get_game
from queries.hardware_queries import get_gpu_by_brand, get_cpu_by_brand, get_cpu_by_model

app = FastAPI(
    title="Game Requirements API",
    description="An API to retrieve hardware requirements for games",
    version="1.0.0")

# Include routers
app.include_router(games.router, prefix="/api/games", tags=["Games"])

# Middleware or custom exceptions can be added here
async def test_search():
    result = await get_cpu_by_model("3")
    for cpu in result:
        print(cpu)

if __name__ == "__main__":
    asyncio.run(test_search())