# app/services/url_builders.py

import urllib.parse


def google_search_url(address: str) -> str | None:
    """
    Builds a Google search URL for a property address
    """
    if not address:
        return None

    query = urllib.parse.quote_plus(f"{address} real estate for sale")
    return f"https://www.google.com/search?q={query}"


def google_maps_url(lat: float, lon: float) -> str | None:
    """
    Direct Google Maps link
    """
    if lat is None or lon is None:
        return None

    return f"https://www.google.com/maps?q={lat},{lon}"


def street_view_url(lat: float, lon: float) -> str | None:
    """
    Non-API Google Street View redirect
    (does NOT require API key)
    """
    if lat is None or lon is None:
        return None

    return (
        "https://www.google.com/maps/@?"
        f"api=1&map_action=pano&viewpoint={lat},{lon}"
    )