import httpx

async def geocode_location(location: str) -> tuple[float, float]:
    async with httpx.AsyncClient() as client:
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        headers = {"User-Agent": "AgriLearn/1.0 (your.email@example.com)"}
        response = await client.get(url, headers=headers)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data["lat"]), float(data["lon"])
        raise ValueError("Invalid location")