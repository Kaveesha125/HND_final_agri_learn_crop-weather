import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API key
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
else:
    raise ValueError("GEMINI_API_KEY not found in .env file")

async def get_crop_recommendations_from_gemini(weather_info: dict, location_info: dict) -> list:
    """
    Get crop recommendations from the Gemini API based on weather and location.
    """
    if not gemini_api_key:
        raise ValueError("Gemini API key is not configured.")

    model = genai.GenerativeModel('gemini-flash-lite-latest')
    prompt = f"""
    Based on the following weather information for {location_info.get('display_name', 'the location')}:
    - Average Temperature: {weather_info['avg_temp']:.2f}°C
    - Total Weekly Rainfall: {weather_info['total_rainfall']:.2f} mm

    Please recommend 5 crops suitable for planting in this region.
    For each crop, provide a short description of why it is suitable.
    The output should be a JSON array of objects, where each object has 'name' and 'details' keys.
    For example:
    [
        {{"name": "Crop Name", "details": "Reason for recommendation."}},
        ...
    ]
    """
    try:
        response = await model.generate_content_async(prompt)
        # Clean the response to extract only the JSON part
        cleaned_response = response.text.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        return json.loads(cleaned_response)
    except Exception as e:
        raise Exception(f"Failed to get recommendations from Gemini: {str(e)}")

