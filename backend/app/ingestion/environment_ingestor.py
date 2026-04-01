# app/ingestion/environment_ingestor.py

import os
import requests
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


def environment_signals(lat: float, lon: float) -> dict:
    GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
    """
    Detect water bodies nearby using Google Maps Places API.
    More water bodies = higher flood/water risk.
    """
    if not GOOGLE_MAPS_KEY:
        print("[Env] GOOGLE_MAPS_KEY not set — returning neutral water_risk")
        return {"water_risk": 0.0}

    try:
        r = requests.get(
            PLACES_URL,
            params={
                "location": f"{lat},{lon}",
                "radius": 2500,
                "keyword": "lake river pond water body",
                "key": GOOGLE_MAPS_KEY,
            },
            timeout=10
        )
        r.raise_for_status()
        count = len(r.json().get("results", []))
        water_risk = min(count / 10.0, 1.0)
        print(f"[Env-Google] water bodies nearby={count}, water_risk={water_risk:.2f}")
        return {"water_risk": water_risk}
    except Exception as e:
        print(f"[Env] Failed: {e}")
        return {"water_risk": 0.0}
