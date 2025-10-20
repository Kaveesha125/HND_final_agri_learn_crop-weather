from .geocode_service import geocode_location
from .weather_service import get_weather
from .plant_service import get_plant_details
from models.schemas import CropRecommendation, CropRecommendationsResponse, WeatherResponse

CROPS = [
    {"name": "Rice", "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 100.0, "max_rainfall": 200.0, "soil_type": "clay"},
    {"name": "Wheat", "min_temp": 10.0, "max_temp": 25.0, "min_rainfall": 50.0, "max_rainfall": 100.0, "soil_type": "loamy"},
    {"name": "Maize", "min_temp": 15.0, "max_temp": 30.0, "min_rainfall": 60.0, "max_rainfall": 150.0, "soil_type": "sandy"},
]

async def recommend_crops(location: str) -> CropRecommendationsResponse:
    lat, lon = await geocode_location(location)
    weather = await get_weather(lat, lon)
    avg_temp = weather["avg_temp"]
    weekly_rainfall = weather["total_rainfall"]

    recommendations = []
    for crop in CROPS:
        if (crop["min_temp"] <= avg_temp <= crop["max_temp"] and
            crop["min_rainfall"] <= weekly_rainfall <= crop["max_rainfall"]):
            details = await get_plant_details(crop["name"])
            recommendations.append(CropRecommendation(name=crop["name"], details=details))

    return CropRecommendationsResponse(
        recommendations=recommendations,
        weather=WeatherResponse(avg_temp=avg_temp, total_rainfall=weekly_rainfall)
    )