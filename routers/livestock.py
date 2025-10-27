from fastapi import APIRouter, HTTPException,Depends
from services.livestock_service import get_livestock_recommendations
from models.schemas import LivestockRequest, LivestockResponse
from utils.auth import verify

router = APIRouter(prefix="/livestock", tags=["livestock"],dependencies=[Depends(verify)])

@router.post("/calculate", response_model=LivestockResponse)
async def calculate_livestock_feed(livestock_data: LivestockRequest):
    """
    Calculates livestock feed recommendations based on the following input:
    - animal_type: Type of animal (e.g., 'cow', 'chicken')
    - age: Age of the animal in months
    - number_of_animals: The number of animals
    - animal_purpose: Purpose of the animal (e.g., 'dairy', 'meat')
    - food_type: Type of food available (e.g., 'grass', 'maize')
    - additional_information: Optional additional information
    """
    try:
        return await get_livestock_recommendations(livestock_data)
    except Exception as e:
        # It's good practice to log the actual error e
        raise HTTPException(status_code=500, detail=str(e))