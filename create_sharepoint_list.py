import os, requests
from msal import PublicClientApplication

# Auth setup
app = PublicClientApplication(os.environ["CLIENT_ID"], authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}")
result = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)
token = result["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Get default site
site = requests.get("https://graph.microsoft.com/v1.0/sites/root", headers=headers).json()

# Create list
list_payload = {
  "displayName": "ProjectTasks",
  "columns": [
    {"name": "Priority", "text": {}},
    {"name": "Status", "choice": {"choices": ["Not Started", "In Progress", "Done"]}}
  ],
  "list": { "template": "genericList" }
}
resp = requests.post(f"https://graph.microsoft.com/v1.0/sites/{site['id']}/lists", headers=headers, json=list_payload)
print("✅ List created" if resp.ok else f"❌ Error: {resp.text}")
