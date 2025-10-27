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

class CropRecommendationsResponse(BaseModel):
    recommendations: str  # Changed from List[CropRecommendation]
    weather: WeatherResponse

class LivestockRequest(BaseModel):
    animal_type: str
    age: float
    number_of_animals: int
    animal_purpose: str
    food_type: str
    additional_information: Optional[str] = None

class LivestockResponse(BaseModel):
    recommendation: str
    animal_type: str
    animal_purpose: str