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
        lat = payload["location"]["lat"]
        lon = payload["location"]["lon"]
        features = payload.get("features", [])

        print("\n" + "="*60)
        print(f"[PlannerAgent] INPUT")
        print(f"  lat={lat}, lon={lon}")
        print(f"  features={features}")
        print("="*60)

        t0 = time.time()
        intent = self.feature_agent.parse(features)
        t1 = time.time()

        print(f"[Intent] parsed weights: {intent}")

        listings = fetch_listings(lat, lon, limit=5)
        t2 = time.time()

        print(f"[Listings] fetched {len(listings)} results")

        for i, l in enumerate(listings):
            scores = {}
            places = places_signals(l["lat"], l["lon"])
            env = environment_signals(l["lat"], l["lon"])

            print(f"\n[Listing {i+1}] address='{l.get('address')}' price='{l.get('price_display', l.get('price'))}'")
            print(f"  OSM places  → schools={places.get('schools',0)}, hospitals={places.get('hospitals',0)}, parks={places.get('parks',0)}")
            print(f"  OSM env     → water_risk={env.get('water_risk', 0):.2f}")

            # Normalize OSM counts to 0-1
            # Indian cities are dense — use higher max values
            scores["schools"]   = min(places.get("schools", 0) / 20.0, 1.0)
            scores["hospitals"] = min(places.get("hospitals", 0) / 10.0, 1.0)
            scores["parks"]     = min(places.get("parks", 0) / 10.0, 1.0)

            # Water risk: lower is better (already 0-1 from environment_ingestor)
            scores["water_risk"] = 1.0 - env.get("water_risk", 0.0)

            # Price score: normalize against Indian market (INR)
            # Typical range: 20L (2M) to 5Cr (50M). Lower price = higher score.
            price = l.get("price")
            if price and price > 0:
                # 5 Crore = 50_000_000 INR as upper bound
                scores["price"] = max(0.0, 1.0 - min(price / 50_000_000, 1.0))
            else:
                scores["price"] = 0.5  # neutral when price unknown

            l["scores"] = scores
            l["image"] = satellite_preview_url(l["lat"], l["lon"])
            l["url"] = google_search_url(l.get("address", ""))

            print(f"  scores      → {scores}")
            print(f"  satellite   → {l['image']}")

        t3 = time.time()

        ranked = self.decision_agent.rank(listings, intent)
        t4 = time.time()

        print(f"\n[Ranked Results]")
        for i, r in enumerate(ranked):
            print(f"  #{i+1} score={r.get('final_score')} | {r.get('address')} | {r.get('price_display', r.get('price'))}")

        print(f"\n[Timings] parse={t1-t0:.3f}s fetch={t2-t1:.3f}s enrich={t3-t2:.3f}s rank={t4-t3:.3f}s total={t4-t0:.3f}s")
        print("="*60 + "\n")

        return ranked
