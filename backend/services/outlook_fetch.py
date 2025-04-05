import requests
from typing import List, Dict

def fetch_recent_emails(access_token: str, max_results=10) -> List[Dict]:
    url = "https://graph.microsoft.com/v1.0/me/messages?$top=" + str(max_results)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    for key, value in response.json().get("value", [])[0].items():
        print(f"--> {key}: {value}")

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print("Error fetching emails:", response.text)
        return []
