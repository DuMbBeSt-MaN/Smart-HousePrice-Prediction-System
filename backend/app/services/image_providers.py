# app/services/image_providers.py

import os

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")


def satellite_preview_url(lat: float, lon: float, zoom: int = 16) -> str | None:
    """
    Returns a satellite image URL for the given lat/lon.
    Uses Google Static Maps if GOOGLE_MAPS_KEY is set, otherwise Yandex.
    Both correctly use the provided lat/lon so each listing gets its own image.
    """
    if lat is None or lon is None:
        return None

    if GOOGLE_MAPS_KEY:
        # Google Static Maps API — accurate, works globally including India
        return (
            f"https://maps.googleapis.com/maps/api/staticmap"
            f"?center={lat},{lon}&zoom={zoom}&size=650x450&maptype=satellite"
            f"&key={GOOGLE_MAPS_KEY}"
        )

    # Yandex static maps — free, no API key, works globally
    # ll = longitude,latitude (note: Yandex uses lon,lat order)
    return (
        f"https://static-maps.yandex.ru/1.x/"
        f"?ll={lon},{lat}&z={zoom}&size=650,450&l=sat"
    )
