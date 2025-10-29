from fastapi import FastAPI
from dotenv import load_dotenv
import os

from starlette.middleware.cors import CORSMiddleware

from routers import crop_weather, livestock
import services.gemini_service  # Import to ensure API key is configured on startup

load_dotenv()

app = FastAPI(title="Agri Learn Crop & Weather Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount routers
app.include_router(crop_weather.router)
app.include_router(livestock.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)