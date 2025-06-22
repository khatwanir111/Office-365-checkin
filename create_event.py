import os
import requests
import datetime
import json

tenant_id = os.environ['TENANT_ID']
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
email = os.environ['EMAIL']

# Get OAuth2 token
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get("access_token")

# Define a calendar event
start_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
end_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=16)).strftime('%Y-%m-%dT%H:%M:%SZ')

event_data = {
    "subject": "Automated Calendar Event",
    "start": {
        "dateTime": start_time,
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": end_time,
        "timeZone": "UTC"
    }
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send event creation request
response = requests.post(
    f"https://graph.microsoft.com/v1.0/users/{email}/events",
    headers=headers,
    json=event_data
)

if response.status_code in [200, 201]:
    print("✅ Calendar event created.")
else:
    print(f"❌ Failed to create event: {response.status_code} {response.text}")
