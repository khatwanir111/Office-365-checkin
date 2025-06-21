import requests
import datetime

# Azure AD App credentials
TENANT_ID = 'your-tenant-id'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
USER_ID = 'user@yourdomain.com'

# Endpoints
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"

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

def get_recent_chats(access_token, user_id):
    url = f"{GRAPH_API_BASE}/users/{user_id}/chats"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])

def get_latest_messages(access_token, chat_id, max_messages=3):
    url = f"{GRAPH_API_BASE}/chats/{chat_id}/messages?$top={max_messages}&$orderby=createdDateTime desc"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])

def main():
    access_token = get_access_token()
    chats = get_recent_chats(access_token, USER_ID)

    if not chats:
        print("No chats found for this user.")
        return

    print(f"Latest messages from user's recent Microsoft Teams chats:\n")
    for chat in chats[:2]:  # Limit to 2 recent chats
        chat_id = chat['id']
        chat_type = chat.get('chatType', 'unknown')
        messages = get_latest_messages(access_token, chat_id)

        print(f"--- Chat ID: {chat_id} | Type: {chat_type} ---")
        for msg in messages:
            sender = msg.get('from', {}).get('user', {}).get('displayName', 'Unknown')
            body = msg.get('body', {}).get('content', '').strip()
            timestamp = msg.get('createdDateTime', '')
            print(f"[{timestamp}] {sender}: {body}")
        print()

if __name__ == "__main__":
    main()
