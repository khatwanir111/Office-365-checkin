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
email = os.environ["EMAIL"]

resp = requests.get(f"https://graph.microsoft.com/v1.0/users/{email}/mailFolders/Inbox/messages?$top=1", headers=headers)
latest = resp.json().get("value", [])[0]
print("📨 Latest email subject:", latest["subject"])
