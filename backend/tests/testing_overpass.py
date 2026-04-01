# # from app.services.listings import fetch_listings
# import os
# import requests
# from dotenv import load_dotenv
# load_dotenv()
# # results = fetch_listings(city="Los Angeles", state="CA")

# # print(len(results))
# # print(results[0])
# # import requests
# # import os


# # RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")

# # url = "https://api.rentcast.io/v1/properties/for-sale"

# # headers = {
# #     "X-Api-Key": RENTCAST_API_KEY
# # }

# # params = {
# #     "latitude": 34.0522,     # Los Angeles
# #     "longitude": -118.2437,
# #     "limit": 20
# # }

# # response = requests.get(url, headers=headers, params=params)
# # response.raise_for_status()

# # data = response.json()
# # print(len(data))
# import requests
# import os

# RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")

# url = "https://api.rentcast.io/v1/listings/sale"

# headers = {
#     "X-Api-Key": RENTCAST_API_KEY
# }

# params = {
#     "latitude": 34.0522,
#     "longitude": -118.2437,
#     "limit": 20
# }

# response = requests.get(url, headers=headers, params=params)
# response.raise_for_status()

# data = response.json()
# print(len(data))
# print(data[0])
import requests
import json

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def overpass_query(query: str):
    response = requests.post(
        OVERPASS_URL,
        data=query,
        headers={"Content-Type": "text/plain"}
    )
    response.raise_for_status()
    return response.json()

def test_hospitals_nearby(lat, lon, radius=3000):
    query = f"""
    [out:json];
    node["amenity"="hospital"](around:{radius},{lat},{lon});
    out;
    """
    data = overpass_query(query)
    return data["elements"]

if __name__ == "__main__":
    # Los Angeles (example)
    lat = 34.0522
    lon = -118.2437

    hospitals = test_hospitals_nearby(lat, lon)

    print(f"Found {len(hospitals)} hospitals:\n")

    for h in hospitals[:5]:  # show first 5
        name = h.get("tags", {}).get("name", "Unnamed")
        print(f"- {name} ({h['lat']}, {h['lon']})")  