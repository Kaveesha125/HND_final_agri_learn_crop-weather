from pydantic import BaseModel
from typing import List, Dict, Optional

class WeatherResponse(BaseModel):
    avg_temp: float
    total_rainfall: float

class CropRecommendation(BaseModel):
    name: str
    details: Optional[Dict]

class CropRecommendationsResponse(BaseModel):
    recommendations: List[CropRecommendation]
    weather: WeatherResponse