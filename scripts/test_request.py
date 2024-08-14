import requests
from dotenv import load_dotenv, find_dotenv
import os

base_url = "https://genotracker-fastapi-3wsqie35cq-uc.a.run.app"

load_dotenv(dotenv_path='~/Projects/GenoTracker/.env')
api_key = os.getenv('API_KEY')

headers = {"X-API-Key": api_key}
response = requests.get(f"{base_url}/data", headers=headers, params={"from_gcs": "true"})

print("Status Code:", response.status_code)
try:
    print("Response Body:", response.json())
except ValueError:
    print("Response Body:", response.text)
