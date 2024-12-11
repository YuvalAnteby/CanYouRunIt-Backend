from fastapi import FastAPI
from app.routes import games

app = FastAPI(
    title="Game Requirements API",
    description="An API to retrieve hardware requirements for games",
    version="1.0.0"
)

# Include routers
app.include_router(games.router, prefix="/api/games", tags=["Games"])

# Middleware or custom exceptions can be added here
