import asyncio
from .geocode_service import geocode_location, reverse_geocode
from .weather_service import get_weather
from .gemini_service import get_crop_recommendations_from_gemini
from models.schemas import CropRecommendation, CropRecommendationsResponse, WeatherResponse, LocationInfo

async def recommend_crops(location: str) -> CropRecommendationsResponse:
    try:
        # Get coordinates
        lat, lon = await geocode_location(location)

        # Add delay to respect API limits
        await asyncio.sleep(1)

        # Get location info
        location_info_dict = await reverse_geocode(lat, lon)

        # Get weather data
        weather = await get_weather(lat, lon)
        avg_temp = weather["avg_temp"]
        weekly_rainfall = weather["total_rainfall"]

        # Create location info object
        location_info = LocationInfo(
            latitude=lat,
            longitude=lon,
            display_name=location_info_dict["display_name"],
            city=location_info_dict["city"],
            district=location_info_dict["district"],
            province=location_info_dict["province"],
            country=location_info_dict["country"]
        )

        # Get crop recommendations from Gemini
        gemini_recommendations = await get_crop_recommendations_from_gemini(
            weather_info={"avg_temp": avg_temp, "total_rainfall": weekly_rainfall},
            location_info=location_info.dict()
        )

        recommendations = [CropRecommendation(name=rec["name"], details={"description": rec["details"]}) for rec in gemini_recommendations]

        return CropRecommendationsResponse(
            recommendations=recommendations,
            weather=WeatherResponse(
                avg_temp=avg_temp,
                total_rainfall=weekly_rainfall,
                location=location_info
            )
        )
    except Exception as e:
        raise ValueError(f"Failed to get crop recommendations: {str(e)}")


async def recommend_crops_by_coords(lat: float, lon: float) -> CropRecommendationsResponse:
    try:
        # Add delay to respect API limits
        await asyncio.sleep(1)

        # Get location info
        location_info_dict = await reverse_geocode(lat, lon)

        # Get weather data
        weather = await get_weather(lat, lon)
        avg_temp = weather["avg_temp"]
        weekly_rainfall = weather["total_rainfall"]

        # Create location info object
        location_info = LocationInfo(
            latitude=lat,
            longitude=lon,
            display_name=location_info_dict["display_name"],
            city=location_info_dict["city"],
            district=location_info_dict["district"],
            province=location_info_dict["province"],
            country=location_info_dict["country"]
        )

        # Get crop recommendations from Gemini
        gemini_recommendations = await get_crop_recommendations_from_gemini(
            weather_info={"avg_temp": avg_temp, "total_rainfall": weekly_rainfall},
            location_info=location_info.dict()
        )

        recommendations = [CropRecommendation(name=rec["name"], details={"description": rec["details"]}) for rec in gemini_recommendations]

        return CropRecommendationsResponse(
            recommendations=recommendations,
            weather=WeatherResponse(
                avg_temp=avg_temp,
                total_rainfall=weekly_rainfall,
                location=location_info
            )
        )
    except Exception as e:
        raise ValueError(f"Failed to get crop recommendations: {str(e)}")
