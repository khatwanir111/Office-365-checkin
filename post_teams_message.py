import os, requests

token = requests.post(
  f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
  data={
    "grant_type":"client_credentials",
    "client_id":os.getenv("CLIENT_ID"),
    "client_secret":os.getenv("CLIENT_SECRET"),
    "scope":"https://graph.microsoft.com/.default"
  }).json().get("access_token")

team_id = os.environ["TEAM_ID"]
channel_id = os.environ["CHANNEL_ID"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
msg = {"body": {"content": "Hello from GitHub Actions via Graph and Teams!"}}

resp = requests.post(f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages", headers=headers, json=msg)
print(resp.status_code, resp.text)
