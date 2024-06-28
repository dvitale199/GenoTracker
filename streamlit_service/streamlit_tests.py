from google.oauth2 import id_token
from google.oauth2 import service_account
from google.auth.transport import requests
import requests as req

def get_iap_access_token(client_id, service_account_file):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    token = id_token.fetch_id_token(requests.Request(), client_id)
    return token

def fetch_data(url, client_id, service_account_file):
    token = get_iap_access_token(client_id, service_account_file)
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    response = req.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Response content: {response.text}")
        raise Exception(f"Request failed with status {response.status_code}")


# Usage
API_URL = "https://genotracker-dot-gp2-release-terra.uc.r.appspot.com/data"
CLIENT_ID = "107367214990901712689"
SERVICE_ACCOUNT_FILE = "/app/.devcontainer/gp2-release-terra-e65c1b67820b.json"

try:
    data = fetch_data(API_URL, CLIENT_ID, SERVICE_ACCOUNT_FILE)
    print(data)
except Exception as e:
    print(f"An error occurred: {str(e)}")

