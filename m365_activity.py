import os
import requests
from msal import PublicClientApplication

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
tenant_id = os.environ["TENANT_ID"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

app = PublicClientApplication(client_id, authority=authority)

result = app.acquire_token_by_username_password(
    username=username,
    password=password,
    scopes=scopes
)

if "access_token" in result:
    access_token = result["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Send email
    email_payload = {
        "message": {
            "subject": "Automated Email from GitHub Action",
            "body": {
                "contentType": "Text",
                "content": "This is a test email to keep M365 dev account active."
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": username
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }
    requests.post("https://graph.microsoft.com/v1.0/me/sendMail", headers=headers, json=email_payload)

    # Create calendar event
    import datetime
    now = datetime.datetime.utcnow()
    start = now.isoformat() + "Z"
    end = (now + datetime.timedelta(hours=1)).isoformat() + "Z"
    event_payload = {
        "subject": "Automated Calendar Event",
        "start": {
            "dateTime": start,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end,
            "timeZone": "UTC"
        }
    }
    requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event_payload)

else:
    print("Error acquiring token:", result.get("error_description"))
