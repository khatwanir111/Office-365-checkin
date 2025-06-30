import os, requests
from msal import PublicClientApplication

app = PublicClientApplication(os.environ["CLIENT_ID"], authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}")
token = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

user = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
chat = requests.post("https://graph.microsoft.com/v1.0/chats", headers=headers, json={
    "chatType": "oneOnOne",
    "members": [{
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["owner"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user['id']}')"
    }]
}).json()

requests.post(f"https://graph.microsoft.com/v1.0/chats/{chat['id']}/messages", headers=headers,
              json={"body": {"content": "!status"}})

requests.post(f"https://graph.microsoft.com/v1.0/chats/{chat['id']}/messages", headers=headers,
              json={"body": {"content": "✅ Status: Running successfully as of today."}})
