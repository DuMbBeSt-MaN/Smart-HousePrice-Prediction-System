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

def test_schools_nearby(lat, lon, radius=3000):
    query = f"""
    [out:json];
    (
      node["amenity"="school"](around:{radius},{lat},{lon});
      node["amenity"="college"](around:{radius},{lat},{lon});
      node["amenity"="university"](around:{radius},{lat},{lon});
    );
    out;
    """
    data = overpass_query(query)
    return data["elements"]

if __name__ == "__main__":
    lat = 34.0522
    lon = -118.2437

    schools = test_schools_nearby(lat, lon)
    print(f"Found {len(schools)} education institutes")

    for s in schools[:5]:
        print("-", s.get("tags", {}).get("name", "Unnamed"))