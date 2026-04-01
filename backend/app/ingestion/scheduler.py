from app.ingestion.listings_ingestor import ingest_listings
from app.ingestion.env_ingestor import ingest_environment
from app.storage.crud import (
    get_listings_by_location,
    is_location_stale
)

def run_ingestion(lat, lon, loc_key):
    if not is_location_stale(loc_key):
        return

    ingest_listings(lat, lon, loc_key)
    listings = get_listings_by_location(loc_key)

    for l in listings:
        ingest_environment(l)
