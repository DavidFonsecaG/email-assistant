import requests
from typing import List, Dict

def fetch_received_emails(token: str, max_results=200) -> List[Dict]:
    url = f"https://graph.microsoft.com/v1.0/me/messages?$top={max_results}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    emails = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Error fetching received emails:", response.text)
            break
        data = response.json()
        emails.extend(data.get("value", []))
        url = data.get("@odata.nextLink", None)

        if len(emails) >= max_results:
            break

    return emails

def fetch_sent_emails(token: str, max_results=200) -> List[Dict]:
    url = f"https://graph.microsoft.com/v1.0/me/mailFolders/sentitems/messages?$top={max_results}"
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

        if len(emails) >= max_results:
            break

    return emails