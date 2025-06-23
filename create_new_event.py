import os, requests, datetime

token = requests.post(
  f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
  data={
    "grant_type":"client_credentials",
    "client_id":os.getenv("CLIENT_ID"),
    "client_secret":os.getenv("CLIENT_SECRET"),
    "scope":"https://graph.microsoft.com/.default"
  }).json().get("access_token")

start = (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat() + "Z"
end = (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).isoformat() + "Z"

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
event = {
    "subject": "Automated Event",
    "start": {"dateTime": start, "timeZone": "UTC"},
    "end": {"dateTime": end, "timeZone": "UTC"}
}
resp = requests.post(f"https://graph.microsoft.com/v1.0/users/{os.environ['EMAIL']}/events", headers=headers, json=event)
print(resp.status_code, resp.text)
