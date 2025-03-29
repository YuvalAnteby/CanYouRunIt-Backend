import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from backend.routes.games import router as games_router

# Create a temporary app with only this router for testing
app = FastAPI()
app.include_router(games_router)


async def test_get_all_games_returns_list(async_client, fake_game):
    with patch("backend.routes.games.get_all_games", new_callable=AsyncMock) as mock_handler:
        mock_handler.return_value = [fake_game]
        response = await async_client.get("/games")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test Game"
