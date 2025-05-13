import requests
import pymongo
import asyncio

from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

API_KEY = "ff0e945f6f964e898f7158eee7993f3c"
BASE_URL = "https://api.rawg.io/api/games"

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client["game_db"]
collection = db.games


# Define helper functions
def parse_rawg_game(rawg_game):
    name = rawg_game["name"]
    print(f"\nAdding: {name}")

    # Ask you only for what RAWG doesn't provide
    developer = input(f"Developer for '{name}': ")
    description = input(f"Short description for '{name}': ")
    upscalers = input(f"Upscalers supported (comma-separated) for '{name}': ").split(",")
    apis = input(f"Supported APIs (comma-separated) for '{name}' [default: DirectX 11]: ").split(",") or ["DirectX 11"]
    is_ssd_recommended = input(f"Is SSD recommended for '{name}'? (y/n) [default: y]: ") or "y"

    return {
        "game_id": str(rawg_game["id"]),
        "name": name,
        "publisher": "Unknown",
        "developer": developer.strip(),
        "release_date": int(rawg_game.get("released", "1970-01-01").replace("-", "")),
        "genres": [g["name"] for g in rawg_game.get("genres", [])],
        "desc": description.strip(),
        "trailer_url": "",
        "portrait_url": rawg_game.get("background_image", ""),
        "buy_links": [f"https://{s['store']['domain']}" for s in rawg_game.get("stores", [])],
        "available_resolutions": ["1920x1080", "2560x1440", "3840x2160"],
        "supported_settings": ["Low", "Medium", "High", "Ultra"],
        "is_ssd_recommended": is_ssd_recommended.lower().startswith("y"),
        "upscale_support": [u.strip() for u in upscalers if u.strip()],
        "api_support": [a.strip() for a in apis if a.strip()],
        "created_at": datetime.now(timezone.utc)
    }

async def main():
    params = {
        "key": API_KEY,
        "ordering": "-released",
        "page_size": 5
    }

    response = requests.get(BASE_URL, params=params)
    games = response.json()["results"]

    for game in games:
        existing = await collection.find_one({"game_id": str(game["id"])})
        if existing:
            print(f"⚠️ Game '{game['name']}' already exists in the database. Skipping.")
            continue

        doc = parse_rawg_game(game)
        result = await collection.insert_one(doc)
        print(f"✅ Inserted: {doc['name']}")


if __name__ == "__main__":
    asyncio.run(main())