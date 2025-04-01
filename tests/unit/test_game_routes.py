import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from backend.routes.games import router as games_router

# Create a temporary app with only this router for testing
app = FastAPI()
app.include_router(games_router)


@pytest.mark.asyncio
async def test_get_all_games_returns_list(async_client, fake_game):
    mock_cursor = AsyncMock()
    mock_cursor.to_list = AsyncMock(return_value=[fake_game])
    with patch("backend.routes.games.collection.find", return_value=mock_cursor):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/games")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test Game1"


@pytest.mark.asyncio
async def test_get_all_games_returns_404_when_games_not_found(async_client):
    mock_cursor = AsyncMock()
    mock_cursor.to_list = AsyncMock(return_value=None)

    with patch("backend.routes.games.collection.find", return_value=mock_cursor):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/games")
        assert response.status_code == 404
        assert response.json() == {"detail": "No games found"}
