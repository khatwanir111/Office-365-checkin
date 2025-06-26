# Creates a To Do task

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

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

task_payload = {
    "title": "Check automation run",
    "body": {"content": "This task was created automatically.", "contentType": "text"},
    "dueDateTime": {"dateTime": "2025-12-31T17:00:00", "timeZone": "UTC"}
}
requests.post("https://graph.microsoft.com/v1.0/me/todo/lists/tasks/tasks", headers=headers, json=task_payload)
