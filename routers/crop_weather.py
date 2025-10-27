from fastapi import APIRouter, HTTPException,Depends
from services.crop_service import recommend_crops, recommend_crops_by_coords,LocationInfo
from models.schemas import WeatherResponse, CropRecommendationsResponse
from services.geocode_service import reverse_geocode
from utils.auth import verify
import asyncio

router = APIRouter(dependencies=[Depends(verify)])
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

        # Get coordinates
        lat, lon = await geocode_location(location)

        # Get weather and location info in parallel
        weather_data_task = get_weather(lat, lon)
        location_info_task = reverse_geocode(lat, lon)

        weather_data, location_info_dict = await asyncio.gather(
            weather_data_task,
            location_info_task
        )

        # Create the location object
        location_details = LocationInfo(
            latitude=lat,
            longitude=lon,
            display_name=location_info_dict.get("display_name"),
            city=location_info_dict.get("city"),
            district=location_info_dict.get("district"),
            province=location_info_dict.get("province"),
            country=location_info_dict.get("country")
        )

        # Return the full response
        return WeatherResponse(
            avg_temp=weather_data["avg_temp"],
            total_rainfall=weather_data["total_rainfall"],
            location=location_details
        )
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