import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from backend.routes.cpus import router as cpus_router

# Create a temporary app with only this router for testing
app = FastAPI()
app.include_router(cpus_router)
