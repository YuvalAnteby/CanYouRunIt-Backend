import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from queries.hardware_queries import router as hardware_queries_router
from backend.routes.cpus import router as cpus_router, get_cpu_by_brand, get_cpu_by_model

app = FastAPI()

# Include routers
#app.include_router(games.router, prefix="/api/games", tags=["Games"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Can You Run It Backend!"}

app.include_router(hardware_queries_router, prefix="/api/hardware", tags=["Hardware"])
app.include_router(cpus_router, prefix="/api/hardware", tags=["CPUs"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Middleware or custom exceptions can be added here
async def test_search():
    result = await get_cpu_by_model("3600")
    for cpu in result:
        print(cpu)

if __name__ == "__main__":
    asyncio.run(test_search())
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)