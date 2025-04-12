import requests

def send_outlook_email(token: str, to_email: str, subject: str, body_text: str):
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body_text
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_email
                    }
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=message)

    if response.status_code == 202:
        return {"status": "Email sent successfully"}
    else:
        return {
            "error": "Failed to send email",
            "details": response.json()
        }