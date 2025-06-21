import requests
import datetime
import json

# Replace with your tenant details
TENANT_ID = 'your-tenant-id'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
USER_ID = 'user@yourdomain.com'

# Microsoft Identity Platform endpoint
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"

def get_access_token():
    payload = {
        'client_id': CLIENT_ID,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(AUTHORITY, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def get_calendar_events(access_token, user_id, start_datetime, end_datetime):
    url = f"{GRAPH_ENDPOINT}/users/{user_id}/calendarView"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Prefer': 'outlook.timezone="UTC"'
    }
    params = {
        'startDateTime': start_datetime.isoformat(),
        'endDateTime': end_datetime.isoformat(),
        '$top': 5
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('value', [])

def main():
    access_token = get_access_token()
    
    now = datetime.datetime.utcnow()
    later = now + datetime.timedelta(days=1)

    events = get_calendar_events(access_token, USER_ID, now, later)
    print(f"Upcoming events for {USER_ID} (next 24 hours):\n")
    
    if not events:
        print("No events found.")
    else:
        for event in events:
            print(f"📅 {event['subject']} | {event['start']['dateTime']} ➡ {event['end']['dateTime']}")
            print(f"    Location: {event.get('location', {}).get('displayName', 'N/A')}")
            print()

if __name__ == "__main__":
    main()
