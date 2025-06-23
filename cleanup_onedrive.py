import os, requests

token = requests.post(
  f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
  data={
    "grant_type":"client_credentials",
    "client_id":os.getenv("CLIENT_ID"),
    "client_secret":os.getenv("CLIENT_SECRET"),
    "scope":"https://graph.microsoft.com/.default"
  }).json().get("access_token")

headers = {"Authorization": f"Bearer {token}"}
items = requests.get("https://graph.microsoft.com/v1.0/me/drive/root/children", headers=headers).json().get("value", [])
deleted = 0

for item in items:
    if item['name'].startswith("temp_"):
        resp = requests.delete(f"https://graph.microsoft.com/v1.0/me/drive/items/{item['id']}", headers=headers)
        if resp.status_code == 204:
            deleted += 1

print(f"✅ Deleted {deleted} temporary files.")
