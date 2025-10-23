import httpx
import asyncio

async def geocode_location(location: str) -> tuple[float, float]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        headers = {"User-Agent": "AgriLearnApp/1.0 (contact@agrilearn.com) FastAPI"}

        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            if not data:
                raise ValueError(f"Location '{location}' not found")

            return float(data[0]["lat"]), float(data[0]["lon"])
        except httpx.HTTPError as e:
            raise ValueError(f"Geocoding failed: {str(e)}")


async def reverse_geocode(lat: float, lon: float, max_retries: int = 3) -> dict:
    """Convert GPS coordinates to location name with retry logic"""

    # Validate coordinates
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError(f"Invalid coordinates: lat={lat}, lon={lon}")

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
                headers = {"User-Agent": "AgriLearn/1.0 (your.email@example.com)"}

                response = await client.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    # Check if we got valid data
                    if "error" in data:
                        raise ValueError(f"Reverse geocoding error: {data['error']}")

                    address = data.get("address", {})

                    return {
                        "display_name": data.get("display_name", f"{lat}, {lon}"),
                        "city": address.get("city") or address.get("town") or address.get("village") or address.get(
                            "suburb", ""),
                        "district": address.get("state_district") or address.get("county", ""),
                        "province": address.get("state") or address.get("region", ""),
                        "country": address.get("country", "")
                    }
                elif response.status_code == 429:
                    # Rate limit hit - wait before retry
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise ValueError(f"API returned status code {response.status_code}")

        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            raise ValueError("Reverse geocoding request timed out")
        except httpx.HTTPError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            raise ValueError(f"Reverse geocoding failed: {str(e)}")

    raise ValueError("Reverse geocoding failed after multiple attempts")