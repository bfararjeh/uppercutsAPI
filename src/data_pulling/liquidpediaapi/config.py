import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

config_path = Path(__file__).parent / "config.json"
with open(config_path, "r") as f:
    json_data = json.load(f)
    print(json_data)


BASE_URL = json_data["base_url"]
HEADERS = {
    "User-Agent": os.getenv("LP_USER_AGENT"),
    "Accept-Encoding": "gzip"
}

LPDB_API_KEY = os.getenv("LP_LPDB_API_KEY", "")

# Rate limits
RATE_LIMIT_QUERY = int(os.getenv("LP_RATE_LIMIT_QUERY", 2))
RATE_LIMIT_PARSE = int(os.getenv("LP_RATE_LIMIT_PARSE", 30))