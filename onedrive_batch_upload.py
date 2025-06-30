import os, requests, json
from msal import PublicClientApplication

app = PublicClientApplication(os.environ["CLIENT_ID"], authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}")
token = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)["access_token"]
headers = {"Authorization": f"Bearer {token}"}

links = {}
for i in range(3):
    name = f"auto_file_{i}.txt"
    content = f"This is test file #{i}"
    upload = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{name}:/content", headers=headers, data=content).json()
    links[name] = upload.get("webUrl")

# Save preview links
requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/file_links.json:/content",
             headers={**headers, "Content-Type": "application/json"}, data=json.dumps(links))
