from pathlib import Path
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_TOKEN = os.getenv("STARTGG_API_TOKEN")
ENDPOINT = "https://api.start.gg/gql/alpha"

script_dir = Path(__file__).resolve().parent
query_file = script_dir / "GrabAllTournaments.gql"

with open(query_file, "r") as f:
    query = f.read()

variables = {
    "perPage": 1,
    "videogameId": 43868,
    "page": 1
}

payload = {
    "query": query,
    "variables": variables
}

# Send the POST request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(ENDPOINT, json=payload, headers=headers)

# Print results (or handle errors)
if response.status_code == 200:
    print(response.json())

else:
    print(f"Error {response.status_code}: {response.text}")