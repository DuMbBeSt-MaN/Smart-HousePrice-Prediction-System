# app/ingestion/environment_ingestor.py

# from app.services.overpass_client import query_overpass


# def environment_signals(lat: float, lon: float) -> dict:
#     """
#     Environmental risk proxies using OpenStreetMap
#     """

#     radius = 2000  # meters

#     water = query_overpass(f"""
#         [out:json];
#         way["natural"="water"](around:{radius},{lat},{lon});
#         out;
#     """)

#     rivers = query_overpass(f"""
#         [out:json];
#         way["waterway"="river"](around:{radius},{lat},{lon});
#         out;
#     """)

#     return {
#         "water_bodies": len(water),
#         "rivers_nearby": len(rivers)
#     }
# from app.services.overpass_client import query_overpass

# def places_signals(lat: float, lon: float) -> dict:
#     return {
#         "schools": query_overpass(
#             f'node["amenity"~"school|college|university"](around:1500,{lat},{lon});'
#         ),
#         "hospitals": query_overpass(
#             f'node["amenity"="hospital"](around:3000,{lat},{lon});'
#         ),
#         "parks": query_overpass(
#             f'way["leisure"="park"](around:1200,{lat},{lon});'
#         )
#     }
from app.services.overpass_client import query_overpass

def environment_signals(lat: float, lon: float) -> dict:
    water = query_overpass(
        f'way["natural"="water"](around:2500,{lat},{lon});'
    )

    return {
        # More water = higher flood potential
        "water_risk": min(water / 10, 1.0)
    }