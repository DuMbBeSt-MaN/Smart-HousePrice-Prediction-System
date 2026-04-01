# app/agents/planner_agent.py

from app.agents.unlimited_features_agent import UnlimitedFeaturesAgent
from app.agents.decision_agent import DecisionAgent
from app.ingestion.listings_ingestor import fetch_listings
from app.ingestion.places_ingestor import places_signals
from app.ingestion.environment_ingestor import environment_signals
from app.services.image_providers import satellite_preview_url
from app.services.url_builders import google_search_url
import time


class PlannerAgent:
    def __init__(self):
        self.feature_agent = UnlimitedFeaturesAgent()
        self.decision_agent = DecisionAgent()

    def run(self, payload: dict):
        lat      = payload["location"]["lat"]
        lon      = payload["location"]["lon"]
        features = payload.get("features", [])
        area_name = payload.get("area_name", "")
        city      = payload.get("city", "")
        state     = payload.get("state", "")

        print("\n" + "="*60)
        print(f"[PlannerAgent] INPUT")
        print(f"  lat={lat}, lon={lon}")
        print(f"  area_name='{area_name}' city='{city}' state='{state}'")
        print(f"  features={features}")
        print("="*60)

        t0 = time.time()
        intent = self.feature_agent.parse(features)
        t1 = time.time()
        print(f"[Intent] {intent}")

        listings = fetch_listings(lat, lon, limit=5, area_name=area_name, city=city)
        t2 = time.time()
        print(f"[Listings] fetched {len(listings)}")

        if not listings:
            print("[PlannerAgent] No listings found — returning empty")
            return []

        # OSM signals are area-level — fetch ONCE using the search coords
        # (all listings share the same area since 99acres doesn't give per-listing coords)
        area_lat = listings[0]["lat"]
        area_lon = listings[0]["lon"]
        print(f"[OSM] Fetching area signals for lat={area_lat}, lon={area_lon}")

        places = places_signals(area_lat, area_lon)
        env    = environment_signals(area_lat, area_lon)
        t3 = time.time()

        print(f"[OSM] schools={places.get('schools',0)}, hospitals={places.get('hospitals',0)}, parks={places.get('parks',0)}, water_risk={env.get('water_risk',0):.2f}")

        # Build shared area scores
        area_scores = {
            "schools":    min(places.get("schools",   0) / 20.0, 1.0),
            "hospitals":  min(places.get("hospitals", 0) / 10.0, 1.0),
            "parks":      min(places.get("parks",     0) / 10.0, 1.0),
            "water_risk": 1.0 - env.get("water_risk", 0.0),
        }

        for i, l in enumerate(listings):
            scores = dict(area_scores)

            # Price score — monthly rent in INR (Rs.20K–Rs.5L range)
            price = l.get("price")
            if price and price > 0:
                scores["price"] = max(0.0, 1.0 - min(price / 500_000, 1.0))
            else:
                scores["price"] = 0.5

            l["scores"] = scores
            # Use listing's own image if available (MagicBricks provides one), else satellite
            if not l.get("image"):
                l["image"] = satellite_preview_url(l["lat"], l["lon"])
            l["url"] = l.get("listing_url") or google_search_url(l.get("address", ""))

            print(f"\n[Listing {i+1}] '{l.get('title')}' | {l.get('price_display','N/A')} | {l.get('address')}")
            print(f"  scores -> {scores}")

        ranked = self.decision_agent.rank(listings, intent)
        t4 = time.time()

        print(f"\n[Ranked Results]")
        for i, r in enumerate(ranked):
            print(f"  #{i+1} final_score={r.get('final_score')} | {r.get('title')} | {r.get('price_display','N/A')} | {r.get('address')}")

        print(f"\n[Timings] parse={t1-t0:.2f}s fetch={t2-t1:.2f}s osm={t3-t2:.2f}s rank={t4-t3:.2f}s total={t4-t0:.2f}s")
        print("="*60 + "\n")

        return ranked
