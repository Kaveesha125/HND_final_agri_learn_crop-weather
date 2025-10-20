import httpx
from dotenv import load_dotenv
import os
from typing import Optional, Dict

load_dotenv()
plant_id_api_key = os.getenv("PLANT_ID_API_KEY")

async def get_plant_details(plant_name: str) -> Optional[Dict]:
    async with httpx.AsyncClient() as client:
        url = "https://api.plant.id/v3/details"
        payload = {"common_names": [plant_name], "language": "en"}
        headers = {"Api-Key": plant_id_api_key, "Content-Type": "application/json"}
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None