# # app/services/overpass_client.py

# import requests
# import time

# OVERPASS_URL = "https://overpass-api.de/api/interpreter"


# def query_overpass(query: str, retries: int = 2) -> list[dict]:
#     """
#     Execute an Overpass QL query and return elements.
#     """

#     for attempt in range(retries):
#         try:

#             response = requests.post(
#                 OVERPASS_URL,
#                 data=query,
#                 headers={"Content-Type": "text/plain"},
#                 timeout=30
#             )
#             print(query)
#             response.raise_for_status()
#             return response.json().get("elements", [])

#         except Exception as e:
#             if attempt == retries - 1:
#                 raise e
#             time.sleep(2)

#     return []
# import requests
# import time

# OVERPASS_URL = "https://overpass-api.de/api/interpreter"


# def build_overpass_query(
#     elements: list[dict],
#     lat: float,
#     lon: float,
#     radius: int = 1500,
#     timeout: int = 25,
#     count_only: bool = True
# ) -> str:
#     """
#     elements example:
#     [
#       {"type": "node", "key": "amenity", "value": "hospital"},
#       {"type": "way",  "key": "amenity", "value": "hospital"}
#     ]
#     """

#     body = []
#     for e in elements:
#         body.append(
#             f'{e["type"]}["{e["key"]}"="{e["value"]}"](around:{radius},{lat},{lon});'
#         )

#     out = "out count;" if count_only else "out;"

#     return f"""
#     [out:json][timeout:{timeout}];
#     (
#         {''.join(body)}
#     );
#     {out}
#     """


# def query_overpass(query: str, retries: int = 2) -> list[dict]:
#     for attempt in range(retries):
#         try:
#             print(query)
#             response = requests.post(
#                 OVERPASS_URL,
#                 data=query,
#                 headers={"Content-Type": "text/plain"},
#                 timeout=30
#             )
#             response.raise_for_status()
#             return response.json().get("elements", [])
#         except Exception:
#             if attempt == retries - 1:
#                 return []
#             time.sleep(2)
import requests
import time

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def query_overpass(query: str, timeout: int = 25, retries: int = 1) -> int:
    """
    Runs an Overpass query that RETURNS A COUNT.
    Safer, faster, prevents massive payloads.
    """

    wrapped = f"""
    [out:json][timeout:{timeout}];
    (
        {query}
    );
    out count;
    """

    for attempt in range(retries):
        try:
            r = requests.post(
                OVERPASS_URL,
                data=wrapped,
                headers={"Content-Type": "text/plain"},
                timeout=timeout
            )
            r.raise_for_status()
            data = r.json()
            return int(data["elements"][0]["tags"]["total"])

        except Exception:
            if attempt == retries - 1:
                return 0
            time.sleep(2)