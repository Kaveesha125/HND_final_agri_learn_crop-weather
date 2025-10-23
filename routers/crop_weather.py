from fastapi import APIRouter, HTTPException
from services.crop_service import recommend_crops, recommend_crops_by_coords
from models.schemas import WeatherResponse, CropRecommendationsResponse
from services.geocode_service import reverse_geocode
router = APIRouter()
@router.get("/")
async def health_check():
    return {"site is up"}

@router.get("/geocode")
async def geocode(location: str):
    try:
        from services.geocode_service import geocode_location
        lat, lon = await geocode_location(location)
        return {"latitude": lat, "longitude": lon}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location")

@router.get("/reverse_geocode")
async def reverse_geocode_endpoint(lat: float, lon: float):
    """Convert GPS coordinates to location name"""
    try:
        return await reverse_geocode(lat, lon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/weather", response_model=WeatherResponse)
async def weather(location: str):
    try:
        from services.geocode_service import geocode_location
        from services.weather_service import get_weather
        lat, lon = await geocode_location(location)
        return await get_weather(lat, lon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/recommend_crops", response_model=CropRecommendationsResponse)
async def get_crop_recommendations(location: str):
    try:
        return await recommend_crops(location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get("/recommend_crops_by_coords", response_model=CropRecommendationsResponse)
async def get_crop_recommendations_by_coords(lat: float, lon: float):
    try:
        return await recommend_crops_by_coords(lat, lon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")