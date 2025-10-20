from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routers import crop_weather

load_dotenv()

app = FastAPI(title="Agri Learn Crop & Weather Service")

# Mount routers
app.include_router(crop_weather.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)