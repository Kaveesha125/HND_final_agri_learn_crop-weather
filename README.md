# Agri-Learn Crop & Weather Service

> [!NOTE]
> 🌾 This is a **sub-microservice** of the main website for the **HND Final Project**.

FastAPI service for providing weather data, location geocoding, and AI-powered crop and livestock recommendations. It uses [Gemini](https://gemini.google.com/app) for recommendations, [Open-Meteo](https://open-meteo.com/) for weather, [Nominatim](https://nominatim.openstreetmap.org/) for geocoding, and [Supabase](https://supabase.com/) for authentication.

## Quick Start

1.  **Create virtual environment & install dependencies**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2.  **Configure environment variables**
    ```powershell
    SUPABASE_URL=your-supabase-url
    SUPABASE_KEY=your-supabase-key
    GEMINI_API_KEY="your-gemini-api-key"
    ```
>  [!IMPORTANT]
> **You must add these to a `.env` file.**

4.  **Run the server**
    ```bash
    # Runs on http://localhost:8000
    uvicorn main:app --reload
    ```

## Authentication

This service is protected. All endpoints require a valid Supabase JWT. The server validates the token from either:

* An `access_token` cookie.
* An `Authorization: Bearer <token>` header.
* `X-User-Id` and `X-User-Role` headers (if injected by an API gateway).

## API Endpoints

> Base URL: `http://localhost:8000`

> [!TIP]
> This service includes interactive API documentation (Swagger UI). Once the server is running, you can test all endpoints at: **`http://localhost:8000/docs`**

---

### Crop & Weather

* **GET `/`**
    * Health check to confirm the service is running. (No input needed).

* **GET `/geocode`**
    * Converts a location name (e.g., "Colombo") into coordinates.
    * **Example Input (in Swagger UI):**
        * `location`: `Kandy`

* **GET `/reverse_geocode`**
    * Converts GPS coordinates into a location name and address details.
    * **Example Input (in Swagger UI):**
        * `lat`: `6.9271`
        * `lon`: `79.8612`

* **GET `/weather`**
    * Gets 7-day average weather (temp, rainfall) and location info for a named location.
    * **Example Input (in Swagger UI):**
        * `location`: `Jaffna`

* **GET `/recommend_crops`**
    * Gets AI-powered crop recommendations based on the weather at a named location.
    * **Example Input (in Swagger UI):**
        * `location`: `Matara`

* **GET `/recommend_crops_by_coords`**
    * Gets AI-powered crop recommendations based on the weather at specific coordinates.
    * **Example Input (in Swagger UI):**
        * `lat`: `7.2906`
        * `lon`: `80.6337`

---

### Livestock

* **POST `/livestock/calculate`**
    * Calculates detailed livestock feed and management recommendations based on user input.
    * **Example Request Body (in Swagger UI):**
        ```json
        {
          "animal_type": "Dairy Cow",
          "age": 4.5,
          "number_of_animals": 10,
          "animal_purpose": "dairy",
          "food_type": "grass and silage",
          "additional_information": "Previously had issues with milk fever."
        }
        ```

---

> [!TIP]
> Get your API keys here: [Gemini](https://aistudio.google.com/app/api-keys) | [Supabase](https://supabase.com/).

