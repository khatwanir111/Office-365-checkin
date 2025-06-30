import os, requests, csv
from msal import PublicClientApplication

app = PublicClientApplication(os.environ["CLIENT_ID"], authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}")
token = app.acquire_token_by_username_password(
    os.environ["USERNAME"], os.environ["PASSWORD"],
    scopes=["https://graph.microsoft.com/.default"]
)["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Fetch users
resp = requests.get("https://graph.microsoft.com/v1.0/users?$select=displayName,userPrincipalName,jobTitle", headers=headers)
users = resp.json()["value"]

# Convert to CSV format
csv_content = "Name,Email,Title\n"
csv_content += "\n".join([f"{u['displayName']},{u['userPrincipalName']},{u.get('jobTitle','')}" for u in users])

# Upload to OneDrive
upload_url = "https://graph.microsoft.com/v1.0/me/drive/root:/user_report.csv:/content"
requests.put(upload_url, headers={**headers, "Content-Type": "text/csv"}, data=csv_content)
