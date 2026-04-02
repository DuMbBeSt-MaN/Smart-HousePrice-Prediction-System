from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import re
import json
import traceback
from pathlib import Path

from groq import Groq
import requests
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)

from app.agents.planner_agent import PlannerAgent


class RawTextPayload(BaseModel):
    text: str


router = APIRouter()

try:
    planner = PlannerAgent()
except Exception:
    traceback.print_exc()
    planner = None


def _geocode_with_google(query: str) -> dict:
    GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
    if not GOOGLE_MAPS_KEY:
        raise RuntimeError("GOOGLE_MAPS_KEY not set")
    r = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={"address": query, "key": GOOGLE_MAPS_KEY},
        timeout=10
    )
    results = r.json().get("results", [])
    if not results:
        print(f"[Geocode] No results for '{query}'")
        return {"lat": None, "lon": None}
    loc = results[0]["geometry"]["location"]
    print(f"[Geocode] '{query}' -> lat={loc['lat']}, lon={loc['lng']}")
    return {"lat": loc["lat"], "lon": loc["lng"]}


def _groq_parse(text: str) -> dict:
    # Reload .env every call — guarantees key is present regardless of import order
    load_dotenv(dotenv_path=_ENV_PATH, override=True)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    print(f"[Groq] key present={bool(GROQ_API_KEY)} starts={str(GROQ_API_KEY)[:8] if GROQ_API_KEY else 'NONE'}", flush=True)
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set")

    # Unset broken SSL_CERT_FILE that conda sets to a non-existent path
    ssl_cert = os.environ.get("SSL_CERT_FILE")
    if ssl_cert and not Path(ssl_cert).exists():
        del os.environ["SSL_CERT_FILE"]

    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""You are a real estate search parser for Indian properties.
Extract the following from the user's query and return ONLY a valid JSON object with these exact keys:
- "area_name": specific locality/neighbourhood. Empty string if not mentioned.
- "city": city name. Empty string if not mentioned.
- "state": Indian state, infer from city if needed.
- "features": array of short strings (e.g. ["2 BHK", "for rent", "near schools"]).
- "bhk": integer number of BHK (e.g. 2 for "2 BHK"). null if not mentioned.
- "max_price": maximum monthly rent in INR as integer (e.g. 30000 for "under 30,000"). null if not mentioned.

User query: {text}

JSON:"""

    msg = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=400,
    )
    content = msg.choices[0].message.content.strip()
    print(f"[Groq] Raw response: {content}", flush=True)

    content = re.sub(r"```[a-z]*", "", content).strip()
    start = content.find("{")
    end   = content.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON in Groq response: {content}")
    return json.loads(content[start:end])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/parse")
async def parse_input(request: Request):
    body = await request.body()
    print(f"[/parse] body={body}", flush=True)
    try:
        payload = RawTextPayload.model_validate_json(body)
        text = payload.text.strip()

        load_dotenv(dotenv_path=_ENV_PATH, override=True)
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

        try:
            parsed = _groq_parse(text)
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Groq failed: {type(e).__name__}: {e}")

        area_name = parsed.get("area_name", "").strip()
        city      = parsed.get("city", "").strip()
        state     = parsed.get("state", "").strip()
        features  = parsed.get("features", [])
        print(f"[/parse] area='{area_name}' city='{city}' state='{state}' features={features}", flush=True)

        geocode_query = ", ".join(filter(None, [area_name, city, state, "India"]))
        try:
            coords = _geocode_with_google(geocode_query)
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Geocoding failed: {type(e).__name__}: {e}")

        if coords["lat"] is None:
            raise HTTPException(status_code=400, detail=f"Could not geocode '{geocode_query}'")

        bhk       = parsed.get("bhk")
        max_price = parsed.get("max_price")

        return {
            "location":  coords,
            "area_name": area_name,
            "city":      city,
            "state":     state,
            "features":  features,
            "bhk":       bhk,
            "max_price": max_price,
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@router.post("/search")
def search(payload: dict):
    location = payload.get("location", {})
    lat = location.get("lat")
    lon = location.get("lon")

    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="location.lat and location.lon are required")

    if planner is None:
        raise HTTPException(status_code=500, detail="PlannerAgent failed to initialize")

    results = planner.run(payload=payload)
    return results
