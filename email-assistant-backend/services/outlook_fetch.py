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

def fetch_sent_emails(token, max_results=500):
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/sentitems/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Prefer": 'outlook.body-content-type="text"'
    }
    params = {
        "$top": max_results,
        "$select": "id,subject,body,conversationId,receivedDateTime,toRecipients",
    }

    emails = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        emails.extend(data.get("value", []))
        url = data.get("@odata.nextLink", None)  # pagination

        # optional: safety limit
        if len(emails) >= 500:  # for example
            break

    return emails