from pydantic import BaseModel
from typing import List, Dict, Optional

class LocationInfo(BaseModel):
    latitude: float
    longitude: float
    display_name: str
    city: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None

class WeatherResponse(BaseModel):
    avg_temp: float
    total_rainfall: float
    location: Optional[LocationInfo] = None

class CropRecommendation(BaseModel):
    name: str
    details: Optional[Dict]

class CropRecommendationsResponse(BaseModel):
    recommendations: List[CropRecommendation]
    weather: WeatherResponse