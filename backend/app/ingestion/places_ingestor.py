# # app/ingestion/places_ingestor.py

# from app.services.overpass_client import query_overpass


# def _count(query: str) -> int:
#     return len(query_overpass(query))


# def places_signals(lat: float, lon: float) -> dict:
#     """
#     Extract place-based signals near a house.
#     """

#     radius = 2000  # meters

#     schools = _count(f"""
#         [out:json];
#         node["amenity"~"school|college|university"](around:{radius},{lat},{lon});
#         out;
#     """)

#     hospitals = _count(f"""
#         [out:json];
#         node["amenity"="hospital"](around:{radius},{lat},{lon});
#         out;
#     """)

#     parks = _count(f"""
#         [out:json];
#         way["leisure"="park"](around:{radius},{lat},{lon});
#         out;
#     """)

#     return {
#         "schools_nearby": schools,
#         "hospitals_nearby": hospitals,
#         "parks_nearby": parks
#     }
# """
# Places Ingestor
# ---------------
# Fetches nearby contextual signals (schools, hospitals, parks, safety, water)
# using OpenStreetMap via Overpass API.

# This file is intentionally:
# - atomic (small queries)
# - configurable
# - timeout-safe
# """

# from app.services.overpass_client import (
#     build_overpass_query,
#     query_overpass
# )

# # ---------------------------
# # INTERNAL HELPER
# # ---------------------------

# def _count_from_query(query: str) -> int:
#     """
#     Executes Overpass query and extracts count safely
#     """
#     elements = query_overpass(query)
#     if not elements:
#         return 0

#     # Overpass returns count in tags.total
#     tags = elements[0].get("tags", {})
#     return int(tags.get("total", 0))


# # ---------------------------
# # FEATURE QUERIES
# # ---------------------------

# def places_signals(lat: float, lon: float) -> dict:
#     """
#     Main entry point.
#     Returns ALL place-related signals in one dict.
#     """

#     return {
#         "schools": schools_nearby(lat, lon),
#         "hospitals": hospitals_nearby(lat, lon),
#         "parks": parks_nearby(lat, lon),
#         "police": police_stations_nearby(lat, lon),
#         "fire_stations": fire_stations_nearby(lat, lon),
#         "water_bodies": water_bodies_nearby(lat, lon),
#     }


# # ---------------------------
# # INDIVIDUAL SIGNALS
# # ---------------------------

# def schools_nearby(lat, lon) -> int:
#     query = build_overpass_query(
#         elements=[
#             {"type": "node", "key": "amenity", "value": "school"},
#             {"type": "node", "key": "amenity", "value": "college"},
#             {"type": "node", "key": "amenity", "value": "university"},
#         ],
#         lat=lat,
#         lon=lon,
#         radius=1500
#     )
#     return _count_from_query(query)


# def hospitals_nearby(lat, lon) -> int:
#     query = build_overpass_query(
#         elements=[
#             {"type": "node", "key": "amenity", "value": "hospital"},
#             {"type": "way",  "key": "amenity", "value": "hospital"},
#         ],
#         lat=lat,
#         lon=lon,
#         radius=1500
#     )
#     return _count_from_query(query)


# def parks_nearby(lat, lon) -> int:
#     query = build_overpass_query(
#         elements=[
#             {"type": "way", "key": "leisure", "value": "park"},
#         ],
#         lat=lat,
#         lon=lon,
#         radius=1200
#     )
#     return _count_from_query(query)


# def police_stations_nearby(lat, lon) -> int:
#     query = build_overpass_query(
#         elements=[
#             {"type": "node", "key": "amenity", "value": "police"},
#         ],
#         lat=lat,
#         lon=lon,
#         radius=2000
#     )
#     return _count_from_query(query)


# def fire_stations_nearby(lat, lon) -> int:
#     query = build_overpass_query(
#         elements=[
#             {"type": "node", "key": "amenity", "value": "fire_station"},
#         ],
#         lat=lat,
#         lon=lon,
#         radius=3000
#     )
#     return _count_from_query(query)


# def water_bodies_nearby(lat, lon) -> int:
#     """
#     Proxy for flood / water risk.
#     More water nearby → higher potential risk.
#     """
#     query = build_overpass_query(
#         elements=[
#             {"type": "way", "key": "natural", "value": "water"},
#             {"type": "way", "key": "waterway", "value": "river"},
#         ],
#         lat=lat,
#         lon=lon,
#         radius=2500
#     )
#     return _count_from_query(query)
# from app.services.overpass_client import query_overpass

# def extract_count(elements):
#     if not elements:
#         return 0
#     return int(elements[0]["tags"].get("total", 0))

# def normalize(count, max_expected):
#     return min(count / max_expected, 1.0)

# def places_signals(lat, lon):
#     school_q = f"""
#     [out:json][timeout:25];
#     (
#       node["amenity"~"school|college|university"](around:2000,{lat},{lon});
#     );
#     out count;
#     """

#     hospital_q = f"""
#     [out:json][timeout:25];
#     (
#       node["amenity"="hospital"](around:4000,{lat},{lon});
#       way["amenity"="hospital"](around:4000,{lat},{lon});
#     );
#     out count;
#     """

#     park_q = f"""
#     [out:json][timeout:25];
#     (
#       way["leisure"="park"](around:1500,{lat},{lon});
#     );
#     out count;
#     """

#     schools = extract_count(query_overpass(school_q))
#     hospitals = extract_count(query_overpass(hospital_q))
#     parks = extract_count(query_overpass(park_q))

#     return {
#         "schools": normalize(schools, 5),
#         "hospitals": normalize(hospitals, 5),
#         "parks": normalize(parks, 3),
#     }
from app.services.overpass_client import query_overpass

def places_signals(lat: float, lon: float) -> dict:
    return {
        "schools": query_overpass(
            f'node["amenity"~"school|college|university"](around:1500,{lat},{lon});'
        ),
        "hospitals": query_overpass(
            f'node["amenity"="hospital"](around:3000,{lat},{lon});'
        ),
        "parks": query_overpass(
            f'way["leisure"="park"](around:1200,{lat},{lon});'
        )
    }