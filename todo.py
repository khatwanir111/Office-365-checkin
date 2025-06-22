import os, requests, datetime

token = requests.post(
  f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
  data={
    "grant_type":"client_credentials",
    "client_id":os.getenv("CLIENT_ID"),
    "client_secret":os.getenv("CLIENT_SECRET"),
    "scope":"https://graph.microsoft.com/.default"
  }).json().get("access_token")

due = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
task = {
    "title": "Automated Task",
    "dueDateTime": {"dateTime": due, "timeZone": "UTC"}
}
resp = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists/tasks/tasks", headers=headers, json=task)
print(resp.status_code, resp.text)
