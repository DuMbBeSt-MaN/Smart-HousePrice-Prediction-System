# # from fastapi import APIRouter
# # from app.agents.planner_agent import PlannerAgent

# # router = APIRouter()
# # planner = PlannerAgent()

# # @router.get("/health")
# # def health():
# #     return {"status": "ok"}

# # @router.post("/search")
# # def search(payload: dict):
# #     return planner.run(payload)
# # app/api/routes.py

# from fastapi import APIRouter, HTTPException
# from app.agents.planner_agent import PlannerAgent

# router = APIRouter()
# planner = PlannerAgent()


# @router.get("/health")
# def health():
#     return {"status": "ok"}


# @router.post("/search")
# def search(payload: dict):
#     """
#     Expected payload:
#     {
#       "location": {
#         "lat": 34.05,
#         "lon": -118.24
#       },
#       "features": ["cheap", "near colleges", "safe locality"]
#     }
#     """

#     if "location" not in payload or "features" not in payload:
#         raise HTTPException(status_code=400, detail="Invalid request body")

#     location = payload["location"]
#     features = payload["features"]

#     lat = location.get("lat")
#     lon = location.get("lon")

#     if lat is None or lon is None:
#         raise HTTPException(status_code=400, detail="Latitude / Longitude required")

#     results = planner.run(
#         lat=lat,
#         lon=lon,
#         features=features
#     )

#     return {
#         "count": len(results),
#         "results": results
#     }
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import json
import re

try:
    from groq import Groq
except Exception:
    Groq = None

from app.agents.planner_agent import PlannerAgent
from app.services.geocoding import geocode_or_default
from app.storage.crud import get_cached, save_cached


class RawTextPayload(BaseModel):
    text: str

router = APIRouter()
planner = PlannerAgent()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/search")
def search(payload: dict):
    """
    Expected payload:
    {
      "location": { "lat": 34.05, "lon": -118.24 },
      "features": ["near hospitals", "safe", "cheap"]
    }
    """

    location = payload["location"]
    features = payload.get("features", [])

    # Create cache key
    lat = location.get("lat")
    lon = location.get("lon")
    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Latitude / Longitude required")
    
    location_key = f"{lat:.6f},{lon:.6f}"
    
    # Check cache first
    cached = get_cached(location_key, features)
    if cached:
        print(f"[Cache] HIT for {location_key} with features {features}")
        return cached.result_json
    
    # Cache miss - run planner
    print(f"[Cache] MISS for {location_key} with features {features}")
    results = planner.run(
        payload=payload
    )
    
    # Save to cache
    save_cached(location_key, features, results)
    
    return results


@router.post("/parse")
def parse_input(payload: RawTextPayload):
    """Convert free-form user input into structured JSON suitable for `/search`.

    Uses Groq API for fast LLM-based parsing. If Groq is not available,
    falls back to deterministic regex parsing.

    Returns JSON with shape:
    {
      "location": {"lat": <float> | null, "lon": <float> | null},
      "features": ["feature1", "feature2", ...]
    }
    """

    text = payload.text.strip()

    # Try Groq LLM parsing when configured
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and Groq is not None:
        try:
            client = Groq(api_key=api_key)
            prompt = (
                "You are a JSON generator for a real estate search service. Parse the user's search request into "
                "a JSON object with two keys: 'location' and 'features'. \n\n"
                "'location' must be either:\n"
                "  - {\"lat\": <number>, \"lon\": <number>} if coordinates or specific place are mentioned\n"
                "  - {\"lat\": null, \"lon\": null} if no location is clear\n\n"
                "'features' must be an array of short strings describing what they want (e.g., ['cheap', 'near parks', 'safe']).\n\n"
                "IMPORTANT: Extract place names like city/state if mentioned. Return ONLY valid JSON, no markdown or code fences.\n\n"
                f"User input: {text}\n\nJSON:"
            )

            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=300,
            )
            content = message.choices[0].message.content.strip()

            # Parse the JSON response
            try:
                parsed = json.loads(content)
                
                # If lat/lon are null, try to geocode the input text
                if parsed.get("location", {}).get("lat") is None:
                    coords = geocode_or_default(text)
                    if coords["lat"] is not None:
                        parsed["location"] = coords
                
                return parsed
            except Exception:
                # If response has markdown code fences, extract JSON
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    try:
                        parsed = json.loads(content[start:end+1])
                        
                        # Geocode if needed
                        if parsed.get("location", {}).get("lat") is None:
                            coords = geocode_or_default(text)
                            if coords["lat"] is not None:
                                parsed["location"] = coords
                        
                        return parsed
                    except Exception:
                        pass
        except Exception as e:
            # Log error but fall through to deterministic fallback
            print(f"Groq parsing error: {e}")
            pass

    # Deterministic fallback parser
    lat = None
    lon = None
    coords = re.findall(r"([-+]?[0-9]*\.?[0-9]+)\s*,\s*([-+]?[0-9]*\.?[0-9]+)", text)
    if coords:
        try:
            lat = float(coords[0][0])
            lon = float(coords[0][1])
        except Exception:
            lat = None
            lon = None
    
    # If no coordinates, try geocoding place names
    if lat is None and lon is None:
        geocode_result = geocode_or_default(text)
        lat = geocode_result["lat"]
        lon = geocode_result["lon"]

    # Heuristic features: split on commas and common phrases
    features = []
    parts = re.split(r"[,;]| and | or ", text)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # skip coordinate-looking parts
        if re.match(r"^[-+0-9.\s,]+$", p):
            continue
        # drop overly long fragments
        if len(p) > 120:
            continue
        features.append(p)

    return {"location": {"lat": lat, "lon": lon}, "features": features}