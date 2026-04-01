# app/utils/geo.py

import hashlib


def location_key(lat: float, lon: float, precision: int = 3) -> str:
    """
    Generates a stable location key for nearby coordinates

    precision=3 → ~100m
    precision=4 → ~10m
    """

    lat_r = round(lat, precision)
    lon_r = round(lon, precision)

    raw = f"{lat_r}:{lon_r}"
    return hashlib.sha256(raw.encode()).hexdigest()