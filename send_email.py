import os, requests

token_url = f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": os.environ["CLIENT_ID"],
    "client_secret": os.environ["CLIENT_SECRET"],
    "scope": "https://graph.microsoft.com/.default"
}
token = requests.post(token_url, data=token_data).json().get("access_token")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
email = os.environ["EMAIL"]
message = {
    "message": {
        "subject": "Automated Email",
        "body": {"contentType": "Text", "content": "Hello from GitHub Actions via Graph API!"},
        "toRecipients": [{"emailAddress": {"address": email}}]
    }
}
resp = requests.post(f"https://graph.microsoft.com/v1.0/users/{email}/sendMail", headers=headers, json=message)
print(resp.status_code, resp.text)
