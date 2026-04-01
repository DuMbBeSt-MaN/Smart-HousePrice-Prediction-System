# app/ingestion/places_ingestor.py

import os
import requests

from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


def _count_places(lat: float, lon: float, keyword: str, radius: int) -> int:
    GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
    if not GOOGLE_MAPS_KEY:
        print("[Places] GOOGLE_MAPS_KEY not set")
        return 0
    try:
        r = requests.get(
            PLACES_URL,
            params={
                "location": f"{lat},{lon}",
                "radius": radius,
                "keyword": keyword,
                "key": GOOGLE_MAPS_KEY,
            },
            timeout=10
        )
        r.raise_for_status()
        results = r.json().get("results", [])
        return len(results)
    except Exception as e:
        print(f"[Places] Failed for keyword='{keyword}': {e}")
        return 0


def places_signals(lat: float, lon: float) -> dict:
    """
    Fetch nearby place counts using Google Maps Places API.
    Returns raw counts — planner normalises them.
    """
    schools   = _count_places(lat, lon, "school",   radius=1500)
    hospitals = _count_places(lat, lon, "hospital", radius=3000)
    parks     = _count_places(lat, lon, "park",     radius=1200)

    print(f"[Places-Google] schools={schools}, hospitals={hospitals}, parks={parks}")
    return {"schools": schools, "hospitals": hospitals, "parks": parks}
