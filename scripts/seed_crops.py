from supabase import create_client, Client
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

async def seed_crops():
    crops = [
        {"name": "Rice", "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 100.0, "max_rainfall": 200.0, "soil_type": "clay"},
        {"name": "Wheat", "min_temp": 10.0, "max_temp": 25.0, "min_rainfall": 50.0, "max_rainfall": 100.0, "soil_type": "loamy"},
        {"name": "Maize", "min_temp": 15.0, "max_temp": 30.0, "min_rainfall": 60.0, "max_rainfall": 150.0, "soil_type": "sandy"},
    ]
    try:
        response = supabase.table("crops").insert(crops).execute()
        print("Crops seeded:", response.data)
    except Exception as e:
        print("Error seeding crops:", str(e))

if __name__ == "__main__":
    asyncio.run(seed_crops())