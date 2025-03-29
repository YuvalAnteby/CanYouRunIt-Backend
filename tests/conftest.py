import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from backend.routes.requirements import router as requirements_router
from backend.routes.games import router as games_router

@pytest.fixture
def test_app():
    """
    Creates a minimal FastAPI app with only the relevant routers.
    Can be reused in any test.
    """
    app = FastAPI()
    app.include_router(requirements_router)
    app.include_router(games_router)
    return app

@pytest.fixture
async def async_client(test_app: FastAPI):
    """
    Reusable async client for sending requests to test_app.
    Use this in tests like:

        async def test_something(async_client):
            response = await async_client.get("/games")
    """
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture
def fake_game():
    """
    Returns a dictionary that looks like a real game from the DB.
    Reuse in your game-related tests.
    """
    return {
        "game_id": "g1",
        "name": "Test Game",
        "publisher": "Test Publisher",
        "developer": "Test Dev",
        "release_date": 2024,
        "genres": ["Action"],
        "desc": "Just a test.",
        "trailer_url": "https://example.com/trailer",
        "portrait_url": "https://example.com/portrait",
        "landscape_s": "...",
        "landscape_m": "...",
        "landscape_l": "...",
        "landscape_xl": "...",
        "buy_links": ["https://store.com"],
        "available_resolutions": ["1920x1080"],
        "supported_settings": ["High", "Ultra"],
        "id": "some-mongo-id"
    }