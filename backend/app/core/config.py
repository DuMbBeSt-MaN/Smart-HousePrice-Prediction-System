import os
from dotenv import load_dotenv

load_dotenv()

RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
OVERPASS_URL = "https://overpass-api.de/api/interpreter"