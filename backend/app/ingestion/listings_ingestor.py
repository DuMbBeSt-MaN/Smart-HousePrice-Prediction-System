# app/ingestion/listings_ingestor.py

import os
import re
import requests
from dotenv import load_dotenv
load_dotenv()

SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
SCRAPINGBEE_URL = "https://app.scrapingbee.com/api/v1/"


def _geocode_to_area(lat: float, lon: float) -> str:
    """Use Google Geocoding (if key available) or Nominatim to get locality name for scraping."""
    if GOOGLE_MAPS_KEY:
        r = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"latlng": f"{lat},{lon}", "key": GOOGLE_MAPS_KEY},
            timeout=10
        )
        results = r.json().get("results", [])
        if results:
            # Extract locality + city from address components
            components = results[0].get("address_components", [])
            locality = next((c["long_name"] for c in components if "sublocality" in c["types"] or "locality" in c["types"]), None)
            city = next((c["long_name"] for c in components if "administrative_area_level_2" in c["types"]), None)
            area = locality or city or results[0].get("formatted_address", "")
            print(f"[Geocode] lat={lat}, lon={lon} → area='{area}'")
            return area
    else:
        # Fallback: Nominatim
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "housing-prices-app"},
            timeout=10
        )
        data = r.json()
        addr = data.get("address", {})
        area = addr.get("suburb") or addr.get("city_district") or addr.get("city") or addr.get("town") or ""
        print(f"[Geocode-Nominatim] lat={lat}, lon={lon} → area='{area}'")
        return area


def _parse_price_inr(price_str: str) -> float | None:
    """Convert Indian price strings like '₹45 Lac', '1.2 Cr' to float (in INR)."""
    if not price_str:
        return None
    s = price_str.replace(",", "").replace("₹", "").strip().lower()
    try:
        if "cr" in s:
            return float(re.sub(r"[^\d.]", "", s)) * 1_00_00_000
        elif "lac" in s or "lakh" in s or "l" in s:
            return float(re.sub(r"[^\d.]", "", s)) * 1_00_000
        else:
            return float(re.sub(r"[^\d.]", "", s))
    except Exception:
        return None


def _scrape_99acres(area: str, limit: int = 5) -> list[dict]:
    """Scrape 99acres property listings for a given area using ScrapingBee."""
    if not SCRAPINGBEE_API_KEY:
        print("[ScrapingBee] SCRAPINGBEE_API_KEY not set — returning empty listings")
        return []

    search_area = area.lower().replace(" ", "-")
    target_url = f"https://www.99acres.com/property-for-sale-in-{search_area}-ffid"

    print(f"[ScrapingBee] Scraping: {target_url}")

    try:
        r = requests.get(
            SCRAPINGBEE_URL,
            params={
                "api_key": SCRAPINGBEE_API_KEY,
                "url": target_url,
                "render_js": "false",
                "premium_proxy": "true",
            },
            timeout=60
        )
        r.raise_for_status()
        html = r.text
    except Exception as e:
        print(f"[ScrapingBee] Request failed: {e}")
        return []

    listings = []

    # Extract listing blocks — 99acres uses data-label or card patterns
    # Parse title, price, address from HTML using regex (no BS4 dependency)
    titles = re.findall(r'data-label="[^"]*"[^>]*>([^<]{5,80})</[^>]+>', html)
    prices = re.findall(r'(₹[\d.,]+\s*(?:Cr|Lac|Lakh|L)?)', html, re.IGNORECASE)
    addresses = re.findall(r'(?:locality|address)[^>]*>([^<]{5,100})<', html, re.IGNORECASE)

    print(f"[ScrapingBee] Raw parse → titles={len(titles)}, prices={len(prices)}, addresses={len(addresses)}")

    for i in range(min(limit, max(len(titles), len(prices), 1))):
        title = titles[i] if i < len(titles) else f"Property in {area}"
        price_str = prices[i] if i < len(prices) else None
        address = addresses[i] if i < len(addresses) else area
        price_val = _parse_price_inr(price_str)

        listing = {
            "external_id": f"99acres_{area}_{i}",
            "source": "99acres_scrapingbee",
            "title": title.strip(),
            "price": price_val,
            "price_display": price_str,
            "beds": None,
            "baths": None,
            "sqft": None,
            "year_built": None,
            "property_type": "residential",
            "lat": None,   # individual listing lat/lon not available from list page
            "lon": None,
            "address": address.strip(),
            "city": area,
            "state": None,
            "zip": None,
            "signals": {},
            "scores": {},
            "final_score": None
        }
        print(f"[Listing {i+1}] title='{listing['title']}' price='{price_str}' address='{listing['address']}'")
        listings.append(listing)

    return listings


def fetch_listings(lat: float, lon: float, limit: int = 5) -> list[dict]:
    """
    Main entry point. Resolves lat/lon to an area name, then scrapes 99acres.
    Falls back to using the area centroid lat/lon for all listings (for OSM signals).
    """
    area = _geocode_to_area(lat, lon)
    if not area:
        print(f"[fetch_listings] Could not resolve area for lat={lat}, lon={lon}")
        area = "mumbai"  # safe fallback

    listings = _scrape_99acres(area, limit=limit)

    # Assign the search lat/lon to listings that don't have their own coords
    # so OSM signals can still be computed for the general area
    for l in listings:
        if l["lat"] is None:
            l["lat"] = lat
            l["lon"] = lon

    return listings
