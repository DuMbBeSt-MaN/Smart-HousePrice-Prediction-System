# app/ingestion/safety_ingestor.py

from app.services.overpass_client import query_overpass


def safety_signals(lat: float, lon: float) -> dict:
    """
    Safety-related signals using OpenStreetMap
    """

    radius = 2000  # meters

    police = query_overpass(f"""
        [out:json];
        node["amenity"="police"](around:{radius},{lat},{lon});
        out;
    """)

    fire = query_overpass(f"""
        [out:json];
        node["amenity"="fire_station"](around:{radius},{lat},{lon});
        out;
    """)

    return {
        "police_stations": len(police),
        "fire_stations": len(fire)
    }