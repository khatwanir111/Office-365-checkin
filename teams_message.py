# Sends Teams chat message to self

import os, requests
from msal import PublicClientApplication

app = PublicClientApplication(
    os.environ["CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}"
)
result = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)

token = result["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Get self ID
user_id = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()["id"]

# Create chat with self (1:1)
chat = requests.post("https://graph.microsoft.com/v1.0/chats", headers=headers, json={
    "chatType": "oneOnOne",
    "members": [{
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["owner"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id}')"
    }]
}).json()

# Send message
requests.post(f"https://graph.microsoft.com/v1.0/chats/{chat['id']}/messages", headers=headers, json={
    "body": {
        "content": "👋 Hello from GitHub Action!"
    }
})
