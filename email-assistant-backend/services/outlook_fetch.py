import requests
from typing import List, Dict

def fetch_received_emails(access_token: str, max_results=2) -> List[Dict]:
    url = "https://graph.microsoft.com/v1.0/me/messages?$top=" + str(max_results)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print("Error fetching emails:", response.text)
        return []

def fetch_sent_emails(token, max_results=2):
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/sentitems/messages?$top=" + str(max_results)
    headers = {
        "Authorization": f"Bearer {token}",
        "Prefer": 'outlook.body-content-type="text"'
    }

    emails = []

    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        emails.extend(data.get("value", []))
        url = data.get("@odata.nextLink", None)

        if len(emails) >= 2:
            break

    return emails