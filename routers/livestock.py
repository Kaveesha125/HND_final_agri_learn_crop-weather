from fastapi import APIRouter, HTTPException
from services.livestock_service import get_livestock_recommendations
from models.schemas import LivestockRequest, LivestockResponse

router = APIRouter(prefix="/livestock", tags=["livestock"])

@router.post("/calculate", response_model=LivestockResponse)
async def calculate_livestock_feed(livestock_data: LivestockRequest):
    try:
        return await get_livestock_recommendations(livestock_data)
    except Exception as e:
        # It's good practice to log the actual error e
        raise HTTPException(status_code=500, detail=str(e))