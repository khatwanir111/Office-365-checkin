# Adds a recurring calendar reminder

import os, requests, datetime
from msal import PublicClientApplication

# Auth
app = PublicClientApplication(
    os.environ["CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}"
)
result = app.acquire_token_by_username_password(
    os.environ["USERNAME"],
    os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)
token = result["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create calendar event
now = datetime.datetime.utcnow()
event = {
    "subject": "Daily Dev Reminder",
    "start": {"dateTime": now.isoformat()+"Z", "timeZone": "UTC"},
    "end": {"dateTime": (now + datetime.timedelta(minutes=30)).isoformat()+"Z", "timeZone": "UTC"},
    "recurrence": {
        "pattern": {"type": "daily", "interval": 1},
        "range": {"type": "endDate", "startDate": now.date().isoformat(), "endDate": "2025-12-31"}
    }
}

requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event)
