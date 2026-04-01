import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def overpass_query(query: str):
    response = requests.post(
        OVERPASS_URL,
        data=query,
        headers={"Content-Type": "text/plain"}
    )
    response.raise_for_status()
    return response.json()
def test_water_bodies_nearby(lat, lon, radius=3000):
    query = f"""
    [out:json];
    (
      way["natural"="water"](around:{radius},{lat},{lon});
      way["waterway"](around:{radius},{lat},{lon});
    );
    out geom;
    """
    data = overpass_query(query)
    return data["elements"]

if __name__ == "__main__":
    lat = 34.0522
    lon = -118.2437

    water = test_water_bodies_nearby(lat, lon)
    print(f"Found {len(water)} water bodies nearby")