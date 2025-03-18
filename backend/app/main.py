from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.routes.cpus import router as cpus_router
from backend.routes.gpus import router as gpus_router

app = FastAPI()

# Include routers
#app.include_router(games.router, prefix="/api/games", tags=["Games"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Can You Run It Backend!"}

app.include_router(cpus_router, prefix="/api/hardware", tags=["CPUs"])
app.include_router(gpus_router, prefix="/api/hardware", tags=["GPUs"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

if __name__ == "__main__":
    #test_search()
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)