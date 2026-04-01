# app/utils/location.py

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def resolve_location(location: dict) -> tuple[float, float]:
    """
    Resolves user location input to (lat, lon)

    Supported formats:
    - { "type": "gps", "lat": ..., "lon": ... }
    - { "type": "city", "value": "Los Angeles, CA" }
    - { "type": "address", "value": "10535 Wilshire Blvd, LA" }
    """

    if not isinstance(location, dict):
        raise ValueError("Location must be an object")

    loc_type = location.get("type")

    # ------------------------
    # GPS MODE
    # ------------------------
    if loc_type == "gps":
        lat = location.get("lat")
        lon = location.get("lon")

        if lat is None or lon is None:
            raise ValueError("GPS location requires lat and lon")

        return float(lat), float(lon)

    # ------------------------
    # CITY / ADDRESS MODE
    # ------------------------
    if loc_type in {"city", "address"}:
        query = location.get("value")

        if not query:
            raise ValueError("City / address requires value")

        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "real-estate-ai-search/1.0"
        }

        resp = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()

        data = resp.json()

        if not data:
            raise ValueError(f"Location not found: {query}")

        return float(data[0]["lat"]), float(data[0]["lon"])

    # ------------------------
    # INVALID TYPE
    # ------------------------
    raise ValueError(f"Unsupported location type: {loc_type}")