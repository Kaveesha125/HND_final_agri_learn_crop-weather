import google.generativeai as genai
from models.schemas import LivestockRequest, LivestockResponse

# System prompts for different livestock purposes
SYSTEM_PROMPTS = {
    "dairy": "You are a dairy farm nutrition expert. Provide detailed feed recommendations focusing on milk production quality and quantity. Consider calcium, protein, and energy balance.",
    "meat": "You are a livestock meat production specialist. Provide feed recommendations optimized for healthy growth, muscle development, and meat quality.",
    "breeding": "You are a livestock breeding expert. Provide comprehensive nutritional guidance for optimal reproductive health and genetic potential.",
    "draft": "You are a working animal nutrition specialist. Provide feed recommendations for animals used in farm work, focusing on energy and endurance.",
    "general": "You are a general livestock nutrition consultant. Provide balanced feed recommendations for overall health and productivity."
}

def get_system_prompt(animal_purpose: str) -> str:
    """Dynamically select the appropriate system prompt based on animal purpose."""
    return SYSTEM_PROMPTS.get(animal_purpose.lower(), SYSTEM_PROMPTS["general"])

async def get_livestock_recommendations(livestock_data: LivestockRequest) -> LivestockResponse:
    """
    Get livestock feed and management recommendations from the Gemini API.
    """
    try:
        # The Gemini API key is configured in gemini_service.py, which is loaded at startup.
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        system_prompt = get_system_prompt(livestock_data.animal_purpose)

        prompt = f"""{system_prompt}

Based on the following livestock information, provide detailed feed and management recommendations:

- Animal Type: {livestock_data.animal_type}
- Age: {livestock_data.age} years
- Number of Animals: {livestock_data.number_of_animals}
- Animal Purpose: {livestock_data.animal_purpose}
- Food Type: {livestock_data.food_type}
- Additional Information: {livestock_data.additional_information or 'None'}

Please provide:
1. Recommended daily feed quantity and composition.
2. Nutritional requirements (protein, energy, minerals, vitamins).
3. A suitable feeding schedule.
4. Health and wellness considerations.
5. Any special care recommendations.

Format the entire response in Markdown for clear presentation (e.g., using headings, bold text, and lists).
"""
        response = await model.generate_content_async(prompt)

        return LivestockResponse(
            recommendation=response.text,
            animal_type=livestock_data.animal_type,
            animal_purpose=livestock_data.animal_purpose
        )
    except Exception as e:
        # It's good practice to log the actual error e
        raise Exception(f"Failed to get livestock recommendations from Gemini: {str(e)}")