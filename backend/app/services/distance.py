# # # # # import uuid

# # # # # def fetch_listings(lat, lon):
# # # # #     return [{
# # # # #         "id": str(uuid.uuid4()),
# # # # #         "price": 42000,
# # # # #         "bhk": 3,
# # # # #         "lat": lat,
# # # # #         "lon": lon,
# # # # #         "title": "3 BHK Apartment",
# # # # #         "description": "Spacious apartment near city center",
# # # # #         "image": "https://example.com/house.jpg",
# # # # #         "url": "https://www.zillow.com/"
# # # # #     }]
# # # # import requests
# # # # import os

# # # # ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")

# # # # def fetch_listings(lat, lon, radius=5):
# # # #     # url = "https://zillow-com1.p.rapidapi.com"

# # # #     # headers = {
# # # #     #     "X-RapidAPI-Key": ZILLOW_API_KEY,
# # # #     #     "X-RapidAPI-Host": "zillow-unofficial-api.p.rapidapi.com"
# # # #     # }
# # # #     import requests

# # # #     url = "https://realtor-search.p.rapidapi.com/agents/v2/listings"

# # # #     querystring = {"fulfillmentId":"3155600"}

# # # #     headers = {
# # # #         "x-rapidapi-key": ZILLOW_API_KEY,
# # # #         "x-rapidapi-host": "realtor-search.p.rapidapi.com"
# # # #     }


# # # #     params = {
# # # #             "latitude": lat,
# # # #             "longitude": lon,
# # # #             "radius": radius,
# # # #             "home_type": "Houses,Apartments"
# # # #         }

# # # #     response = requests.get(url, headers=headers, params=params)
# # # #     data = response.json()

# # # #     listings = []
# # # #     for item in data.get("props", []):
# # # #         listings.append({
# # # #             "id": str(item["zpid"]),
# # # #             "price": item.get("price", 0),
# # # #             "bhk": item.get("bedrooms", 0),
# # # #             "lat": item["latitude"],
# # # #             "lon": item["longitude"],
# # # #             "title": item.get("streetAddress", "Property"),
# # # #             "description": item.get("description", ""),
# # # #             "image": item.get("imgSrc"),
# # # #             "url": f"https://www.zillow.com{item.get('detailUrl','')}"
# # # #         })

# # # #     return listings
# # # import requests
# # # import os

# # # RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# # # def fetch_listings(lat, lon, radius=10):
# # #     url = "https://realtor-search.p.rapidapi.com/agents/v2/listings"

# # #     headers = {
# # #         "x-rapidapi-key": RAPIDAPI_KEY,
# # #         "x-rapidapi-host": "realtor-search.p.rapidapi.com"
# # #     }

# # #     params = {
# # #         "latitude": lat,
# # #         "longitude": lon,
# # #         "radius": radius
# # #     }

# # #     response = requests.get(url, headers=headers, params=params)
# # #     response.raise_for_status()

# # #     data = response.json()
# # #     homes = data.get("data", {}).get("home_search", {}).get("results", [])

# # #     listings = []

# # #     for home in homes:
# # #         addr = home.get("location", {}).get("address", {})
# # #         coord = home.get("location", {}).get("coordinate", {})
# # #         photo = home.get("primary_photo", {})

# # #         listings.append({
# # #             "id": home.get("property_id"),
# # #             "price": home.get("list_price"),
# # #             "bhk": home.get("beds"),
# # #             "lat": coord.get("lat"),
# # #             "lon": coord.get("lon"),
# # #             "title": addr.get("line", "Property"),
# # #             "description": f"{home.get('beds', '')} BHK house in {addr.get('city', '')}",
# # #             "image": photo.get("href"),
# # #             "url": f"https://www.realtor.com/realestateandhomes-detail/{home.get('permalink')}"
# # #         })

# # #     return listings
# # # import os
# # # import requests
# # # from dotenv import load_dotenv
# # # load_dotenv()
# # # RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
# # # RENTCAST_BASE_URL = "https://api.rentcast.io/v1/listings/sale"


# # # def fetch_listings(
# # #     city: str | None = None,
# # #     state: str | None = None,
# # #     lat: float | None = None,
# # #     lon: float | None = None,
# # #     limit: int = 20
# # # ):
# # #     """
# # #     Fetch for-sale property listings from RentCast
# # #     Returns normalized listing objects for DB ingestion
# # #     """

# # #     headers = {
# # #         "X-Api-Key": RENTCAST_API_KEY
# # #     }

# # #     params = {
# # #         "limit": limit
# # #     }

# # #     # ---- location handling ----
# # #     if city and state:
# # #         params["city"] = city
# # #         params["state"] = state
# # #     elif lat and lon:
# # #         params["latitude"] = lat
# # #         params["longitude"] = lon
# # #     else:
# # #         raise ValueError("Either city+state or lat+lon must be provided")

# # #     response = requests.get(RENTCAST_BASE_URL, headers=headers, params=params)

# # #     if response.status_code != 200:
# # #         raise Exception(f"RentCast error: {response.text}")

# # #     data = response.json()

# # #     listings = []

# # #     for item in data:
# # #         listings.append({
# # #             "external_id": item.get("id"),
# # #             "price": item.get("price"),
# # #             "beds": item.get("bedrooms"),
# # #             "baths": item.get("bathrooms"),
# # #             "sqft": item.get("squareFootage"),
# # #             "lat": item.get("latitude"),
# # #             "lon": item.get("longitude"),
# # #             "address": item.get("formattedAddress"),
# # #             "city": item.get("city"),
# # #             "state": item.get("state"),
# # #             "zip": item.get("zipCode"),
# # #             "property_type": item.get("propertyType"),
# # #             "year_built": item.get("yearBuilt"),
# # #             "image": item.get("listingImageUrl"),
# # #             "url": item.get("listingUrl"),
# # #             "source": "rentcast"
# # #         })

# # #     return listings
# # import os
# # import requests
# # import urllib.parse

# # # =========================
# # # ENV
# # # =========================
# # RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
# # GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")

# # RENTCAST_BASE_URL = "https://api.rentcast.io/v1/properties"


# # # =========================
# # # GOOGLE URL BUILDER
# # # =========================
# # def build_google_url(address: str):
# #     if not address:
# #         return None
# #     q = urllib.parse.quote(f"{address} real estate for sale")
# #     return f"https://www.google.com/search?q={q}"


# # # =========================
# # # GOOGLE STREET VIEW IMAGE
# # # =========================
# # def build_street_view(lat, lon):
# #     if not GOOGLE_MAPS_KEY or not lat or not lon:
# #         return None

# #     return (
# #         "https://maps.googleapis.com/maps/api/streetview"
# #         f"?size=600x400&location={lat},{lon}"
# #         f"&key={GOOGLE_MAPS_KEY}"
# #     )


# # # =========================
# # # FETCH LISTINGS (CORE)
# # # =========================
# # def fetch_listings_by_city_state(city: str, state: str, limit: int = 20):
# #     """
# #     Single API call:
# #     - Gets houses from RentCast
# #     - Enriches with Google URL + image
# #     """

# #     if not RENTCAST_API_KEY:
# #         raise Exception("RENTCAST_API_KEY not set")

# #     url = f"{RENTCAST_BASE_URL}/for-sale"

# #     headers = {
# #         "X-Api-Key": RENTCAST_API_KEY
# #     }

# #     params = {
# #         "city": city,
# #         "state": state,
# #         "limit": limit
# #     }

# #     response = requests.get(url, headers=headers, params=params)
# #     response.raise_for_status()

# #     raw = response.json()
# #     listings = []

# #     for item in raw:
# #         lat = item.get("latitude")
# #         lon = item.get("longitude")
# #         address = item.get("formattedAddress")

# #         listings.append({
# #             "external_id": item.get("id"),
# #             "price": item.get("price"),
# #             "beds": item.get("bedrooms"),
# #             "baths": item.get("bathrooms"),
# #             "sqft": item.get("squareFootage"),
# #             "lat": lat,
# #             "lon": lon,
# #             "address": address,
# #             "city": item.get("city"),
# #             "state": item.get("state"),
# #             "zip": item.get("zipCode"),
# #             "property_type": item.get("propertyType"),
# #             "year_built": item.get("yearBuilt"),

# #             # 🔥 enrichment happens here
# #             # "url": build_google_url(address),
# #             # "image": build_street_view(lat, lon),

# #             "source": "rentcast"
# #         })

# #     return listings
# import os
# import requests
# import urllib.parse
# from typing import List, Dict, Optional

# # =====================================================
# # ENV
# # =====================================================
# RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")

# if not RENTCAST_API_KEY:
#     raise RuntimeError("RENTCAST_API_KEY not set")

# RENTCAST_BASE_URL = "https://api.rentcast.io/v1/properties/for-sale"


# # =====================================================
# # HELPERS
# # =====================================================
# def build_google_search_url(address: Optional[str]) -> Optional[str]:
#     """
#     Safe fallback URL for frontend preview
#     (no scraping, no legal risk)
#     """
#     if not address:
#         return None
#     q = urllib.parse.quote(f"{address} real estate for sale")
#     return f"https://www.google.com/search?q={q}"


# # =====================================================
# # CORE FETCH FUNCTION (CITY + STATE)
# # =====================================================
# def fetch_listings_by_city_state(
#     city: str,
#     state: str,
#     limit: int = 20
# ) -> List[Dict]:
#     """
#     Fetch real for-sale properties from RentCast
#     Uses ONE API call
#     """

#     headers = {
#         "X-Api-Key": RENTCAST_API_KEY
#     }

#     params = {
#         "city": city,
#         "state": state,
#         "limit": limit
#     }

#     response = requests.get(
#         RENTCAST_BASE_URL,
#         headers=headers,
#         params=params,
#         timeout=20
#     )

#     response.raise_for_status()
#     data = response.json()

#     listings: List[Dict] = []

#     for item in data:
#         address = item.get("formattedAddress")

#         listings.append({
#             # ---- identity ----
#             "external_id": item.get("id"),
#             "source": "rentcast",

#             # ---- pricing & size ----
#             "price": item.get("price"),
#             "beds": item.get("bedrooms"),
#             "baths": item.get("bathrooms"),
#             "sqft": item.get("squareFootage"),

#             # ---- location ----
#             "lat": item.get("latitude"),
#             "lon": item.get("longitude"),
#             "address": address,
#             "city": item.get("city"),
#             "state": item.get("state"),
#             "zip": item.get("zipCode"),

#             # ---- property meta ----
#             "property_type": item.get("propertyType"),
#             "year_built": item.get("yearBuilt"),

#             # ---- enrichment (safe) ----
#             "url": build_google_search_url(address),
#             "image": None,  # intentionally None (frontend can lazy-load)

#         })

#     return listings


# # =====================================================
# # OPTIONAL: GPS WRAPPER (USE ONLY IF YOU REALLY NEED IT)
# # =====================================================
# def fetch_listings_by_lat_lon(
#     lat: float,
#     lon: float,
#     limit: int = 20
# ) -> List[Dict]:
#     """
#     RentCast does NOT officially support radius search.
#     This function exists ONLY if you later map lat/lon → city/state.
#     """

#     raise NotImplementedError(
#         "RentCast requires city+state. "
#         "Convert lat/lon to city/state before calling."
#     )
import os
import requests
import urllib.parse
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
RENTCAST_BASE_URL = "https://api.rentcast.io/v1/listings/sale"




# =========================
# REVERSE GEOCODING (lat/lon → city/state)
# =========================
def reverse_geocode(lat: float, lon: float) -> tuple[str, str]:
    """
    Uses OpenStreetMap Nominatim (free)
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }

    headers = {
        "User-Agent": "real-estate-ai-search"
    }

    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    address = data.get("address", {})
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
    )
    state = address.get("state_code") or address.get("state")

    if not city or not state:
        raise ValueError("Unable to resolve city/state from lat/lon")

    return city, state


# =========================
# SAFE URL BUILDER
# =========================
def build_google_search_url(address: Optional[str]) -> Optional[str]:
    if not address:
        return None
    q = urllib.parse.quote(f"{address} real estate for sale")
    return f"https://www.google.com/search?q={q}"


# =========================
# CORE FETCH (city/state OR lat/lon)
# =========================
def fetch_listings(
    *,
    city: str | None = None,
    state: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    limit: int = 20
) -> List[Dict]:
    """
    Single entry point for ingestion
    """

    # ---- resolve location ----
    if lat is not None and lon is not None:
        city, state = reverse_geocode(lat, lon)
    elif city and state:
        pass
    else:
        raise ValueError("Provide either (city, state) OR (lat, lon)")

    headers = {
        "X-Api-Key": RENTCAST_API_KEY
    }

    params = {
        "city": city,
        "state": state,
        "limit": limit
    }

    response = requests.get(
        RENTCAST_BASE_URL,
        headers=headers,
        params=params,
        timeout=20
    )
    response.raise_for_status()

    data = response.json()
    listings = []

    for item in data:
        address = item.get("formattedAddress")

        listings.append({
            "external_id": item.get("id"),
            "price": item.get("price"),
            "beds": item.get("bedrooms"),
            "baths": item.get("bathrooms"),
            "sqft": item.get("squareFootage"),
            "lat": item.get("latitude"),
            "lon": item.get("longitude"),
            "address": address,
            "city": item.get("city"),
            "state": item.get("state"),
            "zip": item.get("zipCode"),
            "property_type": item.get("propertyType"),
            "year_built": item.get("yearBuilt"),
            "url": build_google_search_url(address),
            "image": None,
            "source": "rentcast"
        })

    return listings