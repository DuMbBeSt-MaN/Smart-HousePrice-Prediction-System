from app.ingestion.listings_ingestor import fetch_listings
from app.ingestion.environment_ingestor import environment_signals

def run_ingestion(lat, lon, loc_key):
    listings = fetch_listings(lat, lon)
    for l in listings:
        environment_signals(l["lat"], l["lon"])
