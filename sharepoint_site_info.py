# Gets SharePoint dev site info

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

headers = {"Authorization": f"Bearer {token}"}
resp = requests.get("https://graph.microsoft.com/v1.0/sites?search=sharepoint", headers=headers)
print(resp.json())
