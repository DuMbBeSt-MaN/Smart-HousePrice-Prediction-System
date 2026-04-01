# app/ingestion/listings_ingestor.py

import os
import re
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
SCRAPINGBEE_URL     = "https://app.scrapingbee.com/api/v1/"


def _build_magicbricks_url(area_name: str, city: str) -> str:
    """
    Build MagicBricks rental search URL.
    e.g. area=Adyar, city=Chennai -> flats-for-rent-in-adyar-chennai-pppfr
    """
    parts = [p.lower().replace(" ", "-") for p in [area_name, city] if p.strip()]
    slug  = "-".join(parts)
    return f"https://www.magicbricks.com/flats-for-rent-in-{slug}-pppfr"


def _scrape_magicbricks(url: str, prices: list[int], limit: int) -> list[dict]:
    """
    Scrape MagicBricks listing page via ScrapingBee (no JS rendering needed).
    Parses structured JSON-LD data embedded in the page — no fragile regex.
    """
    if not SCRAPINGBEE_API_KEY:
        print("[ScrapingBee] SCRAPINGBEE_API_KEY not set")
        return []

    print(f"[ScrapingBee] Scraping: {url}")
    try:
        r = requests.get(
            SCRAPINGBEE_URL,
            params={
                "api_key":      SCRAPINGBEE_API_KEY,
                "url":          url,
                "render_js":    "false",   # MagicBricks serves JSON-LD in static HTML
                "premium_proxy":"true",
                "country_code": "in",
            },
            timeout=60
        )
        r.raise_for_status()
        html = r.text
    except Exception as e:
        print(f"[ScrapingBee] Request failed: {e}")
        return []

    print(f"[ScrapingBee] HTML length: {len(html)} chars")

    # Extract all JSON-LD blocks
    json_blocks = re.findall(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        html, re.DOTALL
    )

    # Extract prices separately (they appear as "price": "170000" in the page)
    raw_prices = re.findall(r'"price"\s*:\s*"?(\d+)"?', html)
    price_list = [int(p) for p in raw_prices]

    apartments = []
    for block in json_blocks:
        try:
            data = json.loads(block.strip())
            items = data if isinstance(data, list) else [data]
            for item in items:
                if item.get("@type") == "Apartment":
                    apartments.append(item)
        except Exception:
            continue

    print(f"[MagicBricks] Found {len(apartments)} apartment listings, {len(price_list)} prices")

    listings = []
    for i, apt in enumerate(apartments[:limit]):
        geo     = apt.get("geo", {})
        address = apt.get("address", {})
        name    = apt.get("name", "")
        url_    = apt.get("url") or apt.get("@id", "")
        image   = apt.get("image", "")
        rooms   = apt.get("numberOfRooms")

        lat = float(geo["latitude"])  if geo.get("latitude")  else None
        lon = float(geo["longitude"]) if geo.get("longitude") else None

        # Extract sqft from URL slug e.g. "3-BHK-1926-Sq-ft-..."
        sqft_match = re.search(r'(\d+)-Sq-ft', url_, re.IGNORECASE)
        sqft = int(sqft_match.group(1)) if sqft_match else None

        price = price_list[i] if i < len(price_list) else None

        listing = {
            "external_id":   f"mb_{i}_{apt.get('@id','')[-10:]}",
            "source":        "magicbricks",
            "title":         name,
            "price":         price,
            "price_display": f"Rs. {price:,}/month" if price else None,
            "beds":          int(rooms) if rooms else None,
            "sqft":          sqft,
            "baths":         None,
            "year_built":    None,
            "property_type": "residential",
            "lat":           lat,
            "lon":           lon,
            "address":       f"{address.get('addressLocality', '')}, {address.get('addressRegion', '')}".strip(", "),
            "city":          address.get("addressRegion", ""),
            "state":         None,
            "image":         image,
            "listing_url":   url_,
            "signals":       {},
            "scores":        {},
            "final_score":   None,
        }
        print(f"[Listing {i+1}] {name} | Rs.{price}/mo | lat={lat}, lon={lon} | sqft={sqft}")
        listings.append(listing)

    return listings


def fetch_listings(lat: float, lon: float, limit: int = 5,
                   area_name: str = "", city: str = "") -> list[dict]:
    """
    Build MagicBricks URL from area_name + city, scrape via ScrapingBee.
    Each listing gets its own lat/lon from JSON-LD geo data.
    Falls back to search-area coords if listing has no geo.
    """
    url      = _build_magicbricks_url(area_name, city)
    listings = _scrape_magicbricks(url, [], limit=limit)

    for l in listings:
        if l["lat"] is None and lat is not None:
            l["lat"] = lat
            l["lon"] = lon

    return listings
