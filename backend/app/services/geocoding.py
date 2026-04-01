"""
Geocoding service using OpenStreetMap Nominatim API
Converts place names (city, state) to latitude/longitude without API keys
"""

import requests
from functools import lru_cache


OSM_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


@lru_cache(maxsize=100)
def geocode_place(place_name: str, timeout: int = 5) -> tuple[float, float] | None:
    """
    Geocode a place name (e.g., "Austin, Texas") to lat/lon using OpenStreetMap Nominatim API.
    
    Args:
        place_name: Location string (e.g., "Austin, Texas" or "Los Angeles")
        timeout: Request timeout in seconds
    
    Returns:
        (lat, lon) tuple or None if not found
    """
    if not place_name or not isinstance(place_name, str):
        return None

    try:
        params = {
            "q": place_name,
            "format": "json",
            "limit": 1
        }
        
        headers = {
            "User-Agent": "HomeFinder-App/1.0 (+http://localhost)"
        }

        response = requests.get(
            OSM_NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        
        results = response.json()
        
        if not results:
            return None
        
        # Extract lat/lon from first result
        first_result = results[0]
        lat = float(first_result.get("lat"))
        lon = float(first_result.get("lon"))
        
        return (lat, lon)
    
    except Exception as e:
        print(f"Geocoding error for '{place_name}': {e}")
        return None


def geocode_or_default(place_name: str, default_coords: tuple[float, float] | None = None) -> dict:
    """
    Geocode a place, returning dict with lat/lon.
    Falls back to default coordinates if geocoding fails.
    
    Args:
        place_name: Location string
        default_coords: (lat, lon) tuple to use if geocoding fails
    
    Returns:
        {"lat": float, "lon": float} or {"lat": None, "lon": None}
    """
    result = geocode_place(place_name)
    
    if result:
        return {"lat": result[0], "lon": result[1]}
    
    if default_coords:
        return {"lat": default_coords[0], "lon": default_coords[1]}
    
    return {"lat": None, "lon": None}
