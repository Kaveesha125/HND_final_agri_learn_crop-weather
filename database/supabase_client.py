from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

async def get_suitable_crops(avg_temp: float, weekly_rainfall: float) -> list:
    try:
        response = supabase.table("crops").select("*").lte("min_temp", avg_temp).gte("max_temp", avg_temp).lte("min_rainfall", weekly_rainfall).gte("max_rainfall", weekly_rainfall).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Supabase query failed: {str(e)}")