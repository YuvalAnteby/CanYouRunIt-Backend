import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from backend.routes.cpus import router as cpus_router

# Create a temporary app with only this router for testing
app = FastAPI()
app.include_router(cpus_router)


@pytest.mark.asyncio
async def test_get_all_cpus_returns_list_of_cpus_only(async_client, fake_cpus_list):
    """
    Test: /cpus should return 200 and only CPUs when data is valid
    :param async_client:
    :param fake_cpus_list:
    """
    # Patch the MongoDB collection.find() call to use our mocked cursor
    mock_cursor = AsyncMock()
    mock_cursor.to_list = AsyncMock(return_value=fake_cpus_list)
    with patch("backend.routes.cpus.collection.find", return_value=mock_cursor):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/cpus")

    assert response.status_code == 200
    assert all(cpu["type"].lower() == "cpu" for cpu in response.json())


@pytest.mark.asyncio
async def test_get_all_cpus_when_gpu_included(async_client, fake_gpus_list):
    """
    Test: /cpus should return 500 if GPU entries are accidentally returned
    :param async_client:
    :param fake_gpus_list:
    """
    # Mock the DB to return GPUs (invalid for this route)
    mock_cursor = AsyncMock()
    mock_cursor.to_list = AsyncMock(return_value=fake_gpus_list)
    with patch("backend.routes.cpus.collection.find", return_value=mock_cursor):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/cpus")

    assert response.status_code == 500
    assert response.json()["detail"] == "Non-CPU hardware found in CPU route"


@pytest.mark.asyncio
async def test_get_cpu_by_model_returns_404_when_no_model_exist(async_client):
    """
    Test: /cpus/model should return 404 when no CPU matches the query
    :param async_client:
    """
    # Simulate DB returning an empty list for a non-existent model
    mock_cursor = AsyncMock()
    mock_cursor.to_list = AsyncMock(return_value=[])
    with patch("backend.routes.cpus.collection.find", return_value=mock_cursor):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/cpus/model",
                                    params={"model": "nonexistent model"})

    assert response.status_code == 404
    assert response.json()["detail"] == "No CPUs found"
