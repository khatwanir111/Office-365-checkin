from msgraph.core import GraphClient
import os
from msal import PublicClientApplication

# Auth setup
app = PublicClientApplication(
    os.environ["CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}"
)
token = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)["access_token"]

# Graph SDK client
client = GraphClient(credential={"access_token": token})

# Get users
resp = client.get("/users?$select=displayName,mail")
for user in resp.json().get("value", []):
    print(f"{user['displayName']}: {user.get('mail')}")
