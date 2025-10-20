import httpx

async def get_weather(lat: float, lon: float) -> dict:
    async with httpx.AsyncClient() as client:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto&forecast_days=7"
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()["daily"]
            avg_max_temp = sum(data["temperature_2m_max"]) / len(data["temperature_2m_max"])
            avg_min_temp = sum(data["temperature_2m_min"]) / len(data["temperature_2m_min"])
            total_rainfall = sum(data["precipitation_sum"])
            return {"avg_temp": (avg_max_temp + avg_min_temp) / 2, "total_rainfall": total_rainfall}
        raise ValueError("Weather fetch failed")